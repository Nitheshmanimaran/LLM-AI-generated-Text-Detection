import json
import time
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from .models import Prediction

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
        
        # Tokenize and predict
        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)
        
        # Get probabilities
        probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
        ai_probability = probabilities[0][1].item()
        is_ai_generated = ai_probability > 0.5
        
        # Save the prediction to the database
        prediction = Prediction.objects.create(
            input_text=text,
            prediction=is_ai_generated,
            confidence=ai_probability
        )
        print(f"Prediction saved with ID: {prediction.id}")  # Debug print
        
        # Simulate processing time (remove in production)
        time.sleep(1)
        
        return JsonResponse({
            'probability': ai_probability,
            'is_ai_generated': is_ai_generated
        })
    except Exception as e:
        print(f"Error in predict view: {str(e)}")  # Debug print
        return JsonResponse({'error': str(e)}, status=400)

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')