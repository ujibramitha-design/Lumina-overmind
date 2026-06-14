/**
 * JARVIS Mobile - Code Explorer Screen
 * ====================================
 * 
 * Interface to ask JARVIS about code files and features
 * Displays code explanations and file structure
 */

import React, { useState } from 'react';
import {
  View,
  Text,
  ScrollView,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
} from 'react-native';
import { LinearGradient } from 'react-native-linear-gradient';
import { theme, colors, spacing, borderRadius, shadows } from '../theme';

// Mock code search results
const mockSearchResults = [
  {
    id: '1',
    file: 'api/endpoints/jarvis.py',
    type: 'python',
    description: 'JARVIS API endpoints for voice commands and system control',
    relevance: 0.95,
  },
  {
    id: '2',
    file: 'dashboard/components/JarvisAssistant.tsx',
    type: 'typescript',
    description: 'React component for JARVIS chat interface with voice waveform',
    relevance: 0.88,
  },
  {
    id: '3',
    file: 'jarvis/channels/hub.js',
    type: 'javascript',
    description: 'Central communication hub for WhatsApp and Telegram integration',
    relevance: 0.82,
  },
];

const mockCodeExplanation = {
  file: 'api/endpoints/jarvis.py',
  summary: 'This file contains the main API endpoints for the JARVIS AI system. It handles voice commands, system status queries, and function calling capabilities.',
  keyFunctions: [
    {
      name: 'process_voice_command',
      description: 'Processes incoming voice commands and routes them to the appropriate handler',
    },
    {
      name: 'get_system_status',
      description: 'Returns current system health metrics including CPU, memory, and database status',
    },
    {
      name: 'execute_function',
      description: 'Executes AI function calls with proper validation and error handling',
    },
  ],
  dependencies: [
    'fastapi',
    'pydantic',
    'speech_recognition',
    'openai',
  ],
  linesOfCode: 754,
  lastModified: '2024-01-15',
};

const SearchResultCard = ({ result, onPress }) => (
  <TouchableOpacity
    style={styles.resultCard}
    onPress={() => onPress(result)}
  >
    <View style={styles.resultHeader}>
      <View style={styles.resultTypeBadge}>
        <Text style={styles.resultTypeText}>{result.type}</Text>
      </View>
      <Text style={styles.resultRelevance}>
        {Math.round(result.relevance * 100)}% match
      </Text>
    </View>
    <Text style={styles.resultFile}>{result.file}</Text>
    <Text style={styles.resultDescription}>{result.description}</Text>
  </TouchableOpacity>
);

const CodeBlock = ({ code, language }) => (
  <View style={styles.codeBlock}>
    <View style={styles.codeBlockHeader}>
      <Text style={styles.codeBlockLanguage}>{language}</Text>
      <TouchableOpacity style={styles.codeBlockCopy}>
        <Text style={styles.codeBlockCopyText}>Copy</Text>
      </TouchableOpacity>
    </View>
    <ScrollView horizontal showsHorizontalScrollIndicator={false}>
      <Text style={styles.codeContent}>{code}</Text>
    </ScrollView>
  </View>
);

const FunctionCard = ({ func }) => (
  <View style={styles.functionCard}>
    <Text style={styles.functionName}>{func.name}</Text>
    <Text style={styles.functionDescription}>{func.description}</Text>
  </View>
);

