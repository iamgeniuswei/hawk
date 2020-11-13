from django.db import models


# Create your models here.

class TInstitute(models.Model):
    f_name = models.CharField(max_length=128, verbose_name='机构名称')


class TAuthor(models.Model):
    f_name = models.CharField(max_length=128, verbose_name='作者名称')
    f_institute = models.ForeignKey(to=TInstitute, on_delete=models.DO_NOTHING)

class TPublication(models.Model):
    f_name = models.CharField(max_length=128, verbose_name='出版物名称')


class TArticle(models.Model):
    f_name = models.CharField(max_length=128, verbose_name='文献名称')
    f_first_author = models.ForeignKey(to=TAuthor, related_name='article_fist_author', on_delete=models.DO_NOTHING)
    f_second_author = models.ForeignKey(to=TAuthor, related_name='article_second_author', null=True, blank=True, on_delete=models.DO_NOTHING)
    f_other_authors = models.ManyToManyField('tauthor', related_name='article_other_authors')
    f_keywords = models.ManyToManyField('tkeyword', related_name='article_keywords')
    f_institutes = models.ManyToManyField('tinstitute', related_name='article_institutes')
    f_publish_time = models.PositiveIntegerField(verbose_name='发表时间')
    f_publication = models.ForeignKey(to=TPublication, on_delete=models.DO_NOTHING, verbose_name='出版物')
    f_abstract = models.TextField(verbose_name='摘要')


class TKeyword(models.Model):
    f_name = models.CharField(max_length=128, verbose_name='关键词')
    f_freq = models.PositiveIntegerField(default=0, verbose_name='频次')
    f_promote = models.PositiveIntegerField(default=0, verbose_name='首次提出')

class TProject(models.Model):
    f_name = models.CharField(max_length=128, verbose_name='分析工程名称')
    f_topic = models.CharField(max_length=128, verbose_name='分析工程主题')
    f_aritcles = models.ManyToManyField('tarticle', related_name='project_articles')
    f_time = models.DateTimeField(editable=True, verbose_name="分析时间")