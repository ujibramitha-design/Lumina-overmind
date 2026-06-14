export const tokens = {
  colors: {
    // Primary colors
    primary: {
      50: '#f0fdf4',
      100: '#dcfce7',
      200: '#bbf7d0',
      300: '#86efac',
      400: '#4ade80',
      500: '#22c55e',
      600: '#16a34a',
      700: '#15803d',
      800: '#166534',
      900: '#14532d',
      950: '#052e16',
    },

    // Neutral colors (zinc theme)
    neutral: {
      50: '#fafafa',
      100: '#f5f5f5',
      200: '#e5e5e5',
      300: '#d4d4d4',
      400: '#a3a3a3',
      500: '#737373',
      600: '#525252',
      700: '#404040',
      800: '#262626',
      900: '#171717',
      950: '#0a0a0a',
    },

    // Semantic colors
    semantic: {
      success: '#22c55e',
      warning: '#f59e0b',
      error: '#ef4444',
      info: '#3b82f6',
    },

    // Background colors
    background: {
      primary: '#000000',
      secondary: '#0a0a0a',
      tertiary: '#171717',
      card: '#0a0a0a',
      cardHover: '#171717',
      border: '#27272a',
      input: '#18181b',
    },

    // Text colors
    text: {
      primary: '#fafafa',
      secondary: '#a3a3a3',
      tertiary: '#737373',
      muted: '#525252',
      inverse: '#000000',
    },
  },

  spacing: {
    0: '0',
    1: '0.25rem', // 4px
    2: '0.5rem', // 8px
    3: '0.75rem', // 12px
    4: '1rem', // 16px
    5: '1.25rem', // 20px
    6: '1.5rem', // 24px
    8: '2rem', // 32px
    10: '2.5rem', // 40px
    12: '3rem', // 48px
    16: '4rem', // 64px
    20: '5rem', // 80px
    24: '6rem', // 96px
    32: '8rem', // 128px
  },

  typography: {
    fontFamily: {
      sans: ['Inter', 'system-ui', 'sans-serif'],
      mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
    },

    fontSize: {
      xs: ['0.75rem', { lineHeight: '1rem' }],
      sm: ['0.875rem', { lineHeight: '1.25rem' }],
      base: ['1rem', { lineHeight: '1.5rem' }],
      lg: ['1.125rem', { lineHeight: '1.75rem' }],
      xl: ['1.25rem', { lineHeight: '1.75rem' }],
      '2xl': ['1.5rem', { lineHeight: '2rem' }],
      '3xl': ['1.875rem', { lineHeight: '2.25rem' }],
      '4xl': ['2.25rem', { lineHeight: '2.5rem' }],
      '5xl': ['3rem', { lineHeight: '1' }],
      '6xl': ['3.75rem', { lineHeight: '1' }],
    },

    fontWeight: {
      thin: '100',
      light: '300',
      normal: '400',
      medium: '500',
      semibold: '600',
      bold: '700',
      extrabold: '800',
      black: '900',
    },

    letterSpacing: {
      tighter: '-0.05em',
      tight: '-0.025em',
      normal: '0em',
      wide: '0.025em',
      wider: '0.05em',
      widest: '0.1em',
    },
  },

  borderRadius: {
    none: '0',
    sm: '0.125rem', // 2px
    base: '0.25rem', // 4px
    md: '0.375rem', // 6px
    lg: '0.5rem', // 8px
    xl: '0.75rem', // 12px
    '2xl': '1rem', // 16px
    full: '9999px',
  },

  shadows: {
    sm: '0 1px 2px 0 rgb(0 0 0 / 0.05)',
    base: '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)',
    md: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
    lg: '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
    xl: '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)',
    '2xl': '0 25px 50px -12px rgb(0 0 0 / 0.25)',
    inner: 'inset 0 2px 4px 0 rgb(0 0 0 / 0.05)',

    // Custom shadows for dark theme
    dark: {
      sm: '0 1px 2px 0 rgb(0 0 0 / 0.3)',
      base: '0 1px 3px 0 rgb(0 0 0 / 0.4), 0 1px 2px -1px rgb(0 0 0 / 0.4)',
      md: '0 4px 6px -1px rgb(0 0 0 / 0.4), 0 2px 4px -2px rgb(0 0 0 / 0.4)',
      lg: '0 10px 15px -3px rgb(0 0 0 / 0.4), 0 4px 6px -4px rgb(0 0 0 / 0.4)',
      xl: '0 20px 25px -5px rgb(0 0 0 / 0.4), 0 8px 10px -6px rgb(0 0 0 / 0.4)',
      glow: '0 0 20px rgb(34 197 94 / 0.3)',
      glowRed: '0 0 20px rgb(239 68 68 / 0.3)',
    },
  },

  animation: {
    duration: {
      75: '75ms',
      100: '100ms',
      150: '150ms',
      200: '200ms',
      300: '300ms',
      500: '500ms',
      700: '700ms',
      1000: '1000ms',
    },

    easing: {
      linear: 'linear',
      ease: 'ease',
      easeIn: 'ease-in',
      easeOut: 'ease-out',
      easeInOut: 'ease-in-out',
    },

    keyframes: {
      fadeIn: {
        '0%': { opacity: '0' },
        '100%': { opacity: '1' },
      },
      fadeOut: {
        '0%': { opacity: '1' },
        '100%': { opacity: '0' },
      },
      slideIn: {
        '0%': { transform: 'translateX(-100%)' },
        '100%': { transform: 'translateX(0)' },
      },
      slideOut: {
        '0%': { transform: 'translateX(0)' },
        '100%': { transform: 'translateX(-100%)' },
      },
      scaleIn: {
        '0%': { transform: 'scale(0.95)', opacity: '0' },
        '100%': { transform: 'scale(1)', opacity: '1' },
      },
      pulse: {
        '0%, 100%': { opacity: '1' },
        '50%': { opacity: '0.5' },
      },
      spin: {
        '0%': { transform: 'rotate(0deg)' },
        '100%': { transform: 'rotate(360deg)' },
      },
      bounce: {
        '0%, 100%': { transform: 'translateY(0)' },
        '50%': { transform: 'translateY(-10px)' },
      },
      glow: {
        '0%, 100%': { boxShadow: '0 0 5px rgb(34 197 94 / 0.5)' },
        '50%': { boxShadow: '0 0 20px rgb(34 197 94 / 0.8)' },
      },
    },
  },

  breakpoints: {
    sm: '640px',
    md: '768px',
    lg: '1024px',
    xl: '1280px',
    '2xl': '1536px',
  },

  zIndex: {
    hide: -1,
    auto: 'auto',
    base: 0,
    docked: 10,
    dropdown: 1000,
    sticky: 1100,
    banner: 1200,
    overlay: 1300,
    modal: 1400,
    popover: 1500,
    skipLink: 1600,
    toast: 1700,
    tooltip: 1800,
  },
}

