from flask_api import status


class ResponseError(RuntimeError):
    __code = None

    def response(self):
        return {'error': str(self)}, self.__code

    # TODO:
    # def __str__(self):
    #     return

class ErrRepoNotBlamed(ResponseError):
    def __init__(self, name):
        self.__code = status.HTTP_428_PRECONDITION_REQUIRED
        super().__init__(f'repo {name} not blamed yet')


# TODO:
class ErrBlame(ResponseError):
    def __init__(self, error):
        super().__init__(str(error))


class ErrRepoExists(ResponseError):
    def __init__(self, name):
        self.__code = status.HTTP_409_CONFLICT
        super().__init__(f'repo {name} already exists')


class ErrRepoMissing(ResponseError):
    def __init__(self, name):
        self.__code = status.HTTP_404_NOT_FOUND
        super().__init__(self, f'no repo with name {name}')
