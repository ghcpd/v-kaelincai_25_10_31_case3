import json
import pathlib
import pytest

from optimized_code import process

def load_cases():
    root = pathlib.Path(__file__).parent.parent
    data = json.loads((root / 'test_data.json').read_text())
    expanded = []
    for case in data:
        if case.get('generate_dynamic'):
            cnt = case['generate_dynamic']['count']
            template = case['generate_dynamic']['template']
            records = []
            for i in range(cnt):
                records.append({
                    'id': f'id_{i}',
                    'timestamp': template['timestamp'],
                    'payload': {'value': i}
                })
            case = dict(case)
            case['input'] = {'records': records}
        expanded.append(case)
    return expanded

TEST_CASES = load_cases()

@pytest.mark.parametrize('case', TEST_CASES, ids=[c['name'] for c in TEST_CASES])
def test_optimized(case):
    should_pass = case['should_pass_optimized']
    if should_pass:
        out = process(case['input'])
        assert out['record_count'] == case['expected_output']['record_count']
        if 'ids' in case['expected_output']:
            # expect sorted IDs
            expected_ids = sorted([str(i) for i in case['expected_output']['ids']]) if case['expected_output']['ids'] else sorted([str(r['id']) for r in case['input']['records']])
            assert out['ids'] == expected_ids
        if case['expected_output'].get('payload_digest') is not None:
            assert isinstance(out['payload_digest'], str) and len(out['payload_digest']) == 64
    else:
        with pytest.raises(Exception):
            process(case['input'])
