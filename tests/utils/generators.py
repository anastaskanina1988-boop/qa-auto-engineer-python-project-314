import uuid


def unique_email():
    return f"{uuid.uuid4().hex[:8]}@example.com"


def unique_label_name(prefix="Label"):
    return f"{prefix} {uuid.uuid4().hex[:6]}"


def unique_status(prefix="Status"):
    suffix = uuid.uuid4().hex[:6]
    return f"{prefix} {suffix}", f"status_{suffix}"


def unique_task_title(prefix="Task"):
    return f"{prefix} {uuid.uuid4().hex[:6]}"
