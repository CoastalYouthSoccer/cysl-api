from app.config import get_settings

from app.helpers.helpers import VerifyToken

config = get_settings()

auth = VerifyToken(config.auth0_domain, config.auth0_algorithms,
                   config.auth0_api_audience, config.auth0_issuer)
