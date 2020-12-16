from django.db import models


# Create your models here.

class TInstitute(models.Model):
    f_name = models.CharField(max_length=128, null=False, blank=False, unique=True, verbose_name='机构名称')
    f_chinese = models.CharField(max_length=128, null=True, blank=True, verbose_name='中文名')
    f_memo = models.TextField(null=True, blank=True, verbose_name='备注')

class TDataSource(models.Model):
    f_name = models.CharField(max_length=128, null=False, blank=False, unique=True, verbose_name='文献类型')
    f_memo = models.TextField(null=True, blank=True, verbose_name='备注')

    def __str__(self):
        return self.f_name








class TPublication(models.Model):
    f_name = models.CharField(max_length=128, verbose_name='出版物名称')


class TTechDomain(models.Model):
    f_name = models.CharField(max_length=128, verbose_name='技术领域')

    def __str__(self):
        return self.f_name

class TArticle(models.Model):
    f_name = models.CharField(max_length=128, verbose_name='文献名称')
    f_authors_str = models.CharField(max_length=512, null=False, blank=False, verbose_name='作者字符串')
    # f_authors_set = models.ManyToManyField('tauthor', related_name='article_other_authors', verbose_name='作者')
    f_keywords_str = models.CharField(max_length=512, null=False, blank=False, verbose_name='关键字字符串')
    f_keywords_set = models.ManyToManyField('tkeyword', related_name='article_keywords', verbose_name='关键字')
    f_institutes_str = models.CharField(max_length=1024, null=False, blank=False, verbose_name='机构字符串')
    # f_institutes_set = models.ManyToManyField('tinstitute', related_name='article_institutes')
    f_year = models.PositiveIntegerField(verbose_name='发表年份', null=False, blank=False, default=2020)
    f_publication = models.ForeignKey(to=TPublication, on_delete=models.DO_NOTHING, verbose_name='出版物')
    f_abstract = models.TextField(verbose_name='摘要')
    f_domain = models.ManyToManyField(to=TTechDomain, related_name='article_domain', verbose_name='技术领域')
    f_source = models.ForeignKey(to=TDataSource, default=1, null=False, blank=False, verbose_name='数据源', on_delete=models.DO_NOTHING)


class TPublicationType(models.Model):
    f_type = models.CharField(max_length=128, verbose_name='出版物类型')
    f_abbr = models.CharField(max_length=128, verbose_name='出版物缩写')
    f_memo = models.TextField(verbose_name='出版物描述')

class TDocumentType(models.Model):
    f_type = models.CharField(max_length=128, verbose_name='文献类型')
    f_memo = models.TextField(verbose_name='文献描述')

class TWoSArticle(models.Model):
    f_pt = models.CharField(max_length=1024, null=True, blank=True, verbose_name='出版物类型')
    f_dt = models.CharField(max_length=1024, null=True, blank=True, verbose_name='文献类型')
    f_fu = models.CharField(max_length=1024, null=True, blank=True, verbose_name='基金资助机构与授权号')
    f_fx = models.CharField(max_length=1024, null=True, blank=True, verbose_name='基金资助正文')
    f_af = models.CharField(max_length=1024, verbose_name='文献作者')
    f_ti = models.CharField(max_length=512, verbose_name='文献标题')
    f_de = models.CharField(max_length=512, verbose_name='作者关键词')
    f_id = models.CharField(max_length=512, verbose_name='Keywords Plus')
    f_ab = models.TextField(null=True, blank=True, verbose_name='摘要')
    f_c1 = models.CharField(max_length=1024, verbose_name='作者地址')
    f_cr = models.CharField(max_length=2048, verbose_name='引用文献')
    f_nr = models.PositiveIntegerField(default=0, verbose_name='引用献数')
    f_tc = models.PositiveIntegerField(default=0, verbose_name='WoS被引数')
    f_z9 = models.PositiveIntegerField(default=0, verbose_name='总被引数')
    f_u1 = models.PositiveIntegerField(default=0, verbose_name='180天使用次数')
    f_u2 = models.PositiveIntegerField(default=0, verbose_name='2013年至今使用次数')
    f_py = models.PositiveIntegerField(default=0, verbose_name='发表年份')
    f_wc = models.CharField(max_length=256, null=True, blank=True, verbose_name='WoS类别')
    f_sc = models.CharField(max_length=256, null=True, blank=True, verbose_name='研究方向')
    f_source = models.ForeignKey(to=TDataSource, null=False, blank=False, verbose_name='文献类型', on_delete=models.DO_NOTHING)
    f_memo = models.TextField(null=True, blank=True, verbose_name='其他信息')
    f_domain = models.ManyToManyField(to=TTechDomain, related_name='wosarticle_domain', verbose_name='技术领域')
    f_keywords = models.ManyToManyField('tkeyword', related_name='wosarticle_keywords', verbose_name='关键字')

    class Meta:
        unique_together = ("f_af", "f_ti")

    def __str__(self):
        return self.f_ti


class TWoSInstitute(models.Model):
    f_name = models.CharField(max_length=128, null=False, blank=False, unique=True, verbose_name='机构名称')
    f_chinese = models.CharField(max_length=128, null=True, blank=True, verbose_name='中文名')
    f_fullname = models.CharField(max_length=128, null=True, blank=True, verbose_name='机构全名')
    f_country = models.CharField(max_length=128, null=True, blank=True, verbose_name='机构国别')
    f_articles = models.ManyToManyField('twosarticle', related_name='institute_articles', verbose_name='机构产出')
    f_memo = models.TextField(null=True, blank=True, verbose_name='备注')

    def __str__(self):
        return self.f_fullname


