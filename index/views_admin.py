
# -*- encoding: utf-8 -*-

import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, Template, Context

import models
from herald_index import settings


import conf

import logging
logger = logging.getLogger("index")

OPERATE_SUCCESS = "True"
OPERATE_FAILED = "False"

##########  login   #############
from django.contrib.auth import authenticate
from django.contrib import auth
def login(request):
    try:
        username = request.POST["username"]
        pwd = request.POST["password"]
        user = authenticate(username=username,password=pwd)
        if user is not None:
            auth.login(request,user)
            return HttpResponseRedirect("/index/admin/")
        else:
            return render_to_response("admin_login.html",{"error":"用户名或密码错误"}, RequestContext(request))
    except Exception,e:
        logger.debug(request.user.is_authenticated())
        return render_to_response("admin_login.html",{}, RequestContext(request))


###########  login   end   ############

###########    index    ################

def get_new_list():
    news_list = models.Herald_news_list.objects.get_latest_news(conf.ITEM_NUM_IN_ONE_PAGE)
    dic = {
        "news_list":news_list,
    }
    return dic

def get_rec_list():
    rec_list = models.Recommend_list.objects.get_latest_recommends(conf.ITEM_NUM_IN_ONE_PAGE)
    dic = {
        "rec_list":rec_list
    }
    return dic

def get_link_list():
    link_list = models.Campus_site_links.objects.all()
    dic = {
        "link_list":link_list
    }
    return dic
    # json_ori = []
    # for link in link_list:
    #     dic = {
    #         "name":link.name,
    #         "url":link.url,
    #         "id":link.id,
    #         "level":link.hot_level
    #     }
    #     json_ori.append(dic)



def admin(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/index/admin/login/")
    dics = {}
    dics.update(get_new_list())
    dics.update(get_rec_list())
    dics.update(get_link_list())
    return render_to_response("admin.html", dics, RequestContext(request))

############   index end    ##################

###############   link   begin   #####################

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
    try:
        id = int(request.POST["id"])
        if models.Campus_site_links.objects.delete_link(id):
            return HttpResponse(OPERATE_SUCCESS)
        else:
            return HttpResponse(OPERATE_FAILED)
    except:
        return HttpResponse(OPERATE_FAILED)

def update_link(request):
    try:
        id = int(request.POST["id"])
        name = request.POST["name"]
        url = request.POST["url"]
        level = int(request.POST['level'])
        if models.Campus_site_links.objects.update_link(id, name, url, level):
            return HttpResponse(OPERATE_SUCCESS)
        else:
            return HttpResponse(OPERATE_FAILED)
    except Exception,e:
        logger.debug(str(e))
        return HttpResponse(OPERATE_FAILED)


##########  link   end    ##################

###########   news  begin   ################

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
            if post_sethead=='true':

                post_sethead = True
            else:
                post_sethead = False
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

def update_news(request):
    id = int(request.POST['id'])
    title = request.POST['title']
    url = request.POST['url']
    is_headline = request.POST['headline']
    if models.Herald_news_list.objects.update_news(id, title, url, is_headline):
        return HttpResponse(OPERATE_SUCCESS)
    else:
        return HttpResponse(OPERATE_FAILED)

def get_async_news(request):
    page = int(request.GET["page_num"])
    news_list = models.Herald_news_list.objects.get_some_news(
        conf.ITEM_NUM_IN_ONE_PAGE*(page-1),
        conf.ITEM_NUM_IN_ONE_PAGE*page)
    json_ori = []
    for news in news_list:
        tmp_dic = {
            "id": news.id,
            "title":news.title,
            "url":news.url,
            "date": str(news.date),
            "headline":news.is_headline
        }
        json_ori.append(tmp_dic)
    return HttpResponse(json.dumps(json_ori))

def delete_news(request):
    try:
        id = int(request.POST["id"])
        if models.Herald_news_list.objects.delete_news(id):
            return HttpResponse(OPERATE_SUCCESS)
        else:
            return HttpResponse(OPERATE_FAILED)
    except:
        return HttpResponse(OPERATE_FAILED)


###################    news    end   #################


##################   recommend   begin   ##############

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
    import json, os
    post_pic = request.FILES["rec_up_pic"]
    # logger.debug("上传文件type："+type(post_pic))
    pic_name = create_filename_by_time(post_pic.name)
    pic_full_path = os.path.join(settings.MEDIA_ROOT, "recommend", pic_name).replace('\\', '/')
    pic = open(pic_full_path, "wb+")
    for chunk in post_pic.chunks():
        pic.write(chunk)
    pic.close()
    import tools
    tools.resize_and_save_img((100,150), pic_full_path)

    return HttpResponse(json.dumps({"picname":pic_name}))

def create_filename_by_time(filename):
    logger.debug(filename)
    import time, random
    t = time.time()
    t_str = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    rand_str = "%03d"% (random.randint(0,100))
    return t_str+rand_str+filename

def delete_recommend(request):
    try:
        id = request.POST["id"]
        if models.Recommend_list.objects.delete_rec(id):
            return HttpResponse(OPERATE_SUCCESS)
        else:
            return HttpResponse(OPERATE_FAILED)
    except Exception,e:
        logger.debug(str(e))
        return HttpResponse(OPERATE_FAILED)

def update_recommend(request):
    try:
        id = int(request.POST["id"])
        title = request.POST["title"]
        link = request.POST["url"]
        img_path = request.POST["img_path"]
        intro = request.POST['intro']
        if models.Recommend_list.objects.update_rec(id, title, link, img_path, intro):
            return HttpResponse(OPERATE_SUCCESS)
        else:
            return HttpResponse(OPERATE_FAILED)
    except Exception,e:
        logger.debug(str(e))
        return HttpResponse(OPERATE_FAILED)

def get_async_recommend(request):
    try:
        page = int(request.GET["page_num"])
        rec_list = models.Recommend_list.objects.get_some_recommends(
            conf.ITEM_NUM_IN_ONE_PAGE*(page-1),
            conf.ITEM_NUM_IN_ONE_PAGE*page
        )
        ori_json = []
        for rec in rec_list:
            dic = {
                "id":rec.id,
                "title":rec.title,
                "intro":rec.intro,
                "url":rec.url,
                "date":str(rec.date)
            }
            ori_json.append(dic)
        return HttpResponse(json.dumps(ori_json))
    except Exception,e:
        logger.debug(str(e))
        return HttpResponse(OPERATE_FAILED)





###########   recommend    end           ############################
