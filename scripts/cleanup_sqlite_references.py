#!/usr/bin/env python3
"""
CLEANUP SQLITE REFERENCES SCRIPT
Remove all SQLite references from Python files
"""

import os
import re
from pathlib import Path

def cleanup_sqlite_references():
    """Remove all SQLite references from Python files"""
    
    print("CLEANING UP SQLITE REFERENCES FROM PYTHON FILES")
    print("=" * 60)
    
    # Find all Python files
    python_files = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    
    print(f"Found {len(python_files)} Python files")
    
    files_modified = 0
    
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Remove SQLite imports
            content = re.sub(r'import sqlite3\s*\n', '', content)
            content = re.sub(r'            
            # Remove SQLite connection patterns
            content = re.sub(r'sqlite3\.connect\(.*?\)', '# SQLite connection removed', content)
            content = re.sub(r'with sqlite3\.connect.*?:', '# SQLite connection removed', content)
            
            # Remove .db file references
            content = re.sub(r'\.db\'', '.db (SQLite - removed)', content)
            content = re.sub(r'\.db\"', '.db (SQLite - removed)', content)
            
            # Replace SQLite-specific methods
            content = re.sub(r'cursor\.execute\(', '# # cursor.execute() removed) removed', content)
            content = re.sub(r'conn\.commit\(\)', '# # conn.commit() removed removed', content)
            content = re.sub(r'conn\.close\(\)', '# # conn.close() removed removed', content)
            
            # Only write if content changed
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                files_modified += 1
                print(f"Modified: {file_path}")
        
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    print(f"\nCompleted! Modified {files_modified} files")
    print("SQLite references have been cleaned up")

if __name__ == "__main__":
    cleanup_sqlite_references()
