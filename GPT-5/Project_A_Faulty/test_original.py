import json
import pathlib
import pytest

from original_code import process

def load_cases():
    root = pathlib.Path(__file__).parent.parent
    data = json.loads((root / 'test_data.json').read_text())
    # Expand dynamic generation for large payload case
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
            case = dict(case)  # shallow copy
            case['input'] = {'records': records}
        expanded.append(case)
    return expanded

TEST_CASES = load_cases()

@pytest.mark.parametrize('case', TEST_CASES, ids=[c['name'] for c in TEST_CASES])
def test_faulty(case):
    should_pass = case['should_pass_faulty']
    if should_pass:
        out = process(case['input'])
        assert out['record_count'] == case['expected_output']['record_count']
        if 'ids' in case['expected_output']:
            assert out['ids'] == [i.lower() for i in case['expected_output']['ids']]  # faulty expects lowercase
        if case['expected_output'].get('payload_digest') is not None:
            assert out['payload_digest'] == case['expected_output']['payload_digest']
    else:
        with pytest.raises(Exception):
            process(case['input'])
