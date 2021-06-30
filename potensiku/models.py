from django.db import models


# Create your models here.
class Question(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    question = models.CharField(max_length=255)
    category = models.CharField(max_length=255)


class Person(models.Model):
    full_name = models.CharField(max_length=255)
    nip = models.CharField(max_length=255)
    ttl = models.CharField(max_length=255)
    marriage_status = models.CharField(max_length=255)
    religion = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    educationSMA = models.CharField(max_length=255)
    educationD3 = models.CharField(max_length=255)
    educationS1 = models.CharField(max_length=255)
    educationS2 = models.CharField(max_length=255)
    educationS3 = models.CharField(max_length=255)
    title1 = models.CharField(max_length=255)
    title2 = models.CharField(max_length=255)
    title3 = models.CharField(max_length=255)
    history1 = models.CharField(max_length=255)
    history2 = models.CharField(max_length=255)
    history3 = models.CharField(max_length=255)
    achievement1 = models.CharField(max_length=255)
    achievement2 = models.CharField(max_length=255)
    achievement3 = models.CharField(max_length=255)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.RESTRICT)
    answer = models.IntegerField()


class Participant(models.Model):
    token = models.CharField(max_length=255)
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    answers = models.ManyToManyField(Answer)


class Token(models.Model):
    token = models.CharField(max_length=255)