const CodeExplorerScreen = ({ navigation }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [explanation, setExplanation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [searching, setSearching] = useState(false);

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;

    setSearching(true);
    // Simulate API call
    setTimeout(() => {
      setSearchResults(mockSearchResults);
      setSearching(false);
    }, 1000);
  };

  const handleSelectFile = (result) => {
    setSelectedFile(result);
    setLoading(true);
    // Simulate API call to get code explanation
    setTimeout(() => {
      setExplanation(mockCodeExplanation);
      setLoading(false);
    }, 1500);
  };

  const handleBack = () => {
    setSelectedFile(null);
    setExplanation(null);
  };

  return (
    <View style={styles.container}>
      {/* Header */}
      <LinearGradient
        colors={[colors.backgroundDark, colors.background]}
        style={styles.header}
      >
        <View style={styles.headerContent}>
          <TouchableOpacity
            style={styles.backButton}
            onPress={selectedFile ? handleBack : () => navigation.goBack()}
          >
            <Text style={styles.backIcon}>{selectedFile ? '←' : '←'}</Text>
          </TouchableOpacity>
          <View style={styles.headerInfo}>
            <Text style={styles.headerTitle}>
              {selectedFile ? 'Code Details' : 'Code Explorer'}
            </Text>
            <Text style={styles.headerSubtitle}>
              {selectedFile ? selectedFile.file : 'Ask JARVIS about any code'}
            </Text>
          </View>
        </View>
      </LinearGradient>

      {/* Content */}
      <ScrollView style={styles.scrollContent} showsVerticalScrollIndicator={false}>
        {!selectedFile ? (
          // Search View
          <View style={styles.searchView}>
            <View style={styles.searchContainer}>
              <TextInput
                style={styles.searchInput}
                placeholder="Search for files, functions, or features..."
                placeholderTextColor={colors.textMuted}
                value={searchQuery}
                onChangeText={setSearchQuery}
                onSubmitEditing={handleSearch}
              />
              <TouchableOpacity
                style={styles.searchButton}
                onPress={handleSearch}
                disabled={searching}
              >
                {searching ? (
                  <ActivityIndicator size="small" color={colors.background} />
                ) : (
                  <Text style={styles.searchIcon}>🔍</Text>
                )}
              </TouchableOpacity>
            </View>

            {/* Quick Filters */}
            <View style={styles.filtersContainer}>
              <TouchableOpacity style={styles.filterButton}>
                <Text style={styles.filterText}>API Endpoints</Text>
              </TouchableOpacity>
              <TouchableOpacity style={styles.filterButton}>
                <Text style={styles.filterText}>Components</Text>
              </TouchableOpacity>
              <TouchableOpacity style={styles.filterButton}>
                <Text style={styles.filterText}>Utils</Text>
              </TouchableOpacity>
              <TouchableOpacity style={styles.filterButton}>
                <Text style={styles.filterText}>Config</Text>
              </TouchableOpacity>
            </View>

            {/* Search Results */}
            {searchResults.length > 0 ? (
              <View style={styles.resultsContainer}>
                <Text style={styles.resultsTitle}>Search Results</Text>
                {searchResults.map(result => (
                  <SearchResultCard
                    key={result.id}
                    result={result}
                    onPress={handleSelectFile}
                  />
                ))}
              </View>
            ) : (
              <View style={styles.emptyState}>
                <Text style={styles.emptyIcon}>🔍</Text>
                <Text style={styles.emptyTitle}>Search the Codebase</Text>
                <Text style={styles.emptyDescription}>
                  Ask JARVIS about any file, function, or feature in the Lumina Overmind system
                </Text>
              </View>
            )}
          </View>
        ) : (
          // File Details View
          <View style={styles.detailsView}>
            {loading ? (
              <View style={styles.loadingContainer}>
                <ActivityIndicator size="large" color={colors.neonGreen} />
                <Text style={styles.loadingText}>Analyzing code...</Text>
              </View>
            ) : explanation ? (
              <>
                {/* File Info */}
                <View style={styles.fileInfoCard}>
                  <View style={styles.fileInfoHeader}>
                    <Text style={styles.fileInfoIcon}>📄</Text>
                    <View style={styles.fileInfoDetails}>
                      <Text style={styles.fileName}>{explanation.file}</Text>
                      <Text style={styles.fileMeta}>
                        {explanation.linesOfCode} lines • Modified {explanation.lastModified}
                      </Text>
                    </View>
                  </View>
                </View>

                {/* Summary */}
                <View style={styles.section}>
                  <Text style={styles.sectionTitle}>Summary</Text>
                  <View style={styles.summaryCard}>
                    <Text style={styles.summaryText}>{explanation.summary}</Text>
                  </View>
                </View>

                {/* Key Functions */}
                <View style={styles.section}>
                  <Text style={styles.sectionTitle}>Key Functions</Text>
                  {explanation.keyFunctions.map((func, index) => (
                    <FunctionCard key={index} func={func} />
                  ))}
                </View>

                {/* Dependencies */}
                <View style={styles.section}>
                  <Text style={styles.sectionTitle}>Dependencies</Text>
                  <View style={styles.dependenciesCard}>
                    {explanation.dependencies.map((dep, index) => (
                      <View key={index} style={styles.dependencyItem}>
                        <Text style={styles.dependencyText}>{dep}</Text>
                      </View>
                    ))}
                  </View>
                </View>

                {/* Ask JARVIS Button */}
                <TouchableOpacity style={styles.askButton}>
                  <Text style={styles.askButtonText}>Ask JARVIS about this file</Text>
                </TouchableOpacity>
              </>
            ) : null}
          </View>
        )}
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
    alignItems: 'center',
  },
  backButton: {
    width: 40,
    height: 40,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: spacing.sm,
  },
  backIcon: {
    fontSize: 24,
    color: colors.text,
  },
  headerInfo: {
    flex: 1,
  },
  headerTitle: {
    fontSize: typography.fontSize.xl,
    fontWeight: typography.fontWeight.bold,
    color: colors.text,
  },
  headerSubtitle: {
    fontSize: typography.fontSize.sm,
    color: colors.textDim,
    marginTop: spacing.xs,
  },
  
  // Content
  scrollContent: {
    flex: 1,
  },
  
  // Search View
  searchView: {
    padding: spacing.lg,
  },
  searchContainer: {
    flexDirection: 'row',
    gap: spacing.sm,
    marginBottom: spacing.lg,
  },
  searchInput: {
    flex: 1,
    backgroundColor: colors.backgroundLight,
    borderWidth: 1,
    borderColor: colors.glassBorder,
    borderRadius: borderRadius.lg,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    color: colors.text,
  },
  searchButton: {
    width: 48,
    height: 48,
    borderRadius: borderRadius.lg,
    backgroundColor: colors.neonGreen,
    justifyContent: 'center',
    alignItems: 'center',
    ...shadows.neon,
  },
  searchIcon: {
    fontSize: 20,
  },
  
  // Filters
  filtersContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: spacing.sm,
    marginBottom: spacing.lg,
  },
  filterButton: {
    backgroundColor: colors.glass,
    borderWidth: 1,
    borderColor: colors.glassBorder,
    borderRadius: borderRadius.full,
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.sm,
  },
  filterText: {
    fontSize: typography.fontSize.sm,
    color: colors.textDim,
  },
  
  // Search Results
  resultsContainer: {
    gap: spacing.md,
  },
  resultsTitle: {
    fontSize: typography.fontSize.lg,
    fontWeight: typography.fontWeight.semibold,
    color: colors.text,
    marginBottom: spacing.md,
  },
  resultCard: {
    backgroundColor: colors.glass,
    borderWidth: 1,
    borderColor: colors.glassBorder,
    borderRadius: borderRadius.lg,
    padding: spacing.md,
    ...shadows.medium,
  },
  resultHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: spacing.sm,
  },
  resultTypeBadge: {
    backgroundColor: colors.neonGreenDim,
    paddingHorizontal: spacing.sm,
    paddingVertical: spacing.xs,
    borderRadius: borderRadius.sm,
  },
  resultTypeText: {
    fontSize: typography.fontSize.xs,
    color: colors.neonGreenBright,
    fontWeight: typography.fontWeight.bold,
  },
  resultRelevance: {
    fontSize: typography.fontSize.xs,
    color: colors.textMuted,
  },
  resultFile: {
    fontSize: typography.fontSize.base,
    fontWeight: typography.fontWeight.semibold,
    color: colors.text,
    marginBottom: spacing.xs,
  },
  resultDescription: {
    fontSize: typography.fontSize.sm,
    color: colors.textDim,
  },
  
  // Empty State
  emptyState: {
    alignItems: 'center',
    paddingVertical: spacing['3xl'],
  },
  emptyIcon: {
    fontSize: 64,
    marginBottom: spacing.lg,
  },
  emptyTitle: {
    fontSize: typography.fontSize.xl,
    fontWeight: typography.fontWeight.semibold,
    color: colors.text,
    marginBottom: spacing.sm,
  },
  emptyDescription: {
    fontSize: typography.fontSize.base,
    color: colors.textDim,
    textAlign: 'center',
  },
  
  // Details View
  detailsView: {
    padding: spacing.lg,
  },
  loadingContainer: {
    alignItems: 'center',
    paddingVertical: spacing['3xl'],
  },
  loadingText: {
    fontSize: typography.fontSize.base,
    color: colors.textDim,
    marginTop: spacing.md,
  },
  
  // File Info
  fileInfoCard: {
    backgroundColor: colors.glass,
    borderWidth: 1,
    borderColor: colors.glassBorderActive,
    borderRadius: borderRadius.lg,
    padding: spacing.lg,
    marginBottom: spacing.lg,
    ...shadows.neon,
  },
  fileInfoHeader: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  fileInfoIcon: {
    fontSize: 32,
    marginRight: spacing.md,
  },
  fileInfoDetails: {
    flex: 1,
  },
  fileName: {
    fontSize: typography.fontSize.lg,
    fontWeight: typography.fontWeight.bold,
    color: colors.text,
    marginBottom: spacing.xs,
  },
  fileMeta: {
    fontSize: typography.fontSize.sm,
    color: colors.textMuted,
  },
  
  // Section
  section: {
    marginBottom: spacing.lg,
  },
  sectionTitle: {
    fontSize: typography.fontSize.lg,
    fontWeight: typography.fontWeight.semibold,
    color: colors.text,
    marginBottom: spacing.md,
    textTransform: 'uppercase',
    letterSpacing: 1,
  },
  
  // Summary
  summaryCard: {
    backgroundColor: colors.glass,
    borderWidth: 1,
    borderColor: colors.glassBorder,
    borderRadius: borderRadius.lg,
    padding: spacing.md,
  },
  summaryText: {
    fontSize: typography.fontSize.base,
    color: colors.textDim,
    lineHeight: typography.lineHeight.relaxed,
  },
  
  // Function Cards
  functionCard: {
    backgroundColor: colors.glass,
    borderWidth: 1,
    borderColor: colors.glassBorder,
    borderRadius: borderRadius.lg,
    padding: spacing.md,
    marginBottom: spacing.sm,
  },
  functionName: {
    fontSize: typography.fontSize.base,
    fontWeight: typography.fontWeight.bold,
    color: colors.neonGreen,
    marginBottom: spacing.xs,
    fontFamily: typography.fontFamily.mono,
  },
  functionDescription: {
    fontSize: typography.fontSize.sm,
    color: colors.textDim,
  },
  
  // Dependencies
  dependenciesCard: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: spacing.sm,
  },
  dependencyItem: {
    backgroundColor: colors.backgroundLight,
    borderWidth: 1,
    borderColor: colors.glassBorder,
    borderRadius: borderRadius.full,
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.sm,
  },
  dependencyText: {
    fontSize: typography.fontSize.sm,
    color: colors.textDim,
    fontFamily: typography.fontFamily.mono,
  },
  
  // Ask Button
  askButton: {
    backgroundColor: colors.neonGreen,
    borderRadius: borderRadius.lg,
    padding: spacing.lg,
    alignItems: 'center',
    marginTop: spacing.lg,
    ...shadows.neon,
  },
  askButtonText: {
    fontSize: typography.fontSize.lg,
    fontWeight: typography.fontWeight.bold,
    color: colors.background,
  },
  
  // Code Block (for future use)
  codeBlock: {
    backgroundColor: colors.backgroundLight,
    borderRadius: borderRadius.lg,
    overflow: 'hidden',
    marginBottom: spacing.md,
  },
  codeBlockHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: spacing.sm,
    backgroundColor: colors.backgroundDark,
    borderBottomWidth: 1,
    borderBottomColor: colors.glassBorder,
  },
  codeBlockLanguage: {
    fontSize: typography.fontSize.xs,
    color: colors.textMuted,
    fontFamily: typography.fontFamily.mono,
  },
  codeBlockCopy: {
    paddingHorizontal: spacing.sm,
  },
  codeBlockCopyText: {
    fontSize: typography.fontSize.xs,
    color: colors.neonGreen,
  },
  codeContent: {
    padding: spacing.md,
    color: colors.textDim,
    fontFamily: typography.fontFamily.mono,
    fontSize: typography.fontSize.sm,
  },
});

export default CodeExplorerScreen;
