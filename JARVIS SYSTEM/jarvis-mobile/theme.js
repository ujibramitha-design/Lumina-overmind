/**
 * JARVIS Mobile Theme Configuration
 * =================================
 * 
 * HUD-style theme with glassmorphism, neon green accents,
 * and futuristic dark aesthetics
 */

import { StyleSheet } from 'react-native';

// Color Palette
export const colors = {
  // Background
  background: '#000000',
  backgroundDark: '#0a0a0a',
  backgroundLight: '#1a1a1a',
  
  // Glassmorphism
  glass: 'rgba(20, 20, 20, 0.7)',
  glassBorder: 'rgba(16, 185, 129, 0.3)',
  glassBorderActive: 'rgba(16, 185, 129, 0.8)',
  
  // Neon Green (JARVIS Brand)
  neonGreen: '#10b981',
  neonGreenBright: '#34d399',
  neonGreenDim: '#059669',
  neonGreenGlow: 'rgba(16, 185, 129, 0.5)',
  
  // Status Colors
  success: '#10b981',
  warning: '#f59e0b',
  error: '#ef4444',
  info: '#3b82f6',
  
  // Text
  text: '#ffffff',
  textDim: '#a1a1aa',
  textMuted: '#71717a',
  
  // Accents
  accent: '#10b981',
  accentSecondary: '#3b82f6',
  accentTertiary: '#8b5cf6',
};

// Typography
export const typography = {
  // Font Families
  fontFamily: {
    mono: 'Courier New',
    sans: 'System',
  },
  
  // Font Sizes
  fontSize: {
    xs: 10,
    sm: 12,
    base: 14,
    lg: 16,
    xl: 18,
    '2xl': 20,
    '3xl': 24,
    '4xl': 32,
    '5xl': 40,
  },
  
  // Font Weights
  fontWeight: {
    light: '300',
    normal: '400',
    medium: '500',
    semibold: '600',
    bold: '700',
  },
  
  // Line Heights
  lineHeight: {
    tight: 1.2,
    normal: 1.5,
    relaxed: 1.75,
  },
};

// Spacing
export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  '2xl': 48,
  '3xl': 64,
};

// Border Radius
export const borderRadius = {
  sm: 4,
  md: 8,
  lg: 12,
  xl: 16,
  '2xl': 24,
  full: 9999,
};

// Shadows
export const shadows = {
  small: {
    shadowColor: colors.neonGreenGlow,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 4,
    elevation: 4,
  },
  medium: {
    shadowColor: colors.neonGreenGlow,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 8,
  },
  large: {
    shadowColor: colors.neonGreenGlow,
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.4,
    shadowRadius: 16,
    elevation: 16,
  },
  neon: {
    shadowColor: colors.neonGreen,
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.8,
    shadowRadius: 8,
    elevation: 12,
  },
};

// Glassmorphism Styles
export const glassStyles = {
  card: {
    backgroundColor: colors.glass,
    borderWidth: 1,
    borderColor: colors.glassBorder,
    borderRadius: borderRadius.lg,
    ...shadows.medium,
  },
  cardActive: {
    backgroundColor: colors.glass,
    borderWidth: 1,
    borderColor: colors.glassBorderActive,
    borderRadius: borderRadius.lg,
    ...shadows.neon,
  },
  panel: {
    backgroundColor: 'rgba(10, 10, 10, 0.8)',
    borderWidth: 1,
    borderColor: colors.glassBorder,
    borderRadius: borderRadius.xl,
    ...shadows.large,
  },
};

