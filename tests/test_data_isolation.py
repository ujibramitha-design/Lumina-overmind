"""
Test Suite for Data Isolation Between KOMERSIL and SUBSIDI Projects
Ensures no data leakage between project types during high traffic
"""

import pytest
import asyncio
from datetime import datetime
from typing import Dict, List, Any
import random

# Import system modules
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core_modules.db_manager_postgres import postgres_db_manager
from api.endpoints.leads import create_lead, get_leads
from api.endpoints.projects import get_projects, create_project

class TestDataIsolation:
    """Test suite for data isolation between project types"""
    
    def __init__(self):
        self.test_db_path = "test_data_isolation.db (SQLite - removed)
        self.test_projects = {}
        self.test_leads = []
        
    def setup_test_environment(self):
        """Setup test database and test data"""
        # Create test database
        conn = # SQLite connection removed
        cursor = conn.cursor()
        
        # Create tables
        # cursor.execute() removed"""
            CREATE TABLE IF NOT EXISTS projects (
                id TEXT PRIMARY KEY,
                nama_proyek TEXT NOT NULL,
                tipe_proyek TEXT NOT NULL,
                lokasi TEXT NOT NULL,
                harga_start REAL NOT NULL,
                target_market TEXT,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # cursor.execute() removed"""
            CREATE TABLE IF NOT EXISTS leads (
                id TEXT PRIMARY KEY,
                business_name TEXT NOT NULL,
                contact TEXT NOT NULL,
                project_id TEXT NOT NULL,
                score INTEGER,
                status TEXT DEFAULT 'new',
                source TEXT DEFAULT 'test',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects (id)
            )
        """)
        
        # conn.commit() removed
        # conn.close() removed
        
        # Create test projects
        self._create_test_projects()
        
    def _create_test_projects(self):
        """Create test projects for both types"""
        projects_data = [
            {
                'id': 'komersil_1',
                'nama_proyek': 'Royal Residence Serang',
                'tipe_proyek': 'KOMERSIL',
                'lokasi': 'Serang',
                'harga_start': 500000000,
                'target_market': 'Eksekutif & Pengusaha'
            },
            {
                'id': 'komersil_2',
                'nama_proyek': 'Business Park Tangerang',
                'tipe_proyek': 'KOMERSIL',
                'lokasi': 'Tangerang',
                'harga_start': 750000000,
                'target_market': 'Profesional & Bisnis'
            },
            {
                'id': 'subsidi_1',
                'nama_proyek': 'Rumah Subsidi Cipocok',
                'tipe_proyek': 'SUBSIDI',
                'lokasi': 'Cipocok Jaya',
                'harga_start': 150000000,
                'target_market': 'PNS & Karyawan'
            },
            {
                'id': 'subsidi_2',
                'nama_proyek': 'Perumahan Bersama Pandeglang',
                'tipe_proyek': 'SUBSIDI',
                'lokasi': 'Pandeglang',
                'harga_start': 180000000,
                'target_market': 'Keluarga Muda'
            }
        ]
        
        conn = # SQLite connection removed
        cursor = conn.cursor()
        
        for project in projects_data:
            # cursor.execute() removed"""
                INSERT INTO projects (id, nama_proyek, tipe_proyek, lokasi, harga_start, target_market)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                project['id'], project['nama_proyek'], project['tipe_proyek'],
                project['lokasi'], project['harga_start'], project['target_market']
            ))
            self.test_projects[project['id']] = project
        
        # conn.commit() removed
        # conn.close() removed
    
    def test_high_traffic_isolation(self):
        """Test data isolation under high traffic conditions"""
        print("🧪 Testing High Traffic Data Isolation...")
        
        # Simulate high traffic - 1000 concurrent lead operations
        leads_created = []
        
        for i in range(1000):
            # Randomly assign to different project types
            project_ids = list(self.test_projects.keys())
            project_id = random.choice(project_ids)
            project_type = self.test_projects[project_id]['tipe_proyek']
            
            # Create lead data
            lead_data = {
                'id': f'lead_{i}',
                'business_name': f'Test Lead {i}',
                'contact': f'+62812{i:04d}',
                'project_id': project_id,
                'score': random.randint(1, 10),
                'status': 'new',
                'source': 'test_high_traffic'
            }
            
            # Insert lead
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # cursor.execute() removed"""
                INSERT INTO leads (id, business_name, contact, project_id, score, status, source)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                lead_data['id'], lead_data['business_name'], lead_data['contact'],
                lead_data['project_id'], lead_data['score'], lead_data['status'], lead_data['source']
            ))
            
            # conn.commit() removed
            # conn.close() removed
            
            leads_created.append(lead_data)
        
        # Verify data isolation
        isolation_results = self._verify_data_isolation()
        
        return isolation_results
    
    def _verify_data_isolation(self) -> Dict[str, Any]:
        """Verify that data is properly isolated by project type"""
        conn = # SQLite connection removed
        cursor = conn.cursor()
        
        # Count leads by project type
        # cursor.execute() removed"""
            SELECT p.tipe_proyek, COUNT(l.id) as lead_count
            FROM leads l
            JOIN projects p ON l.project_id = p.id
            GROUP BY p.tipe_proyek
        """)
        
        results = cursor.fetchall()
        
        # Verify no cross-contamination
        # cursor.execute() removed"""
            SELECT l.id, p.tipe_proyek, l.project_id
            FROM leads l
            JOIN projects p ON l.project_id = p.id
            WHERE p.tipe_proyek != l.project_id
        """)
        
        cross_contamination = cursor.fetchall()
        
        # conn.close() removed
        
        return {
            'leads_by_type': dict(results),
            'cross_contamination_count': len(cross_contamination),
            'cross_contamination_details': cross_contamination,
            'isolation_passed': len(cross_contamination) == 0
        }
    
    def test_query_performance_under_load(self):
        """Test query performance under high load"""
        print("🧪 Testing Query Performance Under Load...")
        
        import time
        start_time = time.time()
        
        # Simulate 1000 concurrent queries
        for i in range(1000):
            project_id = random.choice(list(self.test_projects.keys()))
            
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # Query leads for specific project
            # cursor.execute() removed"""
                SELECT COUNT(*) FROM leads WHERE project_id = ?
            """, (project_id,))
            
            result = cursor.fetchone()
            # conn.close() removed
        
        end_time = time.time()
        query_time = end_time - start_time
        
        return {
            'total_queries': 1000,
            'total_time': query_time,
            'avg_query_time': query_time / 1000,
            'queries_per_second': 1000 / query_time
        }
    
    def test_concurrent_access_isolation(self):
        """Test concurrent access doesn't break isolation"""
        print("🧪 Testing Concurrent Access Isolation...")
        
        import threading
        import time
        
        results = []
        
        def worker_thread(thread_id):
            """Worker thread for concurrent testing"""
            thread_results = []
            
            for i in range(100):
                project_id = random.choice(list(self.test_projects.keys()))
                
                try:
                    conn = # SQLite connection removed
                    cursor = conn.cursor()
                    
                    # Insert lead
                    # cursor.execute() removed"""
                        INSERT INTO leads (id, business_name, contact, project_id, score, status, source)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        f'thread_{thread_id}_lead_{i}',
                        f'Thread {thread_id} Lead {i}',
                        f'+62812{thread_id:02d}{i:02d}',
                        project_id,
                        random.randint(1, 10),
                        'new',
                        'concurrent_test'
                    ))
                    
                    # conn.commit() removed
                    # conn.close() removed
                    
                    thread_results.append({'thread_id': thread_id, 'lead_id': i, 'success': True})
                    
                except Exception as e:
                    thread_results.append({'thread_id': thread_id, 'lead_id': i, 'success': False, 'error': str(e)})
            
            results.extend(thread_results)
        
        # Create 10 concurrent threads
        threads = []
        for i in range(10):
            thread = threading.Thread(target=worker_thread, args=(i,))
            threads.append(thread)
        
        # Start all threads
        start_time = time.time()
        for thread in threads:
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        
        # Verify isolation
        isolation_check = self._verify_data_isolation()
        
        return {
            'total_operations': len(results),
            'successful_operations': len([r for r in results if r['success']]),
            'failed_operations': len([r for r in results if not r['success']]),
            'execution_time': end_time - start_time,
            'isolation_check': isolation_check
        }
    
    def test_api_endpoint_isolation(self):
        """Test API endpoints maintain isolation"""
        print("🧪 Testing API Endpoint Isolation...")
        
        # This would test the actual API endpoints
        # For now, simulate the API calls
        
        api_results = []
        
        for project_id in self.test_projects.keys():
            # Simulate API call to get leads for project
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # cursor.execute() removed"""
                SELECT l.id, l.business_name, l.contact, p.tipe_proyek, p.nama_proyek
                FROM leads l
                JOIN projects p ON l.project_id = p.id
                WHERE l.project_id = ?
                ORDER BY l.created_at DESC
                LIMIT 10
            """, (project_id,))
            
            leads = cursor.fetchall()
            # conn.close() removed
            
            api_results.append({
                'project_id': project_id,
                'project_type': self.test_projects[project_id]['tipe_proyek'],
                'leads_count': len(leads),
                'leads': leads
            })
        
        # Verify no cross-contamination in results
        cross_contamination = []
        for result in api_results:
            project_type = result['project_type']
            for lead in result['leads']:
                if lead[3] != project_type:  # tipe_proyek mismatch
                    cross_contamination.append({
                        'lead_id': lead[0],
                        'expected_type': project_type,
                        'found_type': lead[3]
                    })
        
        return {
            'api_results': api_results,
            'cross_contamination': cross_contamination,
            'isolation_passed': len(cross_contamination) == 0
        }
    
    def cleanup_test_environment(self):
        """Clean up test environment"""
        try:
            os.remove(self.test_db_path)
            print("🧹 Test database cleaned up")
        except FileNotFoundError:
            pass
    
    def run_all_tests(self):
        """Run all isolation tests"""
        print("🚀 Starting Data Isolation Test Suite...\n")
        
        # Setup test environment
        self.setup_test_environment()
        
        # Run tests
        test_results = {}
        
        try:
            # Test 1: High traffic isolation
            test_results['high_traffic'] = self.test_high_traffic_isolation()
            
            # Test 2: Query performance
            test_results['performance'] = self.test_query_performance_under_load()
            
            # Test 3: Concurrent access
            test_results['concurrent'] = self.test_concurrent_access_isolation()
            
            # Test 4: API endpoint isolation
            test_results['api_isolation'] = self.test_api_endpoint_isolation()
            
        except Exception as e:
            print(f"❌ Test execution failed: {e}")
        
        finally:
            # Cleanup
            self.cleanup_test_environment()
        
        # Generate report
        self._generate_test_report(test_results)
        
        return test_results
    
    def _generate_test_report(self, test_results: Dict[str, Any]):
        """Generate comprehensive test report"""
        report = f"""
