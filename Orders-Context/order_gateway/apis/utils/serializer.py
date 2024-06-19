from datetime import datetime, date

def serialize_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")

def serializer(obj):
    serialized_data = {}
    for key in obj:
        data = obj[key]
        if isinstance(data, datetime):
            serialized_data[key] = data.isoformat()
        elif isinstance(data, date):
            serialized_data[key] = data.isoformat()
        else:
            serialized_data[key] = data
    return serialized_data