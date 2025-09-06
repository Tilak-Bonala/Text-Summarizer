from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from datasets import load_from_disk
from textsummarizer.entity import ModelEvaluationConfig
import torch
import pandas as pd
from tqdm import tqdm
import evaluate
import os


class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def generate_batch_sized_chunks(self, list_of_elements, batch_size):
        """Split data into smaller batches that we can process."""
        for i in range(0, len(list_of_elements), batch_size):
            yield list_of_elements[i:i + batch_size]

    def calculate_metrics(
        self, dataset, metric, model, tokenizer,
        batch_size=16, device="cuda" if torch.cuda.is_available() else "cpu",
        column_text="dialogue", column_summary="summary"
    ):
        article_batches = list(self.generate_batch_sized_chunks(dataset[column_text], batch_size))
        target_batches = list(self.generate_batch_sized_chunks(dataset[column_summary], batch_size))

        for article_batch, target_batch in tqdm(zip(article_batches, target_batches), total=len(target_batches)):
            inputs = tokenizer(
                article_batch,
                max_length=1024,
                truncation=True,
                padding="max_length",
                return_tensors="pt"
            ).to(device)

            summaries = model.generate(
                inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                length_penalty=0.8,
                num_beams=8,
                max_length=128
            )

            decoded_summaries = [
                tokenizer.decode(s, skip_special_tokens=True, clean_up_tokenization_spaces=True)
                for s in summaries
            ]
            metric.add_batch(predictions=decoded_summaries, references=target_batch)

        return metric.compute()
    
    def evaluate(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"

       
        model_dir = self.config.model_path
        tokenizer = AutoTokenizer.from_pretrained(model_dir)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_dir).to(device)

        # Load dataset
        dataset = load_from_disk(self.config.data_path)

        # Load ROUGE metric
        rouge = evaluate.load("rouge")

        # Run evaluation on small sample
        score = self.calculate_metrics(dataset["validation"][:10], rouge, model, tokenizer, batch_size=2)

        # Extract metrics
        rouge_names = ["rouge1", "rouge2", "rougeL", "rougeLsum"]
        rouge_dict = {rn: score[rn] for rn in rouge_names}

        # Save with model name dynamically
        model_name = os.path.basename(model_dir)
        df = pd.DataFrame(rouge_dict, index=[model_name])
        df.to_csv(self.config.metric_file_name, index=False)

        return df
