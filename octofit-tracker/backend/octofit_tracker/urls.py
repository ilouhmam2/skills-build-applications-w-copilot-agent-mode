"""octofit_tracker URL Configuration

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
from django.urls import path
from django.http import JsonResponse
from django.views.generic.base import RedirectView
import os


def api_root(request):
    """Return API base endpoints using the Codespace hostname when available.

    This constructs absolute URLs like:
      https://$CODESPACE_NAME-8000.app.github.dev/api/activities/

    - If the env var CODESPACE_NAME is present, we use the app.github.dev URL
      so the frontend can point to the Codespace-hosted backend without
      hard-coding values.
    - Otherwise we fall back to the current request host/scheme.
    """
    codespace = os.environ.get('CODESPACE_NAME')
    # Allow overriding the scheme used for Codespace URLs. Default to https.
    scheme = os.environ.get('CODESPACE_API_SCHEME', 'https')
    if codespace:
        base = f"{scheme}://{codespace}-8000.app.github.dev"
    else:
        # Use the incoming request host/scheme as a safe fallback
        scheme = request.scheme
        host = request.get_host()
        base = f"{scheme}://{host}"

    # Components exposed by the API. Keep these in sync with your app's endpoints.
    endpoints = {
        'activities': f"{base}/api/activities/",
        'users': f"{base}/api/users/",
        'teams': f"{base}/api/teams/",
        'leaderboard': f"{base}/api/leaderboard/",
        'workouts': f"{base}/api/workouts/",
    }
    return JsonResponse(endpoints)


urlpatterns = [
    path('admin/', admin.site.urls),
    # Redirect root URL to the API root so a visit to `/` returns the API mapping
    path('', RedirectView.as_view(url='/api/', permanent=False)),
    path('api/', api_root, name='api-root'),
]
