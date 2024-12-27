import os  # Provides functions to interact with the operating system
import sys  # Provides access to system-specific parameters and functions
from src.logger import logging  # Custom logging module for logging messages
from src.exception import CustomException  # Custom exception class for detailed error handling
import pandas as pd  # Library for data manipulation and analysis

from sklearn.model_selection import train_test_split  # Function for splitting datasets into training and testing sets
from dataclasses import dataclass  # Decorator for creating data classes

# Configuration class for managing file paths
@dataclass
class DataInjectionConfig:
    # Paths to save train, test, and raw data
    train_data_path: str = os.path.join("artifacts", "train.csv")
    test_data_path: str = os.path.join("artifacts", "test.csv")
    raw_data_path: str = os.path.join("artifacts", "raw.csv")

# Main class for handling data injection processes
class DataInjection:
    def __init__(self):
        # Initialize the configuration object
        self.injection_config = DataInjectionConfig()
    
    def initialize_data_injection(self):
        # Log the start of the data injection process
        logging.info("Entered the data injection method/component")

        try:
            # Load the raw dataset into a Pandas DataFrame
            df = pd.read_csv(os.path.join("notebook", "data", "stud.csv"))  # Path to raw data
            logging.info("Read the dataset as dataframe")

            # Ensure the directory for saving artifacts exists
            os.makedirs(os.path.dirname(self.injection_config.train_data_path), exist_ok=True)

            # Save the raw dataset to the specified path
            df.to_csv(self.injection_config.raw_data_path, index=False, header=True)
            logging.info("Raw data saved successfully")

            # Start the train-test split process
            logging.info("Train-test split initiated")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            # Save the training dataset to a file
            train_set.to_csv(self.injection_config.train_data_path, index=False, header=True)

            # Save the testing dataset to a file
            test_set.to_csv(self.injection_config.test_data_path, index=False, header=True)
            logging.info("Train and test datasets saved successfully")

            # Log completion of the data injection process
            logging.info("Data injection completed")

            # Return paths to the train and test datasets
            return (
                self.injection_config.test_data_path,
                self.injection_config.train_data_path
            )

        except Exception as e:
            # Handle any exceptions by raising a custom exception
            raise CustomException(e, sys)

# Main execution block
if __name__ == "__main__":
    # Create an instance of the DataInjection class
    obj = DataInjection()
    # Call the method to start the data injection process
    obj.initialize_data_injection()
