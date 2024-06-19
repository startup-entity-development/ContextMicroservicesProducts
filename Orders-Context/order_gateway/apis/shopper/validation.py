def shopper_create_validation(data):
    if 'name' not in data or not data['name']:
        return False
    return True
