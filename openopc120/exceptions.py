import Pyro4.core


@Pyro4.expose
class TimeoutError(Exception):
    def __init__(self, txt):
        Exception.__init__(self, txt)

    __dict__ = None


@Pyro4.expose
class OPCError(Exception):
    def __init__(self, txt):
        Exception.__init__(self, txt)