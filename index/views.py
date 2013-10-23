
# -*- encoding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

import models
import os
from herald_index import settings
import  conf

WIKI_TIP_HALF_URL = ""
WIKI_QUES_HALF_URL = "http://herald.seu.edu.cn/xyzn/faq/question/"
WIKI_REC_HALF_URL = "http://baike.baidu.com/view/7161744.htm"

LEAGUE_DETAIL_HALF_URL = ""

import logging
logger = logging.getLogger("index")

OPERATE_FAILED = "False"


def get_hot_dic():
    #####  hot module
    links = models.Campus_site_links.objects.all()
    latest_news_group1 = models.Herald_news_list.objects.get_latest_news(5)
    latest_news_group2 = models.Herald_news_list.objects.get_some_news(5, 10)
    latest_recs_group1 = models.Recommend_list.objects.get_some_recommends(0, 2)
    latest_recs_gruop2 = models.Recommend_list.objects.get_some_recommends(2, 4)
    headline = models.Herald_news_list.objects.get_headline()
    #####
    dic = {'links':links,
            'news_group1':latest_news_group1,
            'news_group2':latest_news_group2,
            'headline':headline,
            'recs_group1':latest_recs_group1,
            'recs_group2':latest_recs_gruop2
    }
    return dic

def get_wiki_dic():
    new_ques = models.Wiki_question.objects.get_new_questions(5)
    hot_ques = models.Wiki_question.objects.get_hot_questions(5)
    hot_tips = models.Entry.objects.get_hot_entry(50)
    rec_entry = models.Recommend_entry.objects.get_new_rec_entry(1)

    dic = {
        "wiki_ques_half_url":WIKI_QUES_HALF_URL,
        "wiki_tip_half_url":WIKI_TIP_HALF_URL,
        "wiki_rec_entry_half_url":WIKI_REC_HALF_URL,
        "new_ques":new_ques,
        "hot_ques":hot_ques,
        "hot_tips":hot_tips,
        "rec_entry":rec_entry[0]
    }
    return dic

def get_league_dic():
    new_acti = models.Activity.objects.get_latest_activity(8)
    hot_acti = models.Activity.objects.get_hot_activity(6)
    album = models.Album.objects.get_latest_album(3)

    dic = {
        "hot_acti":hot_acti,
        "new_acti":new_acti,
        "album":album,
        "acti_detail_half_url":LEAGUE_DETAIL_HALF_URL
    }

    return dic


def get_wrapper():
    wrapper = models.Wrapper.objects.get_latest_wrapper(conf.WRAPPER_NUM)
    logger.debug("wrapper有："+ str(len(wrapper)))
    dic = {
        "wrapper":wrapper
    }
    return dic

def get_app():
    apps = models.App.objects.get_latest_app(conf.APP_NUM)
    dic = {
        "apps":apps
    }
    return dic



def index(request):
    try:
        dics = {}
        ####  ori dics
        dics.update(get_hot_dic())
        dics.update(get_wrapper())
        dics.update(conf.URL_DIC)
        dics.update(get_app())
        #### module dic  added here   #####
        #dics.update(get_wiki_dic())   ##### wiki module
        #dics.update(get_league_dic())    ######  league  module
        return render_to_response("herald_index.html", dics, RequestContext(request))
    except Exception,e:
        logger.debug(e)
        return HttpResponse(OPERATE_FAILED)



def download_file(request):
    try:
        f = open("F:/Workspace-Py/herald_index/static/down.zip","rb")
        data = f.read()
        f.close()
        res = HttpResponse(data, mimetype="application/octet-stream")
        res["Content-Disposition"] = "attachment; fileName=%s"%("app.zip")
        return res
    except Exception,e:
        logger.debug(e)
        return HttpResponse(OPERATE_FAILED)





