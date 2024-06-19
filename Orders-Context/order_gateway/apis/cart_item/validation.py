def cart_item_create_validation(data):
    errors = {
        "is_valid_data": True,
        "errors": {}
    }
    if 'quantity' not in data or not data['quantity']:
        errors["is_valid_data"] = False
        errors["errors"]["quantity"] = "Invalid quantity"
    if 'price' not in data or not data['price']:
        errors["is_valid_data"] = False
        errors["errors"]["price"] = "Invalid price"
    if 'cost' not in data or not data['cost']:
        errors["is_valid_data"] = False
        errors["errors"]["cost"] = "Invalid cost"
    if 'cart_id' not in data or not data['cart_id']:
        errors["is_valid_data"] = False
        errors["errors"]["cart_id"] = "Invalid cart id"
    if 'product_id' not in data or not data['product_id']:
        errors["is_valid_data"] = False
        errors["errors"]["product_id"] = "Invalid product id"
    
    return errors
