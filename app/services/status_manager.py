VALID_STATUSES = [
    requested,
    approved,
    in_progress,
    completed
]

def is_valid_status(status str)
    return status in VALID_STATUSES
