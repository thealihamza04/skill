import React from "react";
import {
  AbsoluteFill,
  Easing,
  Img,
  Sequence,
  interpolate,
  interpolateColors,
  random,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { Audio } from "@remotion/media";
import { useGsapTimeline } from "@remotion/gsap";
import { loadFont } from "@remotion/google-fonts/Figtree";

// Stat-reel engine (see the skill's references/format.md). Every beat is a
// frame-accurate port of a 720×540 @ 60fps reference: each beat component
// runs on its own *reference clock* (T = beat's reference start + local
// seconds) so the measured keyframes stay verbatim, whatever order or subset
// of beats a video uses. Configure it; don't fork its motion.
//
// Remotion drives time; GSAP (via @remotion/gsap's paused, frame-seeked
// timelines) choreographs the many-element moves: scattered letter reveals,
// the outro collage and the logo mark assembly.

const { fontFamily: FIGTREE } = loadFont("normal", {
  weights: ["300", "400", "500", "600", "700"],
  subsets: ["latin"],
});
const { fontFamily: FIGTREE_ITALIC } = loadFont("italic", {
  weights: ["300"],
  subsets: ["latin"],
});

export const STAGE_W = 720;
export const STAGE_H = 540;

// ── Config ───────────────────────────────────────────────────────────────────

export type StatReelColors = {
  lime: string; // light background
  ink: string; // text on light, dark background, badges
  cream: string; // text on dark, badge text
  ghost: string; // giant ghost number
  accent: string; // highlighted number, thanks lead word
  pill: string; // search pill
  squiggleDark: string; // squiggles on the dark background
  end: string; // end-card background
  brand: string; // wordmark dot / mark accent
};

export type Beat =
  | { type: "collageTitle"; line1: string; stat: string; icon: "code" | "eye" | "none"; line2: string; line3: string }
  | { type: "words"; theme: "light" | "dark"; words: string[]; times?: number[]; duration?: number }
  | { type: "cursorCounter"; from: number; to: number; suffix: string; label: string }
  | { type: "ghostCounter"; count: number; word: string; then: [string, string] }
  // steps: 8 values at climb, hold, climb, hold, climb, hold, then the drop.
  | { type: "badgeCounter"; label: string; steps: [number, number, number, number, number, number, number, number] }
  | { type: "badgeSentence"; from: number; to: number; lead: string; tail: string; line2: string }
  | { type: "arrowWords"; lead: string; phrases: [string, string][] }
  | { type: "searchCollage"; url: string }
  | { type: "thanks"; accent: string; rest: string }
  | { type: "endCard"; bold: string; dot: string; light: string };

export type SfxKit = Partial<Record<"darkCut" | "boxSnap" | "ghostWord" | "arrowPull" | "toDark" | "collage" | "logo", { src: string; volume: number }>>;

export type StatReelConfig = {
  fps: number; // 60 matches the reference
  colors: StatReelColors;
  fontFamily?: string; // defaults to Figtree
  italicFontFamily?: string;
  images: string[]; // staticFile paths; 7 used by the intro, 8 by the outro (cycled)
  beats: Beat[];
  // Logo mark for the end card. `t` = seconds since the end card started.
  // Defaults to a monogram of the wordmark's first letter.
  Mark?: React.FC<{ t: number }>;
  music: { src: string; gain: number } | null;
  sfx: SfxKit;
};

// Reference start and length of each beat type (seconds). `words` runs on
// its own clock (times/duration).
const REF: Record<Exclude<Beat["type"], "words">, { start: number; len: number }> = {
  collageTitle: { start: 0, len: 0.8 },
  cursorCounter: { start: 4.5, len: 1.9 },
  ghostCounter: { start: 6.4, len: 3.25 },
  badgeCounter: { start: 9.65, len: 2.55 },
  badgeSentence: { start: 12.2, len: 1.1 },
  arrowWords: { start: 13.3, len: 4.3 },
  searchCollage: { start: 17.6, len: 2.4 },
  thanks: { start: 20.0, len: 1.8 },
  endCard: { start: 21.8, len: 3.52 },
};
const WORD_TIMES = { light: [0, 0.4, 0.8], dark: [0.1, 0.6, 1.4] };
const WORD_LEN = { light: 1.8, dark: 1.9 };
// The arrow beat's exit overlaps the next beat's background crossfade.
const ARROW_TAIL = 0.3;

const beatLen = (b: Beat) => (b.type === "words" ? (b.duration ?? WORD_LEN[b.theme]) : REF[b.type].len);

export const statReelTimeline = (config: StatReelConfig) => {
  let at = 0;
  return config.beats.map((beat) => {
    const from = Math.round(at * config.fps);
    at += beatLen(beat);
    return { beat, from, frames: Math.round(at * config.fps) - from };
  });
};

export const statReelDuration = (config: StatReelConfig) => {
  const tl = statReelTimeline(config);
  const last = tl[tl.length - 1];
  return last.from + last.frames;
};

// ── Helpers ──────────────────────────────────────────────────────────────────

const OUT = Easing.bezier(0.16, 1, 0.3, 1);
const IN_OUT = Easing.bezier(0.65, 0, 0.35, 1);
const IN = Easing.bezier(0.5, 0, 0.75, 0);

const r = (t: number, input: number[], output: number[], easing?: (n: number) => number) =>
  interpolate(t, input, output, { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing });

const Ctx = React.createContext<StatReelConfig | null>(null);
const useReel = () => React.useContext(Ctx)!;

// Local seconds inside the current <Sequence>.
const useLocalTime = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return frame / fps;
};

