# -*- coding:utf-8 -*-


def includeme(config):
    config.add_view(
        None, name="password-login-form", renderer="templates/password-login-form.pt"
    )
    config.include(".admin")
    config.scan()
