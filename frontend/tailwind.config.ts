import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // Marian Blue & Gold Palette (WCAG AA/AAA compliant)
        // Backgrounds
        ivory: "#F7F5F0",      // Soft ivory - primary background
        // Text
        navy: "#102A43",       // Deep navy - primary text (AAA on white/ivory)
        // Accents
        marian: {
          DEFAULT: "#1E5AA8",  // Marian blue - primary accent
          50: "#EBF2FA",
          100: "#D6E4F5",
          200: "#ADC9EB",
          300: "#85AEE0",
          400: "#5C93D6",
          500: "#1E5AA8",       // Base
          600: "#1A4E93",
          700: "#16427E",
          800: "#123669",
          900: "#0E2A54",
        },
        gold: {
          DEFAULT: "#F4B41A",  // Papal gold - secondary accent
          50: "#FEF9E7",
          100: "#FDF3CF",
          200: "#FBE79F",
          300: "#F9DB6F",
          400: "#F6C73F",
          500: "#F4B41A",       // Base
          600: "#D99C0E",
          700: "#B5820C",
          800: "#91680A",
          900: "#6D4E07",
        },
        // Legacy aliases for compatibility
        "crs-navy": "#102A43",
        "crs-gold": "#F4B41A",
      },
    },
  },
  plugins: [],
};

export default config;
