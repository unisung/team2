from django.contrib import admin
from django.urls import path, include
from Final.views import base_views

# from Final import views (더 이상 필요하지 않으므로 삭제)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Final/', include('Final.urls')),
    path('common/', include('common.urls')),
    path('', base_views.index, name='index'),  # '/' 에 해당되는 path
]
