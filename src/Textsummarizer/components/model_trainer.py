from transformers import TrainingArguments,Trainer
from transformers import DataCollatorForSeq2Seq,AutoModelForSeq2SeqLM,AutoTokenizer
from datasets import load_from_disk,load_dataset
import torch
from textsummarizer.entity import ModelTrainerConfig

class Modeltrainer:
    def __init__(self,config:ModelTrainerConfig):
        self.config= config
    
    def train(self):
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        tokenizer = AutoTokenizer.from_pretrained(self.config.model_name)
        model_pegasus= AutoModelForSeq2SeqLM.from_pretrained(self.config.model_name)
        seq2seq_data_collator = DataCollatorForSeq2Seq(tokenizer,model=model_pegasus)
        #Loading the dataset
        dataset = load_from_disk(self.config.data_path)
        trainer_args = TrainingArguments(
            output_dir=self.config.root_dir, num_train_epochs=self.config.epochs, warmup_steps=self.config.warmup_steps,
            per_device_train_batch_size=self.config.batch_size, per_device_eval_batch_size=self.config.batch_size,
            weight_decay=self.config.weight_decay, logging_steps=self.config.logging_steps,
            eval_strategy=self.config.evaluation_strategy, eval_steps=self.config.eval_steps, save_steps=1e6,
            gradient_accumulation_steps=self.config.gradient_accumulation_steps
        ) 
        trainer = Trainer(
            model=model_pegasus,
            args=trainer_args,
            #tokenizer= tokenizer,
            data_collator =seq2seq_data_collator,
            train_dataset=dataset["test"],
            eval_dataset=dataset["validation"],
            processing_class=tokenizer
        )

        trainer.train()

        model_pegasus.save_pretrained(os.path.join(self.config.root_dir,"pegasus_samsum_model"))
        tokenizer.save_pretrained(os.path.join(self.config.root_dir,"tokenizer"))