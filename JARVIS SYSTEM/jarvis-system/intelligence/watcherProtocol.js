/**
 * JARVIS Watcher Protocol - External Codebase Awareness
 * =====================================================
 * 
 * The Watcher Protocol allows JARVIS to maintain 100% codebase awareness
 * of lumina-overmind without being directly integrated into it.
 * 
 * JARVIS reads, analyzes, and indexes the lumina-overmind directory externally
 * as a "Watcher" using the Node.js fs module and RAG/Vector setup.
 */

const fs = require('fs');
const path = require('path');
const { getDocumentIngestionEngine } = require('../omniscient/documentIngestionEngine');

class WatcherProtocol {
  constructor(config = {}) {
    this.config = {
      luminaPath: config.luminaPath || '../',
      watchInterval: config.watchInterval || 60000,  // 1 minute
      excludePatterns: config.excludePatterns || [
        'node_modules',
        '.git',
        '__pycache__',
        '.venv',
        'venv',
        'dist',
        'build',
        '.next',
        'logs',
        'jarvis-system',  // Don't watch JARVIS itself
      ],
      fileExtensions: config.fileExtensions || [
        '.js', '.ts', '.jsx', '.tsx',  // JavaScript/TypeScript
        '.py',  // Python
        '.json',  // Config files
        '.md',  // Documentation
        '.sql',  // Database schemas
      ],
      namespace: config.namespace || 'lumina-codebase',
      ...config,
    };
    
    this.documentIngestionEngine = getDocumentIngestionEngine();
    this.isWatching = false;
    this.watchTimer = null;
    this.lastScanTime = null;
    this.scanResults = {
      filesScanned: 0,
      filesIndexed: 0,
      errors: 0,
    };
  }
  
