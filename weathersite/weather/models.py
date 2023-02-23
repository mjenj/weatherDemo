from django.db import models

class Request(models.Model):
    address_text = models.CharField(max_length=200)
    request_date = models.DateTimeField('date requested')

    def __str__(self):
        return self.address_text


class Weather(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    json_response = models.CharField(max_length=400)

    def __str__(self):
        return self.json_response