// Utility functions for working with tokens
export const getColor = (path: string) => {
  const keys = path.split('.')
  let value: any = tokens.colors

  for (const key of keys) {
    value = value[key]
    if (value === undefined) return undefined
  }

  return value
}

export const getSpacing = (size: keyof typeof tokens.spacing) => {
  return tokens.spacing[size]
}

export const getTypography = (size: keyof typeof tokens.typography.fontSize) => {
  return tokens.typography.fontSize[size]
}

// CSS custom properties generator
export const generateCSSVariables = () => {
  const cssVars: Record<string, string> = {}

  const flattenTokens = (obj: any, prefix = '') => {
    for (const [key, value] of Object.entries(obj)) {
      const cssVar = `--${prefix}${key}`

      if (typeof value === 'object' && value !== null) {
        flattenTokens(value, `${prefix}${key}-`)
      } else {
        cssVars[cssVar] = String(value)
      }
    }
  }

  flattenTokens(tokens.colors, 'color-')
  flattenTokens(tokens.spacing, 'spacing-')
  flattenTokens(tokens.typography.fontSize, 'text-')
  flattenTokens(tokens.typography.fontWeight, 'font-')
  flattenTokens(tokens.borderRadius, 'radius-')
  flattenTokens(tokens.shadows, 'shadow-')
  flattenTokens(tokens.animation.duration, 'duration-')
  flattenTokens(tokens.zIndex, 'z-')

  return cssVars
}

// Component-specific tokens
export const componentTokens = {
  button: {
    padding: {
      sm: `${tokens.spacing[2]} ${tokens.spacing[3]}`,
      md: `${tokens.spacing[3]} ${tokens.spacing[6]}`,
      lg: `${tokens.spacing[4]} ${tokens.spacing[8]}`,
    },
    borderRadius: tokens.borderRadius.md,
    fontSize: tokens.typography.fontSize.sm,
    fontWeight: tokens.typography.fontWeight.medium,
    transition: `all ${tokens.animation.duration[200]} ${tokens.animation.easing.easeOut}`,
  },

  card: {
    padding: tokens.spacing[6],
    borderRadius: tokens.borderRadius.lg,
    backgroundColor: tokens.colors.background.card,
    border: `1px solid ${tokens.colors.background.border}`,
    boxShadow: tokens.shadows.dark.base,
    transition: `all ${tokens.animation.duration[200]} ${tokens.animation.easing.easeOut}`,
  },

  input: {
    padding: `${tokens.spacing[3]} ${tokens.spacing[4]}`,
    borderRadius: tokens.borderRadius.md,
    backgroundColor: tokens.colors.background.input,
    border: `1px solid ${tokens.colors.background.border}`,
    fontSize: tokens.typography.fontSize.base,
    transition: `all ${tokens.animation.duration[200]} ${tokens.animation.easing.easeOut}`,
  },

  sidebar: {
    width: '280px',
    backgroundColor: tokens.colors.background.secondary,
    borderRight: `1px solid ${tokens.colors.background.border}`,
    padding: tokens.spacing[4],
  },

  header: {
    height: '64px',
    backgroundColor: tokens.colors.background.secondary,
    borderBottom: `1px solid ${tokens.colors.background.border}`,
    padding: `0 ${tokens.spacing[6]}`,
  },
}

export default tokens
