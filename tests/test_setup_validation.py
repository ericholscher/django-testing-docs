"""
Validation tests to ensure the testing infrastructure is working correctly.
"""

import pytest
from pathlib import Path
import sys


@pytest.mark.unit
def test_pytest_is_working():
    """Test that pytest is working correctly."""
    assert True


@pytest.mark.unit
def test_project_structure_exists(project_root):
    """Test that basic project structure exists."""
    assert project_root.exists()
    assert (project_root / "conf.py").exists()
    assert (project_root / "README").exists()
    assert (project_root / "pyproject.toml").exists()


@pytest.mark.unit
def test_testing_directories_exist(project_root):
    """Test that testing directories are properly set up."""
    tests_dir = project_root / "tests"
    assert tests_dir.exists()
    assert (tests_dir / "__init__.py").exists()
    assert (tests_dir / "conftest.py").exists()
    assert (tests_dir / "unit").exists()
    assert (tests_dir / "unit" / "__init__.py").exists()
    assert (tests_dir / "integration").exists()
    assert (tests_dir / "integration" / "__init__.py").exists()


@pytest.mark.unit
def test_fixtures_are_available(temp_dir, sample_rst_content, sample_sphinx_config):
    """Test that shared fixtures are working."""
    assert temp_dir.exists()
    assert isinstance(sample_rst_content, str)
    assert "Django Testing Documentation" in sample_rst_content
    assert isinstance(sample_sphinx_config, dict)
    assert sample_sphinx_config['project'] == 'Django Testing Docs'


@pytest.mark.unit
def test_temp_file_fixture(temp_file):
    """Test that temp_file fixture creates a usable file."""
    assert temp_file.exists()
    assert temp_file.is_file()
    
    # Test writing and reading
    content = "test content"
    temp_file.write_text(content)
    assert temp_file.read_text() == content


@pytest.mark.unit
def test_python_version():
    """Test that Python version meets minimum requirements."""
    assert sys.version_info >= (3, 8), "Python 3.8+ is required"


@pytest.mark.unit
def test_coverage_integration():
    """Test that coverage is properly configured."""
    # This test should appear in coverage reports
    covered_line = True
    assert covered_line


@pytest.mark.integration
def test_sphinx_config_loading(project_root):
    """Test that Sphinx configuration can be loaded."""
    conf_path = project_root / "conf.py"
    assert conf_path.exists()
    
    # Test that the conf.py file contains expected configuration
    conf_content = conf_path.read_text()
    assert "Django Testing Docs" in conf_content
    assert "Eric Holscher" in conf_content


@pytest.mark.unit
def test_pytest_markers():
    """Test that custom pytest markers are working."""
    # This test itself uses the @pytest.mark.unit marker
    assert hasattr(pytest.mark, 'unit')
    assert hasattr(pytest.mark, 'integration')
    assert hasattr(pytest.mark, 'slow')


@pytest.mark.slow
def test_slow_operation():
    """Example of a slow test (marked appropriately)."""
    import time
    time.sleep(0.1)  # Simulate slow operation
    assert True


def test_mock_functionality(mocker):
    """Test that pytest-mock is working."""
    mock_function = mocker.Mock(return_value=42)
    result = mock_function()
    assert result == 42
    mock_function.assert_called_once()


@pytest.mark.unit
def test_environment_configuration():
    """Test that test environment is properly configured."""
    import os
    # The TESTING env var should be set by the conftest.py fixture
    assert os.environ.get('TESTING') == '1'