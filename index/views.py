# Create your views here.

# -*- encoding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

import models
import os
from herald_index import settings

WIKI_TIP_HALF_URL = ""
WIKI_QUES_HALF_URL = "http://herald.seu.edu.cn/xyzn/faq/question/"
WIKI_REC_HALF_URL = "http://baike.baidu.com/view/7161744.htm"

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
        "rec_entry":rec_entry
    }
    return dic

def index(request):
    dics = {}
    dics.update(get_hot_dic())
    dics.update(get_wiki_dic())

    return render_to_response("Herald Index.html", dics, RequestContext(request))

def admin(request):
    return render_to_response("admin.html", {}, RequestContext(request))

# from django.views.decorators.csrf import csrf_exempt
# @csrf_exempt
def save_link(request):
    try:
        post_name = request.POST["link_name"]
        post_url = request.POST["link_url"]
        post_level = request.POST["link_level"]
        ori_links = models.Campus_site_links.objects.filter(name=post_name)
        if len(ori_links):
            ori_links[0].url = post_url
            ori_links[0].hot_level = post_level
            ori_links[0].save()
        else:
            link = models.Campus_site_links(name=post_name, url=post_url, hot_level=post_level)
            link.save()
        return HttpResponse("save link success")
    except Exception,e:
        print e
        return HttpResponse(str(e))

def delete_link(request):
    return HttpResponse("delete link success")


def save_news(request):
    """

    :param request:
    :return:
    """
    try:
        post_title = request.POST['title']
        post_link = request.POST['link']
        try:
            post_sethead = request.POST['headline']
            post_sethead = True
        except Exception,e:
            post_sethead = False
        info = models.Herald_news_list.objects.filter(url=post_link)
        if len(info):
            info[0].title = post_title
            info[0].headline = post_sethead
            info[0].save()
        else:
            news = models.Herald_news_list(title=post_title, url=post_link, is_headline=post_sethead )
            news.save()
        return HttpResponse("save news success")
    except Exception,e:
        return HttpResponse(str(e))

def delete_news(request):
    return HttpResponse("delete news success")

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def save_recommend(request):
    try:
        post_title = request.POST["rec_title"]
        post_link = request.POST["rec_link"]
        post_pic_name = request.POST["rec_pic_name"]
        post_intro = request.POST["rec_intro"]
        # pic_path = os.path.join("/media/recommend", post_pic_name).replace('\\', '/')
        ori_rec = models.Recommend_list.objects.filter(url=post_link)
        if len(ori_rec):
            ori_rec[0].title = post_title
            ori_rec[0].img_path = post_pic_name
            ori_rec[0].intro = post_intro
            ori_rec[0].save()
        else:
            rec = models.Recommend_list(title=post_title, url = post_link, img_path=post_pic_name, intro=post_intro)
            rec.save()
        return HttpResponse("publish recommend success!")
    except Exception,e:
        return HttpResponse("publish recommend failed!")

@csrf_exempt
def upload_rec_pic(request):
    import json
    post_pic = request.FILES["rec_up_pic"]
    # pic_name = post_pic.name();
    pic_name = create_filename_by_time(str(post_pic.name))
    pic = open(os.path.join(settings.MEDIA_ROOT, "recommend", pic_name).replace('\\', '/'), "wb+")
    for chunk in post_pic.chunks():
        pic.write(chunk)
    pic.close()
    return HttpResponse(json.dumps({"picname":pic_name}))

def create_filename_by_time(filename):
    import time, random
    t = time.time()
    t_str = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    rand_str = "%03d"% (random.randint(0,100))
    return t_str+rand_str+filename

def delete_recommend(request):
    return HttpResponse("delete recommend success")





