
from .models import UserTopic


def find_matches_for_user(user):
    user_can_guide = set(
        UserTopic.objects.filter(
            user=user,
            topic_type=UserTopic.TopicType.CAN_GUIDE,
        ).values_list("topic_id", flat=True)
    )

    user_wants_guidance = set(
        UserTopic.objects.filter(
            user=user,
            topic_type=UserTopic.TopicType.WANTS_GUIDANCE,
        ).values_list("topic_id", flat=True)
    )

    potential_matches = (
        UserTopic.objects.filter(
            topic_id__in=user_wants_guidance,
            topic_type=UserTopic.TopicType.CAN_GUIDE,
        )
        .exclude(user=user)
        .select_related("user", "topic")
    )

    matches = {}

    for user_topic in potential_matches:
        other_user = user_topic.user

        other_user_wants = UserTopic.objects.filter(
            user=other_user,
            topic_type=UserTopic.TopicType.WANTS_GUIDANCE,
            topic_id__in=user_can_guide,
        ).select_related("topic")

        if not other_user_wants.exists():
            continue

        if other_user.pk not in matches:
            matches[other_user.pk] = {
                "user": other_user,
                "they_can_guide": set(),
                "you_can_guide": set(),
            }

        matches[other_user.pk]["they_can_guide"].add(
            user_topic.topic
        )

        for wanted_topic in other_user_wants:
            matches[other_user.pk]["you_can_guide"].add(
                wanted_topic.topic
            )

    results = []

    for match in matches.values():
        results.append({
            "user": match["user"],
            "they_can_guide": sorted(
                match["they_can_guide"],
                key=lambda topic: topic.name,
            ),
            "you_can_guide": sorted(
                match["you_can_guide"],
                key=lambda topic: topic.name,
            ),
        })

    return results