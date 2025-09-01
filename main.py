from textsummarizer.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from textsummarizer.pipeline.stage_02_data_validation import DataValidationTrainingPipeline
from textsummarizer.pipeline.stage_03_data_transformation import DataTransformationTrainingPipeline
from textsummarizer.pipeline.stage_04_model_trainer import ModelTrainerTrainingPipeline
from textsummarizer.pipeline.stage_05_Modelevaluatin import ModelEvaluationPipeline   
from textsummarizer.logging import logger

STAGE_NAME ="Data Ingestion"
try:
    logger.info(f">>>stage {STAGE_NAME} Intiated<<<")
    data_ingestion_pipeline = DataIngestionTrainingPipeline()
    data_ingestion_pipeline.main()
    logger.info(f">>> stage {STAGE_NAME} Completed <<<\n\nx=========x")
except Exception as e:
        logger.exception(e)
        raise e


STAGE_NAME ="Data Validation"
try:
    logger.info(f">>>stage {STAGE_NAME} Intiated<<<")
    data_validation_pipeline = DataValidationTrainingPipeline()
    data_validation_pipeline.main()
    logger.info(f">>> stage {STAGE_NAME} Completed <<<\n\nx=========x")
except Exception as e:
        logger.exception(e)
        raise e


STAGE_NAME ="Data Transforamtion"
try:
    logger.info(f">>>stage {STAGE_NAME} Intiated<<<")
    data_Tranformation = DataTransformationTrainingPipeline()
    data_Tranformation.main()
    logger.info(f">>> stage {STAGE_NAME} Completed <<<\n\nx=========x")
except Exception as e:
        logger.exception(e)
        raise e

STAGE_NAME = "Model Trainer stage"
try: 
   logger.info(f"*******************")
   logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
   model_trainer = ModelTrainerTrainingPipeline()
   model_trainer.main()
   logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        logger.exception(e)
        raise e




STAGE_NAME = "Model Evaluation stage"
try: 
   logger.info(f"*******************")
   logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
   model_evaluation = ModelEvaluationPipeline()
   model_evaluation.main()
   logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        logger.exception(e)
        raise e