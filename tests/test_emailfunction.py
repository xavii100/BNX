import pytest
from app import emailfunction
from app.exception import BadRequest
from unittest.mock import MagicMock, patch, mock_open
import os

def test_send():
    with patch.object(os,'popen') as mock_open:
        lines = ["hello"]
        mock_open().readlines.return_values = lines
        message = "This is a test message"
        subject = "This is a test subject"
        receiver = "test@citi.com"
        sender = ["tes1@citi.com","test2@citi.com"]
        response = emailfunction.send(message, subject, receiver, sender)
        assert response