class TWoSAuthor(models.Model):
    f_name = models.CharField(max_length=128, verbose_name='作者名称')
    f_chinese = models.CharField(max_length=128, null=True, blank=True, verbose_name='中文名')
    f_institutes = models.ManyToManyField(to=TWoSInstitute, related_name='author_institutes', verbose_name='作者机构')
    f_memo = models.TextField(null=True, blank=True, verbose_name='备注')
    f_articles = models.ManyToManyField(to=TWoSArticle, through='TAuthorOrder',  related_name='author_articles', verbose_name='作者产出')

    def __str__(self):
        return self.f_name

class TAuthorOrder(models.Model):
    f_author = models.ForeignKey(TWoSAuthor, related_name='authororder', on_delete=models.DO_NOTHING)
    f_article = models.ForeignKey(TWoSArticle, related_name='authororder', on_delete=models.DO_NOTHING)
    f_order = models.PositiveIntegerField(default=1)


class TKeyword(models.Model):
    f_name = models.CharField(max_length=128, verbose_name='关键词')
    f_freq = models.PositiveIntegerField(default=0, verbose_name='频次')
    f_promote = models.PositiveIntegerField(default=0, verbose_name='首次提出')


class TKeywordMerging(models.Model):
    f_keyword = models.ForeignKey(TKeyword, related_name='merge_keyword', on_delete=models.DO_NOTHING, verbose_name='唯一关键词')
    f_tomerge = models.CharField(max_length=128, verbose_name='舍弃关键词')



class TProject(models.Model):
    f_name = models.CharField(max_length=128, verbose_name='分析工程名称')
    f_topic = models.CharField(max_length=128, verbose_name='分析工程主题')
    f_aritcles = models.ManyToManyField('twosarticle', related_name='project_articles')
    f_time = models.DateTimeField(editable=True, auto_now_add=False, auto_now=True ,verbose_name="分析时间")


ANALYSIS_OBJECT = (
    (1, '研究人员'),
    (2, '研究机构'),
    (3, '研究热点')
)


class TAnalysisObject(models.Model):
    f_object = models.CharField(max_length=128, verbose_name='分析对象')
    f_memo = models.TextField(null=True, blank=True, verbose_name='对象描述')

    def __str__(self):
        return self.f_object

    class Meta:
        verbose_name_plural = '分析对象'



ANALYSIS_THRESHOLD_TYPE = (
    (1, 'TOPN'),
    (2, 'TOP%N'),
    (3, 'h-index'),
    (4, 'g-index')
)

class TParserParams(models.Model):
    f_path = models.CharField(max_length=256, null=False, blank=False, verbose_name='文件路径')
    f_source = models.ForeignKey(to=TDataSource, null=False, blank=False, verbose_name='文献类型', on_delete=models.DO_NOTHING)
    f_domain = models.ManyToManyField(to=TTechDomain, null=True, blank=True, related_name='parser_domain',
                                      verbose_name='技术领域')
    f_iscluster = models.BooleanField(default=False, null=True, blank=True, verbose_name='保存项目')
    f_batchname = models.CharField(max_length=256, null=True, blank=True, verbose_name='文献描述')

    class Meta:
        managed = False


class TTopAnalysisIndex(models.Model):
    f_index = models.CharField(max_length=256, null=False, blank=False, verbose_name='分析指标')
    f_abbrv = models.CharField(max_length=256, null=False, blank=False, verbose_name='指标缩写')
    f_memo = models.TextField(null=True, blank=True, verbose_name='指标描述')

    def __str__(self):
        return self.f_index



class TTopAnalysisParams(models.Model):
    f_start = models.PositiveIntegerField(default=2000, null=True, blank=True, verbose_name='起始年度')
    f_end = models.PositiveIntegerField(default=2020, null=True, blank=True,verbose_name='终止年度')
    f_object = models.ForeignKey(to=TAnalysisObject, on_delete=models.DO_NOTHING, verbose_name='分析对象')
    f_index = models.ForeignKey(to=TTopAnalysisIndex, verbose_name='分析指标', on_delete=models.DO_NOTHING)
    f_domain = models.ManyToManyField(to=TTechDomain, null=True, blank=True, related_name='top_domain', verbose_name='技术领域')
    f_top = models.PositiveIntegerField(default=30, null=True, blank=True, verbose_name='词频TOP数')
    f_source = models.ManyToManyField(to=TDataSource, related_name='top_source', verbose_name='文献类型')



    class Meta:
        managed = False


class TCoNetworkPrune(models.Model):
    f_prune = models.CharField(max_length=256, null=False, blank=False, verbose_name='剪枝算法')
    f_memo = models.TextField(null=True, blank=True, verbose_name='算法描述')


class TCoAnalysisParams(models.Model):
    f_start = models.PositiveIntegerField(default=2000, null=True, blank=True, verbose_name='起始年度')
    f_end = models.PositiveIntegerField(default=2020, null=True, blank=True,verbose_name='终止年度')
    f_domain = models.ManyToManyField(to=TTechDomain, null=True, blank=True, related_name='co_domain',
                                      verbose_name='技术领域')
    f_source = models.ForeignKey(to=TDataSource, verbose_name='数据源', on_delete=models.DO_NOTHING)
    f_slice = models.PositiveIntegerField(default=1, null=True, blank=True, verbose_name='年份切片')
    f_object = models.PositiveIntegerField(choices=ANALYSIS_OBJECT, default=1, verbose_name='分析对象')
    f_threshold_type = models.PositiveIntegerField(choices=ANALYSIS_THRESHOLD_TYPE, default=1, verbose_name='阈值类型')
    f_threshold = models.CharField(max_length=128, null=True, blank=True, verbose_name='阈值')
    f_prune = models.ManyToManyField(to=TCoNetworkPrune, null=True, blank=True, related_name='co_prune', verbose_name='剪枝算法')

    class Meta:
        managed = False
