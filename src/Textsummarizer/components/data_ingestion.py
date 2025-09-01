import os
import urllib.request
import zipfile
from textsummarizer.logging import logger
from textsummarizer.utils.common import get_size
from pathlib import Path
from textsummarizer.entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
            self.config = config


    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            filename, headers = urllib.request.urlretrieve(
                      url =self.config.source_url,
                      filename =self.config.local_data_file
            )
            logger.info(f"{filename} download! with following info:\n{headers}")
        else:
             logger.info(f"File already exists at size of :{get_size(Path(self.config.local_data_file))}")

    def extract_zip_file(self):
         """ zip_file_path: str
         Extracts the zip file into the specified directory.
         Function will returns None if the extraction is successful, otherwise it will raise an exception.
         """

         unzip_path = self.config.unzip_dir
         os.makedirs(unzip_path, exist_ok =True)
         with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
              zip_ref.extractall(unzip_path)             