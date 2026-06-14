/**
 * JARVIS CFO Ledger - World-Class Senior Accountant
 * =================================================
 * 
 * Double-entry bookkeeping system with tiered financial reporting
 * and automated PDF generation for cash flow, P&L, and balance sheets.
 */

const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const fs = require('fs');
const PDFDocument = require('pdfkit');
require('dotenv').config();

class FinancialLedger {
  constructor(config = {}) {
    this.config = {
      dbPath: config.dbPath || './jarvis/data/financial_ledger.db',
      currency: config.currency || 'USD',
      fiscalYearStart: config.fiscalYearStart || 'january',
      ...config,
    };
    
    this.db = null;
    this._initializeDatabase();
  }
  
  /**
   * Initialize database with double-entry bookkeeping schema
   */
  _initializeDatabase() {
    try {
      const dbDir = path.dirname(this.config.dbPath);
      if (!fs.existsSync(dbDir)) {
        fs.mkdirSync(dbDir, { recursive: true });
      }
      
      this.db = new sqlite3.Database(this.config.dbPath);
      
      // Create tables
      this.db.serialize(() => {
        // Chart of Accounts
        this.db.run(`
          CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_code TEXT UNIQUE NOT NULL,
            account_name TEXT NOT NULL,
            account_type TEXT NOT NULL,
            account_category TEXT NOT NULL,
            balance REAL DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
          )
        `);
        
        // Journal Entries (Double-Entry)
        this.db.run(`
          CREATE TABLE IF NOT EXISTS journal_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_date TEXT NOT NULL,
            description TEXT,
            reference TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
          )
        `);
        
        // Journal Entry Lines (Debits and Credits)
        this.db.run(`
          CREATE TABLE IF NOT EXISTS journal_entry_lines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            journal_entry_id INTEGER NOT NULL,
            account_id INTEGER NOT NULL,
            debit REAL DEFAULT 0,
            credit REAL DEFAULT 0,
            description TEXT,
            FOREIGN KEY (journal_entry_id) REFERENCES journal_entries(id),
            FOREIGN KEY (account_id) REFERENCES accounts(id)
          )
        `);
        
        // Revenue Tracking
        this.db.run(`
          CREATE TABLE IF NOT EXISTS revenue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            amount REAL NOT NULL,
            currency TEXT DEFAULT 'USD',
            date TEXT NOT NULL,
            category TEXT,
            description TEXT,
            journal_entry_id INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (journal_entry_id) REFERENCES journal_entries(id)
          )
        `);
        
        // Expense Tracking
        this.db.run(`
          CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            currency TEXT DEFAULT 'USD',
            date TEXT NOT NULL,
            description TEXT,
            vendor TEXT,
            journal_entry_id INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (journal_entry_id) REFERENCES journal_entries(id)
          )
        `);
        
        // Initialize default chart of accounts
        this._initializeChartOfAccounts();
      });
      
      console.log('✅ Financial Ledger initialized');
      
    } catch (error) {
      console.error('❌ Error initializing financial ledger:', error.message);
    }
  }
  
