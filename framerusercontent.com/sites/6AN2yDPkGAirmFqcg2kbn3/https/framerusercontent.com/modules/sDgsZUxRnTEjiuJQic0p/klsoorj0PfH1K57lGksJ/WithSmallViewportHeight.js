import { jsx as _jsx } from "react/jsx-runtime";
import { useEffect, useState } from "react";
/**
 * @framerDisableUnlink
 */ export function withSmallViewportHeight(Component) {
  return (props) => {
    const [heightValue, setHeightValue] = useState("100vh");
    useEffect(() => {
      const vw = window.innerWidth;
      if (vw <= 390) {
        // Mobile: calculamos el svh estático en píxeles
        const vh = window.innerHeight * 0.01;
        document.documentElement.style.setProperty("--svh", `${vh}px`);
        setHeightValue(`${window.innerHeight}px`);
      } else {
        // Desktop (o small desktop): altura CSS normal
        setHeightValue("100vh");
      } // No añadimos resize listener para mantenerlo estático
    }, []);
    return /*#__PURE__*/ _jsx(Component, {
      ...props,
      style: { ...props.style, height: heightValue },
    });
  };
}
export const __FramerMetadata__ = {
  exports: {
    withSmallViewportHeight: {
      type: "reactHoc",
      name: "withSmallViewportHeight",
      annotations: { framerDisableUnlink: "", framerContractVersion: "1" },
    },
    __FramerMetadata__: { type: "variable" },
  },
};
//# sourceMappingURL=./WithSmallViewportHeight.map
