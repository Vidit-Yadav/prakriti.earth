import { jsx as _jsx } from "react/jsx-runtime";
export function BackOverride() {
  return {
    onTap() {
      // If there's somewhere to go back to, go back…
      if (window.history.length > 1) {
        window.history.back();
      } else {
        // …otherwise fall back to some “home” URL
        window.location.href = "/case-studies";
      }
    },
  };
}
import { useContext as __legacyOverrideHOC_useContext } from "react";
import { DataObserverContext as __legacyOverrideHOC_DataObserverContext } from "framer";
export function withBackOverride(C) {
  return (props) => {
    __legacyOverrideHOC_useContext(__legacyOverrideHOC_DataObserverContext);
    return _jsx(C, { ...props, ...BackOverride(props) });
  };
}
withBackOverride.displayName = "BackOverride";
export const __FramerMetadata__ = {
  exports: {
    withBackOverride: {
      type: "reactHoc",
      name: "withBackOverride",
      annotations: { framerContractVersion: "1" },
    },
    BackOverride: {
      type: "override",
      name: "BackOverride",
      annotations: { framerContractVersion: "1" },
    },
    __FramerMetadata__: { type: "variable" },
  },
};
//# sourceMappingURL=./navigate_case.map
