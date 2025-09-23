from django.forms.models import model_to_dict

def create_transaction_description(object: object, **kwargs):
    # Capture the initial state
    initial = object

    # Capture the new state from kwargs
    updated = kwargs.get('updated_data', {})
    # Create the change description
    changes = [
        f"Cambio en  {key}, antes: {initial[key]}, después: {updated[key]}"
        for key in initial.keys()
        if initial[key] != updated[key]
    ]

    return ', \n'.join(changes)