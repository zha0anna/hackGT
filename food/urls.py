from django.urls import path
from . import views

urlpatterns = [
    path("", views.listings_view, name="listings"),
    path("create/", views.create_listing_view, name="create_listing"),
    path("<int:pk>/", views.listing_detail_view, name="listing_detail"),
    path("<int:pk>/claim/", views.claim_listing_view, name="claim_listing"),
    path("<int:pk>/unclaim/", views.unclaim_listing_view, name="unclaim_listing"),
    path("my-activity/", views.my_activity_view, name="my_activity"),

]
