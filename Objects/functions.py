def create_transaction_description(object: object, **kwargs):
    # Capture the initial state
    initial = {
        'name': object.name,
        'description': object.description,
        'stock': object.stock,
        'group': object.group.name if object.group else None,
        'in_charge': object.in_charge.username if object.in_charge else None
    }

    # Capture the new state from kwargs
    updated = {
        'name': kwargs.get('name', initial['name']),
        'description': kwargs.get('description', initial['description']),
        'stock': kwargs.get('stock', initial['stock']),
        'group': kwargs.get('group').name if kwargs.get('group') else initial['group'],
        'in_charge': kwargs.get('in_charge').username if kwargs.get('in_charge') else initial['in_charge'],
    }

    # Create the change description
    changes = [
        f"Change in {key}, before: {initial[key]}, after: {updated[key]}"
        for key in initial.keys()
        if initial[key] != updated[key]
    ]

    return '\n'.join(changes)