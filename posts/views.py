from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import CommentForm, PostForm
from .models import Like, Post


def _back(request, fallback="home"):
    url = request.META.get("HTTP_REFERER")
    if url and url_has_allowed_host_and_scheme(url, allowed_hosts={request.get_host()}):
        return redirect(url)
    return redirect(fallback)


def liked_ids_for(user):
    if not user.is_authenticated:
        return set()
    return set(Like.objects.filter(user=user).values_list("post_id", flat=True))


@login_required
@require_POST
def post_create(request):
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        messages.success(request, "Публікацію створено.")
    else:
        for errors in form.errors.values():
            for error in errors:
                messages.error(request, error)
    return redirect("home")


def post_detail(request, pk):
    post = get_object_or_404(Post.objects.select_related("author", "shared_from__author"), pk=pk)
    return render(request, "posts/post_detail.html", {
        "post": post,
        "comments": post.comments.select_related("author"),
        "comment_form": CommentForm(),
        "liked_ids": liked_ids_for(request.user),
    })


@login_required
@require_POST
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return _back(request)


@login_required
@require_POST
def comment_add(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect("post_detail", pk=post.pk)


@login_required
@require_POST
def post_share(request, pk):
    original = get_object_or_404(Post, pk=pk)
    Post.objects.create(author=request.user, shared_from=original.shared_from or original)
    messages.success(request, "Публікацію поширено.")
    return redirect("home")


@login_required
@require_POST
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user and not request.user.is_staff:
        return HttpResponseForbidden("Немає прав на видалення.")
    post.delete()
    messages.success(request, "Публікацію видалено.")
    return redirect("home")


def post_list(request):
    posts = (
        Post.objects
        .select_related("author", "shared_from", "shared_from__author")
        .prefetch_related("likes", "comments")
        .order_by("-created_at")
    )

    liked_ids = liked_ids_for(request.user)

    return render(request, "posts/post_list.html", {
        "posts": posts,
        "post_form": PostForm() if request.user.is_authenticated else None,
        "liked_ids": liked_ids,
    })
