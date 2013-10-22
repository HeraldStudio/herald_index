
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

class Campus_site_link_Manager(models.Manager):
    def delete_link(self, lid):
        try:
            link = self.get(id=lid)
            link.delete()
            return True
        except:
            return False

    def update_link(self, id, name, url, level):
        try:
            link = self.get(id=id)
            link.name = name
            link.url = url
            link.hot_level = level
            link.save()
            return True
        except Exception,e:
            return False

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
    objects = Campus_site_link_Manager()

    def __unicode__(self):
        return self.name+","+self.url+","+ str(self.hot_level)

    class Meta:
        app_label = HOT_APP



class Herald_news_list_Manager(models.Manager):

    def get_headline(self):
        headlines = self.filter(is_headline=True)
        if len(headlines):
            tmp_headline = headlines[0]
            if len(tmp_headline.title)>20:
                tmp_headline.title = tmp_headline.title[0:20]+"..."
                return tmp_headline
            else:
                return tmp_headline
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
        tmp_news_list = []
        for news_item in news:
            if news_item.is_headline and (not meet_head):
                meet_head = True
            else:
                news_list.append(news_item)
        if len(news_list)>=end:
            tmp_news_list = news_list[begin:end]
        elif len(news_list)<=begin:
            tmp_news_list = []
        else:
            tmp_news_list = news_list[begin:]
        for news in tmp_news_list:
            if len(news.title)>18:
                news.title = news.title[0:18]+"..."
        return tmp_news_list

    def delete_news(self, id):
        try:
            news = self.get(id = id)
            news.delete()
            return True
        except Exception,e:
            return False

    def update_news(self, id,title, url, is_headline):
        try:
            news = self.get(id = id)
            news.title = title
            news.url = url
            news.is_headline = is_headline
            news.save()
            return True
        except:
            return False





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
        import logging
        logger = logging.getLogger("index")

        tmp_recs = []
        if len(recs)>=end:
            tmp_recs = recs[begin:end]
        elif len(recs)<=begin:
            tmp_recs = []
        else:
            tmp_recs = recs[begin:]
        for rec in tmp_recs:
            logger.info("标题长度:"+str(len(rec.title)))
            if len(rec.intro)>60:
                rec.intro = rec.intro[0:60]+"..."
            if len(rec.title)>25:
                rec.title = rec.title[0:25]+"..."
        return tmp_recs

    def delete_rec(self, rid):
        try:
            rec = self.get(id=rid)
            rec.delete()
            return True
        except:
            return False

    def update_rec(self, id, title, url, img_path, intro):
        try:
            rec = self.get(id=id)
            rec.title = title
            rec.url = url
            rec.img_path = img_path
            rec.intro = intro
            rec.save()
            return True
        except:
            return False


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
        tmp_ques = []
        if len(ques)<num:
            tmp_ques = ques
        else:
            tmp_ques = ques[0:num]
        for q in tmp_ques:
            if len(q.title)>20:
                q.title = q.title[0:20]+"..."
        return tmp_ques

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
        tmp_entry = []
        if len(entry)<num:
            tmp_entry = entry
        else:
            tmp_entry = entry[0:num]
        for e in tmp_entry:
            if len(e.content)>100:
                e.content = e.content[0:150]+"..."
            if len(e.title)>20:
                e.title = e.title[0:13]+"..."
        return tmp_entry

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
        tmp_acts = []
        if len(acts)<num:
            tmp_acts = acts
        else:
            tmp_acts = acts[0:num]
        for act in tmp_acts:
            if len(act.name)>8:
                act.name = act.name[0:8]+"..."
        return tmp_acts

    def get_hot_activity(self, num):
        acts = self.all().order_by("-hits_on")
        tmp_acts=[]
        if len(acts)<num:
            tmp_acts = acts
        else:
            tmp_acts = acts[0:num]
        for act in tmp_acts:
            if len(act.name)>15:
                act.name = act.name[0:15]+"..."
            if len(act.place)>16:
                act.place = act.place[0:16]+"..."
        return  tmp_acts

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


########     wrapper  #########################

class Wrapper_Manager(models.Manager):
    def save_wrapper(self,title, intro, tip, tip_url, img_name):
        try:
            obj = Wrapper(title=title, intro=intro, tip=tip, tip_url=tip_url, img_name=img_name)
            obj.save()
            return True
        except:
            return False

    def get_latest_wrapper(self, num):
        wrapper = self.all().order_by("-date")
        if len(wrapper)>num:
            return wrapper[0:num]
        else:
            return wrapper

class Wrapper(models.Model):
    title = models.CharField(max_length=20)
    intro = models.CharField(max_length=100)
    tip = models.CharField(max_length=10)
    tip_url = models.URLField(max_length=100)
    img_name = models.FilePathField()
    date = models.DateTimeField(auto_now=True)

    objects = Wrapper_Manager()

    def __unicode__(self):
        return self.title

    class Meta:
        app_label = HOT_APP


##############   wrapper db   ---------end   ##############

#############   app   ######################

class App_Manager(models.Manager):
    def get_latest_app(self, num):
        apps = self.all().order_by('-date')
        if len(apps)>num:
            return apps[0:num]
        else:
            return apps

    def save_app(self, name, intro, down_url, img_name):
        try:
            app = App(name=name, intro=intro, down_url=down_url, img_name=img_name)
            app.save()
            return True
        except:
            return False

class App(models.Model):
    name = models.CharField(max_length=20)
    intro = models.CharField(max_length=50)
    down_url = models.CharField(max_length=100)
    img_name = models.FilePathField()
    date = models.DateTimeField(auto_now=True)

    objects = App_Manager()

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = HOT_APP

###########  app   db  ----------end   ########