const Center: React.FC<{ children: React.ReactNode; style?: React.CSSProperties }> = ({ children, style }) => (
  <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", ...style }}>{children}</AbsoluteFill>
);

const Shot: React.FC<{ src: string; x: number; y: number; w: number; h: number; style?: React.CSSProperties; className?: string }> = ({
  src,
  x,
  y,
  w,
  h,
  style,
  className,
}) => (
  <Img
    className={className}
    src={staticFile(src)}
    style={{ position: "absolute", left: x, top: y, width: w, height: h, objectFit: "cover", ...style }}
  />
);

const Squiggle: React.FC<{ d: string; progress: number; color: string; width: number; dx?: number; dy?: number }> = ({
  d,
  progress,
  color,
  width,
  dx = 0,
  dy = 0,
}) => (
  <path
    d={d}
    pathLength={1}
    fill="none"
    stroke={color}
    strokeWidth={width}
    strokeLinecap="round"
    strokeDasharray="1 1"
    strokeDashoffset={1 - progress}
    transform={`translate(${dx} ${dy})`}
  />
);

const PillIcon: React.FC<{ kind: "code" | "eye"; color: string }> = ({ kind, color }) => (
  <svg width={46} height={28} viewBox="0 0 50 30" style={{ marginLeft: 10 }}>
    {kind === "code" ? (
      <g fill="none" stroke={color} strokeWidth={2.8} strokeLinecap="round" strokeLinejoin="round">
        <polyline points="14,5 4,15 14,25" />
        <polyline points="36,5 46,15 36,25" />
        <line x1={29} y1={4} x2={21} y2={26} />
      </g>
    ) : (
      <g fill="none" stroke={color} strokeWidth={2.6}>
        <path d="M3 15 C 12 3, 38 3, 47 15 C 38 27, 12 27, 3 15 Z" />
        <circle cx={25} cy={15} r={6.5} />
        <circle cx={25} cy={15} r={2} fill={color} />
      </g>
    )}
  </svg>
);

// Letters fading in at seeded random offsets — a GSAP timeline local to the
// current Sequence. `start`/`spread` are local seconds.
const ScatterText: React.FC<{ text: string; start: number; spread: number; seed: string; color?: (i: number) => string }> = ({
  text,
  start,
  spread,
  seed,
  color,
}) => {
  const ref = useGsapTimeline<HTMLSpanElement>(
    ({ timeline, selector }) => {
      (selector(".ch") as HTMLElement[]).forEach((el, i) => {
        timeline.fromTo(el, { opacity: 0 }, { opacity: 1, duration: 0.14, ease: "none" }, start + random(`${seed}-${i}`) * spread);
      });
    },
    { dependencies: [text, start, spread, seed] },
  );
  return (
    <span ref={ref}>
      {text.split("").map((ch, i) => (
        <span key={i} className="ch" style={{ opacity: 0, color: color?.(i), whiteSpace: "pre" }}>
          {ch}
        </span>
      ))}
    </span>
  );
};

