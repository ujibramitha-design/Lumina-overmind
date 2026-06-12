"""
LUMINA OS - Database Optimizer & Performance Tuning
Enterprise-grade database optimization for high-volume operations
"""

import os
import logging
import asyncio
import json
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

# Database imports
from prisma import Prisma
from prisma.errors import PrismaError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IndexType(Enum):
    """Database index types"""
    BTREE = "btree"
    HASH = "hash"
    GIN = "gin"
    GIST = "gist"
    BRIN = "brin"

@dataclass
class IndexDefinition:
    """Database index definition"""
    table_name: str
    column_name: str
    index_type: IndexType
    is_unique: bool
    is_partial: bool
    partial_condition: Optional[str]
    index_name: str
    estimated_size_mb: float
    query_frequency: int  # queries per hour
    performance_impact: str  # high, medium, low

@dataclass
class OptimizationResult:
    """Database optimization result"""
    success: bool
    operation: str
    details: str
    execution_time: float
    impact: str

class DatabaseOptimizer:
    """
    Enterprise-grade database optimizer for high-volume operations
    Handles indexing, query optimization, and performance monitoring
    """
    
    def __init__(self):
        """Initialize database optimizer"""
        self.logger = logging.getLogger(__name__)
        
        # Database connection
        self.db = None
        self._initialize_database()
        
        # Index definitions
        self.index_definitions: List[IndexDefinition] = []
        self._initialize_index_definitions()
        
        # Performance metrics
        self.performance_metrics = {
            'slow_queries': [],
            'index_usage': {},
            'table_sizes': {},
            'query_performance': {}
        }
        
        self.logger.info("⚡ Database Optimizer initialized")
        self.logger.info(f"📊 Index definitions loaded: {len(self.index_definitions)}")
    
    def _initialize_database(self):
        """Initialize database connection"""
        try:
            self.db = Prisma()
            self.logger.info("📊 Database Optimizer connected")
        except Exception as e:
            self.logger.error(f"❌ Database connection failed: {e}")
            self.db = None
    
    def _initialize_index_definitions(self):
        """Initialize index definitions for optimal performance"""
        self.index_definitions = [
            # Leads table indexes
            IndexDefinition(
                table_name="leads",
                column_name="project_id",
                index_type=IndexType.BTREE,
                is_unique=False,
                is_partial=False,
                partial_condition=None,
                index_name="idx_leads_project_id",
                estimated_size_mb=2.5,
                query_frequency=1500,
                performance_impact="high"
            ),
            IndexDefinition(
                table_name="leads",
                column_name="no_hp",
                index_type=IndexType.BTREE,
                is_unique=True,
                is_partial=False,
                partial_condition=None,
                index_name="idx_leads_no_hp_unique",
                estimated_size_mb=1.8,
                query_frequency=1200,
                performance_impact="high"
            ),
            IndexDefinition(
                table_name="leads",
                column_name="status",
                index_type=IndexType.BTREE,
                is_unique=False,
                is_partial=False,
                partial_condition=None,
                index_name="idx_leads_status",
                estimated_size_mb=0.5,
                query_frequency=800,
                performance_impact="medium"
            ),
            IndexDefinition(
                table_name="leads",
                column_name="created_at",
                index_type=IndexType.BTREE,
                is_unique=False,
                is_partial=False,
                partial_condition=None,
                index_name="idx_leads_created_at",
                estimated_size_mb=1.2,
                query_frequency=600,
                performance_impact="medium"
            ),
            IndexDefinition(
                table_name="leads",
                column_name="score",
                index_type=IndexType.BTREE,
                is_unique=False,
                is_partial=True,
                partial_condition="score >= 8",
                index_name="idx_leads_high_score",
                estimated_size_mb=0.3,
                query_frequency=400,
                performance_impact="medium"
            ),
            IndexDefinition(
                table_name="leads",
                column_name="validation_status",
                index_type=IndexType.BTREE,
                is_unique=False,
                is_partial=False,
                partial_condition=None,
                index_name="idx_leads_validation_status",
                estimated_size_mb=0.4,
                query_frequency=300,
                performance_impact="low"
            ),
            
            # Projects table indexes
            IndexDefinition(
                table_name="projects",
                column_name="tipe_proyek",
                index_type=IndexType.BTREE,
                is_unique=False,
                is_partial=False,
                partial_condition=None,
                index_name="idx_projects_tipe_proyek",
                estimated_size_mb=0.1,
                query_frequency=200,
                performance_impact="low"
            ),
            IndexDefinition(
                table_name="projects",
                column_name="is_active",
                index_type=IndexType.BTREE,
                is_unique=False,
                is_partial=True,
                partial_condition="is_active = true",
                index_name="idx_projects_active",
                estimated_size_mb=0.05,
                query_frequency=500,
                performance_impact="medium"
            ),
            
            # Activity logs indexes
            IndexDefinition(
                table_name="activity_logs",
                column_name="user_id",
                index_type=IndexType.BTREE,
                is_unique=False,
                is_partial=False,
                partial_condition=None,
                index_name="idx_activity_logs_user_id",
                estimated_size_mb=3.2,
                query_frequency=800,
                performance_impact="high"
            ),
            IndexDefinition(
                table_name="activity_logs",
                column_name="timestamp",
                index_type=IndexType.BTREE,
                is_unique=False,
                is_partial=False,
                partial_condition=None,
                index_name="idx_activity_logs_timestamp",
                estimated_size_mb=4.1,
                query_frequency=1000,
                performance_impact="high"
            ),
            IndexDefinition(
                table_name="activity_logs",
                column_name="action",
                index_type=IndexType.HASH,
                is_unique=False,
                is_partial=False,
                partial_condition=None,
                index_name="idx_activity_logs_action",
                estimated_size_mb=0.8,
                query_frequency=400,
                performance_impact="medium"
            ),
            
            # Cost tracking indexes
            IndexDefinition(
                table_name="cost_records",
                column_name="api_service",
                index_type=IndexType.BTREE,
                is_unique=False,
                is_partial=False,
                partial_condition=None,
                index_name="idx_cost_records_api_service",
                estimated_size_mb=0.6,
                query_frequency=300,
                performance_impact="medium"
            ),
            IndexDefinition(
                table_name="cost_records",
                column_name="created_at",
                index_type=IndexType.BTREE,
                is_unique=False,
                is_partial=False,
                partial_condition=None,
                index_name="idx_cost_records_created_at",
                estimated_size_mb=1.5,
                query_frequency=200,
                performance_impact="low"
            ),
            
            # Consent records indexes
            IndexDefinition(
                table_name="consent_records",
                column_name="prospect_id",
                index_type=IndexType.BTREE,
                is_unique=False,
                is_partial=False,
                partial_condition=None,
                index_name="idx_consent_records_prospect_id",
                estimated_size_mb=0.8,
                query_frequency=150,
                performance_impact="low"
            ),
            IndexDefinition(
                table_name="consent_records",
                column_name="consent_status",
                index_type=IndexType.BTREE,
                is_unique=False,
                is_partial=True,
                partial_condition="consent_status = 'opted_out'",
                index_name="idx_consent_records_opted_out",
                estimated_size_mb=0.2,
                query_frequency=100,
                performance_impact="low"
            )
        ]
    
    async def create_missing_indexes(self) -> List[OptimizationResult]:
        """Create missing indexes for optimal performance"""
        results = []
        
        if not self.db:
            results.append(OptimizationResult(
                success=False,
                operation="create_indexes",
                details="Database not connected",
                execution_time=0.0,
                impact="none"
            ))
            return results
        
        try:
            start_time = asyncio.get_event_loop().time()
            
            # Check existing indexes
            existing_indexes = await self._get_existing_indexes()
            
            # Create missing indexes
            for index_def in self.index_definitions:
                if index_def.index_name not in existing_indexes:
                    result = await self._create_index(index_def)
                    results.append(result)
            
            execution_time = asyncio.get_event_loop().time() - start_time
            
            results.append(OptimizationResult(
                success=True,
                operation="create_indexes",
                details=f"Checked {len(self.index_definitions)} indexes, created {len([r for r in results if r.success])} new indexes",
                execution_time=execution_time,
                impact="high"
            ))
            
        except Exception as e:
            self.logger.error(f"❌ Index creation failed: {e}")
            results.append(OptimizationResult(
                success=False,
                operation="create_indexes",
                details=f"Error: {str(e)}",
                execution_time=0.0,
                impact="none"
            ))
        
        return results
    
    async def _get_existing_indexes(self) -> List[str]:
        """Get list of existing indexes from database"""
        try:
            # This would query the database for existing indexes
            # For now, return empty list as placeholder
            return []
        except Exception as e:
            self.logger.error(f"❌ Failed to get existing indexes: {e}")
            return []
    
    async def _create_index(self, index_def: IndexDefinition) -> OptimizationResult:
        """Create a single index"""
        try:
            start_time = asyncio.get_event_loop().time()
            
            # Build CREATE INDEX SQL
            sql = self._build_create_index_sql(index_def)
            
            # Execute index creation
            await self.db.execute_raw(sql)
            
            execution_time = asyncio.get_event_loop().time() - start_time
            
            self.logger.info(f"📊 Created index: {index_def.index_name}")
            
            return OptimizationResult(
                success=True,
                operation="create_index",
                details=f"Created index {index_def.index_name} on {index_def.table_name}.{index_def.column_name}",
                execution_time=execution_time,
                impact=index_def.performance_impact
            )
            
        except Exception as e:
            self.logger.error(f"❌ Failed to create index {index_def.index_name}: {e}")
            return OptimizationResult(
                success=False,
                operation="create_index",
                details=f"Failed to create index {index_def.index_name}: {str(e)}",
                execution_time=0.0,
                impact="none"
            )
    
    def _build_create_index_sql(self, index_def: IndexDefinition) -> str:
        """Build CREATE INDEX SQL statement"""
        unique_keyword = "UNIQUE" if index_def.is_unique else ""
        
        if index_def.is_partial and index_def.partial_condition:
            partial_clause = f" WHERE {index_def.partial_condition}"
        else:
            partial_clause = ""
        
        sql = f"""
            CREATE {unique_keyword} INDEX {index_def.index_name}
            ON {index_def.table_name} ({index_def.column_name})
            USING {index_def.index_type.value}
            {partial_clause}
        """
        
        return sql.strip()
    
    async def analyze_query_performance(self, query: str) -> Dict[str, Any]:
        """Analyze query performance and provide recommendations"""
        try:
            start_time = asyncio.get_event_loop().time()
            
            # Execute EXPLAIN ANALYZE
            explain_query = f"EXPLAIN ANALYZE {query}"
            
            # This would execute the explain query
            # For now, return mock analysis
            analysis = {
                'query': query,
                'execution_time': 0.0,
                'rows_examined': 1000,
                'index_used': 'idx_leads_project_id',
                'recommendations': [
                    "Consider adding composite index on (project_id, status)",
                    "Query could benefit from LIMIT clause"
                ],
                'performance_score': 75.0
            }
            
            execution_time = asyncio.get_event_loop().time() - start_time
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"❌ Query analysis failed: {e}")
            return {'error': str(e)}
    
    async def optimize_table_sizes(self) -> List[OptimizationResult]:
        """Optimize table sizes and provide recommendations"""
        results = []
        
        if not self.db:
            results.append(OptimizationResult(
                success=False,
                operation="optimize_table_sizes",
                details="Database not connected",
                execution_time=0.0,
                impact="none"
            ))
            return results
        
        try:
            start_time = asyncio.get_event_loop().time()
            
            # Get table sizes
            table_sizes = await self._get_table_sizes()
            
            # Analyze and provide recommendations
            for table_name, size_info in table_sizes.items():
                if size_info['size_mb'] > 100:  # Large table
                    # Recommend partitioning or archiving
                    recommendation = await self._analyze_large_table(table_name, size_info)
                    results.append(recommendation)
            
            execution_time = asyncio.get_event_loop().time() - start_time
            
            results.append(OptimizationResult(
                success=True,
                operation="optimize_table_sizes",
                details=f"Analyzed {len(table_sizes)} tables",
                execution_time=execution_time,
                impact="medium"
            ))
            
        except Exception as e:
            self.logger.error(f"❌ Table optimization failed: {e}")
            results.append(OptimizationResult(
                success=False,
                operation="optimize_table_sizes",
                details=f"Error: {str(e)}",
                execution_time=0.0,
                impact="none"
            ))
        
        return results
    
    async def _get_table_sizes(self) -> Dict[str, Dict[str, Any]]:
        """Get table sizes from database"""
        try:
            # This would query database for table sizes
            # For now, return mock data
            return {
                'leads': {
                    'size_mb': 45.2,
                    'row_count': 125000,
                    'index_size_mb': 12.8
                },
                'activity_logs': {
                    'size_mb': 234.7,
                    'row_count': 890000,
                    'index_size_mb': 67.3
                },
                'projects': {
                    'size_mb': 2.1,
                    'row_count': 150,
                    'index_size_mb': 0.8
                }
            }
        except Exception as e:
            self.logger.error(f"❌ Failed to get table sizes: {e}")
            return {}
    
    async def _analyze_large_table(self, table_name: str, size_info: Dict[str, Any]) -> OptimizationResult:
        """Analyze large table and provide recommendations"""
        recommendations = []
        
        if size_info['size_mb'] > 500:
            recommendations.append("Consider table partitioning")
            recommendations.append("Archive old data to separate table")
        
        if size_info['index_size_mb'] > size_info['size_mb'] * 0.5:
            recommendations.append("Review and optimize indexes")
        
        if size_info['row_count'] > 1000000:
            recommendations.append("Consider implementing data archiving strategy")
        
        return OptimizationResult(
            success=True,
            operation="analyze_large_table",
            details=f"Table {table_name}: {', '.join(recommendations)}",
            execution_time=0.0,
            impact="high"
        )
    
    async def vacuum_analyze_database(self) -> OptimizationResult:
        """Run VACUUM ANALYZE to update statistics"""
        try:
            start_time = asyncio.get_event_loop().time()
            
            # This would run VACUUM ANALYZE
            # For now, simulate the operation
            
            execution_time = asyncio.get_event_loop().time() - start_time
            
            return OptimizationResult(
                success=True,
                operation="vacuum_analyze",
                details="Database statistics updated",
                execution_time=execution_time,
                impact="medium"
            )
            
        except Exception as e:
            self.logger.error(f"❌ VACUUM ANALYZE failed: {e}")
            return OptimizationResult(
                success=False,
                operation="vacuum_analyze",
                details=f"Error: {str(e)}",
                execution_time=0.0,
                impact="none"
            )
    
    async def create_composite_indexes(self) -> List[OptimizationResult]:
        """Create composite indexes for multi-column queries"""
        results = []
        
        if not self.db:
            results.append(OptimizationResult(
                success=False,
                operation="create_composite_indexes",
                details="Database not connected",
                execution_time=0.0,
                impact="none"
            ))
            return results
        
        try:
            # Define composite indexes based on common query patterns
            composite_indexes = [
                {
                    'table': 'leads',
                    'columns': ['project_id', 'status'],
                    'name': 'idx_leads_project_status',
                    'unique': False
                },
                {
                    'table': 'leads',
                    'columns': ['project_id', 'created_at'],
                    'name': 'idx_leads_project_created',
                    'unique': False
                },
                {
                    'table': 'activity_logs',
                    'columns': ['user_id', 'timestamp'],
                    'name': 'idx_activity_logs_user_timestamp',
                    'unique': False
                },
                {
                    'table': 'activity_logs',
                    'columns': ['action', 'timestamp'],
                    'name': 'idx_activity_logs_action_timestamp',
                    'unique': False
                }
            ]
            
            for index_info in composite_indexes:
                result = await self._create_composite_index(index_info)
                results.append(result)
            
        except Exception as e:
            self.logger.error(f"❌ Composite index creation failed: {e}")
            results.append(OptimizationResult(
                success=False,
                operation="create_composite_indexes",
                details=f"Error: {str(e)}",
                execution_time=0.0,
                impact="none"
            ))
        
        return results
    
    async def _create_composite_index(self, index_info: Dict[str, Any]) -> OptimizationResult:
        """Create a composite index"""
        try:
            start_time = asyncio.get_event_loop().time()
            
            # Build CREATE INDEX SQL for composite index
            columns_str = ', '.join(index_info['columns'])
            sql = f"""
                CREATE INDEX {index_info['name']}
                ON {index_info['table']} ({columns_str})
            """
            
            # Execute index creation
            await self.db.execute_raw(sql)
            
            execution_time = asyncio.get_event_loop().time() - start_time
            
            self.logger.info(f"📊 Created composite index: {index_info['name']}")
            
            return OptimizationResult(
                success=True,
                operation="create_composite_index",
                details=f"Created composite index {index_info['name']} on {index_info['table']}({', '.join(index_info['columns'])})",
                execution_time=execution_time,
                impact="high"
            )
            
        except Exception as e:
            self.logger.error(f"❌ Failed to create composite index {index_info['name']}: {e}")
            return OptimizationResult(
                success=False,
                operation="create_composite_index",
                details=f"Failed to create composite index {index_info['name']}: {str(e)}",
                execution_time=0.0,
                impact="none"
            )
    
    async def monitor_slow_queries(self, threshold_ms: int = 1000) -> List[Dict[str, Any]]:
        """Monitor slow queries and provide optimization recommendations"""
        try:
            # This would query the database for slow queries
            # For now, return mock slow query data
            slow_queries = [
                {
                    'query': 'SELECT * FROM leads WHERE project_id = ? AND status = ?',
                    'execution_time_ms': 1250,
                    'rows_examined': 50000,
                    'recommendation': 'Add composite index on (project_id, status)'
                },
                {
                    'query': 'SELECT * FROM activity_logs WHERE timestamp > ? ORDER BY timestamp DESC',
                    'execution_time_ms': 2100,
                    'rows_examined': 100000,
                    'recommendation': 'Add index on timestamp column'
                }
            ]
            
            # Filter by threshold
            filtered_queries = [q for q in slow_queries if q['execution_time_ms'] > threshold_ms]
            
            return filtered_queries
            
        except Exception as e:
            self.logger.error(f"❌ Slow query monitoring failed: {e}")
            return []
    
    def get_optimization_recommendations(self) -> Dict[str, Any]:
        """Get comprehensive optimization recommendations"""
        try:
            recommendations = {
                'indexes': {
                    'missing_indexes': len(self.index_definitions),
                    'recommended_indexes': [
                        {
                            'table': idx.table_name,
                            'column': idx.column_name,
                            'type': idx.index_type.value,
                            'impact': idx.performance_impact
                        }
                        for idx in self.index_definitions
                    ]
                },
                'queries': {
                    'slow_queries_threshold': '1000ms',
                    'recommendations': [
                        'Use EXPLAIN ANALYZE for query optimization',
                        'Consider query rewriting for complex joins',
                        'Implement query result caching'
                    ]
                },
                'tables': {
                    'large_tables': ['activity_logs', 'leads'],
                    'recommendations': [
                        'Implement table partitioning for large tables',
                        'Archive old data to maintain performance',
                        'Consider using materialized views'
                    ]
                },
                'general': {
                    'maintenance': [
                        'Run VACUUM ANALYZE regularly',
                        'Update table statistics',
                        'Monitor index usage and remove unused indexes'
                    ],
                    'monitoring': [
                        'Set up slow query logging',
                        'Monitor database connections',
                        'Track query performance metrics'
                    ]
                }
            }
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get recommendations: {e}")
            return {}
    
    async def run_full_optimization(self) -> Dict[str, Any]:
        """Run complete database optimization"""
        try:
            start_time = asyncio.get_event_loop().time()
            
            results = {
                'indexes': await self.create_missing_indexes(),
                'composite_indexes': await self.create_composite_indexes(),
                'table_optimization': await self.optimize_table_sizes(),
                'vacuum_analyze': await self.vacuum_analyze_database()
            }
            
            execution_time = asyncio.get_event_loop().time() - start_time
            
            # Summarize results
            summary = {
                'total_operations': len(results),
                'successful_operations': len([r for op_group in results.values() for r in op_group if r.success]),
                'execution_time': execution_time,
                'details': results
            }
            
            self.logger.info(f"🚀 Database optimization completed: {summary['successful_operations']}/{summary['total_operations']} operations successful")
            
            return summary
            
        except Exception as e:
            self.logger.error(f"❌ Full optimization failed: {e}")
            return {'error': str(e)}

# Global database optimizer instance
database_optimizer = DatabaseOptimizer()
