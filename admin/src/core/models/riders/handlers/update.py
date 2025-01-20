def update_rider(rider, updates):
    """
    Update a rider.
    """
    for key, value in updates.items():
        setattr(rider, key, value)
    return rider


def update_academic(academic, updates):
    """
    Update a rider.
    """
    for key, value in updates.items():
        setattr(academic, key, value)
    return academic


def update_previtional_situation(previtionalSituation, updates):
    """
    Update a previtionalSituation.
    """
    for key, value in updates.items():
        setattr(previtionalSituation, key, value)
    return previtionalSituation


def update_work(work, updates):
    """
    Update a work.
    """
    for key, value in updates.items():
        setattr(work, key, value)
    return work
