from datetime import datetime
import sys
from typing import Any, Dict


def dict_exception():
    """Get the traceback details of the exception."""
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback_details = {}
    if exc_type is not None:
        traceback_details = {
            "filename": exc_traceback.tb_frame.f_code.co_filename,
            "lineno": exc_traceback.tb_lineno,
            "id_name": exc_traceback.tb_frame.f_code.co_name,
            "type": exc_type.__name__,
            "message": str(exc_value),
        }
        del (exc_type, exc_value, exc_traceback)
    return traceback_details


class GeneralException(Exception):

    """GeneralException.
    Attributes:
        description: String description of the error
        class_name: String Name of the class
        function_name: String Name of the function
        code: Integer Number to identify the error with a unique code
        data_dict: Extra Data to help to identify the exception
        traceback_details:Dict[str,str], see the function: dict_exception
    """

    def __init__(
        self,
        class_name: str = None,
        function_name: str = None,
        data_dict: [str, Any] = None,
        message: str = "GeneralException",
    ):
        self.class_name: str = class_name
        self.function_name: str = function_name
        self.code: int = None
        self.traceback_details = dict_exception()
        self.message: str = f"""message: {message},
            code_exeption: {self.code},
            extra_data: {data_dict}"""
        self.data_dict: Dict[str, Any] = data_dict
        self.time: str = f'Run on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'

        super().__init__(self.message)


class InternalServerException(GeneralException):
    pass


class MisusedDecoratorException(GeneralException):
    pass


class UnauthorizedException(GeneralException):
    pass


class ForbiddenException(GeneralException):
    pass
