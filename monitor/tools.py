from django.shortcuts import redirect


def login_required(func):
    """Check if user is logged decorator"""
    def wrapper(*args, **kw):
        if args[0].session.get('logged_in', False) and args[0].session.get('username', ""):
            if kw:
                return func(args[0], kw)
            else:
                return func(args[0])
        else:
            return redirect("login")
    return wrapper

