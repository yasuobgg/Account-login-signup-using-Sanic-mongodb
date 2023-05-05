from functools import wraps
import jwt
from sanic import Blueprint, text
from datetime import datetime, timedelta

"________________________________________________________________________"
def check_token(request):
    if not request.token:
        return False

    try:
        # jwt.decode(
        #     request.token, request.app.config.SECRET, algorithms=["HS256"]
        # )
        decoded = jwt.decode(
            request.token, request.app.config.SECRET, algorithms=["HS256"]
        )
        exp = decoded.get("exp")
        if exp and datetime.utcfromtimestamp(exp) < datetime.utcnow():
            # Token has expired
            return False
    except jwt.exceptions.InvalidTokenError:
        return False
    else:
        return True


def protected(wrapped):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            is_authenticated = check_token(request)

            if is_authenticated:
                response = await f(request, *args, **kwargs)
                return response
            else:
                return text("You are unauthorized.", 401)

        return decorated_function

    return decorator(wrapped)


"______________________________________________________________"
login = Blueprint("login", url_prefix="/jwt")


@login.post("/")
async def do_login(request):
    now = datetime.utcnow()
    expiration_time = now + timedelta(minutes=15)
    payload = {"sub": "1234567890", "exp": expiration_time}
    secret_key = request.app.config.SECRET  # "mysecretkey"
    token = jwt.encode(payload, secret_key, algorithm="HS256")

    return text(token)
