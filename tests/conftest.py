"""
Shared pytest fixtures for Django Testing Docs project.
"""

import os
import tempfile
import shutil
from pathlib import Path
from typing import Generator, Dict, Any
import pytest


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Provide a temporary directory that gets cleaned up after the test."""
    temp_path = Path(tempfile.mkdtemp())
    try:
        yield temp_path
    finally:
        shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def temp_file(temp_dir: Path) -> Generator[Path, None, None]:
    """Provide a temporary file within a temporary directory."""
    temp_file_path = temp_dir / "test_file.txt"
    temp_file_path.touch()
    yield temp_file_path


@pytest.fixture
def sample_rst_content() -> str:
    """Provide sample RST content for testing."""
    return """
Django Testing Documentation
============================

This is a sample RST document for testing purposes.

Basic Testing
-------------

Here's how to write a basic test:

.. code-block:: python

    def test_example():
        assert True
"""


@pytest.fixture
def sample_sphinx_config() -> Dict[str, Any]:
    """Provide sample Sphinx configuration for testing."""
    return {
        'project': 'Django Testing Docs',
        'copyright': '2009, Eric Holscher',
        'version': '0.01',
        'release': '0.01',
        'extensions': [],
        'templates_path': ['_templates'],
        'source_suffix': '.rst',
        'master_doc': 'index',
        'html_static_path': ['_static'],
    }


@pytest.fixture
def mock_sphinx_app(mocker):
    """Provide a mock Sphinx application for testing."""
    mock_app = mocker.Mock()
    mock_app.config = mocker.Mock()
    mock_app.env = mocker.Mock()
    mock_app.builder = mocker.Mock()
    return mock_app


@pytest.fixture
def sample_django_test_code() -> str:
    """Provide sample Django test code content."""
    return '''
from django.test import TestCase
from django.contrib.auth.models import User


class UserTestCase(TestCase):
    """Test case for User model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_user_creation(self):
        """Test user creation."""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpass123'))
'''


@pytest.fixture
def project_root() -> Path:
    """Provide the project root path."""
    return Path(__file__).parent.parent


@pytest.fixture
def sphinx_build_dir(temp_dir: Path) -> Path:
    """Provide a temporary Sphinx build directory."""
    build_dir = temp_dir / "_build"
    build_dir.mkdir()
    return build_dir


@pytest.fixture
def mock_file_system(mocker):
    """Provide mocks for common file system operations."""
    return {
        'open': mocker.mock_open(),
        'exists': mocker.patch('os.path.exists'),
        'isfile': mocker.patch('os.path.isfile'),
        'isdir': mocker.patch('os.path.isdir'),
        'listdir': mocker.patch('os.listdir'),
    }


@pytest.fixture
def clean_environment() -> Generator[None, None, None]:
    """Provide a clean environment by backing up and restoring env vars."""
    original_env = os.environ.copy()
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(original_env)


@pytest.fixture
def test_data_dir(project_root: Path) -> Path:
    """Provide path to test data directory."""
    return project_root / "tests" / "data"


@pytest.fixture(autouse=True)
def configure_test_settings():
    """Auto-configure test settings for all tests."""
    # Set any global test configuration here
    os.environ.setdefault('TESTING', '1')
    yield
    # Cleanup after test
    if 'TESTING' in os.environ:
        del os.environ['TESTING']


# Markers for test categorization
pytest.mark.unit = pytest.mark.unit
pytest.mark.integration = pytest.mark.integration  
pytest.mark.slow = pytest.mark.slow