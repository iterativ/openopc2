import Pyro5.api


@Pyro5.api.expose
class TimeoutError(Exception):
    def __init__(self, txt):
        Exception.__init__(self, txt)

    __dict__ = None


@Pyro5.api.expose
class OPCError(Exception):
    def __init__(self, txt):
        Exception.__init__(self, txt)
