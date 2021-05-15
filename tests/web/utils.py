from http import HTTPStatus
from urllib.parse import urlparse


def assert_redirect_response(response, expected_url):
    assert response.status_code == HTTPStatus.FOUND
    assert urlparse(response.location).path == expected_url
