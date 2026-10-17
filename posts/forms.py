from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["text", "image", "video", "link"]

    def clean_video(self):
        video = self.cleaned_data.get("video")
        if video and video.size > 50 * 1024 * 1024:
            raise forms.ValidationError("Відео завелике (максимум 50 МБ).")
        return video

    def clean(self):
        data = super().clean()
        if not any([data.get("text", "").strip(), data.get("image"), data.get("video"), data.get("link")]):
            raise forms.ValidationError("Публікація порожня: додайте текст, фото, відео або посилання.")
        return data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {"text": forms.Textarea(attrs={"rows": 2, "placeholder": "Напишіть коментар"})}
        labels = {"text": ""}