const Badge: React.FC<{ children: React.ReactNode; size: number; style?: React.CSSProperties }> = ({ children, size, style }) => {
  const { colors: C } = useReel();
  return (
    <span
      style={{
        display: "inline-block",
        fontSize: size,
        fontWeight: 600,
        lineHeight: 1,
        padding: "0.32em 0.3em 0.28em",
        borderRadius: "0.2em",
        backgroundColor: C.ink,
        color: C.cream,
        ...style,
      }}
    >
      {children}
    </span>
  );
};

// ── Beats ────────────────────────────────────────────────────────────────────

const INTRO_SHOTS = [
  { x: 37, y: 0, w: 118, h: 90 },
  { x: 356, y: 0, w: 143, h: 104 },
  { x: 617, y: 40, w: 103, h: 98 },
  { x: 219, y: 117, w: 86, h: 67 },
  { x: 497, y: 208, w: 173, h: 135 },
  { x: 559, y: 421, w: 161, h: 119 },
  { x: 360, y: 474, w: 123, h: 66 },
];

const CollageTitle: React.FC<Extract<Beat, { type: "collageTitle" }>> = (b) => {
  const { colors: C, images } = useReel();
  const t = useLocalTime();
  const textX = r(t, [0, 0.75], [0, -150], Easing.in(Easing.quad));
  const textO = r(t, [0.3, 0.75], [1, 0]);
  const imgO = r(t, [0.45, 0.78], [1, 0]);
  const line = (top: number): React.CSSProperties => ({ position: "absolute", top, transform: "translateY(-50%)", whiteSpace: "nowrap" });
  return (
    <AbsoluteFill style={{ backgroundColor: C.lime }}>
      {INTRO_SHOTS.map((s, i) => (
        <Shot key={i} src={images[i % images.length]} {...s} style={{ opacity: imgO, transform: `translateY(${-t * 14}px) scale(${1 + t * 0.05})` }} />
      ))}
      <div style={{ position: "absolute", left: 58, top: 0, color: C.ink, fontWeight: 500, lineHeight: 1, opacity: textO, transform: `translateX(${textX}px)` }}>
        <div style={{ ...line(268), fontSize: 62 }}>{b.line1}</div>
        <div style={{ ...line(355), display: "flex", alignItems: "center", fontSize: 51 }}>
          <div style={{ display: "flex", alignItems: "center", height: 60, padding: "0 18px 0 20px", borderRadius: 30, backgroundColor: C.ink, color: C.cream, fontSize: 34 }}>
            {b.stat}
            {b.icon !== "none" && <PillIcon kind={b.icon} color={C.cream} />}
          </div>
          <span style={{ marginLeft: 20 }}>{b.line2}</span>
        </div>
        <div style={{ ...line(440), fontSize: 70, fontWeight: 600 }}>{b.line3}</div>
      </div>
    </AbsoluteFill>
  );
};

const SQUIGGLES = {
  light: [
    { d: "M -20 40 C 40 70, 90 105, 140 102 C 190 98, 215 50, 222 -10", sway: [-1, 0.5] },
    { d: "M 740 440 C 690 480, 640 505, 590 505 C 530 505, 480 478, 420 478 C 360 478, 325 500, 322 560", sway: [1, -0.4] },
  ],
  dark: [
    { d: "M 380 -10 C 420 40, 470 45, 530 35 C 600 22, 660 20, 740 45", sway: [1, 0] },
    { d: "M -20 540 C 10 505, 60 490, 110 505 C 140 515, 150 530, 155 545", sway: [-1, 0] },
  ],
};

const Words: React.FC<Extract<Beat, { type: "words" }>> = (b) => {
  const { colors: C } = useReel();
  const t = useLocalTime();
  const light = b.theme === "light";
  const times = b.times ?? WORD_TIMES[b.theme];
  const draw = light ? r(t, [0.3, 0.9], [0, 1], OUT) : r(t, [0, 0.7], [0, 1], OUT);
  const amp = light ? 6 : 10;
  const drift = Math.sin(t * (light ? 2 : 1.6)) * amp;
  let idx = -1;
  times.forEach((s, i) => {
    if (t >= s && i < b.words.length) idx = i;
  });
  const lt = idx >= 0 ? t - times[idx] : 0;
  const last = idx === b.words.length - 1;
  const size = light ? 61 : last ? 66 : 57;
  return (
    <AbsoluteFill style={{ backgroundColor: light ? C.lime : C.ink }}>
      <svg width={STAGE_W} height={STAGE_H} style={{ position: "absolute" }}>
        {SQUIGGLES[b.theme].map((s, i) => (
          <Squiggle key={i} d={s.d} progress={draw} color={light ? "#fff" : C.squiggleDark} width={light ? 7 : 6} dx={drift * s.sway[0]} dy={drift * s.sway[1]} />
        ))}
      </svg>
      {idx >= 0 && (
        <Center>
          <div style={{ color: light ? C.ink : C.cream, fontSize: size, fontWeight: 500, opacity: r(lt, [0, 0.12], [0.35, 1]), transform: `scale(${r(lt, [0, 1], [0.95, 1.03])})` }}>
            {b.words[idx]}
          </div>
        </Center>
      )}
    </AbsoluteFill>
  );
};

