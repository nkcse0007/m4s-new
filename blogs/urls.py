from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rest_framework_swagger.views import get_swagger_view
from django.views.decorators.csrf import csrf_protect
from .views import BlogView, CommentView, LikeView, CommentReplyView

urlpatterns = [
                  path('blog/', csrf_protect(BlogView.as_view())),
                  path('comment/', CommentView.as_view()),
                  path('comment-reply/', CommentReplyView.as_view()),
                  path('like/', LikeView.as_view()),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
