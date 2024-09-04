import joblib
import os
import re
from django.conf import settings

def load_model():
    """
    Load the trained model and TfidfVectorizer from the model_saves folder.
    """
    model_path = r"D:\Projects\LLM-AI-generated-Text-Detection\model_saves\logistic_regression_model.joblib"
    vectorizer_path = r"D:\Projects\LLM-AI-generated-Text-Detection\model_saves\tfidf_vectorizer.joblib"
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    
    return model, vectorizer

def preprocess_text(text):
    """
    Preprocess the input text.
    """
    # Convert to lowercase
    text = text.lower()
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text

def predict_text(model, vectorizer, text):
    """
    Make a prediction on the input text.
    """
    # Preprocess the text
    preprocessed_text = preprocess_text(text)
    # Vectorize the text
    text_vectorized = vectorizer.transform([preprocessed_text])
    # Make prediction
    prediction = model.predict(text_vectorized)[0]
    probability = model.predict_proba(text_vectorized)[0]
    confidence = max(probability)
    
    return prediction, confidence

def main(user_input):
    """
    Main function to load the model and make predictions.
    """
    # Load the model and vectorizer
    model, vectorizer = load_model()
    
    # Make prediction
    prediction, confidence = predict_text(model, vectorizer, user_input)
    
    # Prepare the result
    if prediction == 1:
        result = f"The text is likely AI-generated (Confidence: {confidence:.2f})"
    else:
        result = f"The text is likely Human-written (Confidence: {confidence:.2f})"
    
    return result

# This part is not needed for the API, but you can keep it for testing purposes
if __name__ == "__main__":
    # Test the function
    test_text = "This is a test sentence. Please predict if it's AI-generated or human-written."
    print(main(test_text))

#Usage:
'''
{
    "text": "hi my naame is nithesh kumar. i am a freelancer."
}
'''