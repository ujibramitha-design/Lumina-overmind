"""
Twin-Dragon Engine - Stealth Protocol Example Usage
Demonstrates advanced rate limiting, human behavior simulation, and anti-detection
"""

import asyncio
import json
from datetime import datetime

# Import stealth modules
from stealth_protocol import stealth_protocol, human_delay, stealth_operation, get_stealth_stats, change_stealth_mode, StealthMode
from proxy_rotation import add_proxy, get_next_proxy, mark_proxy_success, mark_proxy_failure, get_rotation_stats, ProxyType

async def example_stealth_operations():
    """Example of comprehensive stealth operations"""
    
    print("🥷 Twin-Dragon Stealth Protocol Example")
    print("=" * 50)
    
    # Initial stealth stats
    print("\n📊 Initial Stealth Statistics:")
    stats = get_stealth_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Test different operation types with delays
    print("\n⏱️ Testing Human Delays by Operation Type:")
    operations = ["search", "scrape", "login", "form_submit", "navigation", "content_extraction", "platform_infiltration"]
    
    for i, operation in enumerate(operations, 1):
        print(f"  {i}. {operation.replace('_', ' ').title()}")
        delay = await human_delay(operation)
        print(f"     Delay applied: {delay:.2f}s")
    
    # Test stealth operation decorator
    print("\n🎭 Testing Stealth Operation Decorator:")
    
    @stealth_operation("platform_infiltration", max_retries=3)
    async def mock_infiltration():
        """Mock infiltration operation"""
        # Simulate operation that might fail
        if random.random() < 0.3:  # 30% chance of failure
            raise Exception("Simulated infiltration failure")
        return {"status": "success", "data": "infiltrated", "timestamp": datetime.now().isoformat()}
    
    # Run stealth operation multiple times
    for i in range(3):
        try:
            result = await mock_infiltration()
            print(f"  Attempt {i+1}: ✅ Success - {result['status']}")
        except Exception as e:
            print(f"  Attempt {i+1}: ❌ Failed - {str(e)}")
    
    # Test different stealth modes
    print("\n🔄 Testing Different Stealth Modes:")
    modes = [StealthMode.CONSERVATIVE, StealthMode.BALANCED, StealthMode.AGGRESSIVE, StealthMode.STEALTH]
    
    for mode in modes:
        print(f"\n  Switching to {mode.value.upper()} mode:")
        change_stealth_mode(mode)
        
        # Test a few operations
        delays = []
        for i in range(3):
            delay = await human_delay("search")
            delays.append(delay)
        
        avg_delay = sum(delays) / len(delays)
        print(f"    Average delay: {avg_delay:.2f}s")
        print(f"    Delay range: {min(delays):.2f}s - {max(delays):.2f}s")
    
    # Final stealth stats
    print("\n📈 Final Stealth Statistics:")
    stats = get_stealth_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")

async def example_proxy_rotation():
    """Example of proxy rotation system"""
    
    print("\n🌐 Twin-Dragon Proxy Rotation Example")
    print("=" * 50)
    
    # Add example proxies
    print("\n➕ Adding Example Proxies:")
    proxies = [
        {"host": "proxy1.example.com", "port": 8080, "username": "user1", "password": "pass1", "country": "US"},
        {"host": "proxy2.example.com", "port": 8080, "username": "user2", "password": "pass2", "country": "UK"},
        {"host": "proxy3.example.com", "port": 8080, "username": "user3", "password": "pass3", "country": "DE"},
        {"host": "proxy4.example.com", "port": 1080, "username": "user4", "password": "pass4", "country": "FR"},
        {"host": "proxy5.example.com", "port": 3128, "username": "user5", "password": "pass5", "country": "JP"}
    ]
    
    for proxy_data in proxies:
        success = add_proxy(**proxy_data)
        status = "✅ Added" if success else "❌ Failed"
        print(f"  {status}: {proxy_data['host']}:{proxy_data['port']} ({proxy_data['country']})")
    
    # Test proxy selection
    print("\n🔄 Testing Proxy Selection (Round Robin):")
    for i in range(8):
        proxy = get_next_proxy()
        if proxy:
            # Simulate request with random success/failure
            if random.random() < 0.8:  # 80% success rate
                response_time = random.uniform(0.5, 3.0)
                mark_proxy_success(proxy.id, response_time)
                print(f"  Request {i+1}: ✅ {proxy.id} ({response_time:.2f}s)")
            else:
                mark_proxy_failure(proxy.id, "Connection timeout")
                print(f"  Request {i+1}: ❌ {proxy.id} (Failed)")
        else:
            print(f"  Request {i+1}: ⚠️ No proxy available")
    
    # Get rotation stats
    print("\n📊 Proxy Rotation Statistics:")
    stats = get_rotation_stats()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.2f}")
        else:
            print(f"  {key}: {value}")
    
    # Test different strategies (placeholder)
    print("\n🔄 Testing Different Rotation Strategies:")
    strategies = ["ROUND_ROBIN", "RANDOM", "LEAST_USED", "FASTEST"]
    
    for strategy in strategies:
        print(f"\n  Strategy: {strategy}")
        # Note: Strategy changes would be implemented in the actual proxy_rotator
        print(f"    (Strategy change would be implemented here)")

