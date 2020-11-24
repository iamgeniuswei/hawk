from django.db import models


# Create your models here.

class TInstitute(models.Model):
    f_name = models.CharField(max_length=128, null=False, blank=False, unique=True, verbose_name='机构名称')
    f_memo = models.TextField(null=True, blank=True, verbose_name='备注')

class TDataSource(models.Model):
    f_name = models.CharField(max_length=128, null=False, blank=False, unique=True, verbose_name='数据源')
    f_memo = models.TextField(null=True, blank=True, verbose_name='备注')



class TAuthor(models.Model):
    f_name = models.CharField(max_length=128, null=False, blank=False, verbose_name='作者名称')
    f_institute = models.ForeignKey(to=TInstitute, on_delete=models.DO_NOTHING)



class TPublication(models.Model):
    f_name = models.CharField(max_length=128, verbose_name='出版物名称')


class TTechDomain(models.Model):
    f_name = models.CharField(max_length=128, verbose_name='技术领域')

class TArticle(models.Model):
    f_name = models.CharField(max_length=128, verbose_name='文献名称')
    f_authors_str = models.CharField(max_length=512, null=False, blank=False, verbose_name='作者字符串')
    f_authors_set = models.ManyToManyField('tauthor', related_name='article_other_authors', verbose_name='作者')
    f_keywords_str = models.CharField(max_length=512, null=False, blank=False, verbose_name='关键字字符串')
    f_keywords_set = models.ManyToManyField('tkeyword', related_name='article_keywords', verbose_name='关键字')
    f_institutes_str = models.CharField(max_length=1024, null=False, blank=False, verbose_name='机构字符串')
    f_institutes_set = models.ManyToManyField('tinstitute', related_name='article_institutes')
    f_year = models.PositiveIntegerField(verbose_name='发表年份', null=False, blank=False, default=2020)
    f_publication = models.ForeignKey(to=TPublication, on_delete=models.DO_NOTHING, verbose_name='出版物')
    f_abstract = models.TextField(verbose_name='摘要')
    f_domain = models.ManyToManyField(to=TTechDomain, related_name='article_domain', verbose_name='技术领域')
    f_source = models.ForeignKey(to=TDataSource, default=1, null=False, blank=False, verbose_name='数据源', on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ('f_name', 'f_authors_str')



class TKeyword(models.Model):
    f_name = models.CharField(max_length=128, verbose_name='关键词')
    f_freq = models.PositiveIntegerField(default=0, verbose_name='频次')
    f_promote = models.PositiveIntegerField(default=0, verbose_name='首次提出')

class TProject(models.Model):
    f_name = models.CharField(max_length=128, verbose_name='分析工程名称')
    f_topic = models.CharField(max_length=128, verbose_name='分析工程主题')
    f_aritcles = models.ManyToManyField('tarticle', related_name='project_articles')
    f_time = models.DateTimeField(editable=True, verbose_name="分析时间")


ANALYSIS_OBJECT = (
    (1, '研究人员'),
    (2, '研究机构'),
    (3, '研究热点')
)



class TTopAnalysisParams(models.Model):
    f_purpose = models.CharField(max_length=128, null=True, blank=True, verbose_name='分析目的')
    f_start = models.PositiveIntegerField(default=2000, verbose_name='起始年度')
    f_end = models.PositiveIntegerField(default=2020, verbose_name='终止年度')
    f_top = models.PositiveIntegerField(default=30, verbose_name='TOP数')
    f_domain = models.ManyToManyField(to=TTechDomain, related_name='top_domain', verbose_name='技术领域')
    f_object = models.PositiveIntegerField(choices=ANALYSIS_OBJECT, default=1, verbose_name='分析对象')
