# -*- coding:utf-8 -*-

from datetime import timedelta
from unittest.mock import MagicMock
from unittest.mock import patch

import apweb.authentication.jwt as apweb_jwt
import unittest


class TestJWT(unittest.TestCase):
    @patch("jwt.decode")
    def test_get_jwt_claims(self, jwt_decode):

        request = MagicMock()
        request.registry = {}
        request.registry["jwt_public_key"] = "pub key"
        request.registry["jwt_algorithm"] = "myalgo"
        request.registry["jwt_leeway"] = timedelta(seconds=10)
        request.authorization = ("Bearer", "mytoken")

        claims = apweb_jwt.get_jwt_claims(request)
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

        claims = apweb_jwt.get_jwt_claims(request)
        self.assertIsNone(claims)

    @patch("jwt.encode")
    def test_generate_jwt(self, jwt_encode):
        request = MagicMock()
        request.registry = {}
        request.registry["jwt_private_key"] = "priv key"
        request.registry["jwt_algorithm"] = "myalgo"
        request.registry["jwt_leeway"] = timedelta(seconds=10)
        token = apweb_jwt.generate_jwt(request, sub="user1")
        expected_token = jwt_encode.return_value.decode()
        self.assertEqual(token, expected_token)
        jwt_encode.assert_called_with(
            {"sub": "user1"}, key="priv key", algorithm="myalgo"
        )
