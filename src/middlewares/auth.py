from typing import Optional
import functools
import src.utils.exceptions as exception

import src.models as models
from src.utils.webtokens import retrieve_access_token


# use auth_required() or @auth_required(roles=["some_role"])
def auth_required(roles: list[str] = None, *args, **kwargs):
    def _auth_required(handler):
        @functools.wraps(handler)
        async def wrapper(*args, **kwargs):
            try:
                request = kwargs["request"]
                token = request.cookies.get("access_token")

                if token is None:
                    raise exception.permissionDenied()

                data = retrieve_access_token(token)
                if roles is not None:
                    database = kwargs["db"]
                    user = (
                        database.query(models.Users)
                        .filter(models.Users.id == data["id"])
                        .first()
                    )

                    if user is None:
                        raise exception.permissionDenied()

                    has_role = False
                    for role in user.roles:
                        if role.name in roles:
                            has_role = True

                    if not has_role:
                        raise exception.permissionDenied()

            except KeyError:
                raise exception.internalServerError(
                    "Missing request|db parameter in route declaration"
                )

            return await handler(*args, **kwargs)

        return wrapper

    return _auth_required
