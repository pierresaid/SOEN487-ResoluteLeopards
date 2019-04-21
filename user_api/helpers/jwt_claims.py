import sqlalchemy
from jwcrypto import jwt
from datetime import datetime, timedelta
import pytz


def jwt_base_claims(ttl: timedelta):
    now = datetime.now(tz=pytz.utc)
    return {
        "iss": "ResoluteLeopards",
        "exp": int((now + ttl).timestamp()),
        "iat": int(now.timestamp()),
        "ttl": ttl.total_seconds(),
    }


def jwt_claims(ttl: timedelta, **claims):
    return {
        **jwt_base_claims(ttl),
        **claims,
    }
