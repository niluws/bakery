from datetime import datetime, timedelta

import jwt
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed

from authentication.models import User


class AuthHandler(authentication.BaseAuthentication):
    def __init__(self):
        self.SECRET_KEY = "e850730693d632d699dedab3ced649a8badad345dae49c20ab9989622b840868"
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
        self.REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

    def encode_token(self, data, expire_minutes):
        payload = dict(iss=data)
        to_encode = payload.copy()
        to_encode.update({"exp": datetime.utcnow() + timedelta(seconds=expire_minutes)})
        return jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)

    def encode_login_token(self, data: dict):
        access_token = self.encode_token(data, self.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token = self.encode_token(data, self.REFRESH_TOKEN_EXPIRE_MINUTES)

        login_token = dict(
            access_token=f"{access_token}",
            refresh_token=f"{refresh_token}"
        )

        return login_token

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            return payload['iss']
        except jwt.ExpiredSignatureError:
            self.handle_token_error('Token has expired')
        except jwt.InvalidTokenError:
            self.handle_token_error('Token is invalid')

    def auth_refresh_wrapper(self, token):
        return self.decode_token(token)

    def get_user_from_auth_header(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header:
            return self.decode_token(auth_header)
        else:
            self.handle_token_error('No token found, please authenticate')

    def handle_token_error(self, message):
        raise AuthenticationFailed(detail=message, code=401)

    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            raise AuthenticationFailed(detail='No token found', code=401)

        try:
            user_id = self.decode_token(auth_header)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed(detail='Token has expired', code=401)
        except jwt.InvalidTokenError:
            raise AuthenticationFailed(detail='Token is invalid', code=401)

        user = self.get_user_from_email(user_id)
        if user is None:
            raise AuthenticationFailed(detail='User not found', code=401)

        return (user, None)

    def get_user_from_email(self, email):
        return User.objects.filter(email=email).first()
