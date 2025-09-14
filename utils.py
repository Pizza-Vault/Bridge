import uuid

def new_id(prefix="id_"):
    return f"{prefix}{uuid.uuid4().hex[:12]}"
