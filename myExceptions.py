"""Exceptions used in myBlog."""


class NotUnique(Exception):
    """Value is not unique exception."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class VoteOnOwnPostNotAllowed(Exception):
    """Not allowed to vote on their own posts."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class EditOthersPosts(Exception):
    """Not allowed to edit others posts."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class EditOthersComments(Exception):
    """Not allowed to edit others posts."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class TooShort(Exception):
    """Field is too short."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
