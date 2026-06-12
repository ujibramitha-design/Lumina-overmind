#!/usr/bin/env python3
"""
Test Script for Predictive Scoring Utility
Tests the LeadScorer class with various scenarios and edge cases
"""

import sys
import os

# Add the api/utils directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'api', 'utils'))

try:
    from predictive_scoring import LeadScorer, ScoringResult
    print("✅ Successfully imported LeadScorer")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

# Colors for console output
class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")

def print_header(message):
    print(f"{Colors.BOLD}{Colors.CYAN}🔧 {message}{Colors.END}")

def test_basic_functionality():
    """Test basic LeadScorer functionality"""
    print_header("Testing Basic Functionality")
    print("=" * 60)
    
    try:
        # Initialize scorer
        scorer = LeadScorer()
        print_success("LeadScorer initialized successfully")
        
        # Test basic scoring
        result = scorer.calculate_score(
            title="JUAL Rumah Murah",
            description="Properti dengan harga promo dan KPR mudah",
            source="website"
        )
        
        print(f"Score: {result.score}")
        print(f"Status: {result.status}")
        print(f"Keywords Found: {result.keywords_found}")
        print(f"Breakdown: {result.breakdown}")
        
        # Validate result structure
        assert isinstance(result, ScoringResult), "Result should be ScoringResult instance"
        assert isinstance(result.score, int), "Score should be integer"
        assert isinstance(result.status, str), "Status should be string"
        assert isinstance(result.keywords_found, list), "Keywords found should be list"
        assert isinstance(result.breakdown, dict), "Breakdown should be dictionary"
        
        print_success("Basic functionality test passed")
        
    except Exception as e:
        print_error(f"Basic functionality test failed: {e}")
        return False
    
    return True

def test_hot_keywords():
    """Test hot keyword detection"""
    print_header("Testing Hot Keywords Detection")
    print("=" * 60)
    
    try:
        scorer = LeadScorer()
        
        test_cases = [
            {
                'name': 'Multiple hot keywords',
                'title': 'JUAL BELI Promo Diskon',
                'description': 'Ready stock dengan harga murah dan KPR',
                'expected_keywords': ['jual', 'beli', 'promo', 'diskon', 'ready stock', 'murah', 'kpr'],
                'min_score': 40 + (30 * 7)  # Base + 7 hot keywords
            },
            {
                'name': 'Single hot keyword',
                'title': 'Harga Terbaik',
                'description': 'Properti dengan fasilitas lengkap',
                'expected_keywords': ['harga'],
                'min_score': 40 + 30
            },
            {
                'name': 'No hot keywords',
                'title': 'Informasi Lokasi',
                'description': 'Area perumahan dengan akses jalan',
                'expected_keywords': [],
                'min_score': 40
            }
        ]
        
        for test_case in test_cases:
            result = scorer.calculate_score(
                title=test_case['title'],
                description=test_case['description']
            )
            
            print(f"\nTest: {test_case['name']}")
            print(f"Score: {result.score}")
            print(f"Expected min score: {test_case['min_score']}")
            print(f"Keywords found: {result.keywords_found}")
            print(f"Expected keywords: {test_case['expected_keywords']}")
            
            # Verify score is at minimum expected
            assert result.score >= test_case['min_score'], f"Score too low: {result.score} < {test_case['min_score']}"
            
            # Verify all expected keywords are found
            for keyword in test_case['expected_keywords']:
                assert keyword in result.keywords_found, f"Expected keyword '{keyword}' not found"
            
            print_success(f"✓ {test_case['name']} passed")
        
        print_success("Hot keywords test passed")
        
    except Exception as e:
        print_error(f"Hot keywords test failed: {e}")
        return False
    
    return True

def test_warm_keywords():
    """Test warm keyword detection"""
    print_header("Testing Warm Keywords Detection")
    print("=" * 60)
    
    try:
        scorer = LeadScorer()
        
        test_cases = [
            {
                'name': 'Multiple warm keywords',
                'title': 'Perumahan Cluster Apartemen',
                'description': 'Properti dengan lokasi strategis dan fasilitas lengkap',
                'expected_keywords': ['perumahan', 'cluster', 'apartemen', 'properti', 'lokasi', 'fasilitas'],
                'min_score': 40 + (15 * 6)  # Base + 6 warm keywords
            },
            {
                'name': 'Single warm keyword',
                'title': 'Rumah Type 36',
                'description': 'Bangunan baru dengan design modern',
                'expected_keywords': ['rumah', 'type', 'bangun'],
                'min_score': 40 + (15 * 3)
            }
        ]
        
        for test_case in test_cases:
            result = scorer.calculate_score(
                title=test_case['title'],
                description=test_case['description']
            )
            
            print(f"\nTest: {test_case['name']}")
            print(f"Score: {result.score}")
            print(f"Expected min score: {test_case['min_score']}")
            print(f"Keywords found: {result.keywords_found}")
            
            # Verify score is at minimum expected
            assert result.score >= test_case['min_score'], f"Score too low: {result.score} < {test_case['min_score']}"
            
            # Verify all expected keywords are found
            for keyword in test_case['expected_keywords']:
                assert keyword in result.keywords_found, f"Expected keyword '{keyword}' not found"
            
            print_success(f"✓ {test_case['name']} passed")
        
        print_success("Warm keywords test passed")
        
    except Exception as e:
        print_error(f"Warm keywords test failed: {e}")
        return False
    
    return True

