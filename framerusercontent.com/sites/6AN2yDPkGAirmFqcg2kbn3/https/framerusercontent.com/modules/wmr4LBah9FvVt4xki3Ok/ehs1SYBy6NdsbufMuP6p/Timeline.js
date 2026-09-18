import { jsx as _jsx } from "react/jsx-runtime";
import { useRef } from "react";
import { motion, useScroll, useTransform } from "framer-motion";
import { addPropertyControls, ControlType } from "framer";
export function TimelineLine(props) {
  const {
    width = "4px",
    color = "#0F1F10",
    offsetStart = "start end",
    offsetEnd = "end start",
  } = props;
  const ref = useRef(null); // Track scroll progress of this component
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: [offsetStart, offsetEnd],
  }); // Map scroll progress [0,1] to scaleY [0,1]
  const scaleY = useTransform(scrollYProgress, [0, 1], [0, 1]);
  return /*#__PURE__*/ _jsx(motion.div, {
    ref: ref,
    style: {
      position: "absolute",
      top: 0,
      height: "100%",
      width: width,
      backgroundColor: color,
      transformOrigin: "top center",
      scaleY: scaleY,
    },
  });
}
addPropertyControls(TimelineLine, {
  width: { type: ControlType.String, title: "Width", defaultValue: "4px" },
  color: { type: ControlType.Color, title: "Color", defaultValue: "#0F1F10" },
  offsetStart: {
    type: ControlType.String,
    title: "Offset Start",
    defaultValue: "start end",
    description: "Scroll offset start (e.g. 'start end')",
  },
  offsetEnd: {
    type: ControlType.String,
    title: "Offset End",
    defaultValue: "end start",
    description: "Scroll offset end (e.g. 'end start')",
  },
});
export const __FramerMetadata__ = {
  exports: {
    TimelineLine: {
      type: "reactComponent",
      name: "TimelineLine",
      slots: [],
      annotations: { framerContractVersion: "1" },
    },
    __FramerMetadata__: { type: "variable" },
  },
};
//# sourceMappingURL=./Timeline.map
