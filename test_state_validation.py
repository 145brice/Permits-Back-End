#!/usr/bin/env python3
"""
Test state validation to ensure Phoenix rejects Philadelphia data
"""

from scrapers.utils import validate_state, setup_logger

# Test addresses
test_cases = [
    # Philadelphia addresses (should FAIL for Phoenix)
    ("620 S BROAD ST, Philadelphia, PA", "phoenix", False),
    ("5101-21 WALNUT ST, Philadelphia, PA", "phoenix", False),
    ("4058 W GIRARD AVE, Philadelphia, PA", "phoenix", False),

    # Arizona addresses (should PASS for Phoenix)
    ("1365 Camelback Rd, Phoenix, AZ", "phoenix", True),
    ("4692 Glendale Ave, Phoenix, AZ", "phoenix", True),
    ("6305 Scottsdale Rd, Phoenix, AZ", "phoenix", True),

    # Chicago addresses (should FAIL for Houston)
    ("200 S WACKER DR, Chicago, IL", "houston", False),
    ("259 W 99TH ST, Chicago, IL", "houston", False),

    # Texas addresses (should PASS for Houston)
    ("1000 Main St, Houston, TX", "houston", True),
    ("500 Congress Ave, Austin, TX", "houston", True),
]

print("🧪 Testing State Validation\n")
print("=" * 80)

passed = 0
failed = 0

for address, scraper, should_pass in test_cases:
    result = validate_state(address, scraper, None)

    if result == should_pass:
        status = "✅ PASS"
        passed += 1
    else:
        status = "❌ FAIL"
        failed += 1

    expected = "ACCEPT" if should_pass else "REJECT"
    actual = "ACCEPTED" if result else "REJECTED"

    print(f"{status} | {scraper:10s} | {expected:6s} | {actual:8s} | {address}")

print("=" * 80)
print(f"\n📊 Results: {passed} passed, {failed} failed")

if failed == 0:
    print("🎉 All state validation tests passed!")
else:
    print(f"⚠️  {failed} test(s) failed")
