from django.conf.urls import patterns, url



urlpatterns = patterns("index",
    url(r"^$", "views.index"),
    url(r'^download/$','views.download_file'),
)

urlpatterns += patterns("index",
    url(r"^admin/login/$", "views_admin.login"),
    url(r'^admin/$', "views_admin.admin"),
    url(r'^admin/save_link/$', "views_admin.save_link"),
    url(r'^admin/delete_link/$', "views_admin.delete_link"),
    url(r"^admin/update_link/$", "views_admin.update_link"),
    url(r'^admin/save_news/$', "views_admin.save_news"),
    url(r'^admin/update_news/$', "views_admin.update_news"),
    url(r'^admin/delete_news/$', "views_admin.delete_news"),
    url(r'^admin/save_recommend/$', "views_admin.save_recommend"),
    url(r'^admin/delete_recommend/$', "views_admin.delete_recommend"),
    url(r"^admin/update_rec/$", "views_admin.update_recommend"),
    url(r'^admin/upload_rec_pic/$', "views_admin.upload_rec_pic"),
    url(r"^admin/async_news/$", "views_admin.get_async_news"),
    url(r"^admin/async_rec/$" , "views_admin.get_async_recommend"),

)



