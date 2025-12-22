import os
import torch
from transformers import (
    TrainingArguments,
    Trainer,
    DataCollatorForSeq2Seq,
    AutoModelForSeq2SeqLM,
    AutoTokenizer
)
from datasets import load_from_disk
from textsummarizer.entity import ModelTrainerConfig

class Modeltrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config
    
    def train(self):
        device = 'cuda' if torch.cuda.is_available() else 'cpu'

        # Load tokenizer + model
        tokenizer = AutoTokenizer.from_pretrained(self.config.model_ckpt)
        model = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_ckpt).to(device)

        # Data collator
        seq2seq_data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

        # Load dataset from disk
        dataset = load_from_disk(self.config.data_path)

        # Training arguments
        trainer_args = TrainingArguments(
            output_dir=self.config.root_dir,
            num_train_epochs=self.config.epochs,
            warmup_steps=self.config.warmup_steps,
            per_device_train_batch_size=self.config.batch_size,
            per_device_eval_batch_size=self.config.batch_size,
            weight_decay=self.config.weight_decay,
            logging_steps=self.config.logging_steps,
            eval_strategy=self.config.evaluation_strategy,
            eval_steps=self.config.eval_steps,
            save_steps=1e6,
            gradient_accumulation_steps=self.config.gradient_accumulation_steps
        ) 

        # Hugging Face Trainer
        trainer = Trainer(
            model=model,
            args=trainer_args,
            data_collator=seq2seq_data_collator,
            train_dataset=dataset["test"],
            eval_dataset=dataset["validation"],
            processing_class=tokenizer      
            
        )

        trainer.train()

        # Save model + tokenizer to a model-specific directory
        model_dir = os.path.join(self.config.root_dir, self.config.model_ckpt.replace("/", "_"))
        model.save_pretrained(model_dir)
        tokenizer.save_pretrained(model_dir)
