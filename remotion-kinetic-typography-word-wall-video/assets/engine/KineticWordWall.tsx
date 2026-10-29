/**
 * KineticWordWall — a scene-list engine for text-only kinetic-typography promos.
 *
 * Copy this file into the Remotion project (e.g. src/<Comp>/KineticWordWall.tsx).
 * Don't fork the motion inside it per video: everything that differs between
 * videos lives in a WordWallConfig (copy, palette, fonts, scenes, sound).
 *
 * Scenes play back to back. Every SFX hit and music duck is derived from the
 * scene boundaries, so retiming a scene keeps the sound in sync automatically.
 *
 * Geometry is authored in a 736×414 reference space (the size of the spot this
 * was measured from) and scaled to the composition: S = min(width/736, height/414).
 * Everything is a pure function of the frame (seek-safe, deterministic).
 */
import React from "react";
import {
  AbsoluteFill,
  Sequence,
  interpolate,
  random,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { Audio } from "@remotion/media";

// ---------------------------------------------------------------- types
export type Palette = {
  paper: string; // typed + statement background
  ink: string; // typed + statement text
  wall: string; // word-wall background
  wallInk: string; // word-wall body text (same hue as `wall`, much darker)
  highlight: string; // the one highlighted word per wall segment
  accent: string; // the statement's serif accent word
  endBg: string; // wordmark background
  endInk: string; // wordmark letters
  bar: string; // wordmark reveal bar
};

export type Fonts = {
  sans: string; // typed line, wall body, statement lead
  serif: string; // wall highlight, statement accent
  display: string; // wordmark
  displayWeight?: number; // default 800
  displayCapRatio?: number; // cap height / em, default 0.72 (Inter ≈ 0.727)
};

// Every scene may override palette tokens (e.g. a different wall color per act).
type SceneBase = { palette?: Partial<Palette> };

export type TypedScene = SceneBase & {
  kind: "typed";
  frames: number; // ≥ 14; the run into the cut uses the last 7 frames
  words: string[];
  wordOn: number[]; // scene-relative frame each word cuts on
};
export type WallScene = SceneBase & {
  kind: "wall";
  segments: Array<{ word: string; frames: number }>; // frames ≥ 2 (≥ 7 to read)
  vocab: string[]; // fills the background rows; include the segment words
};
export type StatementScene = SceneBase & {
  kind: "statement";
  frames: number; // ≥ 20; the settle takes ~19
  lead: string; // sans, e.g. "…anything "
  accent: string; // serif, accent color, e.g. "that works"
  tail?: string; // sans, e.g. "."
};
export type WordmarkScene = SceneBase & {
  kind: "wordmark";
  frames: number; // ≥ 20; the reveal settles by ~15
  left: string;
  right: string;
  gap?: number; // px @736 between the groups, default 14
  finalBar?: number; // px @736; 0 (default) = the bar vanishes at hideAt
  slant?: number; // degrees, 0 = vertical bar, e.g. 28 for a "/" slash
  hideAt?: number; // frame the bar vanishes when finalBar is 0, default 15
};
export type CustomScene = SceneBase & {
  kind: "custom";
  frames: number;
  component: React.FC; // uses useCurrentFrame() (scene-relative)
};
export type Scene = TypedScene | WallScene | StatementScene | WordmarkScene | CustomScene;

// Events every scene type emits; the sound kit maps them to files.
export type HitKind =
  | "typeWord" // each typed word
  | "wallIn" // the cut into a wall (whoosh lands ON the cut)
  | "wallSwap" // every highlight swap after the first
  | "statement" // the statement's first frame
  | "reveal" // wordmark / custom scene start
  | "revealImpact"; // layered with reveal
export type SoundHit = {
  src: string; // path under public/ (staticFile) or a URL
  peakOffset: number; // frames from file start to its loudest moment (scripts/sfx_peaks.py)
  volume: number;
};
export type SoundKit = Partial<Record<HitKind, SoundHit | null>>;

export type WordWallConfig = {
  palette: Palette;
  fonts: Fonts;
  lineTracking?: number; // em, default −0.02
  // Multiplies all type sizes. Default: 1 for landscape/square, 1.35 for portrait
  // (the engine scales to the frame's width, which leaves type small on 9:16).
  textScale?: number;
  scenes: Scene[];
  sound?: SoundKit;
  sfxGain?: number; // scales every hit, default 1
  extraSfx?: Array<{ src: string; frame: number; volume: number }>; // absolute frames
  music?: {
    src: string;
    trimBefore: number; // source frames skipped (puts the drop on the right frame)
    rate?: number; // playbackRate, default 1
    gain: number;
    fadeIn?: number; // frames, default 8
    fadeOut?: number; // frames, default 24
    duckOn?: HitKind[]; // dip −6 dB under these hits; never list the drop's wallIn
    duckFrames?: number[]; // extra one-off dips at absolute frames (e.g. one tick that peaks hot)
  } | null;
};

// ---------------------------------------------------------------- timeline
/** scripts/plan_timeline.py writes timing.ts; custom scenes there are `{ kind: "custom", ref }`. */
export type TimingScene =
  | Exclude<Scene, CustomScene>
  | { kind: "custom"; frames: number; ref: string; palette?: Partial<Palette> };
export const scenesFromTiming = (
  scenes: readonly TimingScene[],
  custom: Record<string, React.FC> = {},
): Scene[] =>
  scenes.map((s) => {
    if (s.kind !== "custom") return s as Scene;
    const component = custom[s.ref];
    if (!component) throw new Error(`No component registered for custom scene "${s.ref}"`);
    return { kind: "custom", frames: s.frames, component, palette: s.palette };
  });

export const sceneStarts = (c: WordWallConfig) =>
  c.scenes.reduce<number[]>((acc, s, i) => {
    acc.push(i === 0 ? 0 : acc[i - 1] + sceneFrames(c.scenes[i - 1]));
    return acc;
  }, []);
export const sceneFrames = (s: Scene) =>
  s.kind === "wall" ? s.segments.reduce((a, g) => a + g.frames, 0) : s.frames;
export const totalFrames = (c: WordWallConfig) =>
  c.scenes.reduce((a, s) => a + sceneFrames(s), 0);

/** Every sound event, at absolute frames. scripts/check_audio.py reads the same list from timing.json. */
export const hitsFor = (c: WordWallConfig): Array<{ kind: HitKind; frame: number }> => {
  const starts = sceneStarts(c);
  const hits: Array<{ kind: HitKind; frame: number }> = [];
  c.scenes.forEach((s, i) => {
    const t = starts[i];
    if (s.kind === "typed") s.wordOn.forEach((f) => hits.push({ kind: "typeWord", frame: t + f }));
    if (s.kind === "wall") {
      hits.push({ kind: "wallIn", frame: t });
      let acc = 0;
      s.segments.forEach((g, j) => {
        if (j > 0) hits.push({ kind: "wallSwap", frame: t + acc });
        acc += g.frames;
      });
    }
    if (s.kind === "statement") hits.push({ kind: "statement", frame: t });
    if (s.kind === "wordmark" || s.kind === "custom") {
      hits.push({ kind: "reveal", frame: t });
      hits.push({ kind: "revealImpact", frame: t });
    }
  });
  return hits;
};

// ---------------------------------------------------------------- layout helpers
const Ctx = React.createContext<WordWallConfig | null>(null);
const useCfg = () => React.useContext(Ctx)!;
const useStage = () => {
  const { width, height } = useVideoConfig();
  const c = useCfg();
  const base = Math.min(width / 736, height / 414);
  const S = base * (c.textScale ?? (height > width ? 1.35 : 1));
  return { width, height, S, cx: width / 2, cy: height / 2 };
};
const table = (t: number[], f: number) => t[Math.max(0, Math.min(t.length - 1, f))];

// Reference metrics (px @736), fitted to the source spot.
const LINE_SIZE = 37;
const LINE_BASELINE_OFFSET = 15; // below frame center
const WALL_SIZE = 46;
const WALL_PITCH = 54;
const WALL_HL_BASELINE_OFFSET = 13;
const HIGHLIGHT_SIZE = 49;
const ACCENT_SCALE = 0.92;

// ---------------------------------------------------------------- typed line
// The run into the cut: an accelerating left drift over the last 7 frames
// (measured), plus a −2px ease-in dip on the frame before each new word.
const TYPED_RUN = [-0.5, -1, -2, -4, -6, -10, -19];

const Line: React.FC<{ dx: number; tracking?: number; children: React.ReactNode }> = ({
  dx,
  tracking = 0,
  children,
}) => {
  const c = useCfg();
  const { S, cy } = useStage();
  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        right: 0,
        top: cy + (LINE_BASELINE_OFFSET - LINE_SIZE) * S,
        height: LINE_SIZE * S,
        display: "flex",
        justifyContent: "center",
        alignItems: "baseline",
        transform: `translateX(${dx * S}px)`,
        fontFamily: c.fonts.sans,
        fontWeight: 500,
        fontSize: LINE_SIZE * S,
        lineHeight: 1,
        letterSpacing: `calc(${c.lineTracking ?? -0.02}em + ${tracking * S}px)`,
        color: c.palette.ink,
        whiteSpace: "pre",
      }}
    >
      {children}
    </div>
  );
};

