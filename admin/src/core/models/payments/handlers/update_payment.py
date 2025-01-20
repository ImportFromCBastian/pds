def update(payment, updates):
    """
    Update a payment.
    """
    for key, value in updates.items():
        if value not in [None, "", 0]:
            setattr(payment, key, value)
    return payment
