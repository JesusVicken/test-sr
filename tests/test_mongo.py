import pytest
from unittest.mock import patch, MagicMock
from app.services.mongo_service import save_to_mongo

@patch("app.services.mongo_service.collection.insert_one")
def test_save_to_mongo(mock_insert_one):
    mock_insert_one.return_value.inserted_id = "123456"

    data = {"name": "John Doe", "email": "john@example.com"}
    mongo_id = save_to_mongo(data)

    assert mongo_id == "123456"
    mock_insert_one.assert_called_once_with({"data": data})
