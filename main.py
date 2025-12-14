from textsummarizer.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from textsummarizer.pipeline.stage_02_data_validation import DataValidationTrainingPipeline
from textsummarizer.pipeline.stage_03_data_transformation import DataTransformationTrainingPipeline
from textsummarizer.pipeline.stage_04_model_trainer import ModelTrainerTrainingPipeline
from textsummarizer.pipeline.stage_05_Modelevaluatin import ModelEvaluationPipeline
from textsummarizer.logging import logger


def run_training_pipeline():
    STAGE_NAME = "Data Ingestion"
    try:
        logger.info(f">>>stage {STAGE_NAME} Initiated<<<")
        DataIngestionTrainingPipeline().main()
        logger.info(f">>> stage {STAGE_NAME} Completed <<<\n\nx=========x")
    except Exception as e:
        logger.exception(e)
        raise e

    STAGE_NAME = "Data Validation"
    try:
        logger.info(f">>>stage {STAGE_NAME} Initiated<<<")
        DataValidationTrainingPipeline().main()
        logger.info(f">>> stage {STAGE_NAME} Completed <<<\n\nx=========x")
    except Exception as e:
        logger.exception(e)
        raise e

    STAGE_NAME = "Data Transformation"
    try:
        logger.info(f">>>stage {STAGE_NAME} Initiated<<<")
        DataTransformationTrainingPipeline().main()
        logger.info(f">>> stage {STAGE_NAME} Completed <<<\n\nx=========x")
    except Exception as e:
        logger.exception(e)
        raise e

    STAGE_NAME = "Model Trainer"
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        ModelTrainerTrainingPipeline().main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e

    STAGE_NAME = "Model Evaluation"
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        ModelEvaluationPipeline().main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e


if __name__ == "__main__":
    run_training_pipeline()