async def example_integrated_stealth_system():
    """Example of integrated stealth system with both protocols"""
    
    print("\n🔐 Twin-Dragon Integrated Stealth System Example")
    print("=" * 60)
    
    # Reset to balanced mode
    change_stealth_mode(StealthMode.BALANCED)
    
    # Simulate a comprehensive scraping operation
    print("\n🎯 Simulating Comprehensive Scraping Operation:")
    
    operation_steps = [
        ("Initialize session", "navigation"),
        ("Search for targets", "search"),
        ("Extract content", "content_extraction"),
        ("Process data", "default"),
        ("Submit forms", "form_submit"),
        ("Extract more content", "content_extraction"),
        ("Finalize operation", "navigation")
    ]
    
    for i, (step_name, operation_type) in enumerate(operation_steps, 1):
        print(f"\n  Step {i}: {step_name}")
        
        # Apply stealth delay
        delay = await human_delay(operation_type)
        print(f"    Stealth delay: {delay:.2f}s")
        
        # Simulate proxy selection (if available)
        proxy = get_next_proxy()
        if proxy:
            print(f"    Using proxy: {proxy.id} ({proxy.host})")
            # Simulate success
            mark_proxy_success(proxy.id, random.uniform(0.5, 2.0))
        else:
            print(f"    Using direct connection (no proxy)")
        
        # Simulate operation success/failure
        if random.random() < 0.85:  # 85% success rate
            print(f"    ✅ Operation completed successfully")
        else:
            print(f"    ⚠️ Operation completed with warnings")
    
    # Final integrated stats
    print("\n📈 Integrated System Statistics:")
    
    print("\n  Stealth Protocol:")
    stealth_stats = get_stealth_stats()
    for key, value in stealth_stats.items():
        if isinstance(value, float):
            print(f"    {key}: {value:.2f}")
        else:
            print(f"    {key}: {value}")
    
    print("\n  Proxy Rotation:")
    proxy_stats = get_rotation_stats()
    for key, value in proxy_stats.items():
        if isinstance(value, float):
            print(f"    {key}: {value:.2f}")
        else:
            print(f"    {key}: {value}")

async def main():
    """Main function to run all examples"""
    import random
    
    print("🥷 Twin-Dragon Comprehensive Stealth System Demo")
    print("=" * 70)
    
    # Run stealth protocol example
    await example_stealth_operations()
    
    # Run proxy rotation example
    await example_proxy_rotation()
    
    # Run integrated system example
    await example_integrated_stealth_system()
    
    print("\n✅ All stealth system examples completed!")
    print("\n🎯 Key Features Demonstrated:")
    print("  ✅ Human-like delays with randomization")
    print("  ✅ Context-aware delay adjustment")
    print("  ✅ Rate limiting and burst protection")
    print("  ✅ Stealth operation decorators")
    print("  ✅ Multiple stealth modes")
    print("  ✅ Proxy rotation with health monitoring")
    print("  ✅ Failure handling and retry logic")
    print("  ✅ Comprehensive statistics tracking")
    print("  ✅ Integrated anti-detection system")

if __name__ == "__main__":
    asyncio.run(main())
