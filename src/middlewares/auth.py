import functools
import src.utils.exceptions as exception
from src.utils.webtokens import retrieve_access_token


def auth_required(handler):
    @functools.wraps(handler)
    async def wrapper(*args, **kwargs):
        try:
            request = kwargs["request"]
            token = request.cookies.get("access_token")

            if token is None:
                raise exception.permissionDenied()

            decoded = retrieve_access_token(token)
        except KeyError:
            raise exception.internalServerError(
                "Missing request parameter in route declaration"
            )

        return handler(*args, **kwargs)

    return wrapper
