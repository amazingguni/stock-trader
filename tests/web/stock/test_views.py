# from dataclasses import dataclass
# from unittest import mock

# from flask import url_for

# from tests.web.utils import assert_redirect_response


# @dataclass
# class MockJob:
#     id: int


# @mock.patch('tasks.stock_tasks.sync_stocks.delay')
# def test_sync(mock_delay, client):
#     mock_delay.return_value = MockJob(id=1)
#     response = client.post(url_for('stock.sync'))

#     # Then
#     assert_redirect_response(response, url_for('stock-admin.index_view'))
#     mock_delay.assert_called_with()