const Caret: React.FC<{ left: string; opacity?: number; color: string }> = ({ left, opacity = 1, color }) => (
  <div style={{ position: "absolute", left, top: "-0.12em", width: 3, height: "1.3em", backgroundColor: color, opacity }} />
);

const CursorCounter: React.FC<Extract<Beat, { type: "cursorCounter" }>> = (b) => {
  const { colors: C } = useReel();
  const t = REF.cursorCounter.start + useLocalTime();
  const n = Math.round(r(t, [4.5, 5.3], [b.from, b.to], Easing.out(Easing.cubic)));
  const scale = r(t, [4.5, 6.35], [0.62, 1], Easing.out(Easing.quad));
  // Caret sweeps the whole line, blinks at the end, walks back to the end of
  // the number, then widens into the highlight box behind it.
  const sweep = r(t, [4.5, 5.25], [0, 1], IN_OUT);
  const back = r(t, [5.5, 5.85], [0, 1], IN_OUT);
  const box = r(t, [5.85, 6.15], [0, 1], OUT);
  const blink = t > 5.25 && t < 5.5 ? (Math.floor(t * 8) % 2 === 0 ? 1 : 0.2) : 1;
  return (
    <AbsoluteFill style={{ backgroundColor: C.lime }}>
      <Center>
        <div style={{ fontSize: 45, fontWeight: 500, color: C.ink, transform: `scale(${scale})`, whiteSpace: "nowrap" }}>
          <span style={{ position: "relative", display: "inline-block" }}>
            <span style={{ position: "relative", display: "inline-block" }}>
              {box > 0 && (
                <div
                  style={{
                    position: "absolute",
                    right: -4,
                    top: -18,
                    bottom: -14,
                    width: `calc(${box * 100}% + ${3 + box * 22}px)`,
                    borderRadius: 10,
                    backgroundColor: C.ink,
                  }}
                />
              )}
              <span style={{ position: "relative", color: interpolateColors(box, [0.4, 1], [C.ink, C.accent]) }}>
                {n}
                {b.suffix}
              </span>
            </span>
            <span style={{ position: "relative", display: "inline-block", marginLeft: "0.28em" }}>
              {b.label}
              {t >= 5.25 && box === 0 && <Caret color={C.ink} left={`calc(${(1 - back) * 100}% + ${6 - back * 12}px)`} opacity={blink} />}
            </span>
            {t < 5.25 && <Caret color={C.ink} left={`calc(${sweep * 100}% + ${-12 + sweep * 18}px)`} />}
          </span>
        </div>
      </Center>
    </AbsoluteFill>
  );
};

const GhostCounter: React.FC<Extract<Beat, { type: "ghostCounter" }>> = (b) => {
  const { colors: C } = useReel();
  const lt = useLocalTime();
  const t = REF.ghostCounter.start + lt;
  const n = Math.round(r(t, [6.4, 7.2], [0, b.count], Easing.out(Easing.cubic)));
  const second = t < 9;
  return (
    <AbsoluteFill style={{ backgroundColor: C.lime }}>
      {t < 8.4 ? (
        <>
          <Center>
            <div style={{ fontSize: 470, fontWeight: 600, color: C.ghost, letterSpacing: "-0.02em", opacity: r(t, [6.4, 6.5], [0.5, 1]) }}>{n}</div>
          </Center>
          <Center>
            <div style={{ fontSize: 32, fontWeight: 600, color: C.ink }}>
              <ScatterText text={b.word} start={7.25 - REF.ghostCounter.start} spread={0.55} seed="ghost" />
            </div>
          </Center>
        </>
      ) : (
        <Center>
          <div style={{ fontSize: second ? 48 : 52, fontWeight: 600, color: C.ink, opacity: r(t - (second ? 8.4 : 9), [0, 0.12], [0.4, 1]) }}>
            {second ? b.then[0] : b.then[1]}
          </div>
        </Center>
      )}
    </AbsoluteFill>
  );
};

