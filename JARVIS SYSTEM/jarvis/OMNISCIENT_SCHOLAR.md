# JARVIS Omniscient Scholar & Hyper-Polyglot Documentation

Complete guide for JARVIS's advanced document ingestion and multilingual communication capabilities.

## Overview

JARVIS has evolved into an "Omniscient Scholar" and "Hyper-Polyglot" with:
- **Deep Knowledge Ingestion**: Massive document/URL processing with semantic chunking
- **Vector Database**: ChromaDB integration for semantic search
- **Hyper-Polyglot**: Native communication in 20+ languages with cultural nuances
- **Asynchronous Processing**: Non-blocking document processing for large files

## Deep Knowledge Ingestion (The "Swallow" Protocol)

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│         Document Ingestion Engine                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. Document Input                                      │
│     ├── PDF files                                       │
│     ├── EPUB files                                      │
│     ├── TXT files                                       │
│     └── Web URLs (scraping)                             │
│                                                          │
│  2. Text Extraction                                     │
│     ├── PDF: pdf-parse                                  │
│     ├── EPUB: epub2                                     │
│     ├── TXT: Direct read                                │
│     └── Web: cheerio scraping                           │
│                                                          │
│  3. Semantic Chunking                                   │
│     ├── Gemini AI analysis                              │
│     ├── Meaningful sections                             │
│     ├── Configurable size (1000 chars)                  │
│     └── Overlap (200 chars)                             │
│                                                          │
│  4. Embedding Generation                                │
│     ├── Google text-embedding-004                       │
│     ├── Batch processing (100 chunks)                    │
│     └── Vector representation                           │
│                                                          │
│  5. Vector Database Storage                             │
│     ├── ChromaDB                                        │
│     ├── Namespace isolation                            │
│     ├── Metadata tagging                                │
│     └── Persistent storage                              │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Document Loaders

**Supported Formats:**

1. **PDF Files**
   - Uses `pdf-parse` library
   - Extracts text from PDF documents
   - Handles multi-page documents
   - Preserves text structure

2. **EPUB Files**
   - Uses `epub2` library
   - Extracts text from EPUB chapters
   - Handles complex EPUB structures
   - Preserves chapter organization

3. **TXT Files**
   - Direct UTF-8 text reading
   - Simple and fast
   - Handles large files
   - Preserves formatting

4. **Web URLs**
   - Uses `axios` for fetching
   - Uses `cheerio` for HTML parsing
   - Removes scripts and styles
   - Extracts body text
   - Handles redirects and timeouts

### Semantic Chunking

**Process:**

1. **Gemini AI Analysis**
   - Analyzes document structure
   - Identifies semantic boundaries
   - Creates meaningful sections
   - Maintains context coherence

2. **Chunk Configuration**
   - Chunk size: 1000 characters (configurable)
   - Overlap: 200 characters (configurable)
   - Batch size: 100 chunks (configurable)

3. **Fallback Mechanism**
   - If Gemini fails, uses simple chunking
   - Simple chunking splits by character count
   - Ensures processing always completes

**Example:**

```
Original Text (5000 characters):
"Chapter 1: Introduction to AI. Artificial Intelligence is a field of computer science..."

Semantic Chunks:
- Chunk 1: "Chapter 1: Introduction to AI. Artificial Intelligence is a field of computer science..." (1000 chars)
- Chunk 2: "...that focuses on creating intelligent machines. These systems can learn..." (1000 chars, 200 overlap)
- Chunk 3: "...from data and make decisions. Machine learning is a subset of AI..." (1000 chars, 200 overlap)
```

### Vector Database (ChromaDB)

**Features:**

- **Namespace Isolation**: Separate collections per document/user
- **Metadata Tagging**: Store document ID, chunk index, timestamps
- **Persistent Storage**: Data persists across sessions
- **Semantic Search**: Vector similarity search
- **Batch Operations**: Efficient bulk operations

**Storage Structure:**

```javascript
{
  id: "doc_1234567890_chunk_0",
  embedding: [0.1, 0.2, 0.3, ...],  // 768-dimensional vector
  metadata: {
    userId: "user123",
    documentId: "doc_1234567890",
    chunkIndex: 0,
    chunkText: "Preview of chunk...",
    timestamp: "2024-01-15T10:30:00Z",
  },
  document: "Full chunk text...",
}
```

### Asynchronous Processing

**Non-Blocking Architecture:**

```javascript
// Uses setImmediate to avoid blocking event loop
async _processDocumentAsync(text, namespace, metadata) {
  return new Promise((resolve, reject) => {
    setImmediate(async () => {
      try {
        const result = await this._processDocument(text, namespace, metadata);
        resolve(result);
      } catch (error) {
        reject(error);
      }
    });
  });
}
```

