from django.db import models

# Create your models here.
class sharing(models.Model):
	qr_img_b64 = models.TextField()
	url_origin = models.URLField()
	url = models.URLField()
	code = models.CharField(max_length=10)
	create_date = models.DateTimeField(auto_now_add=True)
