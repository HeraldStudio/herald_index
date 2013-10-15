from django.db import models

import os

# Create your models here.

class CampusSiteLinks(models.Model):
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

class HeraldNewsList(models.Model):
    title = models.CharField(max_length=50) # 取决于首页标题的字数
    url = models.URLField(max_length=200)
    is_headline = models.BooleanField(default=False)

class RecommendList(models.Model):
    media_path = "./media/recommend"
    title = models.CharField(max_length=50)
    url = models.URLField(max_length=200)
    img_path = models.FilePathField(path=media_path,recursive=True,
                                    allow_files=True, allow_folders=True,
                                    default=os.path.join(media_path, 'default.png'))
    intro = models.CharField(max_length=50)