**Benefits:**

- Main server remains responsive
- Large documents don't freeze the system
- Progress updates during processing
- Error handling without blocking

### Usage Examples

**Ingest PDF File:**

```javascript
const { getDocumentIngestionEngine } = require('../omniscient/documentIngestion');

const engine = getDocumentIngestionEngine();

// Ingest PDF from file buffer
const result = await engine.ingestDocument(
  fileBuffer,  // Buffer from WhatsApp/Telegram
  'pdf',       // File type
  'my_documents',  // Namespace
  {
    userId: 'user123',
    source: 'whatsapp',
  }
);

console.log(`Ingested ${result.chunksProcessed} chunks`);
```

**Ingest URL:**

```javascript
// Ingest web page
const result = await engine.ingestURL(
  'https://example.com/article',
  'my_documents',
  {
    userId: 'user123',
    source: 'telegram',
  }
);

console.log(`Ingested ${result.chunksProcessed} chunks`);
```

**Query Vector Database:**

```javascript
// Query ingested documents
const result = await engine.queryVectorDB(
  'What is the main topic of the document?',
  'my_documents',
  5  // Return top 5 results
);

console.log(`Found ${result.documents.length} relevant chunks`);
console.log(result.documents[0]);  // Most relevant chunk
```

## Hyper-Polyglot Capabilities

### Supported Languages

**22 Languages with Cultural Nuances:**

| Language | Code | Cultural Guidelines |
|----------|------|---------------------|
| English | en | Professional but approachable |
| Japanese | ja | Keigo honorifics, indirect communication |
| Korean | ko | Honorifics, formal hierarchy |
| Chinese | zh | Appropriate titles, formal address |
| Spanish | es | Warm and expressive, personal connections |
| French | fr | Formal politeness, intellectual expression |
| German | de | Direct but polite, precise language |
| Russian | ru | Formal patronymics, expressive but structured |
| Arabic | ar | Formal greetings, honorifics |
| Portuguese | pt | Warm and personal, expressive |
| Italian | it | Expressive and passionate |
| Dutch | nl | Direct but polite, practical |
| Polish | pl | Formal titles, indirect communication |
| Turkish | tr | Honorifics, formal hierarchy |
| Vietnamese | vi | Honorifics, respect for age |
| Thai | th | Honorifics, polite particles |
| Indonesian | id | Formal address, polite particles |
| Hindi | hi | Respectful language, honorifics |
| Bengali | bn | Formal address, polite language |
| Swedish | sv | Egalitarian but polite, direct |
| Norwegian | no | Egalitarian, direct but polite |
| Danish | da | Egalitarian, direct |
| Finnish | fi | Egalitarian, direct but reserved |

### Language Detection

**Detection Process:**

1. **Quick Pattern Matching**
   - Checks for unique character sets (Japanese, Korean, Chinese, Arabic, Thai, etc.)
   - Instant detection for languages with unique scripts
   - High confidence (95%)

2. **Gemini AI Detection**
   - For Latin-script languages
   - Analyzes vocabulary and grammar
   - Medium confidence (75%)

3. **Fallback**
   - Defaults to English if detection fails
   - Ensures system always responds

**Implementation:**

```javascript
const { getLanguageDetector } = require('../omniscient/languageDetector');

const detector = getLanguageDetector();

// Detect language
const language = await detector.detectLanguage('こんにちは');
console.log(language);  // 'ja'

// Detect with confidence
const result = await detector.detectLanguageWithConfidence('こんにちは');
console.log(result);  // { language: 'ja', confidence: 0.95 }
```

### Cultural Nuance Guidelines

**Japanese Communication:**

```
- Use keigo (honorifics): です/ます for polite, ございます for formal
- Add sentence-ending particles: ですね, ですね, でしょうか
- Indirect refusals: instead of "no", use "it's difficult" (難しいです)
- Business format: start with お世話になっております, end with よろしくお願いいたします
- Avoid direct confrontation, maintain harmony (和)
```

**Korean Communication:**

```
- Use honorifics: 요/입니다 for polite, 습니다 for formal
- Add polite particles: ~요, ~까요, ~네요
- Respect hierarchy: use appropriate titles (선생님, 사장님)
- Indirect requests: instead of "do this", use "could you please..." (부탁드립니다)
- Business format: formal greetings, respect for age/status
```

**Spanish Communication:**

```
- Use formal usted for professional, tú for casual
- Warm and expressive: use exclamation marks, emojis appropriately
- Personal connections: ask about well-being before business
- Business format: formal greeting (Estimado), polite closing (Saludos cordiales)
- Direct but warm communication style
```

