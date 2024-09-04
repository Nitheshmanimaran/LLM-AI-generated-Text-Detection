from rest_framework.views import APIView
from rest_framework.response import Response
from .predictor import main
from .models import Prediction
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import logging

def home(request):
    return HttpResponse("Welcome to the AI Text Detector API. Use /api/predict/ to make predictions.")


class PredictText(APIView):
    def post(self, request):
        text = request.data.get('text', '')
        if not text:
            return Response({'error': 'No text provided'}, status=400)
        
        result = main(text)
        
        # Parse the result string to extract prediction and confidence
        if "AI-generated" in result:
            prediction = "AI-generated"
        else:
            prediction = "Human-written"
        confidence = float(result.split("Confidence: ")[1].strip(")"))
        
        # Store the prediction in the database
        Prediction.objects.create(
            input_text=text,
            prediction=prediction,
            confidence=confidence
        )
        
        return Response({'result': result})
    
class GetPredictions(APIView):
    def get(self, request):
        predictions = Prediction.objects.all().order_by('-timestamp')[:10]  # Get last 10 predictions
        data = [{
            'input_text': p.input_text,
            'prediction': p.prediction,
            'confidence': p.confidence,
            'timestamp': p.timestamp
        } for p in predictions]
        return Response(data)
    
logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class PredictText(APIView):
    def post(self, request):
        text = request.data.get('text', '')
        if not text:
            return Response({'error': 'No text provided'}, status=400)
        
        result = main(text)
        
        # Parse the result
        if isinstance(result, str):
            # If result is a string, parse it
            if "AI-generated" in result:
                prediction = "AI-generated"
            else:
                prediction = "Human-written"
            confidence = float(result.split("Confidence: ")[1].strip(")"))
        elif isinstance(result, dict):
            # If result is already a dictionary, use it directly
            prediction = result.get('prediction')
            confidence = result.get('confidence')
        else:
            logger.error(f"Unexpected result format: {result}")
            return Response({'error': 'Unexpected result format'}, status=500)
        
        # Save prediction to database
        try:
            saved_prediction = Prediction.objects.create(
                input_text=text,
                prediction=prediction,
                confidence=confidence
            )
            logger.info(f"Saved prediction: {saved_prediction.id}")
        except Exception as e:
            logger.error(f"Error saving prediction: {str(e)}")
            # You might want to return an error response here, or continue without saving
        
        return Response({'result': result})