import pytest
from unittest.mock import Mock
from ..order_tracker import OrderTracker

# --- Fixtures for Unit Tests ---

@pytest.fixture
def mock_storage():
    """
    Provides a mock storage object for tests.
    This mock will be configured to simulate various storage behaviors.
    """
    mock = Mock()
    # By default, mock get_order to return None (no order found)
    mock.get_order.return_value = None
    # By default, mock get_all_orders to return an empty dict
    mock.get_all_orders.return_value = {}
    return mock

@pytest.fixture
def order_tracker(mock_storage):
    """
    Provides an OrderTracker instance initialized with the mock_storage.
    """
    return OrderTracker(mock_storage)

#
# --- TODO: add test functions below this line ---
#
def test_add_order_successfully(order_tracker, mock_storage):
    """Tests adding a new order with default 'pending' status."""
    order_tracker.add_order("ORD001", "Laptop", 1, "CUST001")
    
    # We expect save_order to be called once
    mock_storage.save_order.assert_called_once()

def test_get_order_by_id(order_tracker, mock_storage):
    """Tests fetching an existing order by its ID"""

    # --- Arrange ---
    fake_order = {
        "order_id": "ORD001",
        "item_name": "Laptop",
        "quantity": 1,
        "customer_id": "CUST001",
        "status": "pending"
    }

    # Configure mock storage to return this order
    mock_storage.get_order.return_value = fake_order

    # --- Act ---
    result = order_tracker.get_order_by_id("ORD001")

    # --- Assert ---
    # Verify storage was called correctly
    mock_storage.get_order.assert_called_once_with("ORD001")

    # Verify result is what storage returned
    assert result == fake_order

def test_update_order_status_successfully(order_tracker, mock_storage):
    """Tests changing an order's status from 'pending' to 'shipped'"""

    # --- Arrange ---
    fake_order = {
        "order_id": "ORD001",
        "item_name": "Laptop",
        "quantity": 1,
        "customer_id": "CUST001",
        "status": "pending"
    }

    # Storage returns existing order
    mock_storage.get_order.return_value = fake_order

    # --- Act ---
    order_tracker.update_order_status("ORD001", "shipped")

    # --- Assert ---
    # Status should be updated in the order object
    assert fake_order["status"] == "shipped"

    # Should fetch the order
    mock_storage.get_order.assert_called_once_with("ORD001")

    # Should save the updated order back to storage
    mock_storage.save_order.assert_called_once_with("ORD001", fake_order)

def test_list_all_orders_returns_all_orders(order_tracker, mock_storage):
    """Tests listing all current orders"""

    # --- Arrange ---
    fake_orders = {
        "ORD001": {
            "order_id": "ORD001",
            "item_name": "Laptop",
            "quantity": 1,
            "customer_id": "CUST001",
            "status": "pending"
        },
        "ORD002": {
            "order_id": "ORD002",
            "item_name": "Mouse",
            "quantity": 2,
            "customer_id": "CUST002",
            "status": "shipped"
        }
    }

    mock_storage.get_all_orders.return_value = fake_orders

    # --- Act ---
    result = order_tracker.list_all_orders()

    # --- Assert ---
    # Storage should be queried once
    mock_storage.get_all_orders.assert_called_once()

    # Result should be exactly what storage returns
    assert result == fake_orders

def test_list_orders_by_status_returns_only_matching_orders(order_tracker, mock_storage):
    """Tests retrieving only orders with a specific status (e.g., 'shipped')"""

    # --- Arrange ---
    fake_orders = {
        "ORD001": {
            "order_id": "ORD001",
            "item_name": "Laptop",
            "quantity": 1,
            "customer_id": "CUST001",
            "status": "pending"
        },
        "ORD002": {
            "order_id": "ORD002",
            "item_name": "Mouse",
            "quantity": 2,
            "customer_id": "CUST002",
            "status": "shipped"
        },
        "ORD003": {
            "order_id": "ORD003",
            "item_name": "Keyboard",
            "quantity": 1,
            "customer_id": "CUST003",
            "status": "shipped"
        }
    }

    mock_storage.get_all_orders.return_value = fake_orders

    # --- Act ---
    result = order_tracker.list_orders_by_status("shipped")

    # --- Assert ---
    # Should fetch all orders once
    mock_storage.get_all_orders.assert_called_once()

    # Should return only shipped orders
    expected = {
        "ORD002": fake_orders["ORD002"],
        "ORD003": fake_orders["ORD003"]
    }

    assert result == expected 
