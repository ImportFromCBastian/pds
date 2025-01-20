def convert_role_naming(permission_list):
    """
    Convert the role naming from the format "role_name" to "Role Name"
    """
    translated = []
    for permission in permission_list:
        action = permission.nombre.split("_")[-1]
        translate_action = ""
        message = ""
        icon = ""

        if action == "index":
            translate_action = "Listar"
            message = "Puedes ver todos los registros de este módulo"
            icon = "list"
        elif action == "show":
            translate_action = "Ver"
            message = "Puedes ver los detalles de un registro de este modulo"
            icon = "visibility"
        elif action == "new" or action == "create":
            translate_action = "Crear"
            message = "Puedes crear un nuevo registro de este módulo"
            icon = "add_circle"
        elif action == "update":
            translate_action = "Actualizar"
            message = "Puedes editar un registro de este módulo"
            icon = "edit"
        elif action == "destroy":
            translate_action = "Eliminar"
            message = "Puedes eliminar un registro de este módulo"
            icon = "delete"
        elif action == "files":
            translate_action = "Carga de Archivos"
            message = "Puedes subir archivos complementarios para este módulo"
            icon = "cloud_upload"

        name = permission.nombre.split("_")[0]
        translate_name = ""

        if name == "rider":
            translate_name = "Jinete & Amazona"
        elif name == "team":
            translate_name = "Equipo"
        elif name == "payment":
            translate_name = "Pago"
        elif name == "equestrian":
            translate_name = "Ecuestre"
        elif name == "user":
            translate_name = "Usuario"
        elif name == "charge":
            translate_name = "Cobros"
        elif name == "chart":
            translate_name = "Gráficos"
        elif name == "report":
            translate_name = "Reportes"
        elif name == "content":
            translate_name = "Contenido"
        elif name == "contact":
            translate_name = "Contacto"
        elif name == "provisorio":
            translate_name = "Provisorio"

        translated_dictionary = {
            "name": translate_name,
            "action": translate_action,
            "message": message,
            "icon": icon,
        }
        translated.append(translated_dictionary)

    return sorted(translated, key=lambda x: x["name"])
