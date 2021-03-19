from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rest_framework_swagger.views import get_swagger_view

from .views import ReferFriendView

urlpatterns = [
                  path('refer-friend/', ReferFriendView.as_view()),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
