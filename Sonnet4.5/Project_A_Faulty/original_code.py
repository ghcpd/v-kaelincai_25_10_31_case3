"""
Faulty Implementation with Python Compatibility Issues
This code demonstrates multiple compatibility problems across Python versions
"""
import asyncio
import json
from typing import List, Dict
from collections import Mapping
import time


class LegacyAPIClient:
    """API Client with deprecated asyncio patterns"""
    
    def __init__(self):
        self.results = []
    
    # Using deprecated @asyncio.coroutine decorator (removed in Python 3.11)
    @asyncio.coroutine
    def fetch_data_legacy(self, url: str, timeout: int):
        """Deprecated coroutine style"""
        yield from asyncio.sleep(0.1)  # Simulate network delay
        return {"status": "success", "data": {"result": "sample"}}
    
    def process_list(self, items: List[int]) -> Dict[str, int]:
        """Using deprecated typing.List instead of built-in list"""
        # This works in Python 3.7-3.8 but raises deprecation warnings in 3.9+
        total = sum(items)
        count = len(items)
        return {"sum": total, "count": count}
    
    def merge_configs(self, config: Mapping, overrides: Mapping) -> dict:
        """Using collections.Mapping (deprecated, should use collections.abc.Mapping)"""
        merged = dict(config)
        merged.update(overrides)
        return {"merged": merged}
    
    def run_async_tasks(self, tasks: List[str]) -> int:
        """Using deprecated asyncio.get_event_loop()"""
        # This pattern is deprecated in Python 3.10+ and can fail
        loop = asyncio.get_event_loop()
        
        async def process_task(task_name):
            await asyncio.sleep(0.05)
            return task_name
        
        # Old-style event loop usage
        results = []
        for task in tasks:
            result = loop.run_until_complete(process_task(task))
            results.append(result)
        
        return len(results)
    
    async def complex_nested_operation(self, operations: List[Dict]) -> Dict:
        """Complex nested async with old exception handling"""
        completed = 0
        
        for op in operations:
            try:
                if op["type"] == "fetch":
                    # Old-style exception handling without proper chaining
                    await asyncio.sleep(0.05)
                    completed += 1
                elif op["type"] == "process":
                    # Assumes data exists without validation
                    data = op["data"]
                    _ = sum(data)
                    completed += 1
                elif op["type"] == "save":
                    # No async file handling
                    await asyncio.sleep(0.05)
                    completed += 1
            except Exception as e:
                # Old-style exception handling (loses context)
                raise Exception(f"Operation failed: {op['type']}")
        
        return {"success": True, "operations_completed": completed}


def run_test_case(test_case: Dict, client: LegacyAPIClient) -> Dict:
    """Execute a single test case"""
    test_id = test_case["id"]
    input_data = test_case["input"]
    
    try:
        if test_id == 1:
            # Test async coroutine
            loop = asyncio.get_event_loop()
            result = loop.run_until_complete(
                client.fetch_data_legacy(
                    input_data["url"],
                    input_data["timeout"]
                )
            )
        elif test_id == 2:
            # Test List type hint
            result = client.process_list(input_data["items"])
        elif test_id == 3:
            # Test Mapping usage
            result = client.merge_configs(
                input_data["config"],
                input_data["overrides"]
            )
        elif test_id == 4:
            # Test event loop usage
            result = {"completed": client.run_async_tasks(input_data["tasks"])}
        elif test_id == 5:
            # Test complex nested async
            loop = asyncio.get_event_loop()
            result = loop.run_until_complete(
                client.complex_nested_operation(input_data["operations"])
            )
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
            "error": str(e)
        }


def main():
    """Main execution function"""
    # Load test data
    with open("input_data.json", "r") as f:
        data = json.load(f)
    
    client = LegacyAPIClient()
    results = []
    
    start_time = time.time()
    
    for test_case in data["test_cases"]:
        print(f"Running test case {test_case['id']}: {test_case['description']}")
        result = run_test_case(test_case, client)
        results.append(result)
        print(f"  Status: {result['status']}")
        if result['error']:
            print(f"  Error: {result['error']}")
    
    end_time = time.time()
    
    # Save results
    output = {
        "total_tests": len(results),
        "passed": sum(1 for r in results if r["status"] == "passed"),
        "failed": sum(1 for r in results if r["status"] == "failed"),
        "execution_time": end_time - start_time,
        "results": results
    }
    
    with open("log_original.txt", "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\nTotal: {output['total_tests']}, Passed: {output['passed']}, Failed: {output['failed']}")
    print(f"Execution time: {output['execution_time']:.4f}s")
    
    return output


if __name__ == "__main__":
    main()
