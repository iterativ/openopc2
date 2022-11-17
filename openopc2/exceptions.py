import Pyro5.api


@Pyro5.api.expose
class TimeoutError(Exception):
    def __init__(self, txt):
        Exception.__init__(self, txt)

    __dict__ = None


@Pyro5.api.expose
class OPCError(Exception):
    def __init__(self, message):
        super(OPCError, self).__init__(self, message)
        self.custom_message = message

    def class_to_dict(self):
        default = self.__dict__
        default["__class__"] = "exceptions.OPCError"
        return default

    @classmethod
    def dict_to_class(cls, class_name, opc_error_dict):
        opc_error_dict.pop("__class__")
        p = OPCError(opc_error_dict.get('custom_message','No message'))
        return p
