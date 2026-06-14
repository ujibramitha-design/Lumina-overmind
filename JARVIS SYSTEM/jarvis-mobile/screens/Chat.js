/**
 * JARVIS Mobile - Chat Screen
 * ==============================
 * 
 * Real-time chat interface with JARVIS via WebSocket
 * Bi-directional communication with typing indicators
 */

import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  ScrollView,
  TextInput,
  TouchableOpacity,
  KeyboardAvoidingView,
  Platform,
  StyleSheet,
  ActivityIndicator,
} from 'react-native';
import { LinearGradient } from 'react-native-linear-gradient';
import { theme, colors, spacing, borderRadius, shadows } from '../theme';

// Mock messages (will be replaced with real WebSocket messages)
const mockMessages = [
  {
    id: '1',
    type: 'jarvis',
    content: 'Hello, Commander. JARVIS is online and ready to assist you.',
    timestamp: new Date(Date.now() - 300000),
  },
  {
    id: '2',
    type: 'user',
    content: 'What is the current system status?',
    timestamp: new Date(Date.now() - 240000),
  },
  {
    id: '3',
    type: 'jarvis',
    content: 'All systems are operating within normal parameters. CPU usage at 45%, memory at 62%, and all communication channels are active. Would you like a detailed report?',
    timestamp: new Date(Date.now() - 180000),
  },
];

const MessageBubble = ({ message, isUser }) => (
  <View
    style={[
      styles.messageBubble,
      isUser ? styles.userBubble : styles.jarvisBubble,
    ]}
  >
    <View style={styles.messageHeader}>
      <Text style={[styles.messageSender, isUser ? styles.userSender : styles.jarvisSender]}>
        {isUser ? 'You' : 'JARVIS'}
      </Text>
      <Text style={styles.messageTime}>
        {new Date(message.timestamp).toLocaleTimeString([], {
          hour: '2-digit',
          minute: '2-digit',
        })}
      </Text>
    </View>
    <Text style={[styles.messageContent, isUser ? styles.userContent : styles.jarvisContent]}>
      {message.content}
    </Text>
  </View>
);

const TypingIndicator = () => (
  <View style={styles.typingIndicator}>
    <View style={styles.typingDot} />
    <View style={styles.typingDot} />
    <View style={styles.typingDot} />
  </View>
);

