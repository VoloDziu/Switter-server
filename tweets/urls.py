from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^fetch$', views.fetch),
    url(r'^test$', views.test)
]
