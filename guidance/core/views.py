
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .matching import find_matches_for_user
from .models import Profile, UserTopic, GuidanceRequest, GuidanceOffer
from django.contrib.auth.models import User
from .forms import ProfileForm, UserTopicForm, GuidanceRequestForm, GuidanceOfferForm
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db import IntegrityError
from django.views.decorators.http import require_POST
from .ai.recommendations import find_semantic_matches
from django.views.decorators.http import require_http_methods
@login_required
def my_matches(request):
    matches = find_matches_for_user(request.user)

    semantic_matches = []

    open_requests = (
        GuidanceRequest.objects.filter(
            user=request.user,
            status=GuidanceRequest.Status.OPEN,
        )
        .order_by("-created_at")
    )

    for guidance_request in open_requests:
        recommendations = find_semantic_matches(guidance_request)

        semantic_matches.append({
            "guidance_request": guidance_request,
            "matches": recommendations,
        })

    return render(
        request,
        "core/matches.html",
        {
            "matches": matches,
            "semantic_matches": semantic_matches,
        },
    )


@login_required
def profile_detail(request, username=None):
    if username is None:
        profile_user = request.user
    else:
        profile_user = get_object_or_404(
            User,
            username=username,
        )

    profile, created = Profile.objects.get_or_create(
        user=profile_user
    )

    can_guide = UserTopic.objects.filter(
        user=profile_user,
        topic_type=UserTopic.TopicType.CAN_GUIDE,
    ).select_related("topic")

    wants_guidance = UserTopic.objects.filter(
        user=profile_user,
        topic_type=UserTopic.TopicType.WANTS_GUIDANCE,
    ).select_related("topic")

    return render(
        request,
        "core/profile.html",
        {
            "profile_user": profile_user,
            "profile": profile,
            "can_guide": can_guide,
            "wants_guidance": wants_guidance,
        },
    )

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            return redirect("my_profile")
    else:
        form = ProfileForm(instance=profile)

    return render(
        request,
        "core/edit_profile.html",
        {"form": form},
    )

@login_required
def manage_topics(request):
    if request.method == "POST":
        form = UserTopicForm(
            request.POST,
            user=request.user,
        )

        if form.is_valid():
            user_topic = form.save(commit=False)
            user_topic.user = request.user
            user_topic.save()

            messages.success(request, "Topic added successfully.")
            return redirect("manage_topics")
    else:
        form = UserTopicForm(user=request.user)

    user_topics = UserTopic.objects.filter(
        user=request.user
    ).select_related("topic").order_by("topic__name", "topic_type")

    return render(
        request,
        "core/manage_topics.html",
        {
            "form": form,
            "user_topics": user_topics,
        },
    )


@login_required
@require_POST
def remove_topic(request, topic_id):
    user_topic = get_object_or_404(
        UserTopic,
        pk=topic_id,
        user=request.user,
    )

    user_topic.delete()
    messages.success(request, "Topic removed successfully.")

    return redirect("manage_topics")
@login_required
def create_guidance_request(request):
    if request.method == "POST":
        form = GuidanceRequestForm(request.POST)

        if form.is_valid():
            guidance_request = form.save(commit=False)
            guidance_request.user = request.user
            guidance_request.save()

            messages.success(
                request,
                "Your guidance request was created successfully.",
            )
            return redirect("my_requests")
    else:
        form = GuidanceRequestForm()

    return render(
        request,
        "core/create_request.html",
        {"form": form},
    )

@login_required
def my_requests(request):
    guidance_requests = GuidanceRequest.objects.filter(
        user=request.user
    ).select_related("topic").order_by("-created_at")

    return render(
        request,
        "core/my_requests.html",
        {"guidance_requests": guidance_requests},
    )

@login_required
def browse_open_requests(request):
    open_requests = (
        GuidanceRequest.objects
        .filter(status=GuidanceRequest.Status.OPEN)
        .exclude(user=request.user)
        .select_related("user", "topic")
        .order_by("-created_at")
    )

    return render(
        request,
        "core/browse_requests.html",
        {"open_requests": open_requests},
    )

@login_required
def guidance_request_detail(request, request_id):
    guidance_request = get_object_or_404(
        GuidanceRequest.objects.select_related("user", "topic"),
        pk=request_id,
    )

    return render(
        request,
        "core/request_detail.html",
        {"guidance_request": guidance_request},
    )

