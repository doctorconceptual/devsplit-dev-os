import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pagespeed_api


def test_field_cls_is_scaled_and_not_replaced_by_good_lab_measurement():
    payload = {'http_status': 200, 'response': {
        'loadingExperience': {'id':'https://store.example/', 'metrics': {
            'CUMULATIVE_LAYOUT_SHIFT_SCORE': {'percentile':28,'category':'SLOW'}}},
        'lighthouseResult': {'audits': {'cumulative-layout-shift': {'numericValue':0.0002}}}
    }}
    result = pagespeed_api.evaluate(57, payload)
    assert result['exists'] == 'Y'
    assert '0.28' in result['evidence']
    assert 'field' in result['evidence']
    assert '0.0002' in result['evidence']


def test_field_lcp_marks_slow_page():
    payload = {'response': {
        'loadingExperience': {'metrics': {'LARGEST_CONTENTFUL_PAINT_MS': {'percentile': 4867, 'category': 'SLOW'}}},
        'lighthouseResult': {'audits': {'largest-contentful-paint': {'numericValue': 12000}}},
    }}
    result = pagespeed_api.evaluate(56, payload)
    assert result['exists'] == 'Y'
    assert '4867' in result['evidence']
    assert 'field' in result['evidence']


def test_image_weight_audit_marks_heavy_delivery():
    payload = {'response': {'lighthouseResult': {'audits': {
        'total-byte-weight': {'score': 0.5, 'numericValue': 3161165, 'displayValue': 'Total size was 3,087 KiB'},
    }}}}
    result = pagespeed_api.evaluate(58, payload)
    assert result['exists'] == 'Y'
    assert '3161165' in result['evidence']
