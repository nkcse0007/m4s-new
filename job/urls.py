from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rest_framework_swagger.views import get_swagger_view

from .views import RequestTalentView, SubmitJobView, \
    SubmitCvView, SearchJobView, FieldsView, SearchAll, ContactView

urlpatterns = [
                  path('request-talent/', RequestTalentView.as_view()),
                  path('job/', SubmitJobView.as_view()),
                  path('submit-cv/', SubmitCvView.as_view()),
                  path('search-job/', SearchJobView.as_view()),
                  path('fields/', FieldsView.as_view()),
                  path('contact/', ContactView.as_view(), name="contactus"),
                  path('search-all/', SearchAll.as_view()),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