const ChatScreen = ({ navigation }) => {
  const [messages, setMessages] = useState(mockMessages);
  const [inputText, setInputText] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [isConnected, setIsConnected] = useState(true);
  const [sending, setSending] = useState(false);
  
  const scrollViewRef = useRef(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (scrollViewRef.current) {
      scrollViewRef.current.scrollToEnd({ animated: true });
    }
  }, [messages]);

  // Simulate WebSocket connection
  useEffect(() => {
    // In production, this would be a real WebSocket connection
    const ws = {
      onmessage: null,
      send: (data) => {
        console.log('WebSocket send:', data);
      },
    };

    // Simulate connection
    setIsConnected(true);

    return () => {
      // Cleanup WebSocket
    };
  }, []);

  const sendMessage = async () => {
    if (!inputText.trim() || sending) return;

    const userMessage = {
      id: Date.now().toString(),
      type: 'user',
      content: inputText.trim(),
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setSending(true);
    setIsTyping(true);

    // Simulate JARVIS response (replace with real WebSocket)
    setTimeout(() => {
      const jarvisResponse = {
        id: (Date.now() + 1).toString(),
        type: 'jarvis',
        content: `I understand your request: "${userMessage.content}". Processing this command now...`,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, jarvisResponse]);
      setIsTyping(false);
      setSending(false);
    }, 1500);
  };

  const quickCommand = (command) => {
    setInputText(command);
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
            onPress={() => navigation.goBack()}
          >
            <Text style={styles.backIcon}>←</Text>
          </TouchableOpacity>
          <View style={styles.headerInfo}>
            <Text style={styles.headerTitle}>JARVIS Chat</Text>
            <View style={styles.connectionStatus}>
              <View
                style={[
                  styles.statusDot,
                  isConnected ? styles.statusOnline : styles.statusOffline,
                ]}
              />
              <Text style={styles.statusText}>
                {isConnected ? 'Connected' : 'Disconnected'}
              </Text>
            </View>
          </View>
        </View>
      </LinearGradient>

      {/* Messages */}
      <ScrollView
        ref={scrollViewRef}
        style={styles.messagesContainer}
        contentContainerStyle={styles.messagesContent}
        showsVerticalScrollIndicator={false}
      >
        {messages.map(message => (
          <MessageBubble
            key={message.id}
            message={message}
            isUser={message.type === 'user'}
          />
        ))}
        {isTyping && (
          <View style={styles.typingContainer}>
            <MessageBubble
              message={{
                id: 'typing',
                type: 'jarvis',
                content: <TypingIndicator />,
                timestamp: new Date(),
              }}
              isUser={false}
            />
          </View>
        )}
      </ScrollView>

      {/* Quick Commands */}
      <ScrollView
        horizontal
        style={styles.quickCommandsContainer}
        showsHorizontalScrollIndicator={false}
        contentContainerStyle={styles.quickCommandsContent}
      >
        {[
          'System status',
          'Generate report',
          'Check connections',
          'Analyze performance',
        ].map((command, index) => (
          <TouchableOpacity
            key={index}
            style={styles.quickCommand}
            onPress={() => quickCommand(command)}
          >
            <Text style={styles.quickCommandText}>{command}</Text>
          </TouchableOpacity>
        ))}
      </ScrollView>

      {/* Input Area */}
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        keyboardVerticalOffset={Platform.OS === 'ios' ? 90 : 0}
      >
        <View style={styles.inputContainer}>
          <TextInput
            style={styles.input}
            placeholder="Ask JARVIS anything..."
            placeholderTextColor={colors.textMuted}
            value={inputText}
            onChangeText={setInputText}
            multiline
            maxLength={500}
          />
          <TouchableOpacity
            style={[
              styles.sendButton,
              (!inputText.trim() || sending) && styles.sendButtonDisabled,
            ]}
            onPress={sendMessage}
            disabled={!inputText.trim() || sending}
          >
            {sending ? (
              <ActivityIndicator size="small" color={colors.background} />
            ) : (
              <Text style={styles.sendButtonText}>→</Text>
            )}
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>
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
  connectionStatus: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: spacing.xs,
  },
  statusDot: {
    width: 8,
    height: 8,
    borderRadius: borderRadius.full,
    marginRight: spacing.sm,
  },
  statusOnline: {
    backgroundColor: colors.success,
    ...shadows.neon,
  },
  statusOffline: {
    backgroundColor: colors.error,
  },
  statusText: {
    fontSize: typography.fontSize.sm,
    color: colors.textDim,
  },
  
  // Messages
  messagesContainer: {
    flex: 1,
  },
  messagesContent: {
    padding: spacing.lg,
    paddingBottom: spacing.xl,
  },
  messageBubble: {
    maxWidth: '80%',
    padding: spacing.md,
    borderRadius: borderRadius.lg,
    marginBottom: spacing.md,
    ...shadows.medium,
  },
  userBubble: {
    alignSelf: 'flex-end',
    backgroundColor: colors.neonGreenDim,
    borderWidth: 1,
    borderColor: colors.neonGreen,
  },
  jarvisBubble: {
    alignSelf: 'flex-start',
    backgroundColor: colors.glass,
    borderWidth: 1,
    borderColor: colors.glassBorder,
  },
  messageHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: spacing.xs,
  },
  messageSender: {
    fontSize: typography.fontSize.xs,
    fontWeight: typography.fontWeight.semibold,
  },
  userSender: {
    color: colors.neonGreenBright,
  },
  jarvisSender: {
    color: colors.accentSecondary,
  },
  messageTime: {
    fontSize: typography.fontSize.xs,
    color: colors.textMuted,
  },
  messageContent: {
    fontSize: typography.fontSize.base,
    lineHeight: typography.lineHeight.normal,
  },
  userContent: {
    color: colors.text,
  },
  jarvisContent: {
    color: colors.textDim,
  },
  
  // Typing Indicator
  typingContainer: {
    marginBottom: spacing.md,
  },
  typingIndicator: {
    flexDirection: 'row',
    gap: spacing.xs,
    padding: spacing.sm,
  },
  typingDot: {
    width: 8,
    height: 8,
    borderRadius: borderRadius.full,
    backgroundColor: colors.neonGreen,
    opacity: 0.5,
  },
  
  // Quick Commands
  quickCommandsContainer: {
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.sm,
    backgroundColor: colors.backgroundDark,
    borderBottomWidth: 1,
    borderBottomColor: colors.glassBorder,
  },
  quickCommandsContent: {
    gap: spacing.sm,
  },
  quickCommand: {
    backgroundColor: colors.glass,
    borderWidth: 1,
    borderColor: colors.glassBorder,
    borderRadius: borderRadius.full,
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.sm,
  },
  quickCommandText: {
    fontSize: typography.fontSize.sm,
    color: colors.textDim,
  },
  
  // Input
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    padding: spacing.lg,
    backgroundColor: colors.backgroundDark,
    borderTopWidth: 1,
    borderTopColor: colors.glassBorder,
  },
  input: {
    flex: 1,
    backgroundColor: colors.backgroundLight,
    borderWidth: 1,
    borderColor: colors.glassBorder,
    borderRadius: borderRadius.lg,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    color: colors.text,
    maxHeight: 100,
    marginRight: spacing.sm,
  },
  sendButton: {
    width: 48,
    height: 48,
    borderRadius: borderRadius.full,
    backgroundColor: colors.neonGreen,
    justifyContent: 'center',
    alignItems: 'center',
    ...shadows.neon,
  },
  sendButtonDisabled: {
    backgroundColor: colors.backgroundLight,
    borderWidth: 1,
    borderColor: colors.glassBorder,
    ...shadows.small,
  },
  sendButtonText: {
    fontSize: 24,
    color: colors.background,
    fontWeight: typography.fontWeight.bold,
  },
});

export default ChatScreen;
