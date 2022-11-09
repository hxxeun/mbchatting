from typing import Generic
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from .validators import validate_no_special_characters, validate_email
# from .validators import validate_no_special_characters, validate_restaurant_link
# Create your models here.

class User(AbstractUser):
    mail = models.CharField(max_length=60, unique=True, null=True, validators=[validate_email], error_messages ={'unique': '이미 사용중인 이메일입니다.'})
    nickname = models.CharField(
        max_length=15, 
        unique=True, 
        null=True,
        validators=[validate_no_special_characters],
        error_messages ={'unique': '이미 사용중인 닉네임입니다.'},
    )
    mbti = models.CharField(max_length=60, blank=True)
    profile_img = models.ImageField(null=True)
    profile_pic = models.ImageField(default="default_profile_pic.jpg", upload_to="profile_pics")

    intro = models.CharField(max_length=60, blank=True)

    following = models.ManyToManyField(
        'self', 
        symmetrical=False, 
        blank=True, 
        related_name='followers'
    )
    
    def __str__(self):
        return self.email


class Review(models.Model):
    title = models.CharField(max_length=30)


    image1 = models.ImageField(upload_to="review_pics", blank=True)
    image2 = models.ImageField(upload_to="review_pics", blank=True)
    image3 = models.ImageField(upload_to="review_pics", blank=True)
    content = models.TextField()
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_updated = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')

    likes = GenericRelation('Like', related_query_name='review')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-dt_created']

class Comment(models.Model):
    content = models.TextField(max_length=500, blank=False)

    dt_created = models.DateTimeField(auto_now_add=True)

    dt_updated = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')

    likes = GenericRelation('Like', related_query_name='comment')

    def __str__(self):
        return self.content[:30]

class Like(models.Model):
    dt_created = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    object_id = models.PositiveBigIntegerField()

    liked_object = GenericForeignKey()

    def __str__(self):
        return f"({self.user}, {self.liked_object})"