# -*- coding:utf-8 -*-

from pyramid.httpexceptions import HTTPException
from pyramid.httpexceptions import HTTPFound
from pyramid.view import notfound_view_config
from urllib.parse import urljoin



@notfound_view_config(renderer="apweb.view:templates/error.pt")
def error_notfound(context, request):
    """Check for a redirect, if one is present then redirect. Otherwise contineu with error()"""
    redirect_to = request.site.get_redirect(request.path, request.query_string)

    if redirect_to is not None:
        resolved_redirect_to = urljoin(request.url, redirect_to)
        return HTTPFound(location=resolved_redirect_to)

    assert isinstance(context, HTTPException)

    if request.registry['is_debug']:
        # in debug mode we want to return the HTTPException
        # which is also a valid response object because it displays
        # some useful information regarding the 404
        return context
    else:
        request.response.status_code = context.code
        return {}
