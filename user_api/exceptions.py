class ApiError(Exception):
    def __init__(self, code, msg=""):
        # super(ApiError, self).__init__()
        self.code = code
        self.msg = msg

    def __str__(self):
        return f"[{self.code}]: \"{self.msg}\""
