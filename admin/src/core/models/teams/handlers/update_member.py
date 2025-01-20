def update(team_member, updates):
    """
    Update a team member.
    """
    for key, value in updates.items():
        if value not in [None, ""]:
            setattr(team_member, key, value)
    return team_member
