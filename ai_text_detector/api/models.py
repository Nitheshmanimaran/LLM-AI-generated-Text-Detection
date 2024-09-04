from django.db import models

class Prediction(models.Model):
    input_text = models.TextField()
    prediction = models.CharField(max_length=20)
    confidence = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.prediction} ({self.confidence:.2f})"