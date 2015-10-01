from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'cove.input.views.input', name='index'),
    url(r'^data/(.+)$', 'cove.views.explore', name='explore'),
    url(r'^dataload/$', 'cove.dataload.views.dataload', name='dataload'),
    url(r'^dataload/([^/]+)/$', 'cove.dataload.views.dataset', name='dataload_dataset'),
    url(r'^dataload/([^/]+)/([^/]+)$', 'cove.dataload.views.run_process', name='dataload_dataset'),
    url(r'^stats', 'cove.views.stats', name='stats'),
]
