"""
Test suite for optimized implementation
Tests modern compatibility and robustness improvements
"""
import unittest
import json
import sys
import asyncio
from optimized_code import ModernAPIClient, run_test_case_async


class TestModernCompatibility(unittest.TestCase):
    """Test cases for modern compatibility improvements"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.client = ModernAPIClient()
        with open("input_data.json", "r") as f:
            self.test_data = json.load(f)
    
    def test_modern_async_await(self):
        """Test 1: Modern async/await syntax"""
        print(f"\nTest 1: Testing modern async/await")
        print(f"Python version: {sys.version}")
        
        async def run_test():
            test_case = self.test_data["test_cases"][0]
            result = await run_test_case_async(test_case, self.client)
            print(f"Result: {result['status']}")
            self.assertEqual(result["status"], "passed")
            return result
        
        result = asyncio.run(run_test())
        self.assertEqual(result["status"], "passed")
    
    def test_modern_type_hints(self):
        """Test 2: Modern built-in list type hints"""
        print(f"\nTest 2: Testing built-in list type hints")
        
        async def run_test():
            test_case = self.test_data["test_cases"][1]
            result = await run_test_case_async(test_case, self.client)
            print(f"Result: {result['status']}")
            self.assertEqual(result["status"], "passed")
            self.assertEqual(result["result"]["sum"], 15)
            self.assertEqual(result["result"]["count"], 5)
            return result
        
        result = asyncio.run(run_test())
        self.assertEqual(result["status"], "passed")
    
    def test_modern_collections_abc(self):
        """Test 3: Modern collections.abc.Mapping"""
        print(f"\nTest 3: Testing collections.abc.Mapping")
        
        async def run_test():
            test_case = self.test_data["test_cases"][2]
            result = await run_test_case_async(test_case, self.client)
            print(f"Result: {result['status']}")
            self.assertEqual(result["status"], "passed")
            
            merged = result["result"]["merged"]
            self.assertIn("key1", merged)
            self.assertIn("key2", merged)
            return result
        
        result = asyncio.run(run_test())
        self.assertEqual(result["status"], "passed")
    
    def test_modern_asyncio_patterns(self):
        """Test 4: Modern asyncio.gather and asyncio.run"""
        print(f"\nTest 4: Testing modern asyncio patterns")
        
        async def run_test():
            test_case = self.test_data["test_cases"][3]
            result = await run_test_case_async(test_case, self.client)
            print(f"Result: {result['status']}")
            self.assertEqual(result["status"], "passed")
            self.assertEqual(result["result"]["completed"], 3)
            return result
        
        result = asyncio.run(run_test())
        self.assertEqual(result["status"], "passed")
    
    def test_modern_exception_handling(self):
        """Test 5: Modern exception handling with context"""
        print(f"\nTest 5: Testing modern exception handling")
        
        async def run_test():
            test_case = self.test_data["test_cases"][4]
            result = await run_test_case_async(test_case, self.client)
            print(f"Result: {result['status']}")
            self.assertEqual(result["status"], "passed")
            self.assertTrue(result["result"]["success"])
            self.assertEqual(result["result"]["operations_completed"], 3)
            return result
        
        result = asyncio.run(run_test())
        self.assertEqual(result["status"], "passed")


class TestRobustnessImprovements(unittest.TestCase):
    """Test robustness and edge case handling"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.client = ModernAPIClient()
    
    def test_empty_list_handling(self):
        """Test with empty list - should handle gracefully"""
        print(f"\nRobustness Test: Empty list")
        result = self.client.process_list([])
        self.assertEqual(result["sum"], 0)
        self.assertEqual(result["count"], 0)
        print("✓ Empty list handled correctly")
    
    def test_none_input_handling(self):
        """Test with None input - should handle gracefully"""
        print(f"\nRobustness Test: None input to merge_configs")
        result = self.client.merge_configs(None, None)
        self.assertEqual(result["merged"], {})
        print("✓ None inputs handled correctly")
        
        result = self.client.merge_configs({"key": "value"}, None)
        self.assertEqual(result["merged"], {"key": "value"})
        print("✓ Partial None input handled correctly")
    
    def test_malformed_operation_validation(self):
        """Test with malformed operation - should validate and fail gracefully"""
        print(f"\nRobustness Test: Malformed operation validation")
        
        async def run_malformed():
            # Missing 'type' field
            operations = [{"bad_key": "bad_value"}]
            try:
                result = await self.client.complex_nested_operation(operations)
                print(f"Result: {result}")
                # Should have errors but not crash
                self.assertFalse(result["success"])
                self.assertIsNotNone(result["errors"])
                print("✓ Malformed operation caught and reported")
            except ValueError as e:
                print(f"✓ Validation error raised as expected: {e}")
        
        asyncio.run(run_malformed())
    
    def test_unknown_operation_type(self):
        """Test with unknown operation type"""
        print(f"\nRobustness Test: Unknown operation type")
        
        async def run_unknown():
            operations = [{"type": "unknown_operation"}]
            try:
                result = await self.client.complex_nested_operation(operations)
                print(f"Result: {result}")
                # Should report error but not crash
                self.assertFalse(result["success"])
                self.assertIsNotNone(result["errors"])
                print("✓ Unknown operation type handled gracefully")
            except ValueError as e:
                print(f"✓ Error raised for unknown operation: {e}")
        
        asyncio.run(run_unknown())
    
    def test_concurrent_execution_performance(self):
        """Test that concurrent execution is actually faster"""
        print(f"\nPerformance Test: Concurrent vs Sequential")
        
        async def sequential_test():
            tasks = [f"task_{i}" for i in range(10)]
            start = asyncio.get_event_loop().time()
            
            # Sequential execution
            for task in tasks:
                async def process():
                    await asyncio.sleep(0.01)
                await process()
            
            sequential_time = asyncio.get_event_loop().time() - start
            return sequential_time
        
        async def concurrent_test():
            tasks = [f"task_{i}" for i in range(10)]
            start = asyncio.get_event_loop().time()
            
            # Concurrent execution
            count = await self.client.run_async_tasks_modern(tasks)
            
            concurrent_time = asyncio.get_event_loop().time() - start
            return concurrent_time
        
        seq_time = asyncio.run(sequential_test())
        conc_time = asyncio.run(concurrent_test())
        
        print(f"Sequential time: {seq_time:.4f}s")
        print(f"Concurrent time: {conc_time:.4f}s")
        print(f"Speedup: {seq_time/conc_time:.2f}x")
        
        # Concurrent should be significantly faster
        self.assertLess(conc_time, seq_time * 0.5)


def run_tests():
    """Run all tests"""
    print("="*60)
    print("Running Optimized Implementation Tests")
    print(f"Python Version: {sys.version}")
    print("="*60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestModernCompatibility))
    suite.addTests(loader.loadTestsFromTestCase(TestRobustnessImprovements))
    
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
