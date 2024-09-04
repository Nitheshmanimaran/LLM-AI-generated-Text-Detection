#Plan 
"""
1. Create a function to load the model available in the model_saves folder [model, tfidf]
2. Create a function to preprocess the user input text
3. Create a function to predict the user input text
4. Create a function to postprocess the predicted text

#Paths
#logistic_regression.joblib - "D:\Projects\LLM-AI-generated-Text-Detection\model_saves\logistic_regression_model.joblib"
#tfidf_vectorizer.joblib - "D:\Projects\LLM-AI-generated-Text-Detection\model_saves\tfidf_vectorizer.joblib"


"""
import joblib
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import warnings
warnings.filterwarnings("ignore")

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

def predict_text(text, model, vectorizer):
    """
    Predict whether the input text is AI-generated or not.
    """
    preprocessed_text = preprocess_text(text)
    vectorized_text = vectorizer.transform([preprocessed_text])
    prediction = model.predict(vectorized_text)
    probability = model.predict_proba(vectorized_text)
    return prediction[0], probability[0]

def postprocess_prediction(prediction, probability):
    """
    Postprocess the prediction and return a human-readable result.
    """
    if prediction == 1:
        result = "AI-generated"
        confidence = probability[1]
    else:
        result = "Human-written"
        confidence = probability[0]
    
    return f"The text is likely {result} (Confidence: {confidence:.2f})"

def main(input_text):
    """
    Main function to process user input and return the prediction.
    """
    model, vectorizer = load_model()
    prediction, probability = predict_text(input_text, model, vectorizer)
    result = postprocess_prediction(prediction, probability)
    return result

# Example usage
if __name__ == "__main__":
    sample_text = "hi my naame is nithesh kumar. i am a freelancer."
    result = main(sample_text)
    print(result)
