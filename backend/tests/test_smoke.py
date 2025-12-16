"""Smoke tests to verify test infrastructure"""


def test_framework_works():
    """Verify pytest is working"""
    assert 1 + 1 == 2


def test_imports():
    """Verify basic imports work"""
    import sys
    assert sys.version_info >= (3, 8)
