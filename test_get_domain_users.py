import pytest
from unittest.mock import MagicMock
import csv
import os
import requests
from get_domain_users import get_wordpress_users_info

# Fixture to clean up created CSV files after tests
@pytest.fixture(autouse=True)
def cleanup_files():
    """Clean up any CSV files created during tests."""
    yield
    # Teardown: remove any created csv files
    for item in os.listdir('.'):
        if item.endswith(".csv"):
            os.remove(item)

def test_single_page_of_users(mocker):
    """Test that the script correctly processes a single page of users."""
    domain = "singlepage.com"
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {}
    mock_response.json.return_value = [
        {
            "name": "Alice",
            "slug": "alice",
            "avatar_urls": {"96": "https://secure.gravatar.com/avatar/12345"},
        }
    ]

    mocker.patch('requests.get', return_value=mock_response)

    get_wordpress_users_info(domain, no_header=False)

    output_file = f"{domain}_users.csv"
    assert os.path.exists(output_file)

    with open(output_file, mode='r') as csv_file:
        reader = csv.reader(csv_file)
        rows = list(reader)
        assert rows[0] == ["Domain", "Name", "Slug", "Gravatar Hash"]
        assert rows[1] == [domain, "Alice", "alice", "12345"]
        assert len(rows) == 2

def test_multiple_pages_of_users(mocker):
    """Test that the script correctly handles pagination."""
    domain = "multipage.com"

    # Mock response for page 1
    mock_response_page1 = MagicMock()
    mock_response_page1.status_code = 200
    mock_response_page1.headers = {'link': '<https://multipage.com/wp-json/wp/v2/users?page=2&per_page=50>; rel="next"'}
    mock_response_page1.json.return_value = [
        {"name": "Bob", "slug": "bob", "avatar_urls": {"96": "https://secure.gravatar.com/avatar/abcde"}}
    ]

    # Mock response for page 2
    mock_response_page2 = MagicMock()
    mock_response_page2.status_code = 200
    mock_response_page2.headers = {}
    mock_response_page2.json.return_value = [
        {"name": "Charlie", "slug": "charlie", "avatar_urls": {"96": "https://secure.gravatar.com/avatar/f0987"}}
    ]

    # Set up the mock to return different values on subsequent calls
    mocker.patch('requests.get', side_effect=[mock_response_page1, mock_response_page2])

    get_wordpress_users_info(domain, no_header=False)

    output_file = f"{domain}_users.csv"
    assert os.path.exists(output_file)

    with open(output_file, mode='r') as csv_file:
        reader = csv.reader(csv_file)
        rows = list(reader)
        assert len(rows) == 3 # Header + 2 users
        assert rows[0] == ["Domain", "Name", "Slug", "Gravatar Hash"]
        assert rows[1] == [domain, "Bob", "bob", "abcde"]
        assert rows[2] == [domain, "Charlie", "charlie", "f0987"]

def test_api_error(mocker):
    """Test that the script handles an API error gracefully."""
    domain = "error.com"
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Client Error")

    mocker.patch('requests.get', return_value=mock_response)

    with pytest.raises(requests.exceptions.HTTPError):
        get_wordpress_users_info(domain, no_header=False)

    output_file = f"{domain}_users.csv"
    assert os.path.exists(output_file)
    with open(output_file, 'r') as f:
        # The file is created but should be empty because the request fails
        # before any data (including the header) is written.
        assert f.read() == ""

def test_no_users(mocker):
    """Test that the script handles a site with no users."""
    domain = "nousers.com"
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {}
    mock_response.json.return_value = []

    mocker.patch('requests.get', return_value=mock_response)

    get_wordpress_users_info(domain, no_header=False)

    output_file = f"{domain}_users.csv"
    assert os.path.exists(output_file)

    with open(output_file, mode='r') as csv_file:
        reader = csv.reader(csv_file)
        rows = list(reader)
        # The header should be written, but no user rows.
        assert len(rows) == 1
        assert rows[0] == ["Domain", "Name", "Slug", "Gravatar Hash"]

def test_no_header_mode(mocker):
    """Test that the script can run in no-header mode."""
    domain = "noheader.com"
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {}
    mock_response.json.return_value = [
        {
            "name": "Dave",
            "slug": "dave",
            "avatar_urls": {"96": "https://secure.gravatar.com/avatar/67890"},
        }
    ]

    mocker.patch('requests.get', return_value=mock_response)

    get_wordpress_users_info(domain, no_header=True)

    output_file = f"{domain}_users.csv"
    assert os.path.exists(output_file)

    with open(output_file, mode='r') as csv_file:
        reader = csv.reader(csv_file)
        rows = list(reader)
        assert len(rows) == 1
        assert rows[0] == [domain, "Dave", "dave", "67890"]