### System Instructions

**Hyper-Polyglot System Prompt:**

```
You are a Master Polyglot fluent in 20+ languages.
- You auto-detect the language of incoming messages
- You respond natively in the detected language
- You adopt cultural communication norms for each language
- You use appropriate honorifics, formality, and cultural nuances
- You avoid robotic word-for-word translations

**Detected Language:** {detectedLanguage}
**Cultural Guidelines:** {culturalGuidelines}

**Language-Specific Guidelines:**
{languageGuidelines}
```

### Usage Examples

**Japanese Query:**

```
User: "システムの状態を教えてください"

Process:
1. Detect language: Japanese (ja)
2. Apply cultural guidelines: Keigo honorifics, polite form
3. Generate response in Japanese

Response: "システムの状態をお知らせします。現在、すべてのシステムが正常に動作しています。CPU使用率は45%、メモリ使用率は62%です。✅"
```

**Korean Query:**

```
User: "시스템 상태를 알려주세요"

Process:
1. Detect language: Korean (ko)
2. Apply cultural guidelines: Honorifics, formal hierarchy
3. Generate response in Korean

Response: "시스템 상태를 알려드리겠습니다. 현재 모든 시스템이 정상적으로 작동하고 있습니다. CPU 사용률은 45%, 메모리 사용률은 62%입니다. ✅"
```

**Spanish Query:**

```
User: "¿Cuál es el estado del sistema?"

Process:
1. Detect language: Spanish (es)
2. Apply cultural guidelines: Warm and expressive, personal connection
3. Generate response in Spanish

Response: "¡Hola! El estado del sistema es excelente. Todos los sistemas están operativos. El uso de CPU es del 45% y el uso de memoria es del 62%. ✅"
```

## Integration with geminiService.js

### Language Detection Integration

```javascript
// In generateResponse()
let detectedLanguage = 'en';
if (this.polyglotEnabled && this.languageDetector) {
  const detection = await this.languageDetector.detectLanguage(message);
  detectedLanguage = detection.language;
  console.log(`🌍 Detected language: ${detectedLanguage}`);
}

// Reinitialize model with language
if (this.currentLanguage !== detectedLanguage) {
  this.conversationalModel = this.genAI.getGenerativeModel({
    model: this.models.conversational,
    systemInstruction: this._getConversationalSystemPrompt(persona, detectedLanguage),
  });
  this.currentLanguage = detectedLanguage;
}
```

### Document Ingestion Integration

```javascript
// Handle document ingestion commands
if (this.omniscientEnabled && this.documentIngestionEngine) {
  const ingestionResult = await this._handleDocumentIngestion(message, context);
  if (ingestionResult.isIngestionCommand) {
    return ingestionResult;
  }
}

// Handle document queries
if (this.omniscientEnabled && this.documentIngestionEngine) {
  const queryResult = await this._handleDocumentQuery(message, context);
  if (queryResult.isDocumentQuery) {
    return queryResult;
  }
}
```

## Configuration

### Environment Variables

```bash
# Omniscient Scholar
JARVIS_OMNISCIENT_ENABLED=true
JARVIS_POLYGLOT_ENABLED=true

# Document Ingestion
CHROMA_PATH=./jarvis/data/chroma
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
BATCH_SIZE=100
EMBEDDING_MODEL=text-embedding-004

# Language Detection
GEMINI_API_KEY=your_gemini_api_key
```

### Document Ingestion Configuration

```javascript
const config = {
  chromaPath: './jarvis/data/chroma',
  chunkSize: 1000,
  chunkOverlap: 200,
  batchSize: 100,
  embeddingModel: 'text-embedding-004',
};
```

## Best Practices

### For Document Ingestion

1. **Namespace Organization**: Use descriptive namespaces (e.g., "research_papers", "documentation")
2. **Chunk Size**: Adjust based on document type (larger for technical docs, smaller for narratives)
3. **Batch Processing**: Use appropriate batch size for your hardware
4. **Metadata**: Include relevant metadata for better search
5. **Async Processing**: Always use async for large documents

### For Hyper-Polyglot

1. **Language Detection**: Test detection accuracy for your target languages
2. **Cultural Nuances**: Customize guidelines for your specific use case
3. **Formality Levels**: Adjust formality based on user relationship
4. **Testing**: Test responses in each language before production
5. **Fallback**: Always have English as fallback

### For Integration

1. **Feature Flags**: Use feature flags to enable/disable features
2. **Error Handling**: Graceful fallback if features fail
3. **Logging**: Log language detection and document processing
4. **Monitoring**: Track processing times and success rates
5. **Testing**: Test each feature independently

## Troubleshooting

### Document Ingestion Issues

