from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Notification


@login_required
def notification_list(request):
    notifications = (
        Notification.objects
        .filter(recipient=request.user)
        .select_related("actor", "post", "comment")
        .order_by("-created_at")
    )

    unread_count = notifications.filter(is_read=False).count()

    return render(
        request,
        "notifications/notification_list.html",
        {
            "notifications": notifications,
            "unread_count": unread_count,
        },
    )


@login_required
@require_POST
def notification_read(request, pk):
    notification = get_object_or_404(
        Notification,
        pk=pk,
        recipient=request.user,
    )

    notification.is_read = True
    notification.save(update_fields=["is_read"])

    if notification.post_id:
        return redirect("post_detail", pk=notification.post_id)

    return redirect("notification_list")


@login_required
@require_POST
def notification_read_all(request):
    Notification.objects.filter(
        recipient=request.user,
        is_read=False,
    ).update(is_read=True)

    return redirect("notification_list")


@login_required
@require_POST
def notification_delete(request, pk):
    notification = get_object_or_404(
        Notification,
        pk=pk,
        recipient=request.user,
    )

    notification.delete()
    return redirect("notification_list")