  /**
   * Initialize default chart of accounts
   */
  _initializeChartOfAccounts() {
    const defaultAccounts = [
      // Assets
      { code: '1000', name: 'Cash', type: 'asset', category: 'current' },
      { code: '1100', name: 'Accounts Receivable', type: 'asset', category: 'current' },
      { code: '1200', name: 'Inventory', type: 'asset', category: 'current' },
      { code: '1500', name: 'Equipment', type: 'asset', category: 'fixed' },
      { code: '1600', name: 'Software Licenses', type: 'asset', category: 'intangible' },
      
      // Liabilities
      { code: '2000', name: 'Accounts Payable', type: 'liability', category: 'current' },
      { code: '2100', name: 'Accrued Expenses', type: 'liability', category: 'current' },
      { code: '2500', name: 'Long-term Debt', type: 'liability', category: 'long-term' },
      
      // Equity
      { code: '3000', name: 'Owner\'s Equity', type: 'equity', category: 'owner' },
      { code: '3100', name: 'Retained Earnings', type: 'equity', category: 'retained' },
      
      // Revenue
      { code: '4000', name: 'Service Revenue', type: 'revenue', category: 'operating' },
      { code: '4100', name: 'Product Revenue', type: 'revenue', category: 'operating' },
      { code: '4200', name: 'Consulting Revenue', type: 'revenue', category: 'operating' },
      { code: '4300', name: 'SaaS Revenue', type: 'revenue', category: 'operating' },
      
      // Expenses
      { code: '5000', name: 'Cost of Goods Sold', type: 'expense', category: 'cogs' },
      { code: '5100', name: 'API Costs', type: 'expense', category: 'operating' },
      { code: '5200', name: 'Server Costs', type: 'expense', category: 'operating' },
      { code: '5300', name: 'Software Licenses', type: 'expense', category: 'operating' },
      { code: '5400', name: 'Marketing', type: 'expense', category: 'operating' },
      { code: '5500', name: 'Office Expenses', type: 'expense', category: 'operating' },
      { code: '5600', name: 'Professional Services', type: 'expense', category: 'operating' },
    ];
    
    const stmt = this.db.prepare(`
      INSERT OR IGNORE INTO accounts (account_code, account_name, account_type, account_category)
      VALUES (?, ?, ?, ?)
    `);
    
    defaultAccounts.forEach(account => {
      stmt.run(account.code, account.name, account.type, account.category);
    });
    
    stmt.finalize();
  }
  
  /**
   * Create journal entry (double-entry bookkeeping)
   */
  async createJournalEntry(date, description, lines) {
    return new Promise((resolve, reject) => {
      this.db.serialize(() => {
        this.db.run('BEGIN TRANSACTION');
        
        // Create journal entry header
        const stmt = this.db.prepare(`
          INSERT INTO journal_entries (entry_date, description)
          VALUES (?, ?)
        `);
        
        stmt.run(date, description, function(err) {
          if (err) {
            this.db.run('ROLLBACK');
            reject(err);
            return;
          }
          
          const journalEntryId = this.lastID;
          
          // Validate double-entry (debits must equal credits)
          let totalDebit = 0;
          let totalCredit = 0;
          
          lines.forEach(line => {
            totalDebit += line.debit || 0;
            totalCredit += line.credit || 0;
          });
          
          if (Math.abs(totalDebit - totalCredit) > 0.01) {
            this.db.run('ROLLBACK');
            reject(new Error('Debits must equal credits in double-entry bookkeeping'));
            return;
          }
          
          // Create journal entry lines
          const lineStmt = this.db.prepare(`
            INSERT INTO journal_entry_lines (journal_entry_id, account_id, debit, credit, description)
            VALUES (?, ?, ?, ?, ?)
          `);
          
          let completedLines = 0;
          
          lines.forEach(line => {
            lineStmt.run(
              journalEntryId,
              line.accountId,
              line.debit || 0,
              line.credit || 0,
              line.description || ''
            , (err) => {
              if (err) {
                this.db.run('ROLLBACK');
                reject(err);
                return;
              }
              
              completedLines++;
              
              if (completedLines === lines.length) {
                lineStmt.finalize();
                this.db.run('COMMIT');
                
                // Update account balances
                lines.forEach(line => {
                  this._updateAccountBalance(line.accountId, line.debit || 0, line.credit || 0);
                });
                
                resolve({
                  success: true,
                  journalEntryId: journalEntryId,
                  totalDebit: totalDebit,
                  totalCredit: totalCredit,
                });
              }
            });
          });
        });
        
        stmt.finalize();
      });
    });
  }
  
  /**
   * Update account balance
   */
  _updateAccountBalance(accountId, debit, credit) {
    this.db.run(`
      UPDATE accounts
      SET balance = balance + ? - ?,
          updated_at = CURRENT_TIMESTAMP
      WHERE id = ?
    `, [debit, credit, accountId]);
  }
  
