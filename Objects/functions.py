def create_transaction_description(object: object, **kwargs):
    # Capture the initial state
    initial = {
        'name': object['name'],
        'description': object['description'],
        'stock': object['stock'],
        'group_id': object['group'],
        'in_charge_id': object['in_charge']
    }

    # Capture the new state from kwargs
    updated = kwargs.get('updated_data', {})

    # Create the change description
    changes = [
        f"Cambio en  {key}, antes: {initial[key]}, después: {updated[key]}"
        for key in initial.keys()
        if initial[key] != updated[key]
    ]

    return ', \n'.join(changes)