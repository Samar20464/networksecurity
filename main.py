from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig,DatTransformationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig

import sys

if __name__ == '__main__':
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
        data_ingestion = DataIngestion(dataingestionconfig)
        logging.info("Initiate the data ingestion")
        dataingestionartifacts = data_ingestion.initiate_data_ingestion()
        logging.info("Data Initiation Completed")
        data_validation_config = DataValidationConfig(trainingpipelineconfig)
        data_validation = DataValidation(dataingestionartifacts,data_validation_config)
        logging.info("Initiate the data validation")
        data_validation_Artifact = data_validation.initiate_data_validation()
        logging.info("data validation completed")
        print(data_validation_Artifact)
        data_tranformation_config = DatTransformationConfig(trainingpipelineconfig)
        logging.info("data transformation completed")
        data_tranformation = DataTransformation(data_validation_Artifact,data_tranformation_config)
        data_tranformation_artifact = data_tranformation.initiate_data_transformation()
        print(data_tranformation_artifact)

    except Exception as e:
        raise NetworkSecurityException(e,sys)