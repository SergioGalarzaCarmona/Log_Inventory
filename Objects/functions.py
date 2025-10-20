def create_transaction_description(instance, model_type):
    """Crea una descripción de los cambios entre el estado anterior y el actual."""
    if model_type == "Object":
        # Datos iniciales (de la BD)
        initial = {
            "nombre": instance._old_instance.name,
            "descripción": instance._old_instance.description,
            "stock": instance._old_instance.stock,
            "grupo": instance._old_instance.group.name,
            "encargado": str(instance._old_instance.in_charge),
        }

        # Datos actualizados (nuevos)
        updated = {
            "nombre": instance.name,
            "descripción": instance.description,
            "stock": instance.stock,
            "grupo": instance.group.name,
            "encargado": str(instance.in_charge),
        }

    elif model_type == "ObjectGroup":
        initial = {
            "nombre": instance._old_instance.name,
            "descripción": instance._old_instance.description,
            "encargado": str(instance._old_instance.in_charge),
        }

        updated = {
            "nombre": instance.name,
            "descripción": instance.description,
            "encargado": str(instance.in_charge),
        }

    # Detectar los cambios
    changes = [
        f"Cambio en {key}, antes: {initial[key]}, después: {updated[key]}"
        for key in initial.keys()
        if initial[key] != updated[key]
    ]

    return ", \n".join(changes) if changes else None
