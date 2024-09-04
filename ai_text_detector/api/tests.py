from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Prediction

class PredictionAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_prediction_api(self):
        url = reverse('predict_text')
        data = {'text': 'This is a test sentence.'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('result', response.data)

    def test_get_predictions(self):
        Prediction.objects.create(input_text='Test', prediction='Human', confidence=0.8)
        url = reverse('get_predictions')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)