from app.schemas.order import Order, CostBreakdown

# constants for cost calculate 

TAX_RATE = 0.13 #13% tax rate
DELIVERY_FEE = 3.99 #flat delivery fee 

def calculate_cost(order: Order) -> CostBreakdown:
    """
    Calculates the total cost breakdown for a given order.

    Args:
        order (Order): The order to calculate costs for.

    Returns:
        CostBreakdown: Subtotal, tax, delivery fee, and total.
    """
    subtotal = round(sum(item.order_value * item.quantity for item in order.items), 2)
    tax = round(subtotal * TAX_RATE, 2)
    total = round(subtotal + tax + DELIVERY_FEE, 2)
    

    return CostBreakdown(
        order_id=order.order_id,
        subtotal=subtotal,
        tax=tax,
        delivery_fee=DELIVERY_FEE,
        total=total
    )