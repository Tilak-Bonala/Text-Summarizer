import os
from textsummarizer.logging import logger
from transformers import AutoTokenizer, PegasusTokenizer
from datasets import load_dataset, load_from_disk
from textsummarizer.entity import DataTransformationConfig


class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
        
        if "pegasus" in config.tokenizer_name.lower():
            self.tokenizer = PegasusTokenizer.from_pretrained(config.tokenizer_name)
        else:
            self.tokenizer = AutoTokenizer.from_pretrained(config.tokenizer_name, use_fast=False)

    def convert_examples_to_features(self, example_batch):
      
        input_encodings = self.tokenizer(example_batch['dialogue'],max_length=1024,padding="max_length",truncation=True)

      
        with self.tokenizer.as_target_tokenizer():
            target_encodings = self.tokenizer(example_batch['summary'],max_length=128,padding="max_length",truncation=True)

        return {
            "input_ids": input_encodings["input_ids"],
            "attention_mask": input_encodings["attention_mask"],
            "labels": target_encodings["input_ids"]
        }

    def convert(self):
        dataset_sam = load_from_disk(self.config.data_path)
        dataset_sam_pt = dataset_sam.map(self.convert_examples_to_features, batched=True)
        dataset_sam_pt.save_to_disk(os.path.join(self.config.root_dir,"samsum_dataset"))
