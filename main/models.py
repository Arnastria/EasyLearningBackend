from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    """
    User information generated from SSO UI attributes.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=63)
    npm = models.CharField(max_length=10)
    role = models.CharField(max_length=31)
    org_code = models.CharField(max_length=11)
    faculty = models.CharField(max_length=63)
    study_program = models.CharField(max_length=63)
    educational_program = models.CharField(max_length=63)
    learning_model = models.CharField(max_length=70, default='-')


class Course(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    aliasName = models.CharField(max_length=64)
    intro = models.TextField()
    description = models.TextField()
    links = models.TextField()


class Material(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    intro = models.TextField()
    description = models.TextField()
    pdf = models.TextField()
    pdf_chapter = models.TextField()
    links = models.TextField()


class Post(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    author_name = models.CharField(max_length=200)
    title = models.CharField(max_length=256)
    body = models.TextField()
    category = models.PositiveSmallIntegerField()
    date = models.DateField()


class Reply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    author_name = models.CharField(max_length=200)
    body = models.TextField()
    date = models.DateField()


class Test(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()


class TestScore(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField()


class PDFModel(models.Model):
    file = models.TextField()
