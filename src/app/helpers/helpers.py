import logging

from typing import Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import SecurityScopes, HTTPAuthorizationCredentials, HTTPBearer

logger = logging.getLogger(__name__)

def set_boolean_value(value):
    if value is None:
        return False
    return value.lower() in ['true', '1', 't', 'y', 'yes']

def format_date_yyyy_mm_dd(date) -> str:
    formatted_date = None
    try:
        formatted_date = date.strftime("%Y-%m-%d")
    except Exception as e:
        logger.error(f"Failed to format date: {date}, error: {e}")
    return formatted_date


class UnauthorizedException(HTTPException):
    def __init__(self, detail: str, **kwargs):
        """Returns HTTP 403"""
        super().__init__(status.HTTP_403_FORBIDDEN, detail=detail)


class UnauthenticatedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Requires authentication"
        )


class VerifyToken:
    def __init__(self, auth0_domain, auth0_algorithms, auth0_api_audience,
                 auth0_issuer):
        self.auth0_domain = auth0_domain
        self.auth0_algorithms = auth0_algorithms
        self.auth0_api_audience = auth0_api_audience
        self.auth0_issuer = auth0_issuer

        # This gets the JWKS from a given URL and does processing so you can
        # use any of the keys available
        jwks_url = f'https://{self.auth0_domain}/.well-known/jwks.json'
        self.jwks_client = jwt.PyJWKClient(jwks_url)

    async def verify(self,
                     security_scopes: SecurityScopes,
                     token: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer())
                     ):
        if token is None:
            raise UnauthenticatedException

        # This gets the 'kid' from the passed token
        try:
            signing_key = self.jwks_client.get_signing_key_from_jwt(
                token.credentials
            ).key
        except jwt.exceptions.PyJWKClientError as error:
            raise UnauthorizedException(str(error))
        except jwt.exceptions.DecodeError as error:
            raise UnauthorizedException(str(error))

        try:
            payload = jwt.decode(
                token.credentials,
                signing_key,
                algorithms=self.auth0_algorithms,
                audience=self.auth0_api_audience,
                issuer=self.auth0_issuer,
            )
        except Exception as error:
            raise UnauthorizedException(str(error))
    
        if len(security_scopes.scopes) > 0:
            self._check_claims(payload, security_scopes.scopes)

        return payload

    def _check_claims(self, payload, scopes):
        if 'permissions' not in payload:
            raise UnauthorizedException(detail='No Permissions found in token')

        payload_claim = payload['permissions']

        for scope in scopes:
            if scope not in payload_claim:
                raise UnauthorizedException(detail=f'Missing "{scope}" scope')

def __init__(self):
        self.config = get_settings()

        # This gets the JWKS from a given URL and does processing so you can
        # use any of the keys available
        jwks_url = f'https://{self.config.auth0_domain}/.well-known/jwks.json'
        self.jwks_client = jwt.PyJWKClient(jwks_url)
