from unittest.mock import patch, MagicMock

from adapters.ibkr.client import IBKRClient


@patch("adapters.ibkr.client.IBKRClient._start_event_loop", autospec=True)
@patch("adapters.ibkr.client.ConnectionHandler", autospec=True)
@patch("adapters.ibkr.client.create_thread", autospec=True)
def test_start_client(
    mock_create_thread, mock_connection_handler, mock_start_event_loop
):
    mock_create_thread.return_value = MagicMock()

    connection_handler_instance = mock_connection_handler.return_value

    client = IBKRClient()
    client.start_client()

    mock_create_thread.assert_called_once_with(
        connection_handler_instance.poll_client_connection,
        name="client_connection_handler",
    )
    mock_start_event_loop.assert_called_once()
