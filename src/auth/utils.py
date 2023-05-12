from datetime import timedelta, datetime
from typing import Any
from uuid import UUID

import jwt
from fastapi import Request, HTTPException, status

from src.core.settings import settings


ACCESS_LIFETIME = timedelta(minutes=settings.auth.access_lifetime)
REFRESH_LIFETIME = timedelta(minutes=settings.auth.refresh_lifetime)
SECRET_KEY = settings.auth.jwt_secret_key
ALGORITHM = settings.auth.jwt_algorithm
AUTH_MODEL = 'Bearer'

InvalidTokenException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='Invalid token',
)


async def parse_jwt(jwt_token):
    decoded_token = jwt.decode(
        jwt=jwt_token,
        key=SECRET_KEY,
        algorithms=ALGORITHM,
        options={
            "verify_exp": True,
            "verify_signature": True,
        },
    )

    return decoded_token


async def fetch_client_id_from_jwt(request: Request):
    if not request.headers.get("authorization"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    jwt_token = request.headers["authorization"]

    type_of_token, token_body = jwt_token.split()

    if not type_of_token == AUTH_MODEL:
        raise InvalidTokenException

    try:

        payload = await parse_jwt(token_body)

    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            'Token has expired',
        )
    except (
        jwt.exceptions.InvalidSignatureError,
        jwt.exceptions.DecodeError,
    ):
        raise InvalidTokenException

    client_id = payload.get('client_id')
    if not client_id:
        raise InvalidTokenException

    return client_id


def generate_jwt(payload: dict[str, Any]):
    return jwt.encode(
        payload=payload,
        key=SECRET_KEY,
        algorithm=ALGORITHM,
    )


def _get_token_payload(
        client_id: str,
        lifetime: timedelta = ACCESS_LIFETIME,
):
    return {
        'client_id': client_id,
        'exp': datetime.utcnow() + lifetime,
    }



def generate_pair_jwt(client_id: str):
    if isinstance(client_id, UUID):
        client_id = str(client_id)

    refresh_payload = _get_token_payload(client_id, lifetime=REFRESH_LIFETIME)
    access_payload = _get_token_payload(client_id)
    return [
        generate_jwt(payload)
        for payload
        in (access_payload, refresh_payload)
    ]
