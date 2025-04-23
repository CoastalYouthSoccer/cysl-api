from fastapi import Security
from typing import Callable

from app.config import get_settings

from app.helpers.helpers import VerifyToken

config = get_settings()

auth = VerifyToken(config.auth0_domain, config.auth0_algorithms,
                   config.auth0_api_audience, config.auth0_issuer)

def verify_scopes(required_scopes: list[str]) -> Callable:
    async def _verify_scoped_user(
        token: dict = Security(auth.verify, scopes=required_scopes)
    ):
        return token
    return _verify_scoped_user
