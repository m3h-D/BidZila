import uuid


def uuid_generator(request):
    a = uuid.uuid4()
    web = 'HJM'
    return f"{web}-{str(a)[:8]}"


def product_uuid_generator(request):
    a = uuid.uuid4()
    return f"{str(a)[:8]}"
