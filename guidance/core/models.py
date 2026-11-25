from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class UserTopic(models.Model):

    class TopicType(models.TextChoices):
        CAN_GUIDE = "CAN_GUIDE", "Can guide"
        WANTS_GUIDANCE = "WANTS_GUIDANCE", "Wants guidance"

    class ExperienceLevel(models.TextChoices):
        BEGINNER = "BEGINNER", "Beginner"
        INTERMEDIATE = "INTERMEDIATE", "Intermediate"
        ADVANCED = "ADVANCED", "Advanced"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    topic_type = models.CharField(
        max_length=20,
        choices=TopicType.choices
    )
    experience_level = models.CharField(
        max_length=20,
        choices=ExperienceLevel.choices
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "topic", "topic_type"],
                name="unique_user_topic_type"
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.topic.name} - {self.topic_type}"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

class GuidanceRequest(models.Model):

    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        IN_PROGRESS = "IN_PROGRESS", "In progress"
        CLOSED = "CLOSED", "Closed"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class GuidanceOffer(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        ACCEPTED = "ACCEPTED", "Accepted"
        DECLINED = "DECLINED", "Declined"

    guidance_request = models.ForeignKey(
        GuidanceRequest,
        on_delete=models.CASCADE,
        related_name="offers",
    )
    helper = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="guidance_offers",
    )
    message = models.TextField(
        blank=True,
        help_text="Explain how you can help with this request.",
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["guidance_request", "helper"],
                name="unique_offer_per_user_request",
            )
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.helper.username} - {self.guidance_request.title}"
