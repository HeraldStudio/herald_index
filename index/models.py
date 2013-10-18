
# -*- encoding: utf-8 -*-

from django.db import models

import os

import conf

# Create your models here.

# class Campus_site_links_Manager(models.Manager):
#     def add_link(self, link_name, link_url, link_level):
#         obj = Campus_site_links(name=link_name, url=link_url, hot_level=link_level)
#         obj.save()

LEAGUE_APP = conf.APP_NAME_LEAGUE
WIKI_APP = conf.APP_NAME_WIKI
HOT_APP = conf.APP_NAME_HOT


###################  hot app db   ###################

class Campus_site_links(models.Model):
    COMM = 0
    HOT = 1
    HOT_LEVEL = (
        (COMM, "common"),
        (HOT, "hot"),
    )
    name = models.CharField(max_length=50)
    url = models.URLField(max_length=100)
    hot_level = models.IntegerField(max_length=1,
                                    choices=HOT_LEVEL,
                                    default=COMM) # 热度、点击量等级，可以取两种值：0代表普通，1代表热门

    def __unicode__(self):
        return self.name+","+self.url+","+ str(self.hot_level)

    class Meta:
        app_label = HOT_APP



class Herald_news_list_Manager(models.Manager):

    def get_headline(self):
        headlines = self.filter(is_headline=True)
        if len(headlines):
            return headlines[0]
        else:
            return None

    def get_latest_news(self, num):
        return self.get_some_news(0, num)

    def get_some_news(self, begin, end):
        '''
        不包括第end条.
        '''
        news = self.all()
        news_list = []
        meet_head = False
        for news_item in news:
            if news_item.is_headline and (not meet_head):
                meet_head = True
            else:
                news_list.append(news_item)
        if len(news_list)>=end:
            return news_list[begin:end]
        elif len(news_list)<=begin:
            return []
        else:
            return news_list[begin:]





class Herald_news_list(models.Model):
    title = models.CharField(max_length=50) # 取决于首页标题的字数
    url = models.URLField(max_length=200)
    is_headline = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True, auto_now_add=False)

    objects = Herald_news_list_Manager()

    class Meta:
        ordering = ['-date']
        app_label = HOT_APP

    def __unicode__(self):
        return self.title + str(self.date)


class Recommend_list_Manager(models.Manager):
    def get_latest_recommends(self, num):
        return self.get_some_recommends(0, num)

    def get_some_recommends(self, begin, end):
        recs = self.all()
        if len(recs)>=end:
            return recs[begin:end]
        elif len(recs)<=begin:
            return []
        else:
            return recs[begin:]


class Recommend_list(models.Model):
    media_path = "../media/recommend"
    title = models.CharField(max_length=50)
    url = models.URLField(max_length=200)
    img_path = models.FilePathField(path=media_path,recursive=True,
                                    allow_files=True, allow_folders=True,
                                    default=os.path.join(media_path, 'default.png').replace('\\', '/'))
    intro = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now=True)

    objects = Recommend_list_Manager()

    class Meta:
        ordering = ['-date']
        app_label = HOT_APP


    def __unicode__(self):
        return self.title+str(self.date)


###############  hot app db  ----     end   ##################


###############  wiki app db   ##########################

class Wiki_question_Manager(models.Manager):
    def get_hot_questions(self, num):
        ques = self.all().order_by('-skim_nums')
        if len(ques)<num:
            return ques
        else:
            return ques[0:num]

    def get_new_questions(self, num):
        ques = self.all().order_by('-ask_date')
        if len(ques)<num:
            return ques
        else:
            return ques[0:num]

class Wiki_question(models.Model):
    id = models.IntegerField()
    title = models.CharField(max_length=200)
    ask_date = models.DateTimeField()
    skim_nums = models.IntegerField()

    objects = Wiki_question_Manager()

    class Meta:
        app_label = WIKI_APP
        db_table = conf.VIEW_NAME_WIKI_QUESTION

class Recommend_entry_Manager(models.Manager):

    def get_new_rec_entry(self, num):
        import logging
        logger = logging.getLogger("index")
        entry = self.all().order_by("-publish_date")
        # logger.info("推荐词条共："+str(len(entry)))
        if len(entry)<num:
            return entry
        else:
            return entry[0:num]

class Recommend_entry(models.Model):
    id  = models.IntegerField()
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=500)
    img_href = models.CharField(max_length=200)
    publish_date = models.DateTimeField()

    objects = Recommend_entry_Manager()

    class Meta:
        db_table = conf.VIEW_NAME_WIKI_REC_ENTRY
        app_label = conf.APP_NAME_WIKI

class Entry_Manager(models.Manager):
    def get_hot_entry(self, num):
        entry = self.all().order_by("skim_nums")
        if len(entry)<num:
            return entry
        else:
            return entry[0:num]


class Entry(models.Model):
    id = models.IntegerField()
    title = models.CharField(max_length=50)
    skim_nums = models.IntegerField()

    objects = Entry_Manager()

    class Meta:
        app_label = conf.APP_NAME_WIKI
        db_table = conf.VIEW_NAME_WIKI_HOT_ENTRY


################  wiki app db  ----    end   #########################

###############   league app db   ########################

class ActivityManager(models.Manager):
    def get_latest_activity(self, num):
        acts = self.all().order_by("release_time")
        if len(acts)<num:
            return acts
        else:
            return acts[0:num]

    def get_hot_activity(self, num):
        acts = self.all().order_by("-hits_on")
        if len(acts)<num:
            return acts
        else:
            return acts[0:num]

class Activity(models.Model):
    id = models.IntegerField()
    name = models.CharField(max_length=255)
    post_add = models.CharField(max_length=255)
    release_time = models.CharField()
    hits_on = models.IntegerField()
    hold_time = models.DateTimeField()
    place = models.CharField(max_length=50)

    objects = ActivityManager()

    class Meta:
        app_label = conf.APP_NAME_LEAGUE
        db_table = conf.VIEW_NAME_LEAGUE_ACTIVITY


class AlbumManager(models.Manager):
    def get_latest_album(self, num):
        album = self.all().order_by("pub_date")
        if len(album)<num:
            return album
        else:
            return album[0:num]

class Album(models.Model):
    id = models.IntegerField()
    cover_address = models.CharField(max_length=255)
    pub_date = models.DateTimeField()

    objects = AlbumManager()

    class Meta:
        app_label = conf.APP_NAME_LEAGUE
        db_table = conf.VIEW_NAME_LEAGUE_ALBUM



##############   league app db   ----- end   #################










