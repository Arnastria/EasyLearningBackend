"""SkripzBackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from main import views, api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sample/', views.sample_api),
    path('sample-restricted/', views.restricted_sample_endpoint),
    path('profile/', views.get_profile),
    path('login/', views.login),
    path('api/post/', api.api_test_post),

    path('api/course/create/', api.create_course),
    path('api/course/<int:id>/', api.get_course),
    path('api/course/get/', api.get_all_course),

    path('api/course/<int:id_course>/creatematerial/', api.create_material),
    path('api/material/<int:id>/', api.get_material),
    path('api/material/get-by-course/<int:id_course>/',
         api.get_material_by_course),
    path('api/material/get/', api.get_all_material),

    path('api/material/<int:id_material>/createpost/', api.create_post),
    path('api/post/get-by-material/<int:id_material>', api.get_post_by_material),
    path('api/post/<int:id>/', api.get_post),
    path('api/post/edit/<int:id>/', api.update_post),

    path('api/post/<int:id_post>/createreply/', api.create_reply),
    path('api/reply/get-by-post/<int:id_post>/', api.get_reply_by_post),
    path('api/reply/<int:id>/', api.get_reply),
    path('api/reply/edit/<int:id>/', api.update_reply),

    path('api/test/<int:id_material>/createtest/', api.create_course),
    path('api/test/get/<int:id>/', api.get_all_course),
    path('api/test/submit/<int:id>/', api.get_course),

    path('api/testscore/<int:id_test>/', api.create_course),

    path('api/pdf/<int:id_pdf>/', api.get_pdf),

    # path('api/', include("main.urls")),
    path('token/', views.token, name='token'),
    path('logout/', views.logout),
]
