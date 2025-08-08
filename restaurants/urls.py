from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (MenuViewSet, RestaurantViewSet, TodayMenuList,
                    TodayResultsView, VoteViewSet)

router = DefaultRouter()
router.register(r"restaurants", RestaurantViewSet, basename="restaurant")
router.register(r"menus", MenuViewSet, basename="menu")
router.register(r"votes", VoteViewSet, basename="vote")

urlpatterns = [
    path("", include(router.urls)),
    path("menus/today/", TodayMenuList.as_view(), name="menus-today"),
    path("votes/today/", TodayResultsView.as_view(), name="votes-today"),
]
