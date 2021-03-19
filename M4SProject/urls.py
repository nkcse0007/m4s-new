from common.upload_service import UploadService
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='M4S API')

urlpatterns = [
                  path('api/admin/', admin.site.urls),
                  path('api/swagger/', schema_view),
                  path('api/job/', include('job.urls')),
                  path('api/referal/', include('referal.urls')),
                  path('api/blog/', include('blogs.urls')),
                  path('api/course/', include('cources.urls')),
                  path('api/training/', include('training.urls')),
                  path('api/upload/', UploadService.as_view()),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
