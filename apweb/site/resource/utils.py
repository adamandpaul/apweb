# -*- coding:utf-8 -*-


def settings_property(name):
    """A read only settings property proxy.

    Example::
        class Obj(...):
            foo = settings_propery('foo')
    """

    @property
    def prop(self):
        return self.settings.get(name, None)

    return prop
