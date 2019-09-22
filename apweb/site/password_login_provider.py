# -*- coding:utf-8 -*-

from ..login import ILoginProvider
from pyramid.authentication import extract_http_basic_credentials
from zope.interface import implementer

import logging


logger = logging.getLogger("apweb.site.password_login_provider")


@implementer(ILoginProvider)
class PasswordLoginProvider(object):
    """Provide to the login view ability to login via a password"""

    def userid_for_login_request(self, request):
        """Check the basic auth for email and password"""
        credentials = extract_http_basic_credentials(request)
        if credentials is not None:
            site = request.site
            user = site["users"].get_user_by_email(credentials.username)
            if (
                user
                and user.check_password(credentials.password)
                and user.workflow_state == "active"
            ):
                return user.user_email
            logging.warning(
                f"Unable to authenticate with password authentication: {credentials.username}"
            )
        return None
