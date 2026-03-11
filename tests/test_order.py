import pytest
from src.modules.order import Order

statusTester = status("1d8e87M", "Sent")

def test_complOrd():
    result = statusTester.compOrd()
    assert result == True