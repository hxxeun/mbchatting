from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView,
    DeleteView,
)
from braces.views import LoginRequiredMixin
from allauth.account.views import PasswordChangeView

from .mixins import LoginAndVerificationRequiredMixin, LoginAndOwnershipRequiredMixin
from board.models import Review, User, Comment
from board.forms import ReviewForm, ProfileForm, CommentForm
# Create your views here.

class IndexView(ListView):
    model = Review
    template_name = "board/index.html"
    context_object_name = "reviews"
    paginate_by = 4
    ordering = ["-dt_created"]

class ReviewDetailView(DetailView):
    model = Review
    template_name = "board/review_detail.html"
    pk_url_kwarg = "review_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context

class ReviewCreateView(LoginAndVerificationRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "board/review_form.html"



    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("board:review-detail", kwargs={"review_id": self.object.id})

        

class ReviewUpdateView(LoginAndOwnershipRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = "board/review_form.html"
    pk_url_kwarg = "review_id"


    def get_success_url(self):
        return reverse("board:review-detail", kwargs={"review_id": self.object.id})



class ReviewDeleteView(LoginAndOwnershipRequiredMixin, DeleteView):
    model = Review
    template_name = "board/review_confirm_delete.html"
    pk_url_kwarg = "review_id"

    def get_success_url(self):
        return reverse("board:index")


class CommentCreateView(LoginAndVerificationRequiredMixin, CreateView):
    http_method_names = ['post']
    model = Comment
    form_class = CommentForm


    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.review = Review.objects.get(id=self.kwargs.get('review_id'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('board:review-detail', kwargs={'review_id': self.kwargs.get('review_id')})

class CommentUpdateView(LoginAndOwnershipRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'board/comment_update_form.html'
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse('board:review-detail', kwargs={'review_id': self.object.review.id})


class CommentDeleteView(LoginAndOwnershipRequiredMixin, DeleteView):
    model = Comment
    template_name = 'board/comment_confirm_delete.html'
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse('board:review-detail', kwargs={'review_id': self.object.review.id})


class ProfileView(DetailView):
    model = User
    template_name = "board/profile.html"
    pk_url_kwarg = "user_id"
    context_object_name = "profile_user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get("user_id")
        context["user_reviews"] = Review.objects.filter(author__id=user_id).order_by("-dt_created")[:4]
        return context

class UserReviewListView(ListView):
    model = Review
    template_name = "board/user_review_list.html"
    context_object_name = "user_reviews"
    paginate_by = 4

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        return Review.objects.filter(author__id=user_id).order_by("dt_created")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile_user"] = get_object_or_404(User, id=self.kwargs.get("user_id"))
        return context

class ProfileSetView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = "board/profile_set_form.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse("board:index")

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = "board/profile_update_form.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse("board:profile", kwargs=({"user_id": self.request.user.id}))

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    def get_success_url(self):
        return reverse("board:proile", kwargs=({"user_id": self.request.user.id}))