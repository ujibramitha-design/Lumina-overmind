/**
 * JARVIS Mobile - Dashboard Screen
 * =================================
 * 
 * Main HUD-style dashboard showing real-time system metrics,
 * connection status, and JARVIS thought process
 */

import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  TouchableOpacity,
  ActivityIndicator,
} from 'react-native';
import { LinearGradient } from 'react-native-linear-gradient';
import { theme, colors, spacing, borderRadius, shadows } from '../theme';

// Mock data (will be replaced with real API calls)
const mockSystemMetrics = {
  cpu: 45,
  memory: 62,
  disk: 38,
  network: { upload: 125, download: 340 },
  uptime: '15d 4h 32m',
  activeUsers: 23,
  totalCommands: 1547,
  successRate: 98.5,
};

const mockConnectionStatus = {
  whatsapp: { connected: true, lastSeen: '2m ago' },
  telegram: { connected: true, lastSeen: '1m ago' },
  websocket: { connected: true, latency: 45 },
};

const mockJarvisThought = {
  status: 'active',
  currentTask: 'Analyzing system performance metrics',
  confidence: 0.92,
  processingTime: '0.23s',
  lastAction: 'Generated daily summary report',
};

const StatusIndicator = ({ connected, size = 8 }) => (
  <View
    style={[
      styles.statusIndicator,
      { width: size, height: size, borderRadius: size / 2 },
      connected ? styles.statusOnline : styles.statusOffline,
    ]}
  />
);

const MetricCard = ({ title, value, unit, icon, progress, color = colors.neonGreen }) => (
  <View style={styles.metricCard}>
    <View style={styles.metricHeader}>
      <Text style={styles.metricIcon}>{icon}</Text>
      <Text style={styles.metricTitle}>{title}</Text>
    </View>
    <View style={styles.metricValueContainer}>
      <Text style={[styles.metricValue, { color }]}>
        {value}
        <Text style={styles.metricUnit}>{unit}</Text>
      </Text>
    </View>
    {progress !== undefined && (
      <View style={styles.progressBar}>
        <View
          style={[
            styles.progressFill,
            { width: `${progress}%`, backgroundColor: color },
          ]}
        />
      </View>
    )}
  </View>
);

const ConnectionCard = ({ platform, status, icon }) => (
  <View style={styles.connectionCard}>
    <View style={styles.connectionHeader}>
      <Text style={styles.connectionIcon}>{icon}</Text>
      <Text style={styles.connectionTitle}>{platform}</Text>
      <StatusIndicator connected={status.connected} />
    </View>
    <View style={styles.connectionDetails}>
      <Text style={[styles.connectionStatus, status.connected ? styles.textSuccess : styles.textError]}>
        {status.connected ? 'ONLINE' : 'OFFLINE'}
      </Text>
      <Text style={styles.connectionMeta}>Last seen: {status.lastSeen}</Text>
    </View>
  </View>
);

const ThoughtProcessCard = ({ thought }) => (
  <View style={styles.thoughtCard}>
    <View style={styles.thoughtHeader}>
      <Text style={styles.thoughtIcon}>🧠</Text>
      <Text style={styles.thoughtTitle}>JARVIS Thought Process</Text>
      <View style={styles.thoughtStatus}>
        <ActivityIndicator size="small" color={colors.neonGreen} />
        <Text style={styles.thoughtStatusText}>ACTIVE</Text>
      </View>
    </View>
    <View style={styles.thoughtContent}>
      <Text style={styles.thoughtTask}>{thought.currentTask}</Text>
      <View style={styles.thoughtMetrics}>
        <View style={styles.thoughtMetric}>
          <Text style={styles.thoughtMetricLabel}>Confidence</Text>
          <Text style={styles.thoughtMetricValue}>{(thought.confidence * 100).toFixed(0)}%</Text>
        </View>
        <View style={styles.thoughtMetric}>
          <Text style={styles.thoughtMetricLabel}>Processing</Text>
          <Text style={styles.thoughtMetricValue}>{thought.processingTime}</Text>
        </View>
      </View>
      <View style={styles.thoughtLastAction}>
        <Text style={styles.thoughtLastActionLabel}>Last Action:</Text>
        <Text style={styles.thoughtLastActionText}>{thought.lastAction}</Text>
      </View>
    </View>
  </View>
);

