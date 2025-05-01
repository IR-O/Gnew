def format_user_name(user):
    """Format user name for display"""
    name = user.first_name or ''
    if user.last_name:
        name += f" {user.last_name}"
    if user.username:
        name += f" (@{user.username})"
    return name.strip()