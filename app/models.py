from django.db import models

# Create your models here.

class Content(models.Model):
	owner = models.BigIntegerField(unique=True, null=False)
	title = models.CharField(max_length=100, null=False)
	description = models.TextField(max_length=900, null=False)
	url_path = models.URLField(unique=True)
	amount_rating = models.BigIntegerField()
	image_1 = models.ImageField(upload_to="uploaded_img/", help_text="Content Image 1")
	image_2 = models.ImageField(upload_to="uploaded_img/", help_text="Content Image 2")
	image_3 = models.ImageField(upload_to="uploaded_img/", help_text="Content Image 3")
	tags = models.TextField(max_length=1200)
	category = models.CharField(max_length=500)
