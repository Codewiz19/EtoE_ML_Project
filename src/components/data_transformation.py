import sys
from dataclasses import dataclass

import numpy as np 
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException  # Custom exception class for meaningful error handling
from src.logger import logging  # Logger for tracking events and debugging
import os

from src.utils import save_object  # Utility to save objects like the preprocessor

# Configuration for the data transformation process
@dataclass
class DataTransformationConfig:
    # Path where the preprocessor object will be saved
    preprocessor_obj_file_path = os.path.join('artifacts', "proprocessor.pkl")


class DataTransformation:
    # Initialize the configuration for the data transformation
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        '''
        Creates and returns a preprocessor object to handle 
        numerical and categorical data transformations.
        '''
        try:
            # Columns to be treated as numerical
            numerical_columns = ["writing_score", "reading_score"]
            # Columns to be treated as categorical
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            # Pipeline for preprocessing numerical columns
            num_pipeline = Pipeline(
                steps=[
                    # Fill missing values with the median
                    ("imputer", SimpleImputer(strategy="median")),
                    # Scale numerical data to have a mean of 0 and standard deviation of 1
                    ("scaler", StandardScaler())
                ]
            )

            # Pipeline for preprocessing categorical columns
            cat_pipeline = Pipeline(
                steps=[
                    # Fill missing values with the most frequent value
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    # Convert categorical values to one-hot encoded vectors
                    ("one_hot_encoder", OneHotEncoder()),
                    # Scale the one-hot encoded values (mean adjustment not applicable)
                    ("scaler", StandardScaler(with_mean=False))
                ]
            )

            # Log the column types being processed
            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            # Combine numerical and categorical pipelines into a single preprocessor
            preprocessor = ColumnTransformer(
                transformers=[
                    ("num_pipeline", num_pipeline, numerical_columns),
                    ("cat_pipelines", cat_pipeline, categorical_columns)
                ]
            )

            # Return the combined preprocessor object
            return preprocessor
        
        except Exception as e:
            # Raise a custom exception if any error occurs
            raise CustomException(e, sys)
        
    def initiate_data_transformation(self, train_path, test_path):
        '''
        Reads data from train and test paths, applies preprocessing, 
        and saves the preprocessor object.
        '''
        try:
            # Load training and testing datasets
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read train and test data completed")

            # Obtain the preprocessing object
            logging.info("Obtaining preprocessing object")
            preprocessing_obj = self.get_data_transformer_object()

            # Target column for prediction
            target_column_name = "math_score"
            # Numerical columns
            numerical_columns = ["writing_score", "reading_score"]

            # Separate input features and target variable for training data
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            # Separate input features and target variable for testing data
            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )

            # Apply the preprocessing object to the training and testing data
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            # Combine processed input features with the target variable for training
            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            # Combine processed input features with the target variable for testing
            test_arr = np.c_[
                input_feature_test_arr, np.array(target_feature_test_df)
            ]

            logging.info(f"Saved preprocessing object.")

            # Save the preprocessing object for future use
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            # Return the transformed training data, testing data, and the preprocessor file path
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
        except Exception as e:
            # Raise a custom exception if any error occurs
            raise CustomException(e, sys)
