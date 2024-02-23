import pytest

from unittest.mock import patch

from ibkr_adapter.client import ConnectionHandler
from ibkr_adapter.client import IBKRClient


@pytest.fixture()
def mock_ibkr_client():
    return IBKRClient()


@patch(
    "adapters.ibkr.connection_handler.ConnectionHandler._connect_to_client",
    autospec=True,
)
def test_connect(mock_connect_to_client, mock_ibkr_client):
    connection_handler = ConnectionHandler(mock_ibkr_client)
    connection_handler.connect()
    mock_connect_to_client.assert_called_once()


@patch("adapters.ibkr.connection_handler.logger.info", autospec=True)
@patch(
    "adapters.ibkr.connection_handler.ConnectionHandler._connect_to_client",
    autospec=True,
)
def test_connect_logs_error(mock_logger, mock_connect_to_client, mock_ibkr_client):
    mock_connect_to_client.side_effect = Exception()

    connection_handler = ConnectionHandler(mock_ibkr_client)
    connection_handler.connect()

    mock_logger.assert_called_once()