def test_negative_keywords():
    """Test negative keyword detection"""
    print_header("Testing Negative Keywords Detection")
    print("=" * 60)
    
    try:
        scorer = LeadScorer()
        
        test_cases = [
            {
                'name': 'Single negative keyword',
                'title': 'Berita Penipuan',
                'description': 'Kasus penipuan investasi properti',
                'expected_keywords': ['berita', 'penipuan', 'kasus'],
                'max_score': 40 - (20 * 3)  # Base - 3 negative keywords
            },
            {
                'name': 'Multiple negative keywords',
                'title': 'Komplain Keluhan Buruk',
                'description': 'Pengalaman jelek dan kecewa dengan layanan',
                'expected_keywords': ['komplain', 'keluhan', 'buruk', 'jelek', 'kecewa'],
                'max_score': 40 - (20 * 5)  # Base - 5 negative keywords
            }
        ]
        
        for test_case in test_cases:
            result = scorer.calculate_score(
                title=test_case['title'],
                description=test_case['description']
            )
            
            print(f"\nTest: {test_case['name']}")
            print(f"Score: {result.score}")
            print(f"Expected max score: {test_case['max_score']}")
            print(f"Keywords found: {result.keywords_found}")
            
            # Verify score is at maximum expected
            assert result.score <= test_case['max_score'], f"Score too high: {result.score} > {test_case['max_score']}"
            
            # Verify all expected keywords are found
            for keyword in test_case['expected_keywords']:
                assert keyword in result.keywords_found, f"Expected keyword '{keyword}' not found"
            
            print_success(f"✓ {test_case['name']} passed")
        
        print_success("Negative keywords test passed")
        
    except Exception as e:
        print_error(f"Negative keywords test failed: {e}")
        return False
    
    return True

def test_status_classification():
    """Test lead status classification"""
    print_header("Testing Status Classification")
    print("=" * 60)
    
    try:
        scorer = LeadScorer()
        
        test_cases = [
            {'score': 95, 'expected_status': 'Hot'},
            {'score': 85, 'expected_status': 'Hot'},
            {'score': 80, 'expected_status': 'Hot'},
            {'score': 79, 'expected_status': 'Warm'},
            {'score': 70, 'expected_status': 'Warm'},
            {'score': 60, 'expected_status': 'Warm'},
            {'score': 59, 'expected_status': 'Cold'},
            {'score': 30, 'expected_status': 'Cold'},
            {'score': 0, 'expected_status': 'Cold'},
            {'score': 100, 'expected_status': 'Hot'}
        ]
        
        for test_case in test_cases:
            # Create a mock result with the test score
            result = scorer.calculate_score(
                title="Test",
                description="Test",
                source="test"
            )
            
            # Manually set the score for testing
            result.score = test_case['score']
            result.status = scorer._calculate_status(test_case['score'])
            
            print(f"Score: {test_case['score']} → Status: {result.status}")
            
            assert result.status == test_case['expected_status'], \
                f"Expected status '{test_case['expected_status']}' for score {test_case['score']}, got '{result.status}'"
        
        print_success("Status classification test passed")
        
    except Exception as e:
        print_error(f"Status classification test failed: {e}")
        return False
    
    return True

def test_batch_scoring():
    """Test batch scoring functionality"""
    print_header("Testing Batch Scoring")
    print("=" * 60)
    
    try:
        scorer = LeadScorer()
        
        leads = [
            {
                'title': 'JUAL CEPAT Rumah',
                'description': 'Properti dengan harga murah dan promo',
                'source': 'website'
            },
            {
                'title': 'Perumahan Cluster',
                'description': 'Lokasi strategis dengan fasilitas lengkap',
                'source': 'portal'
            },
            {
                'title': 'Berita Scam',
                'description': 'Kasus penipuan investasi palsu',
                'source': 'social'
            }
        ]
        
        results = scorer.batch_score(leads)
        
        print(f"Batch processed {len(results)} leads")
        
        for i, result in enumerate(results, 1):
            print(f"Lead {i}: Score {result.score} ({result.status})")
            
            # Verify result structure
            assert isinstance(result, ScoringResult), f"Result {i} should be ScoringResult instance"
            assert isinstance(result.score, int), f"Score {i} should be integer"
            assert isinstance(result.status, str), f"Status {i} should be string"
            assert isinstance(result.keywords_found, list), f"Keywords {i} should be list"
        
        print_success("Batch scoring test passed")
        
    except Exception as e:
        print_error(f"Batch scoring test failed: {e}")
        return False
    
    return True

