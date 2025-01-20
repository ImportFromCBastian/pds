def update(horse, updates):
    """
    Update a horse.
    """
    for key, value in updates.items():
        if value not in [None, ""]:
            setattr(horse, key, value)
    return horse