const STEP_TIMES = [9.65, 10.2, 10.35, 10.85, 11.0, 11.5, 11.75, 12.15];
const steppedCount = (t: number, steps: number[]) => {
  for (let i = 0; i < STEP_TIMES.length - 1; i++) {
    const [t0, t1, v0, v1] = [STEP_TIMES[i], STEP_TIMES[i + 1], steps[i], steps[i + 1]];
    if (t <= t1) return Math.round(r(t, [t0, t1], [v0, v1], v1 < v0 ? IN : IN_OUT));
  }
  return steps[steps.length - 1];
};

const BadgeCounter: React.FC<Extract<Beat, { type: "badgeCounter" }>> = (b) => {
  const { colors: C } = useReel();
  const t = REF.badgeCounter.start + useLocalTime();
  const size = r(t, [9.65, 11.5, 11.75, 12.15], [28, 60, 60, 26], IN_OUT);
  return (
    <AbsoluteFill style={{ backgroundColor: C.lime }}>
      <Center>
        <div style={{ display: "flex", alignItems: "center", color: C.ink, opacity: r(t, [9.65, 9.8], [0.5, 1]) }}>
          <Badge size={size}>{steppedCount(t, b.steps)}+</Badge>
          <div style={{ maxWidth: r(t, [11.72, 11.86], [400, 0]), overflow: "hidden", opacity: r(t, [11.72, 11.8], [1, 0]) }}>
            <span style={{ display: "inline-block", fontSize: r(t, [9.65, 11.5], [26, 42]), fontWeight: 500, paddingLeft: 12, whiteSpace: "nowrap" }}>{b.label}</span>
          </div>
        </div>
      </Center>
    </AbsoluteFill>
  );
};

const BadgeSentence: React.FC<Extract<Beat, { type: "badgeSentence" }>> = (b) => {
  const { colors: C } = useReel();
  const t = REF.badgeSentence.start + useLocalTime();
  const n = Math.round(r(t, [12.2, 12.38], [b.from, b.to]));
  return (
    <AbsoluteFill style={{ backgroundColor: C.lime }}>
      <Center>
        <div
          style={{
            fontSize: 28,
            fontWeight: 500,
            color: C.ink,
            textAlign: "center",
            lineHeight: 1.9,
            opacity: r(t, [12.2, 12.3], [0.4, 1]),
            transform: `scale(${r(t, [12.2, 13.25], [0.93, 1.04])})`,
          }}
        >
          {b.lead}{" "}
          <Badge size={23} style={{ margin: "0 6px", padding: "0.4em 0.85em", verticalAlign: "1px" }}>
            {n}+
          </Badge>{" "}
          {b.tail}
          <br />
          {b.line2}
        </div>
      </Center>
    </AbsoluteFill>
  );
};

const Arrow: React.FC<{ tail: number; tip: number; color: string }> = ({ tail, tip, color }) => {
  if (tip - tail < 2) return null;
  const head = Math.min(11, (tip - tail) * 0.5);
  return (
    <svg width={STAGE_W} height={STAGE_H} style={{ position: "absolute" }}>
      <g stroke={color} strokeWidth={2.6} strokeLinecap="round" fill="none">
        <line x1={tail} y1={270} x2={tip} y2={270} />
        <polyline points={`${tip - head},${270 - head} ${tip},270 ${tip - head},${270 + head}`} strokeLinejoin="round" />
      </g>
    </svg>
  );
};

const PHRASE_TIMES = [
  { start: 14.7, end: 15.85 },
  { start: 15.9, end: 16.95 },
  { start: 17.0, end: 18.0 },
];

