from flask import url_for


def test_index(client):
    # When
    response = client.get(url_for('index'))

    # Then
    assert response.status_code == 200
