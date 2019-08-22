# -*- coding: utf-8 -*-

from . import authentication

from datetime import date
from datetime import timedelta
from pyramid_nacl_session import EncryptedCookieSessionFactory
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch
from uuid import UUID

import pyramid.events
import pyramid.httpexceptions
import pyramid.testing
import unittest


class TestJWTAuthenticationPolicy(unittest.TestCase):

    def test_unauthenticated_userid(self):
        policy = authentication.JWTAuthenticationPolicy()
        request = MagicMock()
        request.jwt_claims = {"sub": "foo", "aud": ["access"]}
        userid = policy.unauthenticated_userid_from_jwt_token(request)
        self.assertEqual(userid, "foo")

    def test_unauthenticated_userid_from_jwt_token_without_jwt(self):
        policy = authentication.JWTAuthenticationPolicy()
        request = MagicMock()
        request.jwt_claims = None
        userid = policy.unauthenticated_userid_from_jwt_token(request)
        self.assertIsNone(userid)

    def test_unauthenticated_userid_from_jwt_token_without_access(self):
        policy = authentication.JWTAuthenticationPolicy()
        request = MagicMock()
        request.jwt_claims = {"sub": "foo", "aud": ["refresh"]}
        userid = policy.unauthenticated_userid_from_jwt_token(request)
        self.assertIsNone(userid)


class TestJWT(unittest.TestCase):
    @patch("jwt.decode")
    def test_get_jwt_claims(self, jwt_decode):

        request = MagicMock()
        request.registry = {}
        request.registry["jwt_public_key"] = "pub key"
        request.registry["jwt_algorithm"] = "myalgo"
        request.registry["jwt_leeway"] = timedelta(seconds=10)
        request.authorization = ("Bearer", "mytoken")

        claims = authentication.get_jwt_claims(request)
        self.assertEqual(claims, jwt_decode.return_value)

        jwt_decode.assert_called_with(
            "mytoken",
            key="pub key",
            algorithms=["myalgo"],
            leeway=timedelta(seconds=10),
            options={"verify_aud": False},
        )

    @patch("jwt.decode")
    def test_get_jwt_claims_no_pub_key(self, jwt_decode):

        request = MagicMock()
        request.registry = {}
        request.registry["jwt_public_key"] = None
        request.registry["jwt_algorithm"] = "myalgo"
        request.registry["jwt_leeway"] = timedelta(seconds=10)
        request.authorization = ("Bearer", "mytoken")

        claims = authentication.get_jwt_claims(request)
        self.assertIsNone(claims)

    @patch("jwt.encode")
    def test_generate_jwt(self, jwt_encode):
        request = MagicMock()
        request.registry = {}
        request.registry["jwt_private_key"] = "priv key"
        request.registry["jwt_algorithm"] = "myalgo"
        request.registry["jwt_leeway"] = timedelta(seconds=10)
        token = authentication.generate_jwt(request, sub="user1")
        expected_token = jwt_encode.return_value.decode()
        self.assertEqual(token, expected_token)
        jwt_encode.assert_called_with(
            {"sub": "user1"}, key="priv key", algorithm="myalgo"
        )
