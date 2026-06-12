# Test Suite

## 📋 Test Files Overview

This directory contains all test files for the LUMINA OS system.

### Test Files:
- `test_brochure.py` - Brochure generation system tests
- `test_commission_simple.py` - Simple commission tracking tests
- `test_commission_tracker.py` - Advanced commission tracking tests
- `test_critical_files.py` - Critical system files validation tests
- `test_final_commission.py` - Final commission workflow tests
- `test_masterpiece_brochure.py` - Premium brochure generation tests
- `test_mock_sync.py` - Data synchronization tests
- `test_senior_3d_artist_standards.py` - 3D artist quality standards tests

## 🔧 Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python tests/test_brochure.py

# Run with verbose output
python -m pytest tests/ -v
```

## 📝 Notes

- All tests use dummy data and no real API keys
- Tests are isolated from production data
- Use these tests for development and validation purposes only
