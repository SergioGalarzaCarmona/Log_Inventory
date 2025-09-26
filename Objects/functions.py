from .models import ObjectsGroup, Subprofile

def create_transaction_description(object: object,type:str, **kwargs):
    if type == 'Object':
        initial = {
            'name': object['name'],
            'description': object['description'],
            'stock': object['stock'],
            'group': ObjectsGroup.objects.get(id=object['group']).name,
            'in_charge': Subprofile.objects.get(id=object['in_charge']).__str__()
        }

        updated = kwargs.get('updated_data', {})

        updated_dict = {
            'name' : updated.get('name', initial['name']),
            'description' : updated.get('description', initial['description']),
            'stock' : updated.get('stock', initial['stock']),
            'group' : ObjectsGroup.objects.get(id=updated.get('group_id',object['group'])).name,
            'in_charge' : Subprofile.objects.get(id=updated.get('in_charge_id', object['in_charge'])).__str__()
        }
    elif type == 'ObjectsGroup':
        initial = {
            'name': object['name'],
            'description': object['description'],
            'in_charge': Subprofile.objects.get(id=object['in_charge']).__str__()
        }
        
        updated = kwargs.get('updated_data', {})
        
        updated_dict = {
            'name' : updated.get('name', initial['name']),
            'description' : updated.get('description', initial['description']),
            'in_charge' : Subprofile.objects.get(id=updated.get('in_charge_id', object['in_charge'])).__str__()
        }
        
    changes = [
        f"Cambio en  {key}, antes: {initial[key]}, después: {updated_dict[key]}"
        for key in initial.keys()
        if initial[key] != updated_dict[key]
    ]

    return ', \n'.join(changes)