from django.conf.urls import patterns, url



urlpatterns = patterns("index",
    url(r"^$", "views.index"),
    url(r'^admin/$', "views.admin"),
    url(r'^admin/save_link/$', "views.save_link"),
    url(r'^admin/delete_link/$', "views.delete_link"),
    url(r'^admin/save_news/$', "views.save_news"),
    url(r'^admin/delete_news/$', "views.delete_news"),
    url(r'^admin/save_recommend/$', "views.save_recommend"),
    url(r'^admin/delete_recommend/$', "views.delete_recommend"),
    url(r'^admin/upload_rec_pic/$', "views.upload_rec_pic"),
)



