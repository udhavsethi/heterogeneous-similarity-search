from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.top_k_results, name='results')
]