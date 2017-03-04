"""hashing-functions. Part of myBlog."""

import hmac


def hash_str(s):
    """Hash a string, for security."""
    secret = "fd4c2d860910b3a7b65c576d247292e8"  # Don't store this, use bcrypt
    return hmac.new(secret, s).hexdigest()


def make_secure_val(s):
    """Create a secure string with hash."""
    return "%s|%s" % (s, hash_str(s))


def check_secure_val(h):
    """Check a secure string with hash."""
    val = h.split('|')[0]
    if h == make_secure_val(val):
        return val