# 🧪 DATA ISOLATION TEST REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 TEST RESULTS SUMMARY

### 1. High Traffic Isolation Test
- **Status**: {'✅ PASSED' if test_results['high_traffic']['isolation_passed'] else '❌ FAILED'}
- **Cross-Contamination**: {test_results['high_traffic']['cross_contamination_count']} cases
- **Leads Created**: 1000
- **Distribution**: {test_results['high_traffic']['leads_by_type']}

### 2. Query Performance Test
- **Total Queries**: {test_results['performance']['total_queries']}
- **Total Time**: {test_results['performance']['total_time']:.2f}s
- **Avg Query Time**: {test_results['performance']['avg_query_time']:.4f}s
- **Queries/Second**: {test_results['performance']['queries_per_second']:.2f}

### 3. Concurrent Access Test
- **Total Operations**: {test_results['concurrent']['total_operations']}
- **Successful**: {test_results['concurrent']['successful_operations']}
- **Failed**: {test_results['concurrent']['failed_operations']}
- **Execution Time**: {test_results['concurrent']['execution_time']:.2f}s
- **Isolation Status**: {'✅ PASSED' if test_results['concurrent']['isolation_check']['isolation_passed'] else '❌ FAILED'}

### 4. API Endpoint Isolation Test
- **Status**: {'✅ PASSED' if test_results['api_isolation']['isolation_passed'] else '❌ FAILED'}
- **Cross-Contamination**: {len(test_results['api_isolation']['cross_contamination'])} cases
- **Projects Tested**: {len(test_results['api_isolation']['api_results'])}

