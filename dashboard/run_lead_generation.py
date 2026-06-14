#!/usr/bin/env python3
"""
HUNTER AGENT AI MARKETING DIGITAL - Lead Generation Scraper
Automated lead generation using DuckDuckGo search and predictive scoring
"""

# Import Supabase Cloud Database Manager
try:
    from core_modules.db_manager_supabase import get_supabase_manager
    print("✅ Successfully imported Supabase Cloud Manager")
except ImportError as e:
    print(f"❌ Failed to import Supabase Manager: {e}")
    print("Make sure core_modules/db_manager_supabase.py exists")
    sys.exit(1)

# Import LeadScorer from utils
try:
    from api.utils.predictive_scoring import LeadScorer
    print("✅ Successfully imported LeadScorer")
except ImportError as e:
    print(f"❌ Failed to import LeadScorer: {e}")
    print("Make sure api/utils/predictive_scoring.py exists")
    sys.exit(1)

# Import DuckDuckGo Search
try:
    from duckduckgo_search import DDGS
    print("✅ Successfully imported DuckDuckGo Search")
except ImportError as e:
    print(f"❌ Failed to import DuckDuckGo Search: {e}")
    print("Install with: pip install duckduckgo-search")
    sys.exit(1)

# Import Shadow Network Retargeting Engine
try:
    from core_modules.growth_engine.retargeting_engine import send_lead_to_shadow_network
    print("✅ Successfully imported Shadow Network Retargeting Engine")
except ImportError as e:
    print(f"❌ Failed to import Retargeting Engine: {e}")
    print("Make sure core_modules/growth_engine/retargeting_engine.py exists")
    sys.exit(1)

# ANSI Color Codes for terminal output
class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_header(message):
    print(f"{Colors.BOLD}{Colors.CYAN}🔧 {message}{Colors.END}")

def print_hacker(message):
    """Print message with hacker aesthetic"""
    print(f"{Colors.CYAN}[{datetime.now().strftime('%H:%M:%S')}] {Colors.GREEN}{message}{Colors.END}")

def print_cloud(message):
    """Print message with cloud aesthetic"""
    print(f"{Colors.CYAN}☁️  {Colors.MAGENTA}{message}{Colors.END}")

def initialize_supabase_connection():
    """Initialize Supabase cloud database connection"""
    try:
        manager = get_supabase_manager()
        print_success("Supabase cloud database connection established")
        print_cloud("🌐 Connected to Supabase Cloud PostgreSQL")
        return manager
    except Exception as e:
        print_error(f"Supabase connection failed: {e}")
        return None

