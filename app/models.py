from django.db import models

# Create your models here.

class Content(models.Model):
	""" This is the Table for content details. """
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

	def __str__(self):
		return f"Owner: {self.owner} Title: {self.title} Description: {self.description} URL Path: {self.url_path} Amount of Rates: {self.amount_rating} Image 1: {self.image_1} Image 2: {self.image_2} Image 3: {self.image_3} Tags: {self.tags} Categories: {self.category}"

class account_setting(models.Model):
	""" These are the settings for each account. """
	owner = models.BigIntegerField(unique=True, null=False)
	news_letter = models.BooleanField(default=False, null=False)
	inbox_notifications = models.BooleanField(default=True, null=False)
	browser_notifications = models.BooleanField(default=True, null=False)
	search_collections = models.BooleanField(default=True, null=False)

class feedback_content(models.Model):
	""" This is for storing FeedBack data. """
	owner = models.BigIntegerField(null=False)
	subject = models.CharField(max_length=200, null=False)
	feedback = models.CharField(max_length=500, null=False)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Owner: {self.owner} Subject: {self.subject} Feedback Message: {self.feedback} Date: {self.date}"