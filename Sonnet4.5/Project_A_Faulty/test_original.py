"""
Test suite for original faulty implementation
Tests compatibility issues across Python versions
"""
import unittest
import json
import sys
import asyncio
from original_code import LegacyAPIClient, run_test_case


class TestCompatibilityIssues(unittest.TestCase):
    """Test cases for compatibility issues"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.client = LegacyAPIClient()
        with open("input_data.json", "r") as f:
            self.test_data = json.load(f)
    
    def test_deprecated_coroutine_decorator(self):
        """Test 1: Deprecated asyncio.coroutine usage"""
        print(f"\nTest 1: Testing deprecated @asyncio.coroutine decorator")
        print(f"Python version: {sys.version}")
        
        test_case = self.test_data["test_cases"][0]
        
        try:
            result = run_test_case(test_case, self.client)
            print(f"Result: {result['status']}")
            
            # This may fail in Python 3.11+ where @asyncio.coroutine is removed
            if sys.version_info >= (3, 11):
                self.assertEqual(result["status"], "failed", 
                               "Should fail in Python 3.11+ due to removed decorator")
            else:
                # May pass with deprecation warnings in 3.9-3.10
                print("Warning: Using deprecated asyncio.coroutine")
        except Exception as e:
            print(f"Exception: {e}")
            if sys.version_info >= (3, 11):
                print("Expected failure in Python 3.11+")
    
    def test_deprecated_typing_list(self):
        """Test 2: Deprecated typing.List usage"""
        print(f"\nTest 2: Testing deprecated typing.List")
        
        test_case = self.test_data["test_cases"][1]
        result = run_test_case(test_case, self.client)
        
        print(f"Result: {result['status']}")
        
        # This works but raises DeprecationWarning in Python 3.9+
        if sys.version_info >= (3, 9):
            print("Warning: typing.List is deprecated, use built-in list")
        
        self.assertEqual(result["status"], "passed")
    
    def test_deprecated_collections_mapping(self):
        """Test 3: Deprecated collections.Mapping usage"""
        print(f"\nTest 3: Testing collections.Mapping deprecation")
        
        test_case = self.test_data["test_cases"][2]
        
        try:
            result = run_test_case(test_case, self.client)
            print(f"Result: {result['status']}")
            
            # collections.Mapping removed in Python 3.10+
            if sys.version_info >= (3, 10):
                print("Error: collections.Mapping removed, should use collections.abc.Mapping")
        except Exception as e:
            print(f"Exception: {e}")
            if sys.version_info >= (3, 10):
                print("Expected failure in Python 3.10+")
    
    def test_deprecated_get_event_loop(self):
        """Test 4: Deprecated asyncio.get_event_loop() usage"""
        print(f"\nTest 4: Testing deprecated asyncio.get_event_loop()")
        
        test_case = self.test_data["test_cases"][3]
        
        try:
            result = run_test_case(test_case, self.client)
            print(f"Result: {result['status']}")
            
            # asyncio.get_event_loop() deprecated in Python 3.10+
            if sys.version_info >= (3, 10):
                print("Warning: asyncio.get_event_loop() is deprecated")
                print("Should use asyncio.new_event_loop() or asyncio.run()")
        except Exception as e:
            print(f"Exception: {e}")
    
    def test_complex_nested_async(self):
        """Test 5: Complex nested async operations"""
        print(f"\nTest 5: Testing complex nested async operations")
        
        test_case = self.test_data["test_cases"][4]
        result = run_test_case(test_case, self.client)
        
        print(f"Result: {result['status']}")
        
        # Old exception handling loses context
        if result["status"] == "passed":
            print("Warning: Old-style exception handling may lose context")


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and malformed inputs"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.client = LegacyAPIClient()
    
    def test_empty_list(self):
        """Test with empty list"""
        print(f"\nEdge Test: Empty list")
        result = self.client.process_list([])
        self.assertEqual(result["sum"], 0)
        self.assertEqual(result["count"], 0)
    
    def test_none_input(self):
        """Test with None input"""
        print(f"\nEdge Test: None input to merge_configs")
        try:
            result = self.client.merge_configs(None, {})
            print(f"Unexpectedly passed with result: {result}")
        except Exception as e:
            print(f"Failed as expected: {e}")
    
    def test_malformed_operation(self):
        """Test with malformed operation data"""
        print(f"\nEdge Test: Malformed operation")
        
        async def run_malformed():
            operations = [{"type": "unknown", "bad_key": "bad_value"}]
            try:
                result = await self.client.complex_nested_operation(operations)
                print(f"Result: {result}")
            except Exception as e:
                print(f"Failed as expected: {e}")
        
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(run_malformed())
        except Exception as e:
            print(f"Exception: {e}")


def run_tests():
    """Run all tests"""
    print("="*60)
    print("Running Original Implementation Tests")
    print(f"Python Version: {sys.version}")
    print("="*60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestCompatibilityIssues))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    return result


if __name__ == "__main__":
    run_tests()
