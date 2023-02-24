from django.db import models

class Request(models.Model):
    address_text = models.CharField(max_length=255)
    request_date = models.DateTimeField('date requested')

    def __str__(self):
        return self.address_text


class Weather(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    currentTemp = models.FloatField(default=None, null=True)
    maxTemp = models.FloatField(default=None, null=True)
    minTemp = models.FloatField(default=None, null=True)

    def __str__(self):
        return self.request
