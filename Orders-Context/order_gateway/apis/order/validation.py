from apis.utils.validation import is_valid_datetime

def order_create_validation(data):
    errors = {
        "is_valid_data": True,
        "errors": {}
    }
    if 'address' not in data or not data['address']:
        errors["is_valid_data"] = False
        errors["errors"]["address"] = "Invalid address"
    if 'contact_number' not in data or not data['contact_number']:
        errors["is_valid_data"] = False
        errors["errors"]["contact_number"] = "Invalid contact number"
    if 'shopper_id' not in data or not data['shopper_id']:
        errors["is_valid_data"] = False
        errors["errors"]["shopper_id"] = "Invalid shopper id"
    if 'cart_id' not in data or not data['cart_id']:
        errors["is_valid_data"] = False
        errors["errors"]["cart_id"] = "Invalid cart id"
    if 'product_delivery_date' in data and not is_valid_datetime(data['product_delivery_date'], '%Y-%m-%d'):
        errors["is_valid_data"] = False
        errors["errors"]["product_delivery_date"] = "Invalid product delivery date"
    return errors
