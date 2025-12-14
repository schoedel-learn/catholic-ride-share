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
        // High Contrast Flat Design Palette
        // Text
        navy: "#0A1628",       // Almost black navy - maximum contrast
        // Accents - Vibrant, bold colors
        marian: {
          DEFAULT: "#0052CC",  // Vibrant Marian blue
          50: "#E6F0FF",
          100: "#CCE0FF",
          200: "#99C2FF",
          300: "#66A3FF",
          400: "#3385FF",
          500: "#0052CC",       // Base - more saturated
          600: "#0047B3",
          700: "#003D99",
          800: "#003380",
          900: "#002966",
        },
        gold: {
          DEFAULT: "#FFB800",  // Bright gold - more vibrant
          50: "#FFF8E6",
          100: "#FFF1CC",
          200: "#FFE499",
          300: "#FFD666",
          400: "#FFC933",
          500: "#FFB800",       // Base - brighter
          600: "#E6A600",
          700: "#CC9400",
          800: "#B38200",
          900: "#997000",
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
