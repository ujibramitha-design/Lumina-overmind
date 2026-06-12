"""
LUMINA OS Integration Checker
Verifies all module connections and imports for final orchestration

Author: HUNTER_AGENT_AI_MARKETING_DIGITAL
Version: 1.0.0
"""

import sys
import os
import importlib
import traceback
from typing import Dict, List, Tuple
from datetime import datetime

class IntegrationChecker:
    """Comprehensive integration verification system"""
    
    def __init__(self):
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'total_modules': 0,
            'successful_imports': 0,
            'failed_imports': [],
            'broken_dependencies': [],
            'missing_modules': [],
            'system_health': 'UNKNOWN'
        }
        
        # Critical modules that must be available
        self.critical_modules = {
            'core_modules': [
                'core_modules.db_manager',
                'core_modules.lead_validator', 
                'core_modules.geo_mapper',
                'core_modules.trend_analyzer',
                'lumina_os.core_modules.config'
            ],
            'agents': [
                'agents.scout_agent.market_intelligence',
                'agents.scout_agent.lead_hunter',
                'agents.scout_agent.scoring_logic',
                'agents.closer_agent.sales_consultant',
                'agents.closer_agent.follow_up_manager'
            ],
            'lumina_os': [
                'lumina_os.app',
                'lumina_os.api.endpoints.analytics',
                'lumina_os.core_modules.config'
            ],
            'governance': [
                'core_modules.governance.compliance_manager',
                'core_modules.governance.audit_logger',
                'core_modules.governance.policy_engine'
            ]
        }
        
        # Optional but recommended modules
        self.optional_modules = {
            'analytics_engine': [
                'core_modules.analytics_engine.predictive_scoring'
            ],
            'notifications': [
                'core_modules.notifications.alert_manager'
            ],
            'growth_engine': [
                'growth_engine.ad_campaign_manager',
                'growth_engine.facebook_ads',
                'growth_engine.google_ads'
            ]
        }
    
    def check_integration(self) -> Dict:
        """Run comprehensive integration check"""
        print("🔍 LUMINA OS Integration Checker")
        print("=" * 50)
        print(f"📅 Started: {self.results['timestamp']}")
        print()
        
        # Add project root to Python path
        if self.project_root not in sys.path:
            sys.path.insert(0, self.project_root)
        
        # Check critical modules
        print("🔴 CHECKING CRITICAL MODULES...")
        self._check_modules(self.critical_modules, critical=True)
        
        # Check optional modules
        print("\n🟡 CHECKING OPTIONAL MODULES...")
        self._check_modules(self.optional_modules, critical=False)
        
        # Check specific integrations
        print("\n🔗 CHECKING INTEGRATIONS...")
        self._check_specific_integrations()
        
        # Check database connectivity
        print("\n💾 CHECKING DATABASE CONNECTIVITY...")
        self._check_database_connectivity()
        
        # Check configuration
        print("\n⚙️ CHECKING CONFIGURATION...")
        self._check_configuration()
        
        # Calculate system health
        self._calculate_system_health()
        
        # Generate report
        self._generate_report()
        
        return self.results
    
    def _check_modules(self, modules_dict: Dict, critical: bool = True):
        """Check module imports"""
        for category, module_list in modules_dict.items():
            print(f"\n📁 {category.upper()}:")
            
            for module_name in module_list:
                self.results['total_modules'] += 1
                
                try:
                    # Try to import the module
                    module = importlib.import_module(module_name)
                    
                    # Check if module has required attributes
                    if self._validate_module_structure(module, module_name):
                        print(f"  ✅ {module_name} - OK")
                        self.results['successful_imports'] += 1
                    else:
                        print(f"  ⚠️ {module_name} - MISSING REQUIRED ATTRIBUTES")
                        self.results['failed_imports'].append({
                            'module': module_name,
                            'error': 'Missing required attributes',
                            'critical': critical
                        })
                        
                except ImportError as e:
                    print(f"  ❌ {module_name} - IMPORT ERROR: {str(e)}")
                    self.results['failed_imports'].append({
                        'module': module_name,
                        'error': str(e),
                        'critical': critical
                    })
                except Exception as e:
                    print(f"  ❌ {module_name} - UNEXPECTED ERROR: {str(e)}")
                    self.results['failed_imports'].append({
                        'module': module_name,
                        'error': str(e),
                        'critical': critical
                    })
    
    def _validate_module_structure(self, module, module_name: str) -> bool:
        """Validate module has required structure"""
        required_attrs = []
        
        # Define required attributes based on module type
        if 'db_manager' in module_name:
            required_attrs = ['DatabaseManager', 'db_manager']
        elif 'lead_validator' in module_name:
            required_attrs = ['validate_lead', 'gatekeeper_pipeline']
        elif 'sales_consultant' in module_name:
            required_attrs = ['SalesConsultant']
        elif 'market_intelligence' in module_name:
            required_attrs = ['MarketIntelligence']
        elif 'lead_hunter' in module_name:
            required_attrs = ['LeadHunter']
        elif 'scoring_logic' in module_name:
            required_attrs = ['LeadScoringEngine']
        elif 'compliance_manager' in module_name:
            required_attrs = ['ComplianceManager']
        elif 'audit_logger' in module_name:
            required_attrs = ['AuditLogger']
        elif 'predictive_scoring' in module_name:
            required_attrs = ['PredictiveScoringEngine']
        elif 'config' in module_name:
            required_attrs = ['config']
        elif 'app' in module_name and 'lumina_os' in module_name:
            required_attrs = ['app', 'create_app']
        
        # Check if required attributes exist
        for attr in required_attrs:
            if not hasattr(module, attr):
                return False
        
        return True
    
    def _check_specific_integrations(self):
        """Check specific integrations between modules"""
        integrations = [
            {
                'name': 'Database Manager Integration',
                'test': self._test_db_manager_integration
            },
            {
                'name': 'Sales Consultant Config Integration',
                'test': self._test_sales_consultant_config
            },
            {
                'name': 'Lead Validator Integration',
                'test': self._test_lead_validator_integration
            },
            {
                'name': 'LUMINA OS App Integration',
                'test': self._test_lumina_app_integration
            }
        ]
        
        for integration in integrations:
            try:
                integration['test']()
                print(f"  ✅ {integration['name']} - OK")
            except Exception as e:
                print(f"  ❌ {integration['name']} - FAILED: {str(e)}")
                self.results['broken_dependencies'].append({
                    'integration': integration['name'],
                    'error': str(e)
                })
    
    def _test_db_manager_integration(self):
        """Test database manager integration"""
        try:
            from core_modules.db_manager import DatabaseManager
            db = DatabaseManager()
            
            # Test basic functionality
            if not hasattr(db, 'db_path'):
                raise Exception("Database manager missing db_path attribute")
                
            # Test database connection
                        conn = # SQLite connection removed
            cursor = conn.cursor()
            # cursor.execute() removed"SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            # conn.close() removed
            
            if not tables:
                raise Exception("No tables found in database")
                
        except Exception as e:
            raise Exception(f"Database Manager integration failed: {str(e)}")
    
    def _test_sales_consultant_config(self):
        """Test sales consultant config integration"""
        try:
            from agents.closer_agent.sales_consultant import SalesConsultant
            consultant = SalesConsultant()
            
            # Test product catalog access
            if not hasattr(consultant, 'product_catalog'):
                raise Exception("Product catalog not accessible")
                
            if not consultant.product_catalog:
                raise Exception("Product catalog is empty")
                
        except Exception as e:
            raise Exception(f"Sales Consultant config integration failed: {str(e)}")
    
    def _test_lead_validator_integration(self):
        """Test lead validator integration"""
        try:
            from core_modules.lead_validator import validate_lead
            
            # Test with sample data
            sample_lead = {
                'phone': '+62812345678',
                'email': 'test@example.com',
                'name': 'Test User'
            }
            
            result = validate_lead(sample_lead)
            if not isinstance(result, dict):
                raise Exception("Invalid validation result format")
                
        except Exception as e:
            raise Exception(f"Lead Validator integration failed: {str(e)}")
    
    def _test_lumina_app_integration(self):
        """Test LUMINA OS app integration"""
        try:
            from lumina_os.app import create_app
            app = create_app()
            
            if not app:
                raise Exception("Failed to create Flask app")
                
        except Exception as e:
            raise Exception(f"LUMINA OS app integration failed: {str(e)}")
    
    def _check_database_connectivity(self):
        """Check database connectivity"""
        try:
            from core_modules.db_manager import DatabaseManager
            db = DatabaseManager()
            
            # Test database connection
            stats = db.get_database_stats()
            print(f"  ✅ Database connection - OK")
            print(f"  📊 Database stats: {stats}")
            
        except Exception as e:
            print(f"  ❌ Database connection - FAILED: {str(e)}")
            self.results['broken_dependencies'].append({
                'component': 'Database',
                'error': str(e)
            })
    
    def _check_configuration(self):
        """Check system configuration"""
        try:
            from lumina_os.core_modules.config import config
            
            # Check critical config values
            critical_configs = [
                'DATABASE_PATH',
                'PRODUCT_CATALOG',
                'DASHBOARD_PASSWORD'
            ]
            
            for config_key in critical_configs:
                if not hasattr(config, config_key):
                    raise Exception(f"Missing config: {config_key}")
            
            print(f"  ✅ Configuration - OK")
            print(f"  ⚙️ Database path: {config.DATABASE_PATH}")
            print(f"  📦 Products: {len(config.PRODUCT_CATALOG)}")
            
        except Exception as e:
            print(f"  ❌ Configuration check - FAILED: {str(e)}")
            self.results['broken_dependencies'].append({
                'component': 'Configuration',
                'error': str(e)
            })
    
    def _calculate_system_health(self):
        """Calculate overall system health"""
        critical_success = 0
        critical_total = 0
        
        for category, modules in self.critical_modules.items():
            critical_total += len(modules)
        
        # Count successful critical modules
        for failed in self.results['failed_imports']:
            if failed.get('critical', False):
                continue
            critical_success += 1
        
        critical_success = critical_total - critical_success
        
        if critical_total > 0:
            health_percentage = (critical_success / critical_total) * 100
            
            if health_percentage >= 95:
                self.results['system_health'] = 'EXCELLENT'
            elif health_percentage >= 85:
                self.results['system_health'] = 'GOOD'
            elif health_percentage >= 70:
                self.results['system_health'] = 'FAIR'
            else:
                self.results['system_health'] = 'POOR'
        else:
            self.results['system_health'] = 'UNKNOWN'
    
    def _generate_report(self):
        """Generate integration report"""
        print("\n" + "=" * 50)
        print("📊 INTEGRATION REPORT")
        print("=" * 50)
        
        print(f"📈 System Health: {self.results['system_health']}")
        print(f"📦 Total Modules: {self.results['total_modules']}")
        print(f"✅ Successful Imports: {self.results['successful_imports']}")
        print(f"❌ Failed Imports: {len(self.results['failed_imports'])}")
        print(f"🔗 Broken Dependencies: {len(self.results['broken_dependencies'])}")
        
        if self.results['failed_imports']:
            print("\n❌ FAILED IMPORTS:")
            for failed in self.results['failed_imports']:
                priority = "🔴 CRITICAL" if failed.get('critical', False) else "🟡 OPTIONAL"
                print(f"  {priority} {failed['module']}: {failed['error']}")
        
        if self.results['broken_dependencies']:
            print("\n🔗 BROKEN DEPENDENCIES:")
            for broken in self.results['broken_dependencies']:
                print(f"  ❌ {broken.get('integration', broken.get('component', 'Unknown'))}: {broken['error']}")
        
        # Save detailed report
        self._save_detailed_report()
    
    def _save_detailed_report(self):
        """Save detailed integration report to file"""
        report_path = os.path.join(self.project_root, 'logs', 'integration_report.json')
        
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        import json
        with open(report_path, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        print(f"\n📄 Detailed report saved to: {report_path}")

def main():
    """Main function to run integration check"""
    checker = IntegrationChecker()
    results = checker.check_integration()
    
    # Exit with appropriate code
    if results['system_health'] in ['EXCELLENT', 'GOOD']:
        print("\n🎉 INTEGRATION CHECK PASSED!")
        print("✅ System is ready for deployment")
        return 0
    else:
        print("\n⚠️ INTEGRATION CHECK FAILED!")
        print("❌ System needs fixes before deployment")
        return 1

if __name__ == "__main__":
    exit(main())