// Rendered for its length + ARROW_TAIL so its exit plays over the next beat.
const ArrowWords: React.FC<Extract<Beat, { type: "arrowWords" }>> = (b) => {
  const { colors: C } = useReel();
  const t = REF.arrowWords.start + useLocalTime();
  const end = REF.arrowWords.start + REF.arrowWords.len;
  // The lead rides off the left edge while the arrow is pulled out of it.
  const textLeft = r(t, [13.85, 14.0, 14.1, 14.2, 14.35], [240, 207, 93, -60, -300]);
  const tip = r(t, [13.85, 14.0, 14.1, 14.2, 14.3, 14.4, 14.5, 14.7, 15.0], [492, 501, 462, 384, 315, 270, 237, 210, 205]);
  const textW = 240;
  const tail = t < 13.85 ? tip : textLeft + textW + 14;
  const exitX = r(t, [end, end + 0.25], [0, -160], IN);
  const exitBlur = r(t, [end, end + 0.25], [0, 8]);
  const exitO = r(t, [end + 0.02, end + 0.25], [1, 0]);
  return (
    <AbsoluteFill>
      {t < end && <AbsoluteFill style={{ backgroundColor: C.lime }} />}
      <AbsoluteFill style={{ opacity: exitO, transform: `translateX(${exitX}px)`, filter: `blur(${exitBlur}px)` }}>
        {t < 14.4 && (
          <div
            style={{
              position: "absolute",
              left: textLeft,
              width: textW,
              top: 238,
              textAlign: "center",
              fontSize: 50,
              fontWeight: 500,
              color: C.ink,
              whiteSpace: "nowrap",
              opacity: r(t, [13.3, 13.4], [0.6, 1]) * r(t, [14.15, 14.3], [1, 0]),
              transform: `scale(${r(t, [13.3, 14.0], [0.96, 1.02])})`,
            }}
          >
            {b.lead}
          </div>
        )}
        {t >= 13.85 && <Arrow tail={Math.min(tail, tip)} tip={tip} color={C.ink} />}
        {PHRASE_TIMES.map(({ start, end: e }, i) =>
          b.phrases[i] && t >= start && t < e ? (
            <div key={i} style={{ position: "absolute", left: 272, top: 239, fontSize: 51, fontWeight: 500, color: C.ink, whiteSpace: "nowrap", opacity: r(t, [e - 0.1, e], [1, 0.35]) }}>
              {b.phrases[i].map((w, j) => (
                <span key={j} style={{ opacity: r(t, [start + j * 0.08, start + j * 0.08 + 0.12], [0.3, 1]) }}>
                  {j > 0 ? " " : ""}
                  {w}
                </span>
              ))}
            </div>
          ) : null,
        )}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

const SearchIcon: React.FC<{ color: string }> = ({ color }) => (
  <svg width={28} height={28} viewBox="0 0 24 24">
    <circle cx={13.5} cy={10.5} r={7} fill="none" stroke={color} strokeWidth={2.4} />
    <path d="M8.5 15.5 L3.5 20.5" stroke={color} strokeWidth={2.4} strokeLinecap="round" />
  </svg>
);

const OUTRO_SHOTS = [
  { x: -10, y: -10, w: 188, h: 114, at: 18.9 },
  { x: 548, y: 447, w: 172, h: 93, at: 19.0 },
  { x: 159, y: 465, w: 232, h: 75, at: 19.1 },
  { x: -10, y: 383, w: 99, h: 113, at: 19.1 },
  { x: 372, y: -10, w: 177, h: 72, at: 19.25 },
  { x: 634, y: 90, w: 96, h: 218, at: 19.3 },
  { x: 86, y: 200, w: 136, h: 106, at: 19.4 },
  { x: 259, y: 130, w: 316, h: 247, at: 19.55 },
];

// Shots pop out from the centre (GSAP: expo-out scale + pull from centre,
// then a slow linear zoom), staggered as in the reference.
const Collage: React.FC = () => {
  const { images } = useReel();
  const base = REF.searchCollage.start;
  const ref = useGsapTimeline<HTMLDivElement>(
    ({ timeline, selector }) => {
      (selector(".shot") as HTMLElement[]).forEach((el, i) => {
        const s = OUTRO_SHOTS[i];
        const at = s.at - base;
        const cx = s.x + s.w / 2 - STAGE_W / 2;
        const cy = s.y + s.h / 2 - STAGE_H / 2;
        timeline.fromTo(el, { opacity: 0 }, { opacity: 1, duration: 0.08, ease: "none" }, at);
        timeline.fromTo(el, { x: -cx * 0.25, y: -cy * 0.25, scale: 0.55 }, { x: 0, y: 0, scale: 1, duration: 0.3, ease: "expo.out" }, at);
        timeline.to(el, { scale: 1.03, duration: 1, ease: "none" }, at + 0.3);
      });
    },
    { dependencies: [images.join("|")] },
  );
  return (
    <AbsoluteFill ref={ref}>
      {OUTRO_SHOTS.map(({ at: _at, ...s }, i) => (
        <Shot key={i} className="shot" src={images[i % images.length]} {...s} style={{ opacity: 0 }} />
      ))}
    </AbsoluteFill>
  );
};

const SearchCollage: React.FC<Extract<Beat, { type: "searchCollage" }>> = (b) => {
  const { colors: C } = useReel();
  const t = REF.searchCollage.start + useLocalTime();
  const bg = interpolateColors(r(t, [17.62, 18.35], [0, 1], IN_OUT), [0, 1], [C.lime, C.ink]);
  const url = b.url;
  const typed = t < 18.75 ? r(t, [17.8, 18.5], [0, url.length]) : r(t, [18.75, 19.1], [url.length, 0], IN);
  const visible = url.split("").slice(0, Math.ceil(typed));
  const scale = r(t, [17.75, 18.2], [0.35, 1], OUT) * r(t, [19.15, 19.45], [1, 0.8]);
  const fade = r(t, [19.2, 19.5], [1, 0]);
  return (
    <AbsoluteFill style={{ backgroundColor: bg }}>
      {t >= 17.75 && t < 19.5 && (
        <Center style={{ transform: `translateY(${r(t, [17.75, 18.2], [26, 0], OUT)}px)` }}>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              height: 76,
              minWidth: 76,
              padding: visible.length ? "0 30px 0 28px" : 0,
              borderRadius: 38,
              backgroundColor: C.pill,
              opacity: r(t, [17.75, 17.85], [0, 1]) * r(fade, [0, 0.4], [0, 1]),
              transform: `scale(${scale})`,
              fontSize: 22,
              fontWeight: 500,
              color: C.ink,
              whiteSpace: "pre",
            }}
          >
            <SearchIcon color={C.ink} />
            {visible.length > 0 && (
              <span style={{ marginLeft: 18 }}>
                {visible.map((ch, i) => (
                  <span key={i} style={{ opacity: r(typed - i, [0, 1], [0.3, 1]) }}>
                    {ch}
                  </span>
                ))}
              </span>
            )}
          </div>
        </Center>
      )}
      <Collage />
    </AbsoluteFill>
  );
};

