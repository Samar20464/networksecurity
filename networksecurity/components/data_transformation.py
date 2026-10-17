import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constant.traning_pipeline import TARGET_COLUMN
from networksecurity.constant.traning_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from networksecurity.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact
)

from networksecurity.entity.config_entity import DatTransformationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.utils.utils import save_numpy_array_data,save_object

class DataTransformation:
    def __init__(self,data_validation:DataValidationArtifact,
                 data_transformation_config:DatTransformationConfig):
        try:
            self.data_validation_artifact:DataValidationArtifact= data_validation
            self.data_transformation_config: DatTransformationConfig = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def get_data_transformer_object(cls)->Pipeline:
        logging.info(
            "Entered get_data_tranformer_object of transofrmation class"
        )

        try:
            imputer:KNNImputer =KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(
                f"Initialise KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}"
            )
            processor:Pipeline= Pipeline([("imputer",imputer)])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logging.info(
            "Entered initiate_data_transformation method of DataTransformation class"
        )

        try:
            logging.info("Starting data transformation")

            train_df = DataTransformation.read_data(
                self.data_validation_artifact.valid_train_file_path
            )
            test_df = DataTransformation.read_data(
                self.data_validation_artifact.valid_test_file_path
            )

            # Check target column before cleaning
            print("Train target NaN before cleaning:",
                train_df[TARGET_COLUMN].isna().sum())
            print("Test target NaN before cleaning:",
                test_df[TARGET_COLUMN].isna().sum())

            # STEP 1: Remove rows with missing target labels
            train_df = train_df.dropna(subset=[TARGET_COLUMN]).copy()
            test_df = test_df.dropna(subset=[TARGET_COLUMN]).copy()

            # STEP 2: Convert binary labels -1 and 1 to 0 and 1
            train_df[TARGET_COLUMN] = train_df[TARGET_COLUMN].replace(-1, 0)
            test_df[TARGET_COLUMN] = test_df[TARGET_COLUMN].replace(-1, 0)

            # STEP 3: Separate features and target
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN])
            target_feature_train_df = train_df[TARGET_COLUMN]

            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN])
            target_feature_test_df = test_df[TARGET_COLUMN]

            # Verify that no target NaN values remain
            print("Train target NaN after cleaning:",
                target_feature_train_df.isna().sum())
            print("Test target NaN after cleaning:",
                target_feature_test_df.isna().sum())

            print("Train target values:",
                target_feature_train_df.unique())
            print("Test target values:",
                target_feature_test_df.unique())

            # STEP 4: Create the preprocessing pipeline
            preprocessor_object = self.get_data_transformer_object()

            # Fit on training features only
            transformed_input_train_feature = preprocessor_object.fit_transform(
                input_feature_train_df
            )

            # Transform test features
            transformed_input_test_feature = preprocessor_object.transform(
                input_feature_test_df
            )

            # STEP 5: Combine features and target
            train_arr = np.c_[
                transformed_input_train_feature,
                target_feature_train_df.to_numpy()
            ]

            test_arr = np.c_[
                transformed_input_test_feature,
                target_feature_test_df.to_numpy()
            ]

            # STEP 6: Save transformed arrays and preprocessing object
            save_numpy_array_data(
                self.data_transformation_config.transformed_train_file_path,
                array=train_arr
            )

            save_numpy_array_data(
                self.data_transformation_config.transformed_test_file_path,
                array=test_arr
            )

            save_object(
                self.data_transformation_config.transformed_object_file_path,
                preprocessor_object
            )

            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=(
                    self.data_transformation_config.transformed_object_file_path
                ),
                transformed_train_file_path=(
                    self.data_transformation_config.transformed_train_file_path
                ),
                transformed_test_file_path=(
                    self.data_transformation_config.transformed_test_file_path
                )
            )

            return data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
