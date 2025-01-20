from enum import Enum
from src.core.models.teams.employee import PositionType
from math import ceil


def filter_team_members(team_members, filters, page=1, per_page=5):
    """
    Filter a list of team members based on a dictionary of filters.

    :param team_members: List of team members
    :param filters: Dictionary with filter parameters
    :return: Filtered list of team members.
    """

    def apply_filter(member, key, value):
        """
        Apply a single filter to a team member.
        Handles partial matching for strings and exact matching for other types.
        """

        if not hasattr(member, key):
            return True

        member_value = getattr(member, key, None)

        if value == "" or value is None or value == "Elige una opción...":
            return True

        if key == "puesto_laboral":
            try:
                enum_value = PositionType[value]
                return member_value == enum_value
            except KeyError:
                return False

        if member_value is None:
            return value is None

        if isinstance(member_value, str) and isinstance(value, str):
            return value.lower() in member_value.lower()

        elif isinstance(member_value, (int, float)) and isinstance(value, (int, float)):
            return member_value == value

        return False

    for key in filters:
        if filters[key].isdigit():
            filters[key] = int(filters[key])

    filtered_members = [
        member
        for member in team_members
        if all(apply_filter(member, key, value) for key, value in filters.items())
    ]

    total_items = len(filtered_members)
    total_pages = ceil(total_items / per_page)
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    paginated_members = filtered_members[start_index:end_index]

    pagination_metadata = {
        "pages": page,
        "per_page": per_page,
        "total_items": total_items,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1,
        "next_num": page + 1 if page < total_pages else None,
        "prev_num": page - 1 if page > 1 else None,
        "item": len(paginated_members),
    }

    return {
        "members": paginated_members,
        "pagination": pagination_metadata,
    }
