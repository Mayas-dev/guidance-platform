

import numpy as np

from core.ai.embeddings import embedding_model
from core.models import UserTopic


def cosine_similarity(vector_a, vector_b):
    return np.dot(vector_a, vector_b) / (
        np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
    )


def find_semantic_matches(guidance_request):
    potential_helpers = list(
        UserTopic.objects.filter(
            topic_type=UserTopic.TopicType.CAN_GUIDE
        )
        .exclude(user=guidance_request.user)
        .select_related("user", "topic")
        .order_by("user_id", "id")
    )

    if not potential_helpers:
        return []

    request_text = (
        f"{guidance_request.title}. "
        f"{guidance_request.description}"
    )

    helper_texts = [
        f"{item.topic.name}. {item.topic.description}"
        for item in potential_helpers
    ]

    request_embedding = list(
        embedding_model.embed([request_text])
    )[0]

    helper_embeddings = list(
        embedding_model.embed(helper_texts)
    )

    best_matches = {}

    for helper_topic, helper_embedding in zip(
        potential_helpers, helper_embeddings
    ):
        similarity = float(
            cosine_similarity(request_embedding, helper_embedding)
        )

        user_id = helper_topic.user_id

        result = {
            "user": helper_topic.user,
            "topic": helper_topic.topic,
            "experience_level": helper_topic.experience_level,
            "similarity": similarity,
        }

        # Keep only the highest-scoring topic for each helper.
        if (
            user_id not in best_matches
            or similarity > best_matches[user_id]["similarity"]
        ):
            best_matches[user_id] = result

    results = list(best_matches.values())

    results.sort(
        key=lambda result: result["similarity"],
        reverse=True,
    )

    return results