// HUD Styles
export const hudStyles = {
  header: {
    backgroundColor: 'rgba(0, 0, 0, 0.9)',
    borderBottomWidth: 1,
    borderBottomColor: colors.glassBorder,
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.md,
  },
  statusIndicator: {
    width: 8,
    height: 8,
    borderRadius: borderRadius.full,
    backgroundColor: colors.neonGreen,
    ...shadows.neon,
  },
  metricCard: {
    backgroundColor: colors.glass,
    borderWidth: 1,
    borderColor: colors.glassBorder,
    borderRadius: borderRadius.lg,
    padding: spacing.md,
    ...shadows.medium,
  },
  progressBar: {
    height: 4,
    backgroundColor: colors.backgroundLight,
    borderRadius: borderRadius.full,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    backgroundColor: colors.neonGreen,
    borderRadius: borderRadius.full,
  },
};

// Animation
export const animations = {
  pulse: {
    animation: 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
  },
  glow: {
    animation: 'glow 2s ease-in-out infinite alternate',
  },
  slideIn: {
    animation: 'slideIn 0.3s ease-out',
  },
};

// Complete StyleSheet
export const theme = StyleSheet.create({
  // Base
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  
  // Text
  text: {
    color: colors.text,
    fontFamily: typography.fontFamily.sans,
  },
  textDim: {
    color: colors.textDim,
    fontFamily: typography.fontFamily.sans,
  },
  textMuted: {
    color: colors.textMuted,
    fontFamily: typography.fontFamily.sans,
  },
  textMono: {
    color: colors.text,
    fontFamily: typography.fontFamily.mono,
  },
  
  // Neon Text
  neonText: {
    color: colors.neonGreen,
    textShadowColor: colors.neonGreen,
    textShadowOffset: { width: 0, height: 0 },
    textShadowRadius: 8,
  },
  
  // Glass Components
  glassCard: glassStyles.card,
  glassCardActive: glassStyles.cardActive,
  glassPanel: glassStyles.panel,
  
  // HUD Components
  hudHeader: hudStyles.header,
  statusIndicator: hudStyles.statusIndicator,
  metricCard: hudStyles.metricCard,
  progressBar: hudStyles.progressBar,
  progressFill: hudStyles.progressFill,
  
  // Buttons
  button: {
    backgroundColor: colors.glass,
    borderWidth: 1,
    borderColor: colors.glassBorder,
    borderRadius: borderRadius.md,
    paddingVertical: spacing.sm,
    paddingHorizontal: spacing.lg,
    ...shadows.small,
  },
  buttonActive: {
    backgroundColor: colors.glass,
    borderWidth: 1,
    borderColor: colors.glassBorderActive,
    borderRadius: borderRadius.md,
    paddingVertical: spacing.sm,
    paddingHorizontal: spacing.lg,
    ...shadows.neon,
  },
  buttonPrimary: {
    backgroundColor: colors.neonGreenDim,
    borderWidth: 1,
    borderColor: colors.neonGreen,
    borderRadius: borderRadius.md,
    paddingVertical: spacing.sm,
    paddingHorizontal: spacing.lg,
    ...shadows.neon,
  },
  
  // Inputs
  input: {
    backgroundColor: colors.backgroundLight,
    borderWidth: 1,
    borderColor: colors.glassBorder,
    borderRadius: borderRadius.md,
    paddingVertical: spacing.sm,
    paddingHorizontal: spacing.md,
    color: colors.text,
  },
  inputFocused: {
    backgroundColor: colors.backgroundLight,
    borderWidth: 1,
    borderColor: colors.glassBorderActive,
    borderRadius: borderRadius.md,
    paddingVertical: spacing.sm,
    paddingHorizontal: spacing.md,
    color: colors.text,
    ...shadows.neon,
  },
  
  // Status
  statusOnline: {
    backgroundColor: colors.success,
    ...shadows.neon,
  },
  statusOffline: {
    backgroundColor: colors.error,
  },
  statusWarning: {
    backgroundColor: colors.warning,
  },
  
  // Divider
  divider: {
    height: 1,
    backgroundColor: colors.glassBorder,
    marginVertical: spacing.md,
  },
  
  // Scrollbar (custom styling would need additional setup)
  scrollContent: {
    flexGrow: 1,
  },
});

export default theme;
