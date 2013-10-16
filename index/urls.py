from django.conf.urls import patterns, url



urlpatterns = patterns("index",
    url(r"^$", "views.index"),
)



