# This will contain common functionalities which the whole project will be using

import os  # Module for interacting with the operating system (e.g., paths, directories)
import sys  # Provides access to system-specific parameters and functions

import pandas as pd  # Library for data manipulation and analysis
import numpy as np  # Library for numerical computations

import dill  # Library for serializing and deserializing Python objects

from src.exception import CustomException  # Custom exception class for handling errors

# Function to save a Python object to a specified file path
def save_object(file_path, obj):
    """
    Saves a Python object to the specified file path using dill.
    
    Args:
        file_path (str): Path where the object will be saved.
        obj: The Python object to save.
    
    Raises:
        CustomException: If an error occurs during the saving process.
    """
    try:
        # Ensure the directory for the file path exists
        dir_path = os.path.dirname(file_path)  # Extract the directory path
        os.makedirs(dir_path, exist_ok=True)  # Create the directory if it doesn't exist

        # Open the file in binary write mode and save the object
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)  # Serialize the object using dill

    except Exception as e:
        # Raise a custom exception if any error occurs
        raise CustomException(e, sys)
