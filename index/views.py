# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

import models


def index(request):
    links = models.Campus_site_links.objects.all()
    latest_news_group1 = models.Herald_news_list.objects.get_latest_news(5)
    latest_news_group2 = models.Herald_news_list.objects.get_some_news(5, 10)
    latest_recs_group1 = models.Recommend_list.objects.get_some_recommends(0, 2)
    latest_recs_gruop2 = models.Recommend_list.objects.get_some_recommends(2, 4)
    headline = models.Herald_news_list.objects.get_headline()
    dics = {'links':links,
            'news_group1':latest_news_group1,
            'news_group2':latest_news_group2,
            'headline':headline,
            'recs_group1':latest_recs_group1,
            'recs_group2':latest_recs_gruop2
    }

    return render_to_response("Herald Index.html", dics, RequestContext(request))
