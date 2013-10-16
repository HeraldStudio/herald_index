
# -*- encoding: utf-8 -*-

from django.db import models

import os

# Create your models here.

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
                                    default=os.path.join(media_path, 'default.png'))
    intro = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now=True)

    objects = Recommend_list_Manager()

    class Meta:
        ordering = ['-date']

    def __unicode__(self):
        return self.title+str(self.date)













