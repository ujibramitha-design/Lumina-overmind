/**
 * JARVIS Deep Knowledge Ingestion Engine (The "Swallow" Protocol)
 * ================================================================
 * 
 * Document ingestion system for massive document/URL processing.
 * Supports PDFs, EPUBs, TXT files, and web scraping with semantic chunking
 * and vector database storage using ChromaDB.
 */

const { GoogleGenerativeAI } = require('@google/generative-ai');
const { ChromaClient } = require('chromadb');
const pdf = require('pdf-parse');
const epub = require('epub2');
const cheerio = require('cheerio');
const axios = require('axios');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

class DocumentIngestionEngine {
  constructor(config = {}) {
    this.config = {
      chromaPath: config.chromaPath || './jarvis/data/chroma',
      chunkSize: config.chunkSize || 1000,
      chunkOverlap: config.chunkOverlap || 200,
      batchSize: config.batchSize || 100,
      embeddingModel: config.embeddingModel || 'text-embedding-004',
      ...config,
    };
    
    this.chromaClient = null;
    this.genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
    this.embeddingModel = this.genAI.getGenerativeModel({
      model: this.config.embeddingModel,
    });
    
    this._initializeChromaDB();
  }
  
  /**
   * Initialize ChromaDB
   */
  async _initializeChromaDB() {
    try {
      this.chromaClient = new ChromaClient({
        path: this.config.chromaPath,
      });
      
      console.log('✅ ChromaDB initialized');
    } catch (error) {
      console.error('❌ Error initializing ChromaDB:', error.message);
    }
  }
  
