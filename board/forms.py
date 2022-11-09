from django import forms
from .models import User, Review, Comment

class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["mail", "nickname",]

    def signup(self, request, user):
        user.mail = self.cleaned_data["mail"]
        user.nickname = self.cleaned_data["nickname"]
        user.save()

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            "title",
            # "restaurant_name",
            # "restaurant_link",
            # "rating",
            "image1",
            "image2",
            "image3",
            "content",
        ]
        # widgets = {
        #     "rating": forms.RadioSelect,
        # }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            # "nickname",
            "profile_pic",
            "intro",
            "mbti",
        ]
        widgets = {
            # "intro" : forms.Textarea,
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'content', 
        ]
        widgets = {
            'content' : forms.Textarea,
        }