@login_required
def offer_to_help(request, request_id):
    guidance_request = get_object_or_404(
        GuidanceRequest,
        pk=request_id,
    )

    if guidance_request.user_id == request.user.id:
        messages.error(request, "You cannot offer help on your own request.")
        return redirect("request_detail", request_id=request_id)

    if guidance_request.status != GuidanceRequest.Status.OPEN:
        messages.error(request, "This request is no longer open.")
        return redirect("request_detail", request_id=request_id)

    if GuidanceOffer.objects.filter(
        guidance_request=guidance_request,
        helper=request.user,
    ).exists():
        messages.info(request, "You have already offered to help with this request.")
        return redirect("request_detail", request_id=request_id)

    if request.method == "POST":
        form = GuidanceOfferForm(request.POST)

        if form.is_valid():
            offer = form.save(commit=False)
            offer.guidance_request = guidance_request
            offer.helper = request.user

            try:
                offer.save()
            except IntegrityError:
                messages.info(
                    request,
                    "You have already offered to help with this request.",
                )
            else:
                messages.success(request, "Your offer to help has been submitted.")

            return redirect("request_detail", request_id=request_id)
    else:
        form = GuidanceOfferForm()

    return render(
        request,
        "core/offer_to_help.html",
        {
            "form": form,
            "guidance_request": guidance_request,
        },
    )

@login_required
def received_offers(request, request_id):
    guidance_request = get_object_or_404(
        GuidanceRequest,
        pk=request_id,
        user=request.user,
    )

    offers = (
        GuidanceOffer.objects
        .filter(guidance_request=guidance_request)
        .select_related("helper")
        .order_by("-created_at")
    )

    return render(
        request,
        "core/received_offers.html",
        {
            "guidance_request": guidance_request,
            "offers": offers,
        },
    )

@login_required
@require_POST
def respond_to_offer(request, request_id, offer_id):

    try:
        with transaction.atomic():

            # Lock the parent request first.
            guidance_request = get_object_or_404(
                GuidanceRequest.objects.select_for_update(),
                pk=request_id,
                user=request.user,
            )

            # Retrieve the selected offer after acquiring the lock.
            offer = get_object_or_404(
                GuidanceOffer,
                pk=offer_id,
                guidance_request=guidance_request,
            )

            # Validate the current database state.
            if guidance_request.status != GuidanceRequest.Status.OPEN:
                messages.error(
                    request,
                    "This request is no longer open for decisions.",
                )
                return redirect(
                    "received_offers",
                    request_id=request_id,
                )

            if offer.status != GuidanceOffer.Status.PENDING:
                messages.error(
                    request,
                    "This offer has already been processed.",
                )
                return redirect(
                    "received_offers",
                    request_id=request_id,
                )

            action = request.POST.get("action")

            if action == "accept":

                offer.status = GuidanceOffer.Status.ACCEPTED
                offer.save(update_fields=["status"])

                guidance_request.status = GuidanceRequest.Status.IN_PROGRESS
                guidance_request.save(update_fields=["status"])

                # Decline all remaining pending offers.
                GuidanceOffer.objects.filter(
                    guidance_request=guidance_request,
                    status=GuidanceOffer.Status.PENDING,
                ).exclude(
                    pk=offer.pk
                ).update(
                    status=GuidanceOffer.Status.DECLINED
                )

                messages.success(
                    request,
                    "Offer accepted. The request is now in progress.",
                )

            elif action == "decline":

                offer.status = GuidanceOffer.Status.DECLINED
                offer.save(update_fields=["status"])

                messages.success(request, "Offer declined.")

            else:
                messages.error(request, "Invalid action.")

    except IntegrityError:
        messages.error(
            request,
            "The operation could not be completed because of a database conflict.",
        )

    return redirect("received_offers", request_id=request_id)

@login_required
def my_offers(request):
    offers = (
        GuidanceOffer.objects
        .filter(helper=request.user)
        .select_related("guidance_request", "guidance_request__user", "guidance_request__topic")
        .order_by("-created_at")
    )

    return render(
        request,
        "core/my_offers.html",
        {"offers": offers},
    )