def test_edge_cases():
    """Test edge cases and error handling"""
    print_header("Testing Edge Cases")
    print("=" * 60)
    
    try:
        scorer = LeadScorer()
        
        # Test empty inputs
        result = scorer.calculate_score("", "", "")
        assert result.score == 40, "Empty input should return base score"
        assert result.status == "Cold", "Empty input should return Cold status"
        print_success("✓ Empty input test passed")
        
        # Test None inputs
        result = scorer.calculate_score(None, None, None)
        assert result.score == 40, "None input should return base score"
        assert result.status == "Cold", "None input should return Cold status"
        print_success("✓ None input test passed")
        
        # Test very long text
        long_text = "jual " * 100 + "properti " * 100
        result = scorer.calculate_score(long_text, long_text, long_text)
        assert result.score <= 100, "Score should be capped at 100"
        print_success("✓ Long text test passed")
        
        # Test mixed case
        result = scorer.calculate_score("JUAL jUaL", "Properti PROPERTI", "Source SOURCE")
        assert 'jual' in result.keywords_found, "Should find keyword regardless of case"
        assert 'properti' in result.keywords_found, "Should find keyword regardless of case"
        print_success("✓ Mixed case test passed")
        
        # Test special characters
        result = scorer.calculate_score("JUAL! Rumah?", "Properti... Lokasi;", "Source[site]")
        assert 'jual' in result.keywords_found, "Should find keywords with special characters"
        print_success("✓ Special characters test passed")
        
        print_success("Edge cases test passed")
        
    except Exception as e:
        print_error(f"Edge cases test failed: {e}")
        return False
    
    return True

def test_custom_keywords():
    """Test custom keyword functionality"""
    print_header("Testing Custom Keywords")
    print("=" * 60)
    
    try:
        scorer = LeadScorer()
        
        # Test adding custom keyword
        result = scorer.add_custom_keyword('hot', 'urgent', 25)
        assert result == True, "Should successfully add custom keyword"
        print_success("✓ Custom keyword addition passed")
        
        # Test custom keyword in scoring
        result = scorer.calculate_score("URGENT Sale Available", "Urgent property", "")
        assert 'urgent' in result.keywords_found, "Should find custom keyword"
        assert result.score > 40, "Custom keyword should increase score"
        print_success("✓ Custom keyword scoring passed")
        
        # Test removing keyword
        result = scorer.remove_keyword('hot', 'urgent')
        assert result == True, "Should successfully remove custom keyword"
        print_success("✓ Custom keyword removal passed")
        
        # Test invalid category
        result = scorer.add_custom_keyword('invalid', 'test', 10)
        assert result == False, "Should reject invalid category"
        print_success("✓ Invalid category test passed")
        
        print_success("Custom keywords test passed")
        
    except Exception as e:
        print_error(f"Custom keywords test failed: {e}")
        return False
    
    return True

def test_keyword_stats():
    """Test keyword statistics functionality"""
    print_header("Testing Keyword Statistics")
    print("=" * 60)
    
    try:
        scorer = LeadScorer()
        
        stats = scorer.get_keyword_stats()
        
        # Verify structure
        assert 'hot_keywords' in stats, "Should have hot_keywords stats"
        assert 'warm_keywords' in stats, "Should have warm_keywords stats"
        assert 'negative_keywords' in stats, "Should have negative_keywords stats"
        
        # Verify hot keywords stats
        hot_stats = stats['hot_keywords']
        assert 'count' in hot_stats, "Should have count"
        assert 'score_range' in hot_stats, "Should have score_range"
        assert 'keywords' in hot_stats, "Should have keywords list"
        
        print(f"Hot Keywords: {hot_stats['count']} keywords")
        print(f"Warm Keywords: {stats['warm_keywords']['count']} keywords")
        print(f"Negative Keywords: {stats['negative_keywords']['count']} keywords")
        
        print_success("Keyword stats test passed")
        
    except Exception as e:
        print_error(f"Keyword stats test failed: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print_header("🚀 Predictive Scoring Utility Test Suite")
    print("Testing LeadScorer class with comprehensive coverage")
    print("=" * 80)
    
    tests = [
        test_basic_functionality,
        test_hot_keywords,
        test_warm_keywords,
        test_negative_keywords,
        test_status_classification,
        test_batch_scoring,
        test_edge_cases,
        test_custom_keywords,
        test_keyword_stats
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func in tests:
        if test_func():
            passed += 1
        print()
    
    print_header("🎯 Test Results")
    print("=" * 60)
    print(f"Passed: {Colors.GREEN}{passed}/{total}{Colors.END}")
    
    if passed == total:
        print_success("🎉 All tests passed! LeadScorer is working correctly.")
        print()
        print("📊 Usage Example:")
        print("from api.utils.predictive_scoring import LeadScorer")
        print()
        print("scorer = LeadScorer()")
        print("result = scorer.calculate_score(title, description, source)")
        print("print(f'Score: {result.score}')")
        print("print(f'Status: {result.status}')")
        print("print(f'Keywords: {result.keywords_found}')")
    else:
        print_error(f"❌ {total - passed} tests failed!")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
