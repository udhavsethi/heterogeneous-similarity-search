from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^auto-complete/$', views.auto_complete, name='auto-complete'),
	url(r'^results/$', views.top_k_results, name='results'),
]