  /**
   * Record revenue
   */
  async recordRevenue(source, amount, date, category, description, journalEntryId = null) {
    return new Promise((resolve, reject) => {
      const stmt = this.db.prepare(`
        INSERT INTO revenue (source, amount, currency, date, category, description, journal_entry_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
      `);
      
      stmt.run(source, amount, this.config.currency, date, category, description, journalEntryId, function(err) {
        if (err) {
          reject(err);
        } else {
          resolve({
            success: true,
            revenueId: this.lastID,
          });
        }
      });
      
      stmt.finalize();
    });
  }
  
  /**
   * Record expense
   */
  async recordExpense(category, amount, date, description, vendor, journalEntryId = null) {
    return new Promise((resolve, reject) => {
      const stmt = this.db.prepare(`
        INSERT INTO expenses (category, amount, currency, date, description, vendor, journal_entry_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
      `);
      
      stmt.run(category, amount, this.config.currency, date, description, vendor, journalEntryId, function(err) {
        if (err) {
          reject(err);
        } else {
          resolve({
            success: true,
            expenseId: this.lastID,
          });
        }
      });
      
      stmt.finalize();
    });
  }
  
  /**
   * Generate Simple Cash Flow Report (text summary)
   */
  async generateCashFlowReport(startDate, endDate) {
    return new Promise((resolve, reject) => {
      const sql = `
        SELECT 
          'Revenue' as type,
          SUM(amount) as total,
          COUNT(*) as transactions
        FROM revenue
        WHERE date BETWEEN ? AND ?
        UNION ALL
        SELECT 
          'Expenses' as type,
          SUM(amount) as total,
          COUNT(*) as transactions
        FROM expenses
        WHERE date BETWEEN ? AND ?
      `;
      
      this.db.all(sql, [startDate, endDate, startDate, endDate], (err, rows) => {
        if (err) {
          reject(err);
        } else {
          const revenue = rows.find(r => r.type === 'Revenue') || { total: 0, transactions: 0 };
          const expenses = rows.find(r => r.type === 'Expenses') || { total: 0, transactions: 0 };
          const netCashFlow = revenue.total - expenses.total;
          
          const report = `
===========================================
           CASH FLOW REPORT
===========================================
Period: ${startDate} to ${endDate}
Currency: ${this.config.currency}

-------------------------------------------
REVENUE
-------------------------------------------
Total Revenue: $${revenue.total.toFixed(2)}
Transactions: ${revenue.transactions}

-------------------------------------------
EXPENSES
-------------------------------------------
Total Expenses: $${expenses.total.toFixed(2)}
Transactions: ${expenses.transactions}

-------------------------------------------
NET CASH FLOW
-------------------------------------------
Net Cash Flow: $${netCashFlow.toFixed(2)}
${netCashFlow >= 0 ? '✅ POSITIVE' : '❌ NEGATIVE'}

===========================================
Generated: ${new Date().toISOString()}
===========================================
`;
          
          resolve({
            success: true,
            report: report,
            data: {
              revenue: revenue.total,
              expenses: expenses.total,
              netCashFlow: netCashFlow,
            },
          });
        }
      });
    });
  }
  