const DashboardScreen = ({ navigation }) => {
  const [metrics, setMetrics] = useState(mockSystemMetrics);
  const [connections, setConnections] = useState(mockConnectionStatus);
  const [thought, setThought] = useState(mockJarvisThought);
  const [loading, setLoading] = useState(false);

  // Simulate real-time updates
  useEffect(() => {
    const interval = setInterval(() => {
      setMetrics(prev => ({
        ...prev,
        cpu: Math.max(0, Math.min(100, prev.cpu + (Math.random() - 0.5) * 10)),
        memory: Math.max(0, Math.min(100, prev.memory + (Math.random() - 0.5) * 5)),
      }));
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  const refreshData = async () => {
    setLoading(true);
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));
    setLoading(false);
  };

  return (
    <View style={styles.container}>
      {/* Header */}
      <LinearGradient
        colors={[colors.backgroundDark, colors.background]}
        style={styles.header}
      >
        <View style={styles.headerContent}>
          <View>
            <Text style={styles.headerTitle}>JARVIS</Text>
            <Text style={styles.headerSubtitle}>Mobile Command Center</Text>
          </View>
          <TouchableOpacity
            style={styles.refreshButton}
            onPress={refreshData}
            disabled={loading}
          >
            {loading ? (
              <ActivityIndicator size="small" color={colors.neonGreen} />
            ) : (
              <Text style={styles.refreshIcon}>🔄</Text>
            )}
          </TouchableOpacity>
        </View>
        <View style={styles.statusBar}>
          <View style={styles.statusItem}>
            <StatusIndicator connected={true} />
            <Text style={styles.statusText}>System Online</Text>
          </View>
          <Text style={styles.uptimeText}>Uptime: {metrics.uptime}</Text>
        </View>
      </LinearGradient>

      {/* Content */}
      <ScrollView style={styles.scrollContent} showsVerticalScrollIndicator={false}>
        {/* System Metrics */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>System Metrics</Text>
          <View style={styles.metricsGrid}>
            <MetricCard
              title="CPU Usage"
              value={metrics.cpu.toFixed(0)}
              unit="%"
              icon="⚡"
              progress={metrics.cpu}
              color={metrics.cpu > 80 ? colors.error : colors.neonGreen}
            />
            <MetricCard
              title="Memory"
              value={metrics.memory.toFixed(0)}
              unit="%"
              icon="💾"
              progress={metrics.memory}
              color={metrics.memory > 80 ? colors.warning : colors.neonGreen}
            />
            <MetricCard
              title="Disk"
              value={metrics.disk.toFixed(0)}
              unit="%"
              icon="💿"
              progress={metrics.disk}
              color={colors.neonGreen}
            />
            <MetricCard
              title="Network"
              value={metrics.network.download}
              unit="MB/s"
              icon="📡"
              color={colors.accentSecondary}
            />
          </View>
        </View>

        {/* Connection Status */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Connection Status</Text>
          <ConnectionCard
            platform="WhatsApp"
            status={connections.whatsapp}
            icon="📱"
          />
          <ConnectionCard
            platform="Telegram"
            status={connections.telegram}
            icon="🤖"
          />
          <ConnectionCard
            platform="WebSocket"
            status={connections.websocket}
            icon="🔌"
          />
        </View>

        {/* JARVIS Thought Process */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>JARVIS Intelligence</Text>
          <ThoughtProcessCard thought={thought} />
        </View>

        {/* Quick Stats */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Quick Stats</Text>
          <View style={styles.statsRow}>
            <View style={styles.statItem}>
              <Text style={styles.statValue}>{metrics.activeUsers}</Text>
              <Text style={styles.statLabel}>Active Users</Text>
            </View>
            <View style={styles.statDivider} />
            <View style={styles.statItem}>
              <Text style={styles.statValue}>{metrics.totalCommands}</Text>
              <Text style={styles.statLabel}>Commands</Text>
            </View>
            <View style={styles.statDivider} />
            <View style={styles.statItem}>
              <Text style={styles.statValue}>{metrics.successRate}%</Text>
              <Text style={styles.statLabel}>Success Rate</Text>
            </View>
          </View>
        </View>

        {/* Quick Actions */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Quick Actions</Text>
          <TouchableOpacity
            style={styles.actionButton}
            onPress={() => navigation.navigate('Chat')}
          >
            <Text style={styles.actionIcon}>💬</Text>
            <Text style={styles.actionText}>Open Chat</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={styles.actionButton}
            onPress={() => navigation.navigate('CodeExplorer')}
          >
            <Text style={styles.actionIcon}>🔍</Text>
            <Text style={styles.actionText}>Explore Code</Text>
          </TouchableOpacity>
        </View>

        <View style={styles.spacer} />
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  
  // Header
  header: {
    paddingTop: spacing.xl,
    paddingHorizontal: spacing.lg,
    paddingBottom: spacing.lg,
    borderBottomWidth: 1,
    borderBottomColor: colors.glassBorder,
  },
  headerContent: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: spacing.md,
  },
  headerTitle: {
    fontSize: typography.fontSize['4xl'],
    fontWeight: typography.fontWeight.bold,
    color: colors.neonGreen,
    textShadowColor: colors.neonGreen,
    textShadowOffset: { width: 0, height: 0 },
    textShadowRadius: 10,
  },
  headerSubtitle: {
    fontSize: typography.fontSize.sm,
    color: colors.textDim,
    marginTop: spacing.xs,
  },
  refreshButton: {
    width: 40,
    height: 40,
    borderRadius: borderRadius.full,
    backgroundColor: colors.glass,
    borderWidth: 1,
    borderColor: colors.glassBorder,
    justifyContent: 'center',
    alignItems: 'center',
    ...shadows.small,
  },
  refreshIcon: {
    fontSize: 20,
  },
  statusBar: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  statusItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
  },
  statusText: {
    fontSize: typography.fontSize.sm,
    color: colors.textDim,
  },
  uptimeText: {
    fontSize: typography.fontSize.sm,
    color: colors.textMuted,
    fontFamily: typography.fontFamily.mono,
  },
  
  // Content
  scrollContent: {
    flex: 1,
  },
  
  // Section
  section: {
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.lg,
  },
  sectionTitle: {
    fontSize: typography.fontSize.lg,
    fontWeight: typography.fontWeight.semibold,
    color: colors.text,
    marginBottom: spacing.md,
    textTransform: 'uppercase',
    letterSpacing: 1,
  },
  
  // Metrics Grid
  metricsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: spacing.md,
  },
  metricCard: {
    width: '48%',
    backgroundColor: colors.glass,
    borderWidth: 1,
    borderColor: colors.glassBorder,
    borderRadius: borderRadius.lg,
    padding: spacing.md,
    ...shadows.medium,
  },
  metricHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
    marginBottom: spacing.sm,
  },
  metricIcon: {
    fontSize: 20,
  },
  metricTitle: {
    fontSize: typography.fontSize.sm,
    color: colors.textDim,
  },
  metricValueContainer: {
    marginBottom: spacing.sm,
  },
  metricValue: {
    fontSize: typography.fontSize['3xl'],
    fontWeight: typography.fontWeight.bold,
  },
  metricUnit: {
    fontSize: typography.fontSize.sm,
    color: colors.textMuted,
    fontWeight: typography.fontWeight.normal,
  },
  progressBar: {
    height: 4,
    backgroundColor: colors.backgroundLight,
    borderRadius: borderRadius.full,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    borderRadius: borderRadius.full,
  },
  
  // Connection Cards
  connectionCard: {
    backgroundColor: colors.glass,
    borderWidth: 1,
    borderColor: colors.glassBorder,
    borderRadius: borderRadius.lg,
    padding: spacing.md,
    marginBottom: spacing.md,
    ...shadows.medium,
  },
  connectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: spacing.sm,
  },
  connectionIcon: {
    fontSize: 24,
  },
  connectionTitle: {
    flex: 1,
    fontSize: typography.fontSize.lg,
    fontWeight: typography.fontWeight.semibold,
    color: colors.text,
    marginLeft: spacing.sm,
  },
  connectionDetails: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  connectionStatus: {
    fontSize: typography.fontSize.sm,
    fontWeight: typography.fontWeight.bold,
  },
  connectionMeta: {
    fontSize: typography.fontSize.xs,
    color: colors.textMuted,
  },
  
  // Thought Process Card
  thoughtCard: {
    backgroundColor: colors.glass,
    borderWidth: 1,
    borderColor: colors.glassBorderActive,
    borderRadius: borderRadius.xl,
    padding: spacing.lg,
    ...shadows.neon,
  },
  thoughtHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: spacing.md,
  },
  thoughtIcon: {
    fontSize: 28,
  },
  thoughtTitle: {
    flex: 1,
    fontSize: typography.fontSize.lg,
    fontWeight: typography.fontWeight.semibold,
    color: colors.text,
    marginLeft: spacing.sm,
  },
  thoughtStatus: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
  },
  thoughtStatusText: {
    fontSize: typography.fontSize.xs,
    color: colors.neonGreen,
    fontWeight: typography.fontWeight.bold,
  },
  thoughtContent: {
    gap: spacing.md,
  },
  thoughtTask: {
    fontSize: typography.fontSize.base,
    color: colors.text,
    fontStyle: 'italic',
  },
  thoughtMetrics: {
    flexDirection: 'row',
    gap: spacing.lg,
  },
  thoughtMetric: {
    flex: 1,
  },
  thoughtMetricLabel: {
    fontSize: typography.fontSize.xs,
    color: colors.textMuted,
    marginBottom: spacing.xs,
  },
  thoughtMetricValue: {
    fontSize: typography.fontSize.lg,
    fontWeight: typography.fontWeight.bold,
    color: colors.neonGreen,
  },
  thoughtLastAction: {
    backgroundColor: colors.backgroundLight,
    borderRadius: borderRadius.md,
    padding: spacing.sm,
  },
  thoughtLastActionLabel: {
    fontSize: typography.fontSize.xs,
    color: colors.textMuted,
    marginBottom: spacing.xs,
  },
  thoughtLastActionText: {
    fontSize: typography.fontSize.sm,
    color: colors.textDim,
  },
  
  // Stats Row
  statsRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    backgroundColor: colors.glass,
    borderWidth: 1,
    borderColor: colors.glassBorder,
    borderRadius: borderRadius.lg,
    padding: spacing.lg,
    ...shadows.medium,
  },
  statItem: {
    alignItems: 'center',
  },
  statValue: {
    fontSize: typography.fontSize['3xl'],
    fontWeight: typography.fontWeight.bold,
    color: colors.neonGreen,
  },
  statLabel: {
    fontSize: typography.fontSize.sm,
    color: colors.textDim,
    marginTop: spacing.xs,
  },
  statDivider: {
    width: 1,
    backgroundColor: colors.glassBorder,
  },
  
  // Action Buttons
  actionButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.glass,
    borderWidth: 1,
    borderColor: colors.glassBorder,
    borderRadius: borderRadius.lg,
    padding: spacing.md,
    marginBottom: spacing.md,
    ...shadows.small,
  },
  actionIcon: {
    fontSize: 24,
    marginRight: spacing.md,
  },
  actionText: {
    fontSize: typography.fontSize.lg,
    fontWeight: typography.fontWeight.semibold,
    color: colors.text,
  },
  
  // Status Indicators
  statusIndicator: {
    borderRadius: borderRadius.full,
  },
  statusOnline: {
    backgroundColor: colors.success,
    ...shadows.neon,
  },
  statusOffline: {
    backgroundColor: colors.error,
  },
  
  // Text Styles
  textSuccess: {
    color: colors.success,
  },
  textError: {
    color: colors.error,
  },
  
  // Spacer
  spacer: {
    height: spacing['2xl'],
  },
});

export default DashboardScreen;
