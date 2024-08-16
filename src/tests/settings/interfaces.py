from blog.settings import interfaces


class InterfaceMixin(interfaces.InterfaceMixin):
    pass


class Site(interfaces.Site):
    pass


class Shell(InterfaceMixin, interfaces.Shell):
    pass
