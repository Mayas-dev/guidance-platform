
from django import forms
from .models import Profile, UserTopic, GuidanceRequest, GuidanceOffer

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio"]
        widgets = {
            "bio": forms.Textarea(attrs={
                "rows": 5,
                "placeholder": "Tell others about yourself and what you can help with.",
            }),
        }
class UserTopicForm(forms.ModelForm):
    class Meta:
        model = UserTopic
        fields = [
            "topic",
            "topic_type",
            "experience_level",
        ]

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()

        topic = cleaned_data.get("topic")
        topic_type = cleaned_data.get("topic_type")

        if self.user and topic and topic_type:
            duplicate_exists = UserTopic.objects.filter(
                user=self.user,
                topic=topic,
                topic_type=topic_type,
            ).exists()

            if duplicate_exists:
                raise forms.ValidationError(
                    "You have already added this topic with this selection."
                )

        return cleaned_data
class GuidanceRequestForm(forms.ModelForm):
    class Meta:
        model = GuidanceRequest
        fields = ["title", "description", "topic"]
        widgets = {
            "title": forms.TextInput(attrs={
                "placeholder": "What do you need guidance with?",
            }),
            "description": forms.Textarea(attrs={
                "rows": 5,
                "placeholder": "Explain what you need help with.",
            }),
        }

class GuidanceOfferForm(forms.ModelForm):
    class Meta:
        model = GuidanceOffer
        fields = ["message"]
        widgets = {
            "message": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Explain how you can help with this request.",
            }),
        }


