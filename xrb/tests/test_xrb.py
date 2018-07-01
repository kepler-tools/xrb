import pytest
import xrb


def test_project_defines_author_and_version():
    assert hasattr(xrb, '__author__')
    assert hasattr(xrb, '__version__')
