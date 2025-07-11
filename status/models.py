from django.db import models
from django.core.exceptions import ValidationError

def image_upload_path(instance, filename):
    model_name = instance.__class__.__name__  # 예: 'Nation', 'City' 등
    pk = instance.pk if instance.pk else 'temp'  # 저장 전이면 None이므로 대비
    return f'{model_name}/{pk}/{filename}'

# Create your models here.
class Nation(models.Model):
    nation_id = models.AutoField(primary_key=True)
    nation_name = models.CharField(max_length=20, verbose_name="국가 이름")
    nation_info = models.TextField(verbose_name="국가 정보")
    nation_economic = models.TextField(null=True, blank=True, verbose_name="국가 경제현황")
    nation_relation = models.TextField(null=True, blank=True, verbose_name="우리나라와의 관계")
    # nation_image = models.ImageField(upload_to=image_upload_path, blank=True, null=True)

    class Meta:
        verbose_name_plural = "(국가관련 모델) Nations"

    def __str__(self):
        return f"{self.nation_name}"
    
class LocalGoverment(models.Model):
    local_id = models.AutoField(primary_key=True)
    local_name = models.CharField(max_length=50, verbose_name="지방자치단체 이름")
    # local_image = models.ImageField(upload_to=image_upload_path, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "(지자체관련 모델) LocalGoverments"
    
    def __str__(self):
        return f"{self.local_name}"

class NationDashboard(models.Model):
    nation_dash_id = models.AutoField(primary_key=True)
    nation = models.OneToOneField(Nation, on_delete=models.CASCADE)

    nation_map_explain = models.TextField(verbose_name="교류 현황 설명")
    nation_ratio_explain = models.TextField(verbose_name="분야별 교류 비율 설명")
    nation_ratio_explain_detail = models.TextField(verbose_name="분야별 교류 비율 상세 설명")
    nation_recent_explain = models.TextField(verbose_name="최근 교류 사례 설명")
    nation_num_tend = models.TextField(verbose_name="교류 사업 수 추이 설명")
    # dash_image = models.ImageField(upload_to=image_upload_path, blank=True, null=True)

    class Meta:
        verbose_name_plural = "(국가관련 모델) NationDashboards"

    def __str__(self):
        return f"{self.nation_dash_id} : {self.nation} 대시보드"

class LocalDashboard(models.Model):
    local_dash_id = models.AutoField(primary_key=True)
    local = models.OneToOneField(LocalGoverment, on_delete=models.CASCADE)

    local_map_explain = models.TextField(verbose_name="교류 현황 설명")
    local_sister_explain = models.TextField(verbose_name="자매도시 설명")
    local_friendly_explain = models.TextField(verbose_name="우호 결연 도시 설명")
    local_ratio_explain = models.TextField(verbose_name="주요 교류국 순위 설명")
    local_ratio_explain_detail = models.TextField(verbose_name="주요 교류국 순위 상세 설명")
    local_category_explain = models.TextField(verbose_name="주요 교류 분야 설명")
    local_vision_explain = models.TextField(verbose_name="비전 설명")

    class Meta:
        verbose_name_plural = "(지자체관련 모델) LocalDashboards"

    def __str__(self):
        return f"{self.local_dash_id} : {self.local} 대시보드"

class ExchangeData(models.Model):
    CATEGORIES = [
        ('health', '보건/환경/기술'), # 보건 환경 기술
        ('edu', '교육/역량강화'),
        ('culture', '문화/공공외교'),
        ('system', '제도/행정/포용'),
        ('etc', '기타')
    ]
    exchange_id = models.AutoField(primary_key=True)
    exchange_name_kr = models.CharField(max_length=100, null=True, blank=True, verbose_name="교류 데이터 국문 이름")
    exchange_name_en = models.CharField(max_length=100, null=True, blank=True, verbose_name="교류 데이터 영문 이름")
    exchange_category = models.CharField(max_length=50, choices=CATEGORIES, default='etc', verbose_name="분야", null=True, blank=True)
    exchange_content = models.TextField(verbose_name="교류 데이터 내용", null=True, blank=True)
    exchange_nation = models.ForeignKey(Nation, on_delete=models.CASCADE)
    start_year = models.PositiveIntegerField(null=True, blank=True, verbose_name="시작 연도")
    end_year = models.PositiveIntegerField(null=True, blank=True, verbose_name="종료 연도")
    others = models.TextField(verbose_name="기타사항", null=True, blank=True)
    pub_date = models.DateField(verbose_name="등록일", null=True, blank=True)

    class Meta:
        verbose_name_plural = "[공공데이터] (국가관련 모델) ExchangeDatas"

    def __str__(self):
        return f"{self.exchange_id} : {self.exchange_nation} - {self.get_exchange_category_display()} - {self.exchange_name_kr}"
    
class LocalData(models.Model):
    LOCAL_CATEGORIES = [
        ('sister', '자매도시'),
        ('friendly', '우호결연 도시')
    ]
    local_data_id = models.AutoField(primary_key=True)
    origin_city = models.ForeignKey(LocalGoverment, on_delete=models.CASCADE)
    partner_country = models.CharField(max_length=50, verbose_name="대상 국가")
    partner_city = models.CharField(max_length=70, verbose_name="대상 도시")
    category = models.CharField(max_length=50, choices=LOCAL_CATEGORIES, verbose_name="도시 구분")
    agreement_date = models.DateField(verbose_name="결연일자")

    class Meta:
        verbose_name_plural = "[공공데이터] (지자체관련 모델) LocalDatas"

    def __str__(self):
        return f"{self.local_data_id} : {self.origin_city} - {self.partner_city} {"("+self.get_category_display()+")"}"

# 주요 교류 분야
class ExchangeCategory(models.Model):
    CATEGORIES = [
        ('health', '보건/환경/기술'),
        ('edu', '교육/역량강화'),
        ('culture', '문화/공공외교'),
        ('system', '제도/행정/포용'),
        ('etc', '기타'),
    ]
    exchange_category_id = models.AutoField(primary_key=True)
    local = models.ForeignKey(LocalGoverment, on_delete=models.CASCADE, related_name='exchange_category_relations')
    exchange_name = models.CharField(max_length=50, choices=CATEGORIES, verbose_name="교류 분야 이름")
    exchange_num = models.PositiveIntegerField(verbose_name="교류 분야 수(또는 순위)")

    class Meta:
        unique_together = ('local', 'exchange_name') 
        verbose_name_plural = "(지자체관련 모델) ExchangeCategories"

    def __str__(self):
        return f"{self.exchange_category_id} : {self.local} - {self.get_exchange_name_display()} - {self.exchange_num}"
    
class Vision(models.Model):
    vision_id = models.AutoField(primary_key=True)
    vision_category = models.CharField(max_length=30, verbose_name="분류")
    local = models.ForeignKey(LocalGoverment, on_delete=models.CASCADE)
    vision_title = models.CharField(max_length=50, verbose_name="제목")
    vision_content = models.TextField(verbose_name="내용")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일자")

    class Meta:
        ordering = ['-created_at']  # 최신 순으로 정렬
        verbose_name_plural = "(지자체관련 모델) Visions"

    def __str__(self):
        return f"{self.vision_id} : [{self.local.local_name}] {self.vision_title}"