**PDF Extraction Fails:**
```javascript
// Check if PDF is valid
try {
  const data = await pdf(buffer);
  console.log('PDF pages:', data.numpages);
} catch (error) {
  console.error('Invalid PDF:', error.message);
}
```

**ChromaDB Connection Error:**
```javascript
// Check ChromaDB path
const path = './jarvis/data/chroma';
console.log('Path exists:', fs.existsSync(path));

// Reinitialize ChromaDB
await engine._initializeChromaDB();
```

**Embedding Generation Slow:**
```javascript
// Reduce batch size
engine.config.batchSize = 50;

// Use smaller chunk size
engine.config.chunkSize = 500;
```

### Language Detection Issues

**Wrong Language Detected:**
```javascript
// Check quick detection
const quick = detector._quickDetect(text);
console.log('Quick detection:', quick);

// Use Gemini for accurate detection
const accurate = await detector.detectLanguage(text);
console.log('Accurate detection:', accurate);
```

**Detection Fails:**
```javascript
// Check Gemini API key
console.log('API key exists:', !!process.env.GEMINI_API_KEY);

// Test detection
const test = await detector.detectLanguage('test');
console.log('Test detection:', test);
```

### Cultural Nuance Issues

**Response Too Formal:**
```javascript
// Adjust persona to casual
const result = await geminiService.generateResponse(userId, message, {
  persona: 'casual',
  language: detectedLanguage,
});
```

**Response Not Culturally Appropriate:**
```javascript
// Customize cultural guidelines
const customGuidelines = detector._getCulturalGuidelines('ja');
console.log('Current guidelines:', customGuidelines);

// Modify guidelines in system prompt
```

## Performance Considerations

### Document Ingestion

- **PDF Processing**: ~1-2 seconds per page
- **EPUB Processing**: ~0.5-1 second per chapter
- **Web Scraping**: ~2-5 seconds per page
- **Chunking**: ~1-3 seconds per 1000 chunks
- **Embedding**: ~0.5-1 second per chunk
- **ChromaDB Storage**: ~0.1 second per chunk

**Total for 500-page book:**
- PDF extraction: ~5-10 minutes
- Chunking: ~1-2 minutes
- Embedding: ~5-10 minutes
- Storage: ~1-2 minutes
- **Total: ~12-24 minutes** (async, non-blocking)

### Language Detection

- **Quick Detection**: <1ms for unique scripts
- **Gemini Detection**: ~500ms-1s for Latin scripts
- **Overall**: <1s for most languages

### Vector Database Query

- **Query Time**: ~100-500ms
- **Result Retrieval**: ~50-100ms
- **Overall**: <1s for typical queries

## Monitoring

### Document Ingestion Metrics

```javascript
// Get namespace statistics
const stats = await engine.getNamespaceStats('my_documents');
console.log('Document count:', stats.documentCount);

// List all namespaces
const namespaces = await engine.listNamespaces();
console.log('Namespaces:', namespaces.namespaces);
```

### Language Detection Metrics

```javascript
// Detect with confidence
const result = await detector.detectLanguageWithConfidence(text);
console.log('Language:', result.language);
console.log('Confidence:', result.confidence);
```

## Security Considerations

### Document Ingestion

- **File Validation**: Validate file types before processing
- **Size Limits**: Implement size limits to prevent abuse
- **Sanitization**: Sanitize web-scraped content
- **Access Control**: Restrict namespace access
- **Data Privacy**: Encrypt stored documents if sensitive

### Language Detection

- **Privacy**: Language detection doesn't store data
- **API Security**: Secure Gemini API key
- **Rate Limiting**: Limit detection requests
- **Logging**: Log detection events for audit

## Future Enhancements

### Planned Features

- **More Document Formats**: DOCX, PPTX, Markdown
- **Image OCR**: Extract text from images
- **Audio Transcription**: Extract text from audio
- **Video Analysis**: Extract text from video
- **More Languages**: Add support for more languages
- **Dialect Detection**: Detect regional dialects
- **Formality Detection**: Auto-detect formality level
- **Tone Detection**: Detect emotional tone
- **Cross-Language Search**: Search across languages
- **Document Summarization**: Auto-summarize ingested documents

### Community Contributions

Contributions welcome for:
- Additional document loaders
- Better chunking algorithms
- Enhanced embedding models
- More language support
- Cultural nuance improvements
- Performance optimizations
- Cross-platform adaptations

## Support

For issues or questions:
- Check document ingestion logs
- Verify ChromaDB connection
- Test language detection
- Review configuration settings
- Check API credentials
- Monitor processing times
- Test with small documents first

## License

This feature is part of JARVIS AI System.
See main project license for details.
