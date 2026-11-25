from django.urls import include, path
from .views import my_matches
from django.contrib.auth import views as auth_views
from .views import my_offers,respond_to_offer,received_offers,offer_to_help,guidance_request_detail, browse_open_requests, my_matches, profile_detail, edit_profile, manage_topics, remove_topic, create_guidance_request, my_requests
urlpatterns = [
    path("matches/", my_matches, name="my_matches"),
    path("accounts/login/",auth_views.LoginView.as_view(template_name="core/login.html"),name="login",),
    path("profile/", profile_detail, name="my_profile"),
    path("users/<str:username>/", profile_detail, name="user_profile"),
    path("profile/edit/", edit_profile, name="edit_profile"),
    path("topics/", manage_topics, name="manage_topics"),
    path("topics/<int:topic_id>/remove/",remove_topic,name="remove_topic",),
    path("requests/create/",create_guidance_request,name="create_request",),
    path("requests/mine/", my_requests, name="my_requests"),
    path("requests/browse/",browse_open_requests,name="browse_requests",),
    path("requests/<int:request_id>/",guidance_request_detail,name="request_detail",),
    path("requests/<int:request_id>/offer/",offer_to_help,name="offer_to_help",),
    path("requests/<int:request_id>/offers/",received_offers,name="received_offers",),
    path("requests/<int:request_id>/offers/<int:offer_id>/respond/",respond_to_offer,name="respond_to_offer",),
    path("offers/mine/", my_offers, name="my_offers"),

]