"""hashing-functions. Part of myBlog."""

from lib.pybcrypt import bcrypt  # This is slow, one should use regular bcrypt.


def hash_str(s):
    """Hash a string, for security."""
    return bcrypt.hashpw(s, bcrypt.gensalt())


def make_secure_val(s):
    """Create a secure string with hash."""
    return "%s|%s" % (s, hash_str(s))


def check_secure_val(h):
    """Check a secure string with hash."""
    val, hashed = h.split('|')
    try:
        if bcrypt.hashpw(val, hashed) == hashed:
            return val
    except ValueError:
        return None