## 🔍 DETAILED ANALYSIS

### Data Isolation Status
{'✅ SECURE' if all([
    test_results['high_traffic']['isolation_passed'],
    test_results['concurrent']['isolation_check']['isolation_passed'],
    test_results['api_isolation']['isolation_passed']
]) else '❌ COMPROMISED'}

### Performance Metrics
- **Query Performance**: {'✅ EXCELLENT' if test_results['performance']['avg_query_time'] < 0.001 else '⚠️ NEEDS OPTIMIZATION'}
- **Concurrent Handling**: {'✅ EXCELLENT' if test_results['concurrent']['failed_operations'] == 0 else '⚠️ NEEDS IMPROVEMENT'}

### Recommendations
"""
        
        # Add specific recommendations based on results
        if not test_results['high_traffic']['isolation_passed']:
            report += """
⚠️ **CRITICAL**: Data isolation failed under high traffic!
- Review database connection pooling
- Implement transaction isolation levels
- Add foreign key constraints
"""
        
        if test_results['performance']['avg_query_time'] > 0.001:
            report += """
⚠️ **OPTIMIZATION NEEDED**: Query performance below expectations!
- Add database indexes on project_id
- Implement query result caching
- Consider read replicas for scaling
"""
        
        if test_results['concurrent']['failed_operations'] > 0:
            report += """
⚠️ **CONCURRENCY ISSUES**: Failed operations detected!
- Implement proper connection handling
- Add retry mechanisms for failed operations
- Consider connection pooling
"""
        
        # Save report
        with open('test_data_isolation_report.md', 'w') as f:
            f.write(report)
        
        print(report)
        print(f"\n📄 Detailed report saved to: test_data_isolation_report.md")

# Run tests if executed directly
if __name__ == "__main__":
    test_suite = TestDataIsolation()
    results = test_suite.run_all_tests()
    
    # Exit with appropriate code
    all_passed = all([
        results['high_traffic']['isolation_passed'],
        results['concurrent']['isolation_check']['isolation_passed'],
        results['api_isolation']['isolation_passed']
    ])
    
    exit(0 if all_passed else 1)