const Thanks: React.FC<Extract<Beat, { type: "thanks" }>> = (b) => {
  const { colors: C } = useReel();
  const lt = useLocalTime();
  return (
    <AbsoluteFill style={{ backgroundColor: C.ink }}>
      <Center>
        <div style={{ fontSize: 53, fontWeight: 500, whiteSpace: "nowrap", transform: `scale(${r(lt, [0, 1.8], [1.06, 0.9])})` }}>
          <ScatterText text={b.accent + b.rest} start={0} spread={0.95} seed="thanks" color={(i) => (i < b.accent.length ? C.accent : C.cream)} />
        </div>
      </Center>
    </AbsoluteFill>
  );
};

// Default mark: a monogram tile that pops in on GSAP's back-out.
const MonogramMark: React.FC<{ letter: string }> = ({ letter }) => {
  const { colors: C } = useReel();
  const ref = useGsapTimeline<HTMLDivElement>(
    ({ timeline, scope }) => {
      timeline.fromTo(scope, { scale: 0, rotate: -90, opacity: 0 }, { scale: 1, rotate: 0, opacity: 1, duration: 0.45, ease: "back.out(1.8)" }, 0);
    },
    { dependencies: [letter] },
  );
  return (
    <div
      ref={ref}
      style={{ width: 48, height: 48, borderRadius: 12, backgroundColor: C.brand, color: "#fff", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 30, fontWeight: 700 }}
    >
      {letter.toUpperCase()}
    </div>
  );
};

