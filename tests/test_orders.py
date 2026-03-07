import pytest
from app import app as flask_app
import db

### ORDER TESTS ###


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client


# schema id, product_id (from product table), quantity, total_price, status
@pytest.fixture
def test_order():
    "Get new order to insert"
    return {
        "product_id": 5,
        "quantity": 3,
        "total_price": 30.00,
        "status": "Order Received",
    }


@pytest.fixture
def test_status():
    return {"status": "Order Shipped"}


def test_add_order(client, mocker, test_order):
    """Test insertion of new order to db"""
    mock_write = mocker.patch("db.write_to_db")
    mocker.patch(
        "db.read_from_db",
        return_value=[(1, 5, 3, 30.00, "Order Received")],
    )

    # ping API & check response
    response = client.post("/orders", json=test_order)
    assert response.status_code == 201

    # see if product landed in db
    assert mock_write.called


def test_change_status(client, mocker, test_status):
    """Test status update for order in db."""
    mocker.patch(
        "db.read_from_db",
        return_value=[(37, 5, 3, 30.00, "Order Received")],
    )
    mock_write = mocker.patch("db.write_to_db")

    response = client.put("/orders/37", json=test_status)
    assert response.status_code == 200

    # verify write was called with updated status
    assert mock_write.called
    call_args = mock_write.call_args
    # new status should be "Order Shipped"
    assert "Order Shipped" in call_args[0][1]


def test_get_orders(client, mocker):
    """Test retrieving all orders."""
    mock_data = [
        (1, 5, 3, 30.00, "Order Received"),
        (5, 2, 2, 28.00, "Order Shipped"),
        (6, 3, 1, 50.00, "Order Delivered"),
    ]
    mocker.patch("db.read_from_db", return_value=mock_data)

    response = client.get("/orders")
    assert response.status_code == 200

    data = response.get_json()
    assert len(data) == 3
    assert data[0]["product_id"] == 5
    assert data[2]["status"] == "Order Delivered"


def test_get_orders_db_error(client, mocker):
    """Test that db errors are handled gracefully"""
    mocker.patch("db.read_from_db", side_effect=Exception("DB connection failed"))

    response = client.get("/orders")
    assert response.status_code == 500
    assert "error" in response.get_json()
