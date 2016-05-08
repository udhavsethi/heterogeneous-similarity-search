from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^auto-complete/$', views.auto_complete, name='auto-complete'),
	url(r'^get-topk-results/$', views.top_k_results, name='results'),
]