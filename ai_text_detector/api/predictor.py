import joblib
import os
import re
from django.conf import settings
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os
from django.conf import settings
import joblib
import torch
import logging

logger = logging.getLogger(__name__)

def load_model():
    """
    Load the DeBERTa model and tokenizer from the model_saves/deberta folder.
    """
    base_dir = settings.BASE_DIR
    model_path = settings.MODEL_PATH
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model directory not found at {model_path}")
    
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    
    return model, tokenizer

def predict_text(model, tokenizer, text):
    """
    Predict if the input text is AI-generated using the DeBERTa model.
    """
    # Tokenize the input text
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    
    # Make prediction
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Get probabilities
    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
    
    # Assuming binary classification (AI-generated or not)
    ai_prob = probs[0][1].item()
    
    return ai_prob

def main(user_input):
    """
    Main function to load the model and make predictions.
    """
    logger.info(f"Received input: {user_input}")
    
    # Load the model and tokenizer
    model, tokenizer = load_model()
    
    logger.info("Model and tokenizer loaded successfully.")
    
    # Make prediction
    ai_probability = predict_text(model, tokenizer, user_input)
    
    logger.info(f"AI Probability: {ai_probability}")
    
    # Prepare the result
    result = {
        "probability": ai_probability,
        "is_ai_generated": ai_probability > 0.5
    }
    
    logger.info(f"Final Result: {result}")
    
    return result

if __name__ == "__main__":
    # Test the function
    test_text = "This is a sample text to test the AI detection model."
    print(main(test_text))

#Usage:
'''
{
    "text": "hi my naame is MYNAMEr. i am a IAM."
}
'''