def run_scraper(query, max_results=10):
    """
    Run web scraper using DuckDuckGo search and predictive scoring
    
    Args:
        query (str): Search query for DuckDuckGo
        max_results (int): Maximum number of results to process
        
    Returns:
        dict: Statistics about the scraping session
    """
    print_hacker(f"🚀 INITIATING SCRAPER: '{query}' | Max Results: {max_results}")
    
    # Initialize scorer
    scorer = LeadScorer()
    
    # Initialize Supabase connection
    supabase_manager = initialize_supabase_connection()
    if not supabase_manager:
        return {
            'success': False,
            'error': 'Supabase connection failed',
            'total_searched': 0,
            'total_inserted': 0,
            'total_failed': 0
        }
    
    print_info(f"🔍 Searching DuckDuckGo for: '{query}'")
    
    try:
        # Search DuckDuckGo
        ddgs = DDGS()
        results = ddgs.text(query, max_results=max_results)
        
        if not results:
            print_warning("No results found for the query")
            return {
                'success': True,
                'total_searched': 0,
                'total_inserted': 0,
                'total_failed': 0,
                'query': query
            }
        
        print_hacker(f"📊 FOUND {len(results)} RESULTS FROM DUCKDUCKGO")
        
        # Statistics tracking
        stats = {
            'total_searched': len(results),
            'total_inserted': 0,
            'total_failed': 0,
            'query': query
        }
        
        print_hacker("🔄 PROCESSING RESULTS THROUGH SCORING ENGINE")
        print_cloud("📤 UPLOADING TO SUPABASE CLOUD DATABASE")
        
        # Process each result
        for i, result in enumerate(results, 1):
            try:
                # Extract data from result
                title = result.get('title', '').strip()
                body = result.get('body', '').strip()
                href = result.get('href', '').strip()
                
                if not title and not body:
                    print_warning(f"Skipping result {i}: No title or body content")
                    stats['total_failed'] += 1
                    continue
                
                # Use title as business_name, body as contact/description
                business_name = title if title else f"Lead {i}"
                contact = body if body else "No description available"
                url = href if href else f"result_{i}"
                
                print_hacker(f"🔍 PROCESSING RESULT {i}/{len(results)}: {business_name[:50]}...")
                
                # Score the lead
                scoring_result = scorer.calculate_score(
                    title=business_name,
                    description=contact,
                    source='duckduckgo_search'
                )
                
                # Prepare keywords as CSV
                keywords_csv = ','.join(scoring_result.keywords_found) if scoring_result.keywords_found else ''
                
                # Extract location from content (simple keyword matching)
                location = 'Unknown'
                location_keywords = ['jakarta', 'tangerang', 'bogor', 'depok', 'bekasi', 'bandung', 'surabaya', 'medan', 'semarang', 'yogyakarta']
                content_lower = (title + ' ' + body).lower()
                for loc in location_keywords:
                    if loc in content_lower:
                        location = loc.title()
                        break
                
                # Prepare lead data for Supabase
                lead_data = {
                    'business_name': business_name,
                    'contact': contact,
                    'url': url,
                    'keywords': keywords_csv,
                    'source': 'duckduckgo_search',
                    'score': scoring_result.score,
                    'status': scoring_result.status,
                    'location': location,
                    'date_found': datetime.now().isoformat(),
                    'created_at': datetime.now().isoformat(),
                    'updated_at': datetime.now().isoformat()
                }
                
                # Insert into Supabase cloud database
                insert_result = supabase_manager.insert_lead(lead_data)
                
                if insert_result['success']:
                    stats['total_inserted'] += 1
                    print_hacker(f"✅ UPLOADED: {business_name[:50]}... | Score: {scoring_result.score} ({scoring_result.status})")
                    print_cloud(f"📤 Cloud ID: {insert_result['data']['id']}")
                    
                    # Extract contact info for shadow network
                    email = None
                    phone = None
                    
                    # Extract email from contact/description
                    import re
                    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                    email_match = re.search(email_pattern, contact)
                    if email_match:
                        email = email_match.group(0)
                    
                    # Extract phone from contact/description
                    phone_pattern = r'(\+62|62|08)[0-9]{9,13}'
                    phone_match = re.search(phone_pattern, contact)
                    if phone_match:
                        phone = phone_match.group(0)
                    
                    # Send to shadow network asynchronously
                    if email or phone:
                        try:
                            import threading
                            
                            def send_to_shadow():
                                try:
                                    shadow_result = send_lead_to_shadow_network(
                                        email=email,
                                        phone=phone,
                                        event_name="LeadGeneration"
                                    )
                                    if shadow_result['status'] == 'success':
                                        print_hacker(f"🕸️ SHADOW INJECTION: Lead {insert_result['data']['id']} sent to Meta Pixel")
                                    else:
                                        print_warning(f"⚠️ SHADOW INJECTION FAILED: {shadow_result.get('error', 'Unknown')}")
                                except Exception as e:
                                    print_warning(f"⚠️ SHADOW NETWORK ERROR: {str(e)}")
                            
                            # Start background thread
                            shadow_thread = threading.Thread(target=send_to_shadow, daemon=True)
                            shadow_thread.start()
                            
                        except Exception as e:
                            print_warning(f"⚠️ SHADOW THREAD ERROR: {str(e)}")
                    
                else:
                    stats['total_failed'] += 1
                    print_error(f"❌ FAILED to upload: {insert_result['error']}")
                
                # Add small delay to avoid overwhelming the server
                time.sleep(0.5)
                
            except Exception as e:
                print_error(f"❌ FAILED to process result {i}: {e}")
                stats['total_failed'] += 1
                continue
        
        print_hacker(f"🎯 SCRAPING COMPLETED: {stats['total_inserted']} leads uploaded to cloud")
        print_cloud(f"📊 CLOUD SYNC: {stats['total_searched']} searched, {stats['total_inserted']} uploaded, {stats['total_failed']} failed")
        print_cloud(f"☁️  DATABASE STATUS: All leads stored in Supabase Cloud PostgreSQL")
        
        return stats
        
    except Exception as e:
        print_error(f"❌ Scraper execution failed: {e}")
        return {
            'success': False,
            'error': str(e),
            'total_searched': 0,
            'total_inserted': 0,
            'total_failed': 0,
            'query': query
        }

