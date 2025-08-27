from supt_dashboard.dashboard import stress, get_dashboard_html
import numpy as np

def test_stress_symmetry():
    assert np.isclose(stress(0.3), stress(0.7), atol=1e-6)

def test_stress_saturation():
    assert np.isclose(stress(0.0), -1.0, atol=1e-6)
    assert np.isclose(stress(1.0), -1.0, atol=1e-6)

def test_dashboard_html_contains_traces():
    html = get_dashboard_html()
    assert "ΔΦ Drift" in html
    assert "Stress k(ΔΦ)" in html
    assert "ZFCM Threshold" in html