  /**
   * Generate P&L Report (PDF)
   */
  async generatePandLReport(startDate, endDate, outputPath) {
    return new Promise((resolve, reject) => {
      const sql = `
        SELECT 
          category,
          SUM(amount) as total
        FROM revenue
        WHERE date BETWEEN ? AND ?
        GROUP BY category
        UNION ALL
        SELECT 
          category,
          SUM(amount) as total
        FROM expenses
        WHERE date BETWEEN ? AND ?
        GROUP BY category
      `;
      
      this.db.all(sql, [startDate, endDate, startDate, endDate], async (err, rows) => {
        if (err) {
          reject(err);
          return;
        }
        
        try {
          const doc = new PDFDocument();
          const stream = fs.createWriteStream(outputPath);
          doc.pipe(stream);
          
          // Add content
          doc.fontSize(20).text('Profit & Loss Statement', { align: 'center' });
          doc.moveDown();
          doc.fontSize(12).text(`Period: ${startDate} to ${endDate}`);
          doc.text(`Currency: ${this.config.currency}`);
          doc.moveDown();
          
          // Revenue section
          doc.fontSize(16).text('Revenue', { underline: true });
          doc.moveDown();
          
          let totalRevenue = 0;
          rows.filter(r => !['Cost of Goods Sold', 'API Costs', 'Server Costs'].includes(r.category)).forEach(row => {
            if (row.total > 0) {
              doc.fontSize(12).text(`${row.category}: $${row.total.toFixed(2)}`);
              totalRevenue += row.total;
            }
          });
          
          doc.moveDown();
          doc.fontSize(14).text(`Total Revenue: $${totalRevenue.toFixed(2)}`, { bold: true });
          doc.moveDown();
          
          // Expenses section
          doc.fontSize(16).text('Expenses', { underline: true });
          doc.moveDown();
          
          let totalExpenses = 0;
          rows.filter(r => ['Cost of Goods Sold', 'API Costs', 'Server Costs', 'Marketing', 'Office Expenses'].includes(r.category)).forEach(row => {
            if (row.total > 0) {
              doc.fontSize(12).text(`${row.category}: $${row.total.toFixed(2)}`);
              totalExpenses += row.total;
            }
          });
          
          doc.moveDown();
          doc.fontSize(14).text(`Total Expenses: $${totalExpenses.toFixed(2)}`, { bold: true });
          doc.moveDown();
          
          // Net Profit
          const netProfit = totalRevenue - totalExpenses;
          doc.fontSize(16).text('Net Profit/Loss', { underline: true });
          doc.moveDown();
          doc.fontSize(18).text(`$${netProfit.toFixed(2)}`, { bold: true, color: netProfit >= 0 ? 'green' : 'red' });
          doc.moveDown();
          
          doc.fontSize(10).text(`Generated: ${new Date().toISOString()}`, { align: 'center' });
          
          doc.end();
          
          stream.on('finish', () => {
            resolve({
              success: true,
              filepath: outputPath,
              data: {
                totalRevenue: totalRevenue,
                totalExpenses: totalExpenses,
                netProfit: netProfit,
              },
            });
          });
          
          stream.on('error', reject);
          
        } catch (error) {
          reject(error);
        }
      });
    });
  }
  
