import json
import time
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from .models import Prediction
from .ml_model import ml_model  # This should now work correctly

# Load the model and tokenizer
model_path = 'model_saves/deberta'
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

def home(request):
    return render(request, 'index.html')

@csrf_exempt
@require_http_methods(["POST"])
def predict(request):
    try:
        data = json.loads(request.body)
        text = data.get('text', '')
        
        ai_probability = ml_model.predict(text)
        is_ai_generated = ai_probability > 0.5
        
        # Save the prediction to the database
        prediction_obj = Prediction.objects.create(
            input_text=text,
            prediction=is_ai_generated,
            confidence=ai_probability
        )
        print(f"Prediction saved with ID: {prediction_obj.id}")
        
        return JsonResponse({
            'probability': ai_probability,
            'is_ai_generated': is_ai_generated,
            'message': f"Probability of AI-generated text: {ai_probability:.4f}"
        })
    except Exception as e:
        print(f"Error in predict view: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')