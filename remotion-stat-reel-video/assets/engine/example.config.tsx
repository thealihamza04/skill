import React from "react";
import { useGsapTimeline } from "@remotion/gsap";
import { StatReel, statReelDuration, type StatReelConfig } from "./StatReel";

// Example: the Ali Hamza reel (src/ReachReel in the project this skill came
// from). Every number is a verified fact — github.com/thealihamza04 (22+
// public repos), 4 apps shipped to production, 7 projects in
// public/projects. Keep that rule when you edit the copy.

// A custom logo mark rebuilt as vector shapes (the AH mark on its 97.5px
// grid). GSAP slides A and H in from either side, then snaps the fold on.
// `t` is seconds since the end card started; the timeline is local to it.
const AH_A: [number, number, number, number][] = [
  [1, 0, 3, 1],
  [0, 1, 1, 6],
  [4, 1, 1, 6],
  [1, 4, 3, 1],
];
const AH_H: [number, number, number, number][] = [
  [5.53, 0, 0.98, 7],
  [9.55, 0, 0.98, 7],
  [6.51, 3, 3.04, 1],
];

const AhMark: React.FC<{ t: number }> = () => {
  const ref = useGsapTimeline<SVGSVGElement>(({ timeline, selector }) => {
    timeline.fromTo(selector(".a"), { x: -6, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: "expo.out" }, 0);
    timeline.fromTo(selector(".h"), { x: 6, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: "expo.out" }, 0.06);
    timeline.fromTo(selector(".fold"), { opacity: 0 }, { opacity: 1, duration: 0.01 }, 0.52);
  });
  const rects = (shapes: typeof AH_A) => shapes.map(([x, y, w, h], i) => <rect key={i} x={x} y={y} width={w} height={h} fill="#111" />);
  return (
    <svg ref={ref} width={60} height={40} viewBox="-0.2 -0.2 10.93 7.4" style={{ overflow: "visible" }} shapeRendering="crispEdges">
      <g className="a">{rects(AH_A)}</g>
      <g className="h">{rects(AH_H)}</g>
      <polygon className="fold" points="3.21,4.75 4.75,4.75 4.75,3.22" fill="#5B50E8" shapeRendering="geometricPrecision" />
    </svg>
  );
};

export const EXAMPLE_REEL: StatReelConfig = {
  fps: 60,
  colors: {
    lime: "#ecfaa8",
    ink: "#004449",
    cream: "#f2ffc3",
    ghost: "#d2e59c",
    accent: "#dcf36a",
    pill: "#eef9b8",
    squiggleDark: "#1f5c60",
    end: "#fcfcfc",
    brand: "#5B50E8",
  },
  images: [
    "projects/bidzest.png",
    "projects/readnest.png",
    "projects/bigbrainss.png",
    "projects/anoma_eye.png",
    "projects/linkedin_clone.png",
    "projects/tellmeyourneed.png",
    "projects/lahore_board_insight.png",
  ],
  beats: [
    { type: "collageTitle", line1: "I've Built", stat: "22+", icon: "code", line2: "repos on", line3: "GitHub" },
    { type: "words", theme: "light", words: ["Hi", "I'm", "Building"] },
    { type: "words", theme: "dark", words: ["I", "have", "built"] },
    { type: "cursorCounter", from: 0, to: 22, suffix: "+", label: "public repositories" },
    { type: "ghostCounter", count: 4, word: "Shipped", then: ["to", "Production"] },
    { type: "badgeCounter", label: "projects built", steps: [0, 2, 2, 5, 5, 7, 7, 1] },
    { type: "badgeSentence", from: 9, to: 4, lead: "Taking", tail: "products from", line2: "idea to production" },
    { type: "arrowWords", lead: "Check out", phrases: [["My", "latest"], ["Case", "studies"], ["from", "here"]] },
    { type: "searchCollage", url: "thealihamza04.vercel.app" },
    { type: "endCard", bold: "thealihamza04", dot: "", light: "" },
  ],
  Mark: AhMark,
  music: { src: "electronic-chill.mp3", gain: 0.5 },
  sfx: {
    darkCut: { src: "sfx/swoosh.mp3", volume: 0.35 },
    boxSnap: { src: "sfx/digital-snap.wav", volume: 0.4 },
    ghostWord: { src: "sfx/highlighter.mp3", volume: 0.25 },
    arrowPull: { src: "sfx/air.mp3", volume: 0.35 },
    toDark: { src: "sfx/sub-swoosh.wav", volume: 0.45 },
    collage: { src: "sfx/compute-pulse.wav", volume: 0.3 },
    logo: { src: "sfx/crystal-chime.wav", volume: 0.4 },
  },
};

export const EXAMPLE_REEL_DURATION = statReelDuration(EXAMPLE_REEL);

export const ExampleReel: React.FC<{ mute?: "none" | "sfx" | "music" }> = ({ mute }) => (
  <StatReel config={EXAMPLE_REEL} mute={mute} />
);