  /**
   * Generate Balance Sheet with Financial Ratios (PDF)
   */
  async generateBalanceSheet(outputPath) {
    return new Promise((resolve, reject) => {
      const sql = `
        SELECT 
          account_type,
          account_category,
          SUM(balance) as total
        FROM accounts
        GROUP BY account_type, account_category
      `;
      
      this.db.all(sql, async (err, rows) => {
        if (err) {
          reject(err);
          return;
        }
        
        try {
          const doc = new PDFDocument();
          const stream = fs.createWriteStream(outputPath);
          doc.pipe(stream);
          
          // Add content
          doc.fontSize(20).text('Balance Sheet', { align: 'center' });
          doc.moveDown();
          doc.fontSize(12).text(`As of: ${new Date().toISOString().split('T')[0]}`);
          doc.text(`Currency: ${this.config.currency}`);
          doc.moveDown();
          
          // Assets
          doc.fontSize(16).text('Assets', { underline: true });
          doc.moveDown();
          
          let currentAssets = 0;
          let fixedAssets = 0;
          
          rows.filter(r => r.account_type === 'asset').forEach(row => {
            if (row.account_category === 'current') {
              doc.fontSize(12).text(`Current Assets - ${row.account_category}: $${row.total.toFixed(2)}`);
              currentAssets += row.total;
            } else {
              doc.fontSize(12).text(`Fixed Assets - ${row.account_category}: $${row.total.toFixed(2)}`);
              fixedAssets += row.total;
            }
          });
          
          doc.moveDown();
          doc.fontSize(14).text(`Total Assets: $${(currentAssets + fixedAssets).toFixed(2)}`, { bold: true });
          doc.moveDown();
          
          // Liabilities
          doc.fontSize(16).text('Liabilities', { underline: true });
          doc.moveDown();
          
          let currentLiabilities = 0;
          let longTermLiabilities = 0;
          
          rows.filter(r => r.account_type === 'liability').forEach(row => {
            if (row.account_category === 'current') {
              doc.fontSize(12).text(`Current Liabilities - ${row.account_category}: $${row.total.toFixed(2)}`);
              currentLiabilities += row.total;
            } else {
              doc.fontSize(12).text(`Long-term Liabilities - ${row.account_category}: $${row.total.toFixed(2)}`);
              longTermLiabilities += row.total;
            }
          });
          
          doc.moveDown();
          doc.fontSize(14).text(`Total Liabilities: $${(currentLiabilities + longTermLiabilities).toFixed(2)}`, { bold: true });
          doc.moveDown();
          
          // Equity
          doc.fontSize(16).text('Equity', { underline: true });
          doc.moveDown();
          
          let totalEquity = 0;
          rows.filter(r => r.account_type === 'equity').forEach(row => {
            doc.fontSize(12).text(`${row.account_category}: $${row.total.toFixed(2)}`);
            totalEquity += row.total;
          });
          
          doc.moveDown();
          doc.fontSize(14).text(`Total Equity: $${totalEquity.toFixed(2)}`, { bold: true });
          doc.moveDown();
          
          // Financial Ratios
          doc.fontSize(16).text('Financial Ratios', { underline: true });
          doc.moveDown();
          
          const totalAssets = currentAssets + fixedAssets;
          const totalLiabilities = currentLiabilities + longTermLiabilities;
          
          // Current Ratio
          const currentRatio = currentLiabilities > 0 ? currentAssets / currentLiabilities : 0;
          doc.fontSize(12).text(`Current Ratio: ${currentRatio.toFixed(2)} ${currentRatio >= 2 ? '✅' : '⚠️'}`);
          
          // Debt-to-Equity Ratio
          const debtToEquity = totalEquity > 0 ? totalLiabilities / totalEquity : 0;
          doc.fontSize(12).text(`Debt-to-Equity Ratio: ${debtToEquity.toFixed(2)} ${debtToEquity < 1 ? '✅' : '⚠️'}`);
          
          // Asset Turnover (simplified)
          const assetTurnover = totalAssets > 0 ? totalEquity / totalAssets : 0;
          doc.fontSize(12).text(`Asset Turnover: ${assetTurnover.toFixed(2)}`);
          
          doc.moveDown();
          doc.fontSize(10).text(`Generated: ${new Date().toISOString()}`, { align: 'center' });
          
          doc.end();
          
          stream.on('finish', () => {
            resolve({
              success: true,
              filepath: outputPath,
              data: {
                totalAssets: totalAssets,
                totalLiabilities: totalLiabilities,
                totalEquity: totalEquity,
                currentRatio: currentRatio,
                debtToEquity: debtToEquity,
              },
            });
          });
          
          stream.on('error', reject);
          
        } catch (error) {
          reject(error);
        }
      });
    });
  }
  
  /**
   * Get account balance
   */
  async getAccountBalance(accountCode) {
    return new Promise((resolve, reject) => {
      this.db.get(
        'SELECT balance FROM accounts WHERE account_code = ?',
        [accountCode],
        (err, row) => {
          if (err) {
            reject(err);
          } else {
            resolve({
              success: true,
              balance: row ? row.balance : 0,
            });
          }
        }
      );
    });
  }
  
  /**
   * Close database
   */
  close() {
    if (this.db) {
      this.db.close();
      console.log('✅ Financial Ledger closed');
    }
  }
}

// Singleton instance
let financialLedger = null;

function getFinancialLedger(config = null) {
  if (!financialLedger) {
    if (config === null) {
      config = {};
    }
    financialLedger = new FinancialLedger(config);
  }
  return financialLedger;
}

module.exports = { FinancialLedger, getFinancialLedger };
