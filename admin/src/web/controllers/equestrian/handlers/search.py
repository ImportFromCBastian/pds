from src.core.models.equestrian.Horse import JyAType
from datetime import datetime

def filter_horses(horses, filters):
    """
    Filter a list of horses based on filters for horses name and JyA type.

    :param horses: List of horses
    :param filters: Dictionary with filter horses
    :return: Filtered list of horses.
    """

    def apply_filter(horse, key, value):
        """
        Apply a filter to a horse.
        """
        if key == "nombre" and value:
            return value.lower() in horse.nombre.lower()
        if key == "fecha_ingreso" and value:
            return horse.fecha_ingreso >= datetime.strptime(value, "%Y-%m-%d")
        if key == "fecha_nacimiento" and value:
            return horse.fecha_nacimiento >= datetime.strptime(value, "%Y-%m-%d")
        # Handle JyA type filter (checking enum value)
        if key == "tipo_de_JyA" and value:
            return horse.tipo_de_JyA_asignado == JyAType[value]

        return True


    # Apply the filters to the horses list
    filtered_horses = [
        horse
        for horse in horses
        if all(apply_filter(horse, key, value) for key, value in filters.items())
    ]

    return filtered_horses