  /**
   * Start watching the Lumina codebase
   */
  async startWatching() {
    try {
      console.log('👁️ Starting Watcher Protocol...');
      console.log(`📂 Watching: ${this.config.luminaPath}`);
      
      this.isWatching = true;
      
      // Initial scan
      await this.scanCodebase();
      
      // Set up periodic scanning
      this.watchTimer = setInterval(() => {
        this.scanCodebase();
      }, this.config.watchInterval);
      
      console.log('✅ Watcher Protocol started');
      console.log(`⏱️ Scan interval: ${this.config.watchInterval / 1000} seconds`);
      
      return {
        success: true,
        message: 'Watcher Protocol started',
        config: this.config,
      };
      
    } catch (error) {
      console.error('❌ Error starting Watcher Protocol:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Stop watching the Lumina codebase
   */
  stopWatching() {
    try {
      console.log('👁️ Stopping Watcher Protocol...');
      
      this.isWatching = false;
      
      if (this.watchTimer) {
        clearInterval(this.watchTimer);
        this.watchTimer = null;
      }
      
      console.log('✅ Watcher Protocol stopped');
      
      return {
        success: true,
        message: 'Watcher Protocol stopped',
        scanResults: this.scanResults,
      };
      
    } catch (error) {
      console.error('❌ Error stopping Watcher Protocol:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Scan the Lumina codebase
   */
  async scanCodebase() {
    try {
      console.log('🔍 Scanning Lumina codebase...');
      
      const luminaAbsolutePath = path.resolve(this.config.luminaPath);
      
      if (!fs.existsSync(luminaAbsolutePath)) {
        throw new Error(`Lumina path does not exist: ${luminaAbsolutePath}`);
      }
      
      // Get all files to scan
      const files = this._getFilesToScan(luminaAbsolutePath);
      
      console.log(`📄 Found ${files.length} files to scan`);
      
      // Scan and index files
      let indexedCount = 0;
      let errorCount = 0;
      
      for (const file of files) {
        try {
          const result = await this._indexFile(file);
          if (result.success) {
            indexedCount++;
          } else {
            errorCount++;
          }
        } catch (error) {
          console.error(`Error indexing file ${file}:`, error.message);
          errorCount++;
        }
      }
      
      this.scanResults = {
        filesScanned: files.length,
        filesIndexed: indexedCount,
        errors: errorCount,
      };
      
      this.lastScanTime = new Date().toISOString();
      
      console.log(`✅ Scan complete: ${indexedCount} files indexed, ${errorCount} errors`);
      
      return {
        success: true,
        scanResults: this.scanResults,
        scannedAt: this.lastScanTime,
      };
      
    } catch (error) {
      console.error('❌ Error scanning codebase:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Get files to scan
   */
  _getFilesToScan(directory) {
    const files = [];
    
    const scanDirectory = (dir) => {
      const items = fs.readdirSync(dir);
      
      for (const item of items) {
        const fullPath = path.join(dir, item);
        const stat = fs.statSync(fullPath);
        
        // Skip excluded patterns
        if (this._shouldExclude(item, fullPath)) {
          continue;
        }
        
        if (stat.isDirectory()) {
          scanDirectory(fullPath);
        } else if (stat.isFile()) {
          // Check file extension
          const ext = path.extname(item);
          if (this.config.fileExtensions.includes(ext)) {
            files.push(fullPath);
          }
        }
      }
    };
    
    scanDirectory(directory);
    return files;
  }
  
  /**
   * Check if path should be excluded
   */
  _shouldExclude(item, fullPath) {
    for (const pattern of this.config.excludePatterns) {
      if (item.includes(pattern) || fullPath.includes(pattern)) {
        return true;
      }
    }
    return false;
  }
  
  /**
   * Index a file
   */
  async _indexFile(filePath) {
    try {
      // Read file content
      const content = fs.readFileSync(filePath, 'utf-8');
      
      // Skip empty files
      if (!content || content.trim().length === 0) {
        return { success: true, indexed: false, reason: 'empty file' };
      }
      
      // Skip very large files (>1MB)
      const stats = fs.statSync(filePath);
      if (stats.size > 1024 * 1024) {
        return { success: true, indexed: false, reason: 'file too large' };
      }
      
      // Ingest file into document engine
      const buffer = Buffer.from(content);
      const fileType = path.extname(filePath).replace('.', '');
      
      const result = await this.documentIngestionEngine.ingestDocument(
        buffer,
        fileType,
        this.config.namespace,
        {
          filePath: filePath,
          fileSize: stats.size,
          scannedAt: new Date().toISOString(),
        }
      );
      
      return result;
      
    } catch (error) {
      console.error(`Error indexing file ${filePath}:`, error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Query the indexed codebase
   */
  async queryCodebase(query, topK = 5) {
    try {
      const result = await this.documentIngestionEngine.queryVectorDB(
        query,
        this.config.namespace,
        topK
      );
      
      return {
        success: true,
        query: query,
        results: result.documents,
        count: result.documents.length,
      };
      
    } catch (error) {
      console.error('Error querying codebase:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Get file content by path
   */
  getFileContent(filePath) {
    try {
      const fullPath = path.resolve(this.config.luminaPath, filePath);
      
      if (!fs.existsSync(fullPath)) {
        return {
          success: false,
          error: 'File not found',
        };
      }
      
      const content = fs.readFileSync(fullPath, 'utf-8');
      
      return {
        success: true,
        content: content,
        filePath: fullPath,
      };
      
    } catch (error) {
      console.error('Error reading file:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Get directory structure
   */
  getDirectoryStructure(directoryPath = '') {
    try {
      const fullPath = path.resolve(this.config.luminaPath, directoryPath);
      
      if (!fs.existsSync(fullPath)) {
        return {
          success: false,
          error: 'Directory not found',
        };
      }
      
      const structure = this._buildDirectoryStructure(fullPath);
      
      return {
        success: true,
        structure: structure,
        path: fullPath,
      };
      
    } catch (error) {
      console.error('Error getting directory structure:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Build directory structure
   */
  _buildDirectoryStructure(dirPath, relativePath = '') {
    const items = fs.readdirSync(dirPath);
    const structure = [];
    
    for (const item of items) {
      const fullPath = path.join(dirPath, item);
      const stat = fs.statSync(fullPath);
      
      if (this._shouldExclude(item, fullPath)) {
        continue;
      }
      
      const itemPath = path.join(relativePath, item);
      
      if (stat.isDirectory()) {
        structure.push({
          name: item,
          type: 'directory',
          path: itemPath,
          children: this._buildDirectoryStructure(fullPath, itemPath),
        });
      } else {
        structure.push({
          name: item,
          type: 'file',
          path: itemPath,
          size: stat.size,
          extension: path.extname(item),
        });
      }
    }
    
    return structure;
  }
  
  /**
   * Get watch status
   */
  getWatchStatus() {
    return {
      isWatching: this.isWatching,
      luminaPath: this.config.luminaPath,
      watchInterval: this.config.watchInterval,
      lastScanTime: this.lastScanTime,
      scanResults: this.scanResults,
      namespace: this.config.namespace,
    };
  }
}

// Singleton instance
let watcherProtocol = null;

function getWatcherProtocol(config = null) {
  if (!watcherProtocol) {
    if (config === null) {
      config = {};
    }
    watcherProtocol = new WatcherProtocol(config);
  }
  return watcherProtocol;
}

module.exports = { WatcherProtocol, getWatcherProtocol };