const Typed: React.FC<{ scene: TypedScene }> = ({ scene }) => {
  const f = useCurrentFrame();
  const c = useCfg();
  const shown = scene.words.filter((_, i) => f >= scene.wordOn[i]);
  const runStart = scene.frames - TYPED_RUN.length;
  const dx =
    (scene.wordOn.slice(1).includes(f + 1) ? -2 : 0) + (f >= runStart ? TYPED_RUN[f - runStart] : 0);
  return (
    <AbsoluteFill style={{ background: c.palette.paper }}>
      {shown.length > 0 && <Line dx={dx}>{shown.join(" ")}</Line>}
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- word wall
// Fast–slow–fast drift (px @736) sampled over an 11-frame segment; shorter or
// longer segments resample it, so every word travels the same ~15px and short
// segments move faster. Hard cut between segments.
const SEG_DRIFT = [0, -4.5, -6, -7, -8, -8, -8, -9, -9.5, -11, -15];
const segDrift = (f: number, len: number) => {
  if (len < 2) return 0;
  const x = (f * (SEG_DRIFT.length - 1)) / (len - 1);
  const i = Math.min(SEG_DRIFT.length - 2, Math.floor(x));
  return SEG_DRIFT[i] + (SEG_DRIFT[i + 1] - SEG_DRIFT[i]) * (x - i);
};
const wordRun = (vocab: string[], seed: string, count: number, avoid?: string) => {
  const out: string[] = [];
  for (let i = 0; i < count; i++) {
    let w = vocab[Math.floor(random(`${seed}-${i}`) * vocab.length)];
    if (w === out[out.length - 1] || w === avoid) w = vocab[(vocab.indexOf(w) + 1) % vocab.length];
    out.push(w);
  }
  return out.join(" ");
};

const WallSegment: React.FC<{ word: string; seed: string; f: number; len: number; vocab: string[] }> = ({
  word,
  seed,
  f,
  len,
  vocab,
}) => {
  const c = useCfg();
  const { S, cx, cy, height } = useStage();
  const drift = segDrift(f, len);
  const text: React.CSSProperties = {
    fontFamily: c.fonts.sans,
    fontWeight: 500,
    fontSize: WALL_SIZE * S,
    lineHeight: 1,
    color: c.palette.wallInk,
    whiteSpace: "pre",
  };
  const rowsEachSide = Math.ceil(height / 2 / (WALL_PITCH * S)) + 1;
  // Highlight starts slightly right of center (−2…+14px, seeded), then drifts.
  const anchor = cx + (-2 + random(`${seed}-anchor`) * 16 + drift) * S;
  const half = 2400 * S;
  const rows: React.ReactNode[] = [];
  for (let r = -rowsEachSide; r <= rowsEachSide; r++) {
    const top = cy + (WALL_HL_BASELINE_OFFSET + r * WALL_PITCH - WALL_SIZE * 0.9) * S;
    if (r === 0) {
      rows.push(
        <div
          key={r}
          style={{ position: "absolute", top, left: anchor - half, width: half * 2, display: "flex", alignItems: "baseline", ...text }}
        >
          <span style={{ flex: "1 1 0", textAlign: "right" }}>{wordRun(vocab, `${seed}-l`, 8, word) + " "}</span>
          <span
            style={{
              fontFamily: c.fonts.serif,
              fontWeight: 400,
              fontSize: HIGHLIGHT_SIZE * S,
              color: c.palette.highlight,
              letterSpacing: "-0.01em",
            }}
          >
            {word}
          </span>
          <span style={{ flex: "1 1 0" }}>{" " + wordRun(vocab, `${seed}-r`, 8, word)}</span>
        </div>,
      );
    } else {
      const startX = (-60 - random(`${seed}-x${r}`) * 220 + drift) * S;
      rows.push(
        <div key={r} style={{ position: "absolute", top, left: startX, ...text }}>
          {wordRun(vocab, `${seed}-r${r}`, 18)}
        </div>,
      );
    }
  }
  return <>{rows}</>;
};

const Wall: React.FC<{ scene: WallScene; id: number }> = ({ scene, id }) => {
  const f = useCurrentFrame();
  const c = useCfg();
  let start = 0;
  let seg = 0;
  while (seg < scene.segments.length - 1 && f >= start + scene.segments[seg].frames) {
    start += scene.segments[seg].frames;
    seg++;
  }
  const g = scene.segments[seg];
  return (
    <AbsoluteFill style={{ background: c.palette.wall, overflow: "hidden" }}>
      <WallSegment word={g.word} seed={`w${id}-s${seg}`} f={f - start} len={g.frames} vocab={scene.vocab} />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- statement
// Lands loose and right, tightens to center over ~19 frames (measured, px @736).
const ST_CENTER = [57.5, 39, 27.5, 20.5, 15, 11.5, 8.5, 7, 5.5, 4, 3, 2.5, 1.5, 1.5, 1, 1, 0.5, 0.5, 0];
const ST_EXTRA = [43, 28, 19, 13, 10, 7, 5, 4, 3, 2, 1, 1, 0.5, 0.5, 0];

const Statement: React.FC<{ scene: StatementScene }> = ({ scene }) => {
  const f = useCurrentFrame();
  const c = useCfg();
  const { S } = useStage();
  const extra = table(ST_EXTRA, f);
  const glyphs = (scene.lead + scene.accent + (scene.tail ?? "")).length;
  return (
    <AbsoluteFill style={{ background: c.palette.paper }}>
      <Line dx={table(ST_CENTER, f)} tracking={(extra * 0.2) / Math.max(1, glyphs)}>
        {scene.lead}
        <span style={{ display: "inline-block", width: extra * 0.8 * S }} />
        <span
          style={{ fontFamily: c.fonts.serif, fontWeight: 400, color: c.palette.accent, fontSize: LINE_SIZE * ACCENT_SCALE * S }}
        >
          {scene.accent}
        </span>
        {scene.tail}
      </Line>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- wordmark
// A bar over the center narrows while the two groups slide outward from under
// its edges (each clipped to its side). One curve drives it: p = 1 − 0.765^f.
const Wordmark: React.FC<{ scene: WordmarkScene; id: number }> = ({ scene, id }) => {
  const f = useCurrentFrame();
  const c = useCfg();
  const { width, height, S, cy } = useStage();
  const k = Math.pow(0.765, f);
  // Fit: bold caps average ~0.68 em, so cap the size to keep the whole mark
  // within ~84% of the frame width (long names on portrait frames).
  const capRatio = c.fonts.displayCapRatio ?? 0.72;
  const gapPx = (scene.gap ?? 14) * S;
  const fitSize = (0.84 * width - gapPx) / (0.68 * (scene.left.length + scene.right.length));
  const fontSize = Math.min((38 * S) / capRatio, fitSize);
  const capH = fontSize * capRatio;
  const gapHalf = gapPx / 2;
  // Center the whole mark, not the bar: shift the gap by half the difference
  // between the two groups' estimated widths.
  const ax = width / 2 + (0.68 * fontSize * (scene.left.length - scene.right.length)) / 2;
  const finalBar = (scene.finalBar ?? 0) * S;
  const barOn = finalBar > 0 || f < (scene.hideAt ?? 15);
  const lean = Math.tan(((scene.slant ?? 0) * Math.PI) / 180); // x shift per px up
  const barL = ax - finalBar / 2 - 12 * S * k;
  const barR = ax + finalBar / 2 + 40 * S * k;
  const edge = (x: number, y: number) => x + (cy - y) * lean; // bar edge x at height y
  const clipL = barOn ? barL : ax;
  const clipR = barOn ? barR : ax;
  const yT = cy - capH / 2;
  const yB = cy + capH / 2;
  const txt = (s: string, x: number, anchor: "start" | "end") => (
    <text
      x={x}
      y={yB}
      textAnchor={anchor}
      fontFamily={c.fonts.display}
      fontWeight={c.fonts.displayWeight ?? 800}
      fontSize={fontSize}
      fill={c.palette.endInk}
    >
      {s}
    </text>
  );
  return (
    <AbsoluteFill style={{ background: c.palette.endBg }}>
      <svg width={width} height={height}>
        <defs>
          <clipPath id={`wm${id}-l`}>
            <polygon points={`0,0 ${edge(clipL, 0)},0 ${edge(clipL, height)},${height} 0,${height}`} />
          </clipPath>
          <clipPath id={`wm${id}-r`}>
            <polygon points={`${edge(clipR, 0)},0 ${width},0 ${width},${height} ${edge(clipR, height)},${height}`} />
          </clipPath>
        </defs>
        <g clipPath={`url(#wm${id}-l)`}>{txt(scene.left, ax - gapHalf + 37 * S * k, "end")}</g>
        <g clipPath={`url(#wm${id}-r)`}>{txt(scene.right, ax + gapHalf - 43 * S * k, "start")}</g>
        {barOn && (
          <polygon
            points={`${edge(barL, yT)},${yT} ${edge(barR, yT)},${yT} ${edge(barR, yB)},${yB} ${edge(barL, yB)},${yB}`}
            fill={c.palette.bar}
          />
        )}
      </svg>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- composition
const DUCK = 0.5; // −6 dB

export type WordWallProps = { mute?: "none" | "sfx" | "music" | "all" };

export const KineticWordWall: React.FC<{ config: WordWallConfig } & WordWallProps> = ({ config: c, mute = "none" }) => {
  const starts = sceneStarts(c);
  const duration = totalFrames(c);
  const hits = hitsFor(c);
  const m = c.music;
  const duckFrames = [
    ...(m?.duckOn ? hits.filter((h) => m.duckOn!.includes(h.kind)).map((h) => h.frame) : []),
    ...(m?.duckFrames ?? []),
  ];
  const duck = (f: number) =>
    duckFrames.length === 0
      ? 1
      : Math.min(
          ...duckFrames.map((h) =>
            interpolate(f, [h - 1, h, h + 2, h + 8], [1, DUCK, DUCK, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
          ),
        );
  const sfx = [
    ...hits.flatMap((h) => {
      const s = c.sound?.[h.kind];
      return s ? [{ src: s.src, from: h.frame - s.peakOffset, volume: s.volume }] : [];
    }),
    ...(c.extraSfx ?? []).map((e) => ({ src: e.src, from: e.frame, volume: e.volume })),
  ];
  const src = (s: string) => (/^https?:\/\//.test(s) ? s : staticFile(s));
  return (
    <Ctx.Provider value={c}>
      <AbsoluteFill style={{ background: c.palette.paper }}>
        {c.scenes.map((s, i) => (
          <Sequence key={i} from={starts[i]} durationInFrames={sceneFrames(s)}>
            <Ctx.Provider value={s.palette ? { ...c, palette: { ...c.palette, ...s.palette } } : c}>
              {s.kind === "typed" && <Typed scene={s} />}
              {s.kind === "wall" && <Wall scene={s} id={i} />}
              {s.kind === "statement" && <Statement scene={s} />}
              {s.kind === "wordmark" && <Wordmark scene={s} id={i} />}
              {s.kind === "custom" && <s.component />}
            </Ctx.Provider>
          </Sequence>
        ))}
        {m && mute !== "music" && mute !== "all" && (
          <Audio
            src={src(m.src)}
            trimBefore={m.trimBefore}
            playbackRate={m.rate ?? 1}
            volume={(f) =>
              m.gain *
              duck(f) *
              interpolate(f, [0, m.fadeIn ?? 8, duration - (m.fadeOut ?? 24), duration], [0, 1, 1, 0], {
                extrapolateLeft: "clamp",
                extrapolateRight: "clamp",
              })
            }
          />
        )}
        {mute !== "sfx" &&
          mute !== "all" &&
          sfx.map((h, i) => (
            <Audio key={i} src={src(h.src)} from={Math.max(0, h.from)} volume={h.volume * (c.sfxGain ?? 1)} />
          ))}
      </AbsoluteFill>
    </Ctx.Provider>
  );
};
