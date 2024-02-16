import functools
import src.utils.exceptions as exception


def auth_required(handler):
    @functools.wraps(handler)
    async def wrapper(*args, **kwargs):
        try:
            request = kwargs["request"]
        except KeyError:
            raise exception.internalServerError(
                "Missing request parameter in route declaration"
            )

        return handler(*args, **kwargs)

    return wrapper