  /**
   * Ingest document from file buffer
   */
  async ingestDocument(fileBuffer, fileType, namespace, metadata = {}) {
    try {
      console.log(`📄 Ingesting ${fileType} document...`);
      
      // Extract text from document
      const text = await this._extractText(fileBuffer, fileType);
      
      if (!text || text.length === 0) {
        throw new Error('No text extracted from document');
      }
      
      // Process asynchronously to avoid blocking
      const result = await this._processDocumentAsync(text, namespace, metadata);
      
      return {
        success: true,
        chunksProcessed: result.chunksProcessed,
        namespace: namespace,
        documentId: result.documentId,
      };
      
    } catch (error) {
      console.error('❌ Error ingesting document:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Ingest document from URL
   */
  async ingestURL(url, namespace, metadata = {}) {
    try {
      console.log(`🌐 Ingesting URL: ${url}`);
      
      // Fetch URL content
      const response = await axios.get(url, {
        timeout: 30000,
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        },
      });
      
      // Extract text from HTML
      const text = this._extractTextFromHTML(response.data);
      
      if (!text || text.length === 0) {
        throw new Error('No text extracted from URL');
      }
      
      // Process asynchronously
      const result = await this._processDocumentAsync(text, namespace, {
        ...metadata,
        source: url,
        sourceType: 'url',
      });
      
      return {
        success: true,
        chunksProcessed: result.chunksProcessed,
        namespace: namespace,
        documentId: result.documentId,
      };
      
    } catch (error) {
      console.error('❌ Error ingesting URL:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Extract text from document based on file type
   */
  async _extractText(fileBuffer, fileType) {
    try {
      switch (fileType.toLowerCase()) {
        case 'pdf':
          return await this._extractFromPDF(fileBuffer);
        case 'epub':
          return await this._extractFromEPUB(fileBuffer);
        case 'txt':
          return fileBuffer.toString('utf-8');
        default:
          throw new Error(`Unsupported file type: ${fileType}`);
      }
    } catch (error) {
      console.error(`Error extracting text from ${fileType}:`, error.message);
      throw error;
    }
  }
  
  /**
   * Extract text from PDF
   */
  async _extractFromPDF(buffer) {
    try {
      const data = await pdf(buffer);
      return data.text;
    } catch (error) {
      console.error('Error extracting from PDF:', error.message);
      throw error;
    }
  }
  
  /**
   * Extract text from EPUB
   */
  async _extractFromEPUB(buffer) {
    try {
      // Save buffer to temp file
      const tempPath = path.join('./jarvis/temp', `temp_${Date.now()}.epub`);
      const dir = path.dirname(tempPath);
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
      fs.writeFileSync(tempPath, buffer);
      
      // Extract text using epub2
      const epubBook = await epub.open(tempPath);
      let text = '';
      
      const chapters = await epubBook.getChapters();
      for (const chapter of chapters) {
        const content = await chapter.getContent();
        text += content + '\n\n';
      }
      
      // Clean up temp file
      fs.unlinkSync(tempPath);
      
      return text;
    } catch (error) {
      console.error('Error extracting from EPUB:', error.message);
      throw error;
    }
  }
  
  /**
   * Extract text from HTML
   */
  _extractTextFromHTML(html) {
    try {
      const $ = cheerio.load(html);
      
      // Remove script and style elements
      $('script, style, nav, footer, header').remove();
      
      // Extract text from body
      const text = $('body').text();
      
      // Clean up whitespace
      return text.replace(/\s+/g, ' ').trim();
    } catch (error) {
      console.error('Error extracting from HTML:', error.message);
      throw error;
    }
  }
  
  /**
   * Process document asynchronously
   */
  async _processDocumentAsync(text, namespace, metadata) {
    return new Promise((resolve, reject) => {
      // Use setImmediate to avoid blocking
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
  
  /**
   * Process document: chunk, embed, and store
   */
  async _processDocument(text, namespace, metadata) {
    try {
      console.log(`🔄 Processing document (${text.length} characters)...`);
      
      // Semantic chunking
      const chunks = await this._semanticChunking(text);
      console.log(`📝 Created ${chunks.length} chunks`);
      
      // Get or create collection
      const collection = await this._getOrCreateCollection(namespace);
      
      // Process chunks in batches
      const documentId = `doc_${Date.now()}`;
      let processedCount = 0;
      
      for (let i = 0; i < chunks.length; i += this.config.batchSize) {
        const batch = chunks.slice(i, i + this.config.batchSize);
        
        // Generate embeddings for batch
        const embeddings = await this._generateEmbeddings(batch);
        
        // Add to ChromaDB
        await collection.add({
          ids: batch.map((_, idx) => `${documentId}_chunk_${i + idx}`),
          embeddings: embeddings,
          metadatas: batch.map((chunk, idx) => ({
            ...metadata,
            chunkIndex: i + idx,
            chunkText: chunk.substring(0, 100),  // Preview
            documentId: documentId,
          })),
          documents: batch,
        });
        
        processedCount += batch.length;
        console.log(`📊 Processed ${processedCount}/${chunks.length} chunks`);
      }
      
      console.log(`✅ Document processing complete: ${processedCount} chunks stored`);
      
      return {
        chunksProcessed: processedCount,
        documentId: documentId,
      };
      
    } catch (error) {
      console.error('Error processing document:', error.message);
      throw error;
    }
  }
  
  /**
   * Semantic chunking
   */
  async _semanticChunking(text) {
    try {
      // Use Gemini for semantic chunking
      const prompt = `
Chunk the following text into semantically meaningful sections.
Each chunk should be:
- Around ${this.config.chunkSize} characters
- Overlap by ${this.config.chunkOverlap} characters
- Complete thoughts or paragraphs
- Coherent and self-contained

Text:
${text}

Return as JSON array of chunks.`;
      
      const model = this.genAI.getGenerativeModel({
        model: 'gemini-1.5-flash',
      });
      
      const result = await model.generateContent(prompt);
      const chunks = JSON.parse(result.response.text());
      
      return chunks;
      
    } catch (error) {
      console.error('Error in semantic chunking, falling back to simple chunking:', error.message);
      return this._simpleChunking(text);
    }
  }
  
  /**
   * Simple chunking (fallback)
   */
  _simpleChunking(text) {
    const chunks = [];
    let start = 0;
    
    while (start < text.length) {
      const end = Math.min(start + this.config.chunkSize, text.length);
      chunks.push(text.substring(start, end));
      start = end - this.config.chunkOverlap;
    }
    
    return chunks;
  }
  
  /**
   * Generate embeddings for chunks
   */
  async _generateEmbeddings(chunks) {
    try {
      const embeddings = [];
      
      for (const chunk of chunks) {
        const result = await this.embeddingModel.embedContent(chunk);
        embeddings.push(result.embedding.values);
      }
      
      return embeddings;
      
    } catch (error) {
      console.error('Error generating embeddings:', error.message);
      throw error;
    }
  }
  
  /**
   * Get or create ChromaDB collection
   */
  async _getOrCreateCollection(namespace) {
    try {
      let collection;
      
      try {
        collection = await this.chromaClient.getCollection({ name: namespace });
      } catch (error) {
        // Collection doesn't exist, create it
        collection = await this.chromaClient.createCollection({
          name: namespace,
          metadata: {
            created: new Date().toISOString(),
          },
        });
      }
      
      return collection;
      
    } catch (error) {
      console.error('Error getting/creating collection:', error.message);
      throw error;
    }
  }
  
  /**
   * Query vector database
   */
  async queryVectorDB(query, namespace, nResults = 5) {
    try {
      console.log(`🔍 Querying vector DB: "${query.substring(0, 50)}..."`);
      
      // Get collection
      const collection = await this.chromaClient.getCollection({ name: namespace });
      
      // Generate query embedding
      const queryEmbedding = await this.embeddingModel.embedContent(query);
      
      // Query collection
      const results = await collection.query({
        queryEmbeddings: [queryEmbedding.embedding.values],
        nResults: nResults,
      });
      
      console.log(`✅ Found ${results.documents[0].length} relevant chunks`);
      
      return {
        success: true,
        documents: results.documents[0],
        metadatas: results.metadatas[0],
        distances: results.distances[0],
      };
      
    } catch (error) {
      console.error('Error querying vector DB:', error.message);
      return {
        success: false,
        error: error.message,
        documents: [],
      };
    }
  }
  
  /**
   * Delete document from namespace
   */
  async deleteDocument(documentId, namespace) {
    try {
      const collection = await this.chromaClient.getCollection({ name: namespace });
      
      // Get all chunks for document
      const results = await collection.get({
        where: { documentId: documentId },
      });
      
      if (results.ids.length === 0) {
        return {
          success: true,
          message: 'Document not found',
        };
      }
      
      // Delete chunks
      await collection.delete({
        ids: results.ids,
      });
      
      console.log(`🗑️ Deleted document ${documentId} (${results.ids.length} chunks)`);
      
      return {
        success: true,
        chunksDeleted: results.ids.length,
      };
      
    } catch (error) {
      console.error('Error deleting document:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * List all namespaces
   */
  async listNamespaces() {
    try {
      const collections = await this.chromaClient.listCollections();
      
      return {
        success: true,
        namespaces: collections.map(c => c.name),
      };
      
    } catch (error) {
      console.error('Error listing namespaces:', error.message);
      return {
        success: false,
        error: error.message,
        namespaces: [],
      };
    }
  }
  
  /**
   * Get namespace statistics
   */
  async getNamespaceStats(namespace) {
    try {
      const collection = await this.chromaClient.getCollection({ name: namespace });
      const count = await collection.count();
      
      return {
        success: true,
        namespace: namespace,
        documentCount: count,
      };
      
    } catch (error) {
      console.error('Error getting namespace stats:', error.message);
      return {
        success: false,
        error: error.message,
        documentCount: 0,
      };
    }
  }
}

// Singleton instance
let documentIngestionEngine = null;

function getDocumentIngestionEngine(config = null) {
  if (!documentIngestionEngine) {
    if (config === null) {
      config = {};
    }
    documentIngestionEngine = new DocumentIngestionEngine(config);
  }
  return documentIngestionEngine;
}

module.exports = { DocumentIngestionEngine, getDocumentIngestionEngine };
