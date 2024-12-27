import sys
# from src.logger import logging 

def error_message_detail(error, error_detail: sys):
    # Extract error details from sys.exc_info()
    exc_type, exc_value, exc_tb = error_detail  # Unpack the tuple returned by sys.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = (
        f"Error occurred in script: [{file_name}], "
        f"line number: [{exc_tb.tb_lineno}], "
        f"error message: [{str(error)}]"
    )
    return error_message


class CustomException(Exception):
    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail=error_detail)

    def __str__(self):
        return self.error_message


# if __name__ == "__main__":
#     try:
#         a = 1 / 0
    
#     except Exception as e:
#         logging.info("Divided by zero")
#         # Raise the custom exception with the exception details
#         raise CustomException("Divided by zero", sys.exc_info())
