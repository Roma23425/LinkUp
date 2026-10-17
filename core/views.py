from django.shortcuts import render


def home(request):

    return render(
        request,
        "core/home.html"
    )



# def home(request):
#     posts = (
#         Post.objects
#         .select_related("author", "shared_from__author")
#         .prefetch_related("likes", "comments")[:50]
#     )
#     return render(request, "core/home.html", {
#         "posts": posts,
#         "liked_ids": liked_ids_for(request.user),
#         "popular_users": User.objects.exclude(pk=request.user.pk).order_by("-date_joined")[:5],
#         "popular_groups": [],
#         "events": [],
#     })