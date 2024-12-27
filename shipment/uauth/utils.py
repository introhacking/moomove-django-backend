import secrets
import string

def generate_license_key(length=16):
    """Generate a secure random license key."""
    characters = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))