/**
 * Example video built on KineticWordWall. Copy next to KineticWordWall.tsx and
 * timing.ts (from scripts/plan_timeline.py), then rename and edit.
 *
 * Register in src/Root.tsx:
 *   <Composition id="MyWordWall" component={MyWordWall} durationInFrames={DURATION}
 *     fps={FPS} width={1920} height={1080} defaultProps={{ mute: "none" }} />
 * (1080×1920 or 1080×1080 work too — the engine scales to the frame.)
 */
import React from "react";
import { loadFont as loadInter } from "@remotion/google-fonts/Inter";
import { loadFont as loadSerif } from "@remotion/google-fonts/SourceSerif4";
import { KineticWordWall, WordWallConfig, WordWallProps, scenesFromTiming } from "./KineticWordWall";
import { DURATION, FPS, SCENES, EXTRA_HIT_FRAMES } from "./timing";

const { fontFamily: SANS } = loadInter("normal", { weights: ["500", "800"], subsets: ["latin"] });
const { fontFamily: SERIF } = loadSerif("normal", { weights: ["400"], subsets: ["latin"] });

// Optional bespoke end card (spec end.kind = "custom", ref = "Logo"). Delete it,
// and `{ Logo }` below, if the spec uses a "wordmark" end card. For SFX-only, set
// music: null; for no extra hits, delete extraSfx.
const Logo: React.FC = () => null;

export const MY_CONFIG: WordWallConfig = {
  palette: {
    paper: "#F8F8F8",
    ink: "#111114",
    wall: "#5B50E8", // one saturated brand color
    wallInk: "#1C1652", // the same hue, much darker: body text recedes, the highlight pops
    highlight: "#FFFFFF",
    accent: "#5B50E8",
    endBg: "#0A0A0C",
    endInk: "#FFFFFF",
    bar: "#5B50E8",
  },
  fonts: { sans: SANS, serif: SERIF, display: SANS, displayWeight: 800, displayCapRatio: 0.727 },
  scenes: scenesFromTiming(SCENES, { Logo }),

  // Sound kit: one file per event type. peakOffset from scripts/sfx_peaks.py.
  // Volumes put every hit ~3 dB over a music bed at gain 0.4 for one loud,
  // punchy reference track. They're a starting point, so verify per track
  // with scripts/check_audio.py.
  sound: {
    typeWord: { src: "pop.wav", peakOffset: 0, volume: 0.52 },
    wallIn: { src: "sfx/air.mp3", peakOffset: 9, volume: 4.1 }, // quiet file, hence > 1
    wallSwap: { src: "sfx/digital-snap.wav", peakOffset: 0, volume: 0.69 },
    statement: { src: "sfx/crystal-chime.wav", peakOffset: 0, volume: 0.87 },
    reveal: { src: "sfx/sub-swoosh.wav", peakOffset: 3, volume: 0.76 },
    revealImpact: { src: "sfx/deep-drop.wav", peakOffset: 0, volume: 0.43 },
  },
  extraSfx: EXTRA_HIT_FRAMES.map((frame) => ({ src: "pop.wav", frame, volume: 0.77 })),

  music: {
    src: "music/track.mp3",
    trimBefore: 1710.9, // from analyze_music.py, then nudged after check_audio.py
    gain: 0.4,
    duckOn: ["typeWord", "statement", "reveal"], // never "wallIn" — keep the drop intact
    // duckFrames: [81], // one-off dip where check_audio.py shows a hit stacking hot
  },
};

export const MY_DURATION = DURATION;
export const MY_FPS = FPS;

export const MyWordWall: React.FC<WordWallProps> = ({ mute }) => (
  <KineticWordWall config={MY_CONFIG} mute={mute} />
);
