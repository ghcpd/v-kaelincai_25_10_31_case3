"""
Optimized Implementation with Python 3.10+ Compatibility
This code addresses all compatibility issues and follows modern best practices
"""
import asyncio
import json
from collections.abc import Mapping
import time
import sys
from typing import Any


class ModernAPIClient:
    """API Client with modern asyncio patterns and compatibility fixes"""
    
    def __init__(self):
        self.results = []
    
    # Using modern async/await syntax (Python 3.5+, stable in 3.10+)
    async def fetch_data_modern(self, url: str, timeout: int) -> dict[str, Any]:
        """Modern async coroutine using async/await"""
        await asyncio.sleep(0.1)  # Simulate network delay
        return {"status": "success", "data": {"result": "sample"}}
    
    def process_list(self, items: list[int]) -> dict[str, int]:
        """Using modern built-in list type hints (Python 3.9+)"""
        # Using built-in list instead of typing.List
        total = sum(items) if items else 0
        count = len(items)
        return {"sum": total, "count": count}
    
    def merge_configs(self, config: Mapping | None, overrides: Mapping | None) -> dict[str, Any]:
        """Using collections.abc.Mapping with proper None handling"""
        # Using collections.abc.Mapping (correct import)
        # Added None handling for robustness
        merged = dict(config) if config else {}
        if overrides:
            merged.update(overrides)
        return {"merged": merged}
    
    async def run_async_tasks_modern(self, tasks: list[str]) -> int:
        """Using modern asyncio patterns with asyncio.gather"""
        # Modern pattern: using asyncio.gather for concurrent execution
        async def process_task(task_name: str) -> str:
            await asyncio.sleep(0.05)
            return task_name
        
        # Concurrent execution instead of sequential
        results = await asyncio.gather(*[process_task(task) for task in tasks])
        return len(results)
    
    async def complex_nested_operation(self, operations: list[dict[str, Any]]) -> dict[str, Any]:
        """Complex nested async with modern exception handling and validation"""
        completed = 0
        errors = []
        
        for op in operations:
            try:
                # Input validation
                if "type" not in op:
                    raise ValueError(f"Operation missing 'type' field: {op}")
                
                op_type = op["type"]
                
                if op_type == "fetch":
                    # Validate URL exists
                    if "url" not in op:
                        raise ValueError("Fetch operation requires 'url' field")
                    await asyncio.sleep(0.05)
                    completed += 1
                    
                elif op_type == "process":
                    # Validate and safely access data
                    if "data" not in op:
                        raise ValueError("Process operation requires 'data' field")
                    data = op["data"]
                    if not isinstance(data, list):
                        raise TypeError(f"Expected list, got {type(data).__name__}")
                    _ = sum(data)
                    completed += 1
                    
                elif op_type == "save":
                    # Validate path exists
                    if "path" not in op:
                        raise ValueError("Save operation requires 'path' field")
                    await asyncio.sleep(0.05)
                    completed += 1
                    
                else:
                    # Handle unknown operation types
                    raise ValueError(f"Unknown operation type: {op_type}")
                    
            except Exception as e:
                # Modern exception handling with context preservation
                error_info = {
                    "operation": op,
                    "error": str(e),
                    "type": type(e).__name__
                }
                errors.append(error_info)
                # Re-raise with context if it's critical
                if isinstance(e, (TypeError, KeyError)):
                    raise type(e)(f"Operation failed: {op.get('type', 'unknown')}") from e
        
        return {
            "success": len(errors) == 0,
            "operations_completed": completed,
            "errors": errors if errors else None
        }


async def run_test_case_async(test_case: dict[str, Any], client: ModernAPIClient) -> dict[str, Any]:
    """Execute a single test case using modern async patterns"""
    test_id = test_case["id"]
    input_data = test_case["input"]
    
    try:
        if test_id == 1:
            # Test modern async/await
            result = await client.fetch_data_modern(
                input_data["url"],
                input_data["timeout"]
            )
        elif test_id == 2:
            # Test modern list type hint
            result = client.process_list(input_data["items"])
        elif test_id == 3:
            # Test modern Mapping usage
            result = client.merge_configs(
                input_data["config"],
                input_data["overrides"]
            )
        elif test_id == 4:
            # Test modern async task execution
            result = {"completed": await client.run_async_tasks_modern(input_data["tasks"])}
        elif test_id == 5:
            # Test complex nested async
            result = await client.complex_nested_operation(input_data["operations"])
        else:
            result = {"error": "Unknown test case"}
        
        return {
            "test_id": test_id,
            "status": "passed",
            "result": result,
            "error": None
        }
    except Exception as e:
        return {
            "test_id": test_id,
            "status": "failed",
            "result": None,
            "error": str(e),
            "error_type": type(e).__name__
        }


async def main_async():
    """Main async execution function using modern patterns"""
    # Load test data
    with open("input_data.json", "r") as f:
        data = json.load(f)
    
    client = ModernAPIClient()
    results = []
    
    start_time = time.time()
    
    # Run all test cases concurrently using asyncio.gather
    print("Running test cases with modern asyncio patterns...")
    
    tasks = [run_test_case_async(test_case, client) for test_case in data["test_cases"]]
    results = await asyncio.gather(*tasks)
    
    for i, result in enumerate(results, 1):
        print(f"Test case {i}: {result['status']}")
        if result.get('error'):
            print(f"  Error: {result['error']}")
    
    end_time = time.time()
    
    # Save results
    output = {
        "total_tests": len(results),
        "passed": sum(1 for r in results if r["status"] == "passed"),
        "failed": sum(1 for r in results if r["status"] == "failed"),
        "execution_time": end_time - start_time,
        "python_version": sys.version,
        "compatibility_fixes_applied": [
            "Replaced @asyncio.coroutine with async/await",
            "Changed typing.List to built-in list",
            "Changed collections.Mapping to collections.abc.Mapping",
            "Replaced get_event_loop() with asyncio.run() and modern patterns",
            "Added proper exception context preservation",
            "Added input validation and error handling",
            "Used asyncio.gather for concurrent execution"
        ],
        "results": results
    }
    
    with open("log_optimized.txt", "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\nTotal: {output['total_tests']}, Passed: {output['passed']}, Failed: {output['failed']}")
    print(f"Execution time: {output['execution_time']:.4f}s")
    
    return output


def main():
    """Entry point using asyncio.run() (Python 3.7+)"""
    # Modern pattern: using asyncio.run() instead of get_event_loop()
    return asyncio.run(main_async())


if __name__ == "__main__":
    main()
