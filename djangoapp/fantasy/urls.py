"""fantasy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    LeagueHome,
    Rounds,
    RoundDetail,
    PlayerPointsView,
    PlayerPositionsView,
    EnterScoreView
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("league/<str:league_name>", LeagueHome.as_view(), name="league_home"),
    path("league/<str:league_name>/rounds", Rounds.as_view(), name="rounds"),
    path(
        "league/<str:league_name>/round/<int:round_number>",
        RoundDetail.as_view(),
        name="round_detail",
    ),
    path(
        "league/<str:league_name>/round/<int:round_number>/add-positions",
        PlayerPositionsView.as_view(),
        name="add_positions",
    ),
    path(
        "league/<str:league_name>/round/<int:round_number>/add-points/<int:rule_number>",
        PlayerPointsView.as_view(),
        name="add_points",
    ),
    path("league/<str:league_name>/round/<int:round_number>/add-score",
         EnterScoreView.as_view(),
         name="enter_score"),
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
]

if settings.DEBUG:
    urlpatterns += (path("__debug__/", include("debug_toolbar.urls")),)

if not settings.DEBUG:
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

