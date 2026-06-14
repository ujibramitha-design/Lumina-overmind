/**
 * JARVIS Document Ingestion Engine Wrapper
 * =========================================
 * 
 * Wrapper for document ingestion to provide consistent interface
 */

const { DocumentIngestionEngine } = require('./documentIngestion');

class DocumentIngestionEngineWrapper {
  constructor(config = {}) {
    this.engine = new DocumentIngestionEngine(config);
  }

  async ingestDocument(fileBuffer, fileType, namespace, metadata = {}) {
    return await this.engine.ingestDocument(fileBuffer, fileType, namespace, metadata);
  }

  async ingestURL(url, namespace, metadata = {}) {
    return await this.engine.ingestURL(url, namespace, metadata);
  }

  async queryVectorDB(query, namespace, nResults = 5) {
    return await this.engine.queryVectorDB(query, namespace, nResults);
  }

  async deleteDocument(documentId, namespace) {
    return await this.engine.deleteDocument(documentId, namespace);
  }

  async listNamespaces() {
    return await this.engine.listNamespaces();
  }

  async getNamespaceStats(namespace) {
    return await this.engine.getNamespaceStats(namespace);
  }
}

// Singleton instance
let documentIngestionEngine = null;

function getDocumentIngestionEngine(config = null) {
  if (!documentIngestionEngine) {
    if (config === null) {
      config = {};
    }
    documentIngestionEngine = new DocumentIngestionEngineWrapper(config);
  }
  return documentIngestionEngine;
}

module.exports = { DocumentIngestionEngineWrapper, getDocumentIngestionEngine };
