# ml_model.py

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os

class MLModel:
    _instance = None
    _is_loaded = False

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.model_path = os.path.join(os.getcwd(), 'model_saves', 'deberta')

    def load(self):
        if not self._is_loaded:
            print("Loading ML model...")
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, use_fast=False)
                self.model = AutoModelForSequenceClassification.from_pretrained(self.model_path)
                self._is_loaded = True
                print("ML model loaded successfully.")
            except Exception as e:
                print(f"Error loading model: {str(e)}")
                raise

    def predict(self, text):
        if not self._is_loaded:
            self.load()
        
        try:
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
            with torch.no_grad():
                outputs = self.model(**inputs)
            
            logits = outputs.logits
            probabilities = torch.nn.functional.softmax(logits, dim=-1)
            
            # Assuming index 1 is for AI-generated probability
            ai_probability = probabilities[0][1].item()
            
            # Ensure the probability is valid
            ai_probability = max(0, min(1, ai_probability))
            
            return ai_probability
        except Exception as e:
            print(f"Error in prediction: {str(e)}")
            return 0.5  # Return a neutral probability in case of error

# Global instance
ml_model = MLModel.get_instance()