import sqlalchemy
from jwcrypto import jwt
from datetime import datetime, timedelta
import pytz
from models import RefreshToken, db
from exceptions import ApiError
from uuid import uuid4
from keys import get_signing_key
from helpers.jwt_claims import jwt_claims


def refresh_token(user):
    # Check if the user has already a refresh token
    db_token = RefreshToken.query.filter_by(user_id=user.id, revoked=False).first()

    if db_token:
        if datetime.now(tz=pytz.utc) <= db_token.exp:
            return db_token
        else:
            # Token has expired
            db.session.delete(db_token)

    db_token = RefreshToken(user_id=user.id, jti=str(uuid4()), exp=datetime.now(tz=pytz.utc) + timedelta(weeks=4))
    try:
        db.session.add(db_token)
        db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        raise ApiError(500, "unable to persist refresh token")
    return db_token


def access_token(rt: RefreshToken):
    ttl = timedelta(minutes=10)
    return jwt_claims(ttl, user_id=rt.user.id, iss=rt.jti)


def create_tokens_for_user(user):
    try:
        rt = refresh_token(user)
        at_payload = access_token(rt)
        print("Access Token Payload: ", at_payload)
        token = jwt.JWT(header={"alg": "RS256", "typ": "JWT"}, claims=at_payload)
        token.make_signed_token(get_signing_key())
        return {
            "refresh_token": rt.jti,
            "access_token": token.serialize()
        }
    except:
        print("Couldn't create tokens...")


def get_fresh_token(rt: str):
    db_token = RefreshToken.query.filter_by(jti=rt, revoked=False).first()
    if not db_token:
        # Refresh token does not exist
        raise ApiError(401, "Invalid refresh token.")

    if datetime.now(tz=pytz.utc) > db_token.exp:
        # Token has expired
        try:
            db.session.delete(db_token)
            db.session.commit()
        except sqlalchemy.exc.SQLAlchemyError:
            raise ApiError(500, "Unable to delete expired refresh token.")
        raise ApiError(401, "Invalid refresh token.")

    token = jwt.JWT(header={"alg": "RS256", "typ": "JWT"}, claims=access_token(db_token))
    token.make_signed_token(get_signing_key())
    return token.serialize()
