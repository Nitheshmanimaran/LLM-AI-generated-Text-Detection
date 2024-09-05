from django.db import models

class Prediction(models.Model):
    input_text = models.TextField()
    prediction = models.BooleanField()
    confidence = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{'AI' if self.prediction else 'Human'} ({self.confidence:.2f})"