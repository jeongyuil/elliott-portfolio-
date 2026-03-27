import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.safety_filter import filter_input

def test_safety():
    print("🛡️ Testing Safety Filter...")
    
    # Test Cases
    cases = [
        ("Hello world", True),
        ("You are a bad bitch", False),
        ("This is shit", False),
        ("My email is test@example.com", False),
        ("Call me at 010-1234-5678", False),
        ("I love you", True),
        ("꺼져", False)
    ]
    
    passed = 0
    for text, expected_safe in cases:
        result = filter_input(text)
        status = "✅" if result.is_safe == expected_safe else "❌"
        print(f"{status} Text: '{text}' -> Safe: {result.is_safe} ({result.reason or 'OK'})")
        if not result.is_safe:
            print(f"   Response: {result.safe_text}")
        
        if result.is_safe == expected_safe:
            passed += 1
            
    print(f"\nResult: {passed}/{len(cases)} passed")
    
if __name__ == "__main__":
    test_safety()