def run_multiple_queries():
    """Run multiple search queries and aggregate results"""
    print_header("🚀 MULTI-QUERY LEAD GENERATION")
    print("=" * 80)
    
    queries = [
        'jual rumah baru tangerang selatan',
        'promo perumahan banten',
        'jual apartemen murah jakarta',
        'beli tanah kavling bogor',
        'investasi properti cimahi',
        'jual ruko murah depok',
        'promo cluster bekasi',
        'beli apartemen bandung',
        'jual townhouse bekasi',
        'investasi tanah tangerang'
    ]
    
    total_stats = {
        'total_queries': len(queries),
        'total_searched': 0,
        'total_inserted': 0,
        'total_failed': 0,
        'queries_processed': []
    }
    
    for i, query in enumerate(queries, 1):
        print_hacker(f"🔥 QUERY {i}/{len(queries)}: '{query}'")
        
        try:
            stats = run_scraper(query, max_results=5)
            
            if stats['success']:
                total_stats['total_searched'] += stats['total_searched']
                total_stats['total_inserted'] += stats['total_inserted']
                total_stats['total_failed'] += stats['total_failed']
                total_stats['queries_processed'].append({
                    'query': query,
                    'inserted': stats['total_inserted'],
                    'failed': stats['total_failed']
                })
                
                print_hacker(f"✅ Query {i} completed: {stats['total_inserted']} inserted")
            else:
                total_stats['total_failed'] += 1
                total_stats['queries_processed'].append({
                    'query': query,
                    'error': stats.get('error', 'Unknown error'),
                    'inserted': 0,
                    'failed': 1
                })
                
                print_error(f"❌ Query {i} failed: {stats.get('error')}")
                
        except Exception as e:
            print_error(f"❌ Exception in query {i}: {e}")
            total_stats['total_failed'] += 1
            total_stats['queries_processed'].append({
                'query': query,
                'error': str(e),
                'inserted': 0,
                'failed': 1
            })
        
        # Add delay between queries to avoid rate limiting
        if i < len(queries):
            print_hacker("⏳️ WAITING 3 SECONDS BEFORE NEXT QUERY...")
            time.sleep(3)
    
    # Final summary
    print_header("🎯 MULTI-QUERY SUMMARY")
    print("=" * 80)
    print_hacker(f"📊 TOTAL QUERIES PROCESSED: {total_stats['total_queries']}")
    print_hacker(f"🔍 TOTAL RESULTS SEARCHED: {total_stats['total_searched']}")
    print_hacker(f"💾 TOTAL LEADS INSERTED: {total_stats['total_inserted']}")
    print_hacker(f"❌ TOTAL FAILURES: {total_stats['total_failed']}")
    
    print_hacker("📈 QUERY DETAILS:")
    for query_data in total_stats['queries_processed']:
        status = "✅" if query_data['inserted'] > 0 else "❌"
        print_hacker(f"  {status} {query_data['query']}: {query_data['inserted']} inserted, {query_data['failed']} failed")
    
    return total_stats

def main():
    """Main execution function"""
    print_header("🚀 HUNTER AGENT AI MARKETING DIGITAL - Lead Generation Scraper")
    print("Automated lead generation using DuckDuckGo search and predictive scoring")
    print("=" * 80)
    
    try:
        # Initialize Supabase connection
        supabase_manager = initialize_supabase_connection()
        if not supabase_manager:
            print_error("❌ Failed to connect to Supabase cloud database")
            return 1
        
        print_cloud(f"🌐 Supabase Cloud Database ready for 24/7 operation")
        
        # Test connection
        test_result = supabase_manager.test_connection()
        if test_result['success']:
            print_success("✅ Cloud database connection verified")
        else:
            print_error("❌ Cloud database connection test failed")
            return 1
        
        # Run multiple predefined queries
        return run_multiple_queries()
        
    except KeyboardInterrupt:
        print_warning("\n⚠️  Process interrupted by user")
        return 130
    except Exception as e:
        print_error(f"❌ Fatal error: {e}")
        return 1

if __name__ == '__main__':
    exit_code = main()
    if exit_code != 0:
        sys.exit(exit_code)
    else:
        print_hacker("🎉 LEAD GENERATION COMPLETED SUCCESSFULLY!")
        print_cloud("🌐 ALL LEADS STORED IN SUPABASE CLOUD DATABASE")
        print_hacker("🚀 Ready for next 24/7 autonomous scraping session...")