const EndCard: React.FC<Extract<Beat, { type: "endCard" }>> = (b) => {
  const { colors: C, Mark, italicFontFamily } = useReel();
  const lt = useLocalTime();
  const reveal = r(lt, [0.65, 1.15], [0, 1], OUT);
  return (
    <AbsoluteFill style={{ backgroundColor: C.end }}>
      <Center>
        <div style={{ display: "flex", alignItems: "center" }}>
          {Mark ? <Mark t={lt} /> : <MonogramMark letter={b.bold.charAt(0)} />}
          <div style={{ maxWidth: reveal * 520, overflow: "hidden", whiteSpace: "nowrap" }}>
            <div style={{ paddingLeft: 12, fontSize: 60, lineHeight: 1.2, opacity: r(reveal, [0, 0.3], [0, 1]) }}>
              <span style={{ fontWeight: 700, color: "#111" }}>{b.bold}</span>
              <span style={{ fontWeight: 700, color: C.brand }}>{b.dot}</span>
              <span style={{ fontFamily: italicFontFamily ?? FIGTREE_ITALIC, fontStyle: "italic", fontWeight: 300, color: interpolateColors(reveal, [0.6, 1], ["#888", "#111"]) }}>
                {b.light}
              </span>
            </div>
          </div>
        </div>
      </Center>
      <AbsoluteFill style={{ backgroundColor: "#000", opacity: r(lt, [1.4, 3.0], [0, 1], Easing.inOut(Easing.quad)) }} />
    </AbsoluteFill>
  );
};

const BeatView: React.FC<{ beat: Beat }> = ({ beat }) => {
  switch (beat.type) {
    case "collageTitle":
      return <CollageTitle {...beat} />;
    case "words":
      return <Words {...beat} />;
    case "cursorCounter":
      return <CursorCounter {...beat} />;
    case "ghostCounter":
      return <GhostCounter {...beat} />;
    case "badgeCounter":
      return <BadgeCounter {...beat} />;
    case "badgeSentence":
      return <BadgeSentence {...beat} />;
    case "arrowWords":
      return <ArrowWords {...beat} />;
    case "searchCollage":
      return <SearchCollage {...beat} />;
    case "thanks":
      return <Thanks {...beat} />;
    case "endCard":
      return <EndCard {...beat} />;
  }
};

// SFX derived from structure: [kit key, beat type, seconds into the beat].
const SFX_POINTS: [keyof SfxKit, Beat["type"], number, ((b: Beat) => boolean)?][] = [
  ["darkCut", "words", -0.05, (b) => b.type === "words" && b.theme === "dark"],
  ["boxSnap", "cursorCounter", 1.38],
  ["ghostWord", "ghostCounter", 0.85],
  ["arrowPull", "arrowWords", 0.55],
  ["toDark", "searchCollage", 0],
  ["collage", "searchCollage", 1.3],
  ["logo", "endCard", 0.05],
];

export const StatReel: React.FC<{ config: StatReelConfig; mute?: "none" | "sfx" | "music" }> = ({ config, mute = "none" }) => {
  const scale = useVideoConfig().width / STAGE_W;
  const duration = statReelDuration(config);
  const timeline = statReelTimeline(config);
  const { music, fps } = config;
  const tail = Math.round(ARROW_TAIL * fps);
  return (
    <Ctx.Provider value={config}>
      <AbsoluteFill style={{ backgroundColor: "#000", fontFamily: config.fontFamily ?? FIGTREE }}>
        <div style={{ position: "absolute", width: STAGE_W, height: STAGE_H, transform: `scale(${scale})`, transformOrigin: "0 0", overflow: "hidden" }}>
          {timeline.map(({ beat, from, frames }, i) => (
            <Sequence
              key={i}
              from={from}
              durationInFrames={beat.type === "arrowWords" ? frames + tail : frames}
              style={{ zIndex: beat.type === "arrowWords" ? 2 : 1 }}
            >
              <BeatView beat={beat} />
            </Sequence>
          ))}
        </div>
        {music && mute !== "music" && (
          <Audio
            src={staticFile(music.src)}
            volume={(f) => music.gain * r(f, [0, 10, duration - 90, duration], [0, 1, 1, 0])}
          />
        )}
        {mute !== "sfx" &&
          SFX_POINTS.flatMap(([key, type, offset, match]) => {
            const kit = config.sfx[key];
            if (!kit) return [];
            return timeline
              .filter(({ beat }) => beat.type === type && (!match || match(beat)))
              .map(({ from }, j) => (
                <Sequence key={`${key}-${j}`} from={Math.max(0, from + Math.round(offset * fps))} layout="none">
                  <Audio src={staticFile(kit.src)} volume={kit.volume} />
                </Sequence>
              ));
          })}
      </AbsoluteFill>
    </Ctx.Provider>
  );
};
