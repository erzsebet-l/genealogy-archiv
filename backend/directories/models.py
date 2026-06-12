from django.db import models
from django.conf import settings


class Clergy(models.Model):
    clergy_id = models.BigAutoField(primary_key=True, verbose_name="Код духовенства")
    name = models.CharField(max_length=255, verbose_name="Духовенство")

    class Meta:
        verbose_name = "Степень духовенства"
        verbose_name_plural = "Степени духовенства"
        db_table = "Clergy"

    def __str__(self):
        return self.name


class Estates(models.Model):
    estate_id = models.AutoField(primary_key=True, verbose_name="Код сословия")
    name = models.CharField(max_length=255, verbose_name="Сословие")

    class Meta:
        verbose_name = "Сословие"
        verbose_name_plural = "Сословия"
        ordering = ['name']
        db_table = "Estates"

    def __str__(self):
        return self.name


class Religions(models.Model):
    creed_id = models.AutoField(primary_key=True, verbose_name="Код веры")
    name = models.CharField(max_length=255, verbose_name="Вера")

    class Meta:
        verbose_name = "Вероисповедание"
        verbose_name_plural = "Вероисповедания"
        ordering = ['name']
        db_table = "Religions"

    def __str__(self):
        return self.name


class Archive(models.Model):
    archive_id = models.BigAutoField(primary_key=True, verbose_name="Код архива")
    name = models.CharField(max_length=255, verbose_name="Архив")
    number_case = models.CharField(max_length=255, verbose_name="Номер дела")
    year = models.IntegerField(verbose_name="Год индексации")

    class Meta:
        verbose_name = "Архив"
        verbose_name_plural = "Архивы"
        db_table = "Archive"

    def __str__(self):
        return f"{self.name} - {self.number_case} ({self.year})"


class Provinces(models.Model):
    province_id = models.AutoField(primary_key=True, verbose_name="Код губернии")
    name = models.CharField(max_length=255, verbose_name="Губерния")

    class Meta:
        verbose_name = "Губерния"
        verbose_name_plural = "Губернии"
        ordering = ['name']
        db_table = "Provinces"

    def __str__(self):
        return self.name


class Yezds(models.Model):
    yezd_id = models.AutoField(primary_key=True, verbose_name="Код уезда")
    name = models.CharField(max_length=255, verbose_name="Уезд")

    class Meta:
        verbose_name = "Уезд"
        verbose_name_plural = "Уезды"
        ordering = ['name']
        db_table = "Yezds"

    def __str__(self):
        return self.name


class Volosts(models.Model):
    volost_id = models.AutoField(primary_key=True, verbose_name="Код волости")
    name = models.CharField(max_length=255, verbose_name="Волость")

    class Meta:
        verbose_name = "Волость"
        verbose_name_plural = "Волости"
        ordering = ['name']
        db_table = "Volosts"

    def __str__(self):
        return self.name


class Villages(models.Model):
    village_id = models.AutoField(primary_key=True, verbose_name="Код села")
    name = models.CharField(max_length=255, verbose_name="Село")

    class Meta:
        verbose_name = "Село"
        verbose_name_plural = "Сёла"
        ordering = ['name']
        db_table = "Villages"

    def __str__(self):
        return self.name


class Kinship(models.Model):
    kinship_id = models.AutoField(primary_key=True, verbose_name="Код родства")
    name = models.CharField(max_length=255, verbose_name="Родство")

    class Meta:
        verbose_name = "Родство"
        verbose_name_plural = "Родство"
        ordering = ['name']
        db_table = "Kinship"

    def __str__(self):
        return self.name


class ChurchWorkers(models.Model):
    pries_id = models.BigAutoField(primary_key=True, verbose_name="Код священнослужителя")
    name = models.CharField(max_length=255, verbose_name="Имя")
    surname = models.CharField(max_length=255, verbose_name="Фамилия")
    patronymic = models.CharField(max_length=255, null=True, blank=True, verbose_name="Отчество")
    clergy = models.ForeignKey(
        Clergy, on_delete=models.PROTECT,
        verbose_name="Духовенство", db_column="clergy_id"
    )

    class Meta:
        verbose_name = "Священнослужитель"
        verbose_name_plural = "Священнослужители"
        db_table = "ChurchWorkers"

    def __str__(self):
        return f"{self.clergy.name}: {self.surname} {self.name} {self.patronymic or ''}"


class StatusChoice(models.Model):
    status_choice_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, verbose_name="Статус")
 
    class Meta:
        verbose_name = "Статус (справочник)"
        verbose_name_plural = "Статусы (справочник)"
        ordering = ['name']
        db_table = "StatusChoices"
 
    def __str__(self):
        return self.name
 

class Persons(models.Model):
    GENDER_CHOICES = [('М', 'Мужской'), ('Ж', 'Женский')]

    person_id = models.BigAutoField(primary_key=True, verbose_name="Код персоны")
    name = models.CharField(max_length=255, verbose_name="Имя")
    surname = models.CharField(max_length=255, verbose_name="Фамилия")
    patronymic = models.CharField(max_length=255, verbose_name="Отчество")
    date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    sex = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Пол")
    # Это поле остается как есть - оно ссылается на статус персоны
    status = models.ForeignKey(StatusChoice, on_delete=models.PROTECT, db_column="status_choice_id", verbose_name="Код статуса",
        null=True, blank=True, related_name="persons")
    estate = models.ForeignKey(Estates, on_delete=models.PROTECT,db_column="estate_id", verbose_name="Сословие", null=True, blank=True)
    creed = models.ForeignKey(Religions, on_delete=models.PROTECT,null=True, blank=True,db_column="creed_id", verbose_name="Вероисповедание")
    province = models.ForeignKey(Provinces, null=True, blank=True, on_delete=models.PROTECT,db_column="province_id", verbose_name="Губерния")
    yezd = models.ForeignKey(Yezds, null=True, blank=True, on_delete=models.PROTECT,db_column="yezd_id", verbose_name="Уезд")
    volost = models.ForeignKey(Volosts, null=True, blank=True, on_delete=models.PROTECT,db_column="volost_id", verbose_name="Волость")
    village = models.ForeignKey(Villages, null=True, blank=True, on_delete=models.PROTECT,db_column="village_id", verbose_name="Село")
    duplicate = models.IntegerField(default=0, verbose_name="Дубликат")
    comment = models.TextField(null=True, blank=True, verbose_name="Комментарий")

    class Meta:
        verbose_name = "Персона"
        verbose_name_plural = "Персоны"
        ordering = ['surname', 'name', 'patronymic']
        db_table = "Persons"

    def __str__(self):
        return f"{self.surname} {self.name} {self.patronymic} ({self.duplicate})"


class Statuses(models.Model):
    status_id = models.AutoField(primary_key=True)
    person = models.ForeignKey(Persons, on_delete=models.CASCADE,db_column="person_id", verbose_name="Персона",related_name="statuses",)
    status_choice = models.ForeignKey(StatusChoice, on_delete=models.PROTECT,db_column="status_choice_id", verbose_name="Статус",)
    date_start = models.DateField(verbose_name="Начало действия")
    date_end = models.DateField(null=True, blank=True, verbose_name="Конец действия")
    marriage = models.ForeignKey('Marriage', on_delete=models.PROTECT,null=True, blank=True,db_column="marriage_id", verbose_name="Брак",)
 
    class Meta:
        verbose_name = "Статус персоны"
        verbose_name_plural = "Статусы персон"
        ordering = ['date_start']
        db_table = "Statuses"
 
    def __str__(self):
        return f"{self.person} — {self.status_choice.name} c {self.date_start}"


class DraftRecord(models.Model):
    RECORD_TYPES = [
        ('birth',    'Рождение'),
        ('marriage', 'Брак'),
        ('death',    'Смерть'),
    ]
 
    draft_id = models.BigAutoField(primary_key=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,db_column="created_by_id", verbose_name="Пользователь",related_name="drafts",)
    record_type = models.CharField(max_length=10, choices=RECORD_TYPES, verbose_name="Тип записи")
    payload = models.JSONField(verbose_name="Данные формы (JSON)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_record_id = models.BigIntegerField(null=True, blank=True, verbose_name="ID опубликованной записи")
 
    class Meta:
        verbose_name = "Черновик"
        verbose_name_plural = "Черновики"
        ordering = ['-updated_at']
        db_table = "DraftRecords"
 
    def __str__(self):
        return f"[{self.record_type}] черновик #{self.draft_id} — {self.created_by}"


class CanonicalName(models.Model):
    canonical_id = models.BigAutoField(primary_key=True, verbose_name="Код канонического имени")
    person = models.ForeignKey(Persons, on_delete=models.PROTECT,verbose_name="Код персоны", db_column="person_id",null=True, blank=True)
    can_name = models.CharField(max_length=255, unique=True, verbose_name="Каноническое имя")
    gender = models.CharField(max_length=1, choices=[('М', 'Мужской'), ('Ж', 'Женский')],verbose_name="Пол")

    class Meta:
        db_table = "CanonicalNames"
        verbose_name = "Каноническое имя"
        verbose_name_plural = "Канонические имена"

    def __str__(self):
        return self.can_name


class Marriage(models.Model):
    marriage_id = models.BigAutoField(primary_key=True, verbose_name="Код брака")
    archive = models.ForeignKey(Archive, on_delete=models.PROTECT,db_column="archive_id", verbose_name="Архив")
    page = models.IntegerField(verbose_name="Лист")
    page_turn = models.BooleanField(default=False, verbose_name="Оборот")
    number_record = models.IntegerField(verbose_name="Номер записи")
    date = models.DateField(verbose_name="Дата бракосочетания")
    pries = models.ForeignKey(ChurchWorkers, on_delete=models.PROTECT, null=True, blank=True,db_column="pries_id", verbose_name="Священнослужитель")
    comment = models.TextField(null=True, blank=True, verbose_name="Комментарий")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,db_column="created_by_id", verbose_name="Создал пользователь",related_name="marriages_created")

    class Meta:
        verbose_name = "Брак"
        verbose_name_plural = "Браки"
        ordering = ['date']
        db_table = "Marriage"


class Deaths(models.Model):
    death_id = models.BigAutoField(primary_key=True, verbose_name="Код смерти")
    archive = models.ForeignKey(Archive, on_delete=models.PROTECT,db_column="archive_id", verbose_name="Архив")
    person = models.ForeignKey(Persons, on_delete=models.PROTECT,db_column="person_id", verbose_name="Персона",null=True, blank=True, related_name="death_records")
    page = models.IntegerField(verbose_name="Лист")
    page_turn = models.BooleanField(default=False, verbose_name="Оборот")
    number_record = models.IntegerField(verbose_name="Номер записи")
    number_record_book = models.IntegerField(null=True, blank=True, verbose_name="Номер записи в книге")
    sex = models.CharField(max_length=1, choices=[('М', 'Мужской'), ('Ж', 'Женский')], verbose_name="Пол")
    date = models.DateField(verbose_name="Дата смерти")
    death_month = models.IntegerField(null=True, blank=True, verbose_name="Месяц смерти")
    death_day = models.IntegerField(null=True, blank=True, verbose_name="Число смерти")
    burial_day = models.IntegerField(null=True, blank=True, verbose_name="Число погребения")
    age = models.IntegerField(null=True, blank=True, verbose_name="Возраст")
    cause_of_death = models.CharField(max_length=255, null=True, blank=True, verbose_name="Причина смерти")
    buried_by = models.CharField(max_length=255, null=True, blank=True, verbose_name="Кем погребён")
    pries = models.ForeignKey(ChurchWorkers, null=True, blank=True, on_delete=models.PROTECT,db_column="pries_id", verbose_name="Священнослужитель")
    burial_place = models.CharField(max_length=255, null=True, blank=True,db_column="burial_place", verbose_name="Место погребения")
    comment = models.TextField(null=True, blank=True, verbose_name="Комментарий")
    province = models.ForeignKey(Provinces, null=True, blank=True, on_delete=models.PROTECT,db_column="province_id", verbose_name="Губерния")
    yezd = models.ForeignKey(Yezds, null=True, blank=True, on_delete=models.PROTECT,db_column="yezd_id", verbose_name="Уезд")
    volost = models.ForeignKey(Volosts, null=True, blank=True, on_delete=models.PROTECT,db_column="volost_id", verbose_name="Волость")
    village = models.ForeignKey(Villages, null=True, blank=True, on_delete=models.PROTECT,db_column="village_id", verbose_name="Село")
    estate = models.ForeignKey(Estates, null=True, blank=True, on_delete=models.PROTECT,db_column="estate_id", verbose_name="Сословие")
    kinship = models.ForeignKey(Kinship, null=True, blank=True, on_delete=models.PROTECT,db_column="kinship_id", verbose_name="Степень родства")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,db_column="created_by_id", verbose_name="Создал пользователь",related_name="deaths_created")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Смерть"
        verbose_name_plural = "Смерти"
        ordering = ['-date']
        db_table = "Deaths"

    def __str__(self):
        if self.person:
            return f"{self.person.surname} {self.person.name} — {self.date}"
        return f"Смерть #{self.death_id} — {self.date}"


class DeathRecordPriest(models.Model):
    id = models.BigAutoField(primary_key=True)
    death = models.ForeignKey(Deaths, on_delete=models.CASCADE,related_name='priests', db_column="death_id",verbose_name="Запись о смерти")
    name = models.CharField(max_length=255, verbose_name="Имя")
    surname = models.CharField(max_length=255, verbose_name="Фамилия")
    patronymic = models.CharField(max_length=255, null=True, blank=True, verbose_name="Отчество")
    clergy = models.ForeignKey(Clergy, on_delete=models.SET_NULL, null=True, blank=True,verbose_name='Степень духовенства')
    church_worker = models.ForeignKey(ChurchWorkers, null=True, blank=True, on_delete=models.SET_NULL,db_column="pries_id", verbose_name="Священнослужитель из базы")

    class Meta:
        db_table = "DeathRecordsPriests"
        verbose_name = "Священник при смерти"
        verbose_name_plural = "Священники при смерти"

    def __str__(self):
        return f"{self.surname} {self.name} → смерть #{self.death_id}"


class BirthRecords(models.Model):
    GENDER_CHOICES = [('М', 'Мужской'), ('Ж', 'Женский')]

    birth_id = models.BigAutoField(primary_key=True, verbose_name="Код рождения")
    archive = models.ForeignKey(Archive, on_delete=models.PROTECT,db_column="archive_id", verbose_name="Архив")
    page = models.IntegerField(verbose_name="Лист")
    page_turn = models.BooleanField(default=False, verbose_name="Оборот")
    number_record = models.IntegerField(verbose_name="Номер записи")
    person = models.ForeignKey(Persons, on_delete=models.PROTECT,db_column="person_id", verbose_name="Персона",related_name="birth_records")
    sex = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Пол")
    birth_month = models.IntegerField(null=True, blank=True, verbose_name="Месяц рождения")
    birth_day = models.IntegerField(null=True, blank=True, verbose_name="Число рождения")
    baptism_day = models.IntegerField(null=True, blank=True, verbose_name="Число крещения")
    date_of_baptism = models.DateField(verbose_name="Дата крещения")
    father_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Имя отца")
    father_patronymic = models.CharField(max_length=255, null=True, blank=True, verbose_name="Отчество отца")
    father_surname = models.CharField(max_length=255, null=True, blank=True, verbose_name="Фамилия отца")
    father_estate = models.ForeignKey(Estates, null=True, blank=True, on_delete=models.PROTECT,db_column="father_estate_id", verbose_name="Сословие отца",related_name="birth_fathers")
    father_province = models.ForeignKey(Provinces, null=True, blank=True, on_delete=models.PROTECT,db_column="father_province_id", verbose_name="Губерния отца",related_name="birth_fathers_province")
    father_yezd = models.ForeignKey(Yezds, null=True, blank=True, on_delete=models.PROTECT,db_column="father_yezd_id", verbose_name="Уезд отца",related_name="birth_fathers_yezd")
    father_volost = models.ForeignKey(Volosts, null=True, blank=True, on_delete=models.PROTECT,db_column="father_volost_id", verbose_name="Волость отца",related_name="birth_fathers_volost")
    father_village = models.ForeignKey(Villages, null=True, blank=True, on_delete=models.PROTECT,db_column="father_village_id", verbose_name="Село отца",related_name="birth_fathers_village")
    mother_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Имя матери")
    mother_patronymic = models.CharField(max_length=255, null=True, blank=True, verbose_name="Отчество матери")
    mother_surname = models.CharField(max_length=255, null=True, blank=True, verbose_name="Фамилия матери")
    mother_status = models.CharField(max_length=50, null=True, blank=True,verbose_name="Статус матери",help_text="законная / вдова / другое")
    comment = models.TextField(null=True, blank=True, verbose_name="Комментарий")
    scan = models.ImageField(upload_to='scans/births/%Y/%m/',null=True, blank=True,verbose_name="Скан документа")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,db_column="created_by_id", verbose_name="Создал пользователь",related_name="birth_records_created")

    class Meta:
        verbose_name = "Рождение"
        verbose_name_plural = "Рождения"
        db_table = "BirthRecords"

    def __str__(self):
        return f"{self.person.surname} {self.person.name} {self.person.patronymic}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if not any([
            self.father_province_id,
            self.father_yezd_id,
            self.father_volost_id,
            self.father_village_id,
        ]):
            raise ValidationError(
                "Укажите хотя бы одно поле местоположения отца: "
                "губернию, уезд, волость или село."
            )


class BirthRecordsPriest(models.Model):
    id = models.BigAutoField(primary_key=True)
    birth = models.ForeignKey(BirthRecords, on_delete=models.CASCADE,related_name='priests', db_column="birth_id",verbose_name="Запись о рождении")
    name = models.CharField(max_length=255, verbose_name="Имя")
    surname = models.CharField(max_length=255, verbose_name="Фамилия")
    clergy = models.ForeignKey(Clergy, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Степень духовенства')
    church_worker = models.ForeignKey(ChurchWorkers, null=True, blank=True, on_delete=models.SET_NULL,db_column="pries_id", verbose_name="Священнослужитель из базы")

    class Meta:
        db_table = "BirthRecordsPriests"
        verbose_name = "Священник при рождении"
        verbose_name_plural = "Священники при рождении"

    def __str__(self):
        return f"{self.surname} {self.name} → рождение #{self.birth_id}"


class Godmen(models.Model):
    godmen_id = models.BigAutoField(primary_key=True, verbose_name="Код восприемника-мужчины")
    birth = models.ForeignKey(BirthRecords, on_delete=models.CASCADE,db_column="birth_id", verbose_name="Запись о рождении",related_name="godmen")
    name = models.CharField(max_length=255, verbose_name="Имя")
    patronymic = models.CharField(max_length=255, null=True, blank=True, verbose_name="Отчество")
    surname = models.CharField(max_length=255, null=True, blank=True, verbose_name="Фамилия")
    province = models.ForeignKey(Provinces, null=True, blank=True, on_delete=models.PROTECT,db_column="province_id", verbose_name="Губерния")
    yezd = models.ForeignKey(Yezds, null=True, blank=True, on_delete=models.PROTECT,db_column="yezd_id", verbose_name="Уезд")
    volost = models.ForeignKey(Volosts, null=True, blank=True, on_delete=models.PROTECT,db_column="volost_id", verbose_name="Волость")
    village = models.ForeignKey(Villages, null=True, blank=True, on_delete=models.PROTECT,db_column="village_id", verbose_name="Село")
    estate = models.ForeignKey(Estates, null=True, blank=True, on_delete=models.PROTECT,db_column="estate_id", verbose_name="Сословие")
    person = models.ForeignKey(Persons, null=True, blank=True, on_delete=models.SET_NULL,db_column="person_id", verbose_name="Персона в базе", related_name="godmen_records")
    creed = models.ForeignKey(Religions, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Вероисповедание')

    class Meta:
        verbose_name = "Восприемник (мужчина)"
        verbose_name_plural = "Восприемники (мужчины)"
        db_table = "Godmen"

    def __str__(self):
        return f"{self.surname or ''} {self.name} {self.patronymic or ''} → рождение #{self.birth_id}"


class Godmothers(models.Model):
    godmother_id = models.BigAutoField(primary_key=True, verbose_name="Код восприемницы")
    birth = models.ForeignKey(BirthRecords, on_delete=models.CASCADE, db_column="birth_id", verbose_name="Запись о рождении", related_name="godmothers")
    name = models.CharField(max_length=255, verbose_name="Имя")
    patronymic = models.CharField(max_length=255, null=True, blank=True, verbose_name="Отчество")
    surname = models.CharField(max_length=255, null=True, blank=True, verbose_name="Фамилия")
    province = models.ForeignKey(Provinces, null=True, blank=True, on_delete=models.PROTECT,db_column="province_id", verbose_name="Губерния")
    yezd = models.ForeignKey(Yezds, null=True, blank=True, on_delete=models.PROTECT,db_column="yezd_id", verbose_name="Уезд")
    volost = models.ForeignKey(Volosts, null=True, blank=True, on_delete=models.PROTECT,db_column="volost_id", verbose_name="Волость")
    village = models.ForeignKey(Villages, null=True, blank=True, on_delete=models.PROTECT,db_column="village_id", verbose_name="Село")
    estate = models.ForeignKey(Estates, null=True, blank=True, on_delete=models.PROTECT,db_column="estate_id", verbose_name="Сословие")
    status = models.ForeignKey(StatusChoice, on_delete=models.PROTECT,db_column="status_choice_id", verbose_name="Код статуса",null=True, blank=True)
    person = models.ForeignKey(Persons, null=True, blank=True, on_delete=models.SET_NULL,db_column="person_id", verbose_name="Персона в базе",related_name="godmothers_records")
    creed = models.ForeignKey(Religions, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Вероисповедание')

    class Meta:
        verbose_name = "Восприемница (женщина)"
        verbose_name_plural = "Восприемницы (женщины)"
        db_table = "Godmothers"

    def __str__(self):
        return f"{self.surname or ''} {self.name} {self.patronymic or ''} → рождение #{self.birth_id}"


class Husband(models.Model):
    man_id = models.BigAutoField(primary_key=True, verbose_name="Код жениха")
    person = models.ForeignKey(Persons, on_delete=models.PROTECT,db_column="person_id", verbose_name="Персона",related_name="marriages_as_husband")
    marriage = models.ForeignKey(Marriage, on_delete=models.PROTECT,db_column="marriage_id", verbose_name="Брак",related_name="husbands")
    number_marriage = models.IntegerField(verbose_name="Номер брака")
    age = models.IntegerField(verbose_name="Возраст")

    class Meta:
        verbose_name = "Жених"
        verbose_name_plural = "Женихи"
        db_table = "Husband"

    def __str__(self):
        return f"{self.person.surname} {self.person.name} → брак #{self.marriage_id}"


class Wife(models.Model):
    wife_id = models.BigAutoField(primary_key=True, verbose_name="Код невесты")
    person = models.ForeignKey(Persons, on_delete=models.PROTECT,db_column="person_id", verbose_name="Персона",related_name="marriages_as_wife")
    marriage = models.ForeignKey(Marriage, on_delete=models.PROTECT,db_column="marriage_id", verbose_name="Брак",related_name="wives")
    number_marriage = models.IntegerField(verbose_name="Номер брака")
    age = models.IntegerField(verbose_name="Возраст")

    class Meta:
        verbose_name = "Невеста"
        verbose_name_plural = "Невесты"
        db_table = "Wife"

    def __str__(self):
        return f"{self.person.surname} {self.person.name} → брак #{self.marriage_id}"


class MaleGuarantors(models.Model):
    guarantors_id = models.BigAutoField(primary_key=True, verbose_name="Код поручителя-мужчины")
    person = models.ForeignKey(Persons, on_delete=models.PROTECT,db_column="person_id", verbose_name="Персона",related_name="male_guarantors")
    marriage = models.ForeignKey(Marriage, on_delete=models.PROTECT,db_column="marriage_id", verbose_name="Брак",related_name="male_guarantors")

    class Meta:
        verbose_name = "Поручитель (мужчина)"
        verbose_name_plural = "Поручители (мужчины)"
        db_table = "MaleGuarantors"

    def __str__(self):
        return f"{self.person.surname} {self.person.name} → брак #{self.marriage_id}"


class FemaleGuarantors(models.Model):
    guarantors_id = models.BigAutoField(primary_key=True, verbose_name="Код поручителя-женщины")
    person = models.ForeignKey(Persons, on_delete=models.PROTECT,db_column="person_id", verbose_name="Персона",related_name="female_guarantors")
    marriage = models.ForeignKey(Marriage, on_delete=models.PROTECT,db_column="marriage_id", verbose_name="Брак",related_name="female_guarantors")

    class Meta:
        verbose_name = "Поручитель (женщина)"
        verbose_name_plural = "Поручители (женщины)"
        db_table = "FemaleGuarantors"

    def __str__(self):
        return f"{self.person.surname} {self.person.name} → брак #{self.marriage_id}"


class Relationships(models.Model):
    relationship_id = models.BigAutoField(primary_key=True, verbose_name="Код отношений")
    who = models.ForeignKey(Persons, on_delete=models.PROTECT,related_name='relations_from', db_column="person1_id", verbose_name="Кто")
    whom = models.ForeignKey(Persons, on_delete=models.PROTECT,related_name='relations_to', db_column="person2_id", verbose_name="Кому")
    kinship = models.ForeignKey(Kinship, on_delete=models.PROTECT,db_column="kinship_id", verbose_name="Родство")
    birth = models.ForeignKey(BirthRecords, on_delete=models.PROTECT,null=True, blank=True, db_column="birth_id", verbose_name="Запись о рождении")
    marriage = models.ForeignKey(Marriage, on_delete=models.PROTECT,null=True, blank=True, db_column="marriage_id", verbose_name="Брак")

    class Meta:
        verbose_name = "Отношение"
        verbose_name_plural = "Отношения"
        db_table = "Relationships"

    def __str__(self):
        return (
            f"{self.who.surname} {self.who.name} — "
            f"{self.kinship.name} для "
            f"{self.whom.surname} {self.whom.name}"
        )


class MarriageRecordPriest(models.Model):
    id = models.BigAutoField(primary_key=True)
    marriage = models.ForeignKey(Marriage, on_delete=models.CASCADE,related_name='priests', db_column="marriage_id",verbose_name="Запись о браке")
    name = models.CharField(max_length=255, verbose_name="Имя")
    surname = models.CharField(max_length=255, verbose_name="Фамилия")
    patronymic = models.CharField(max_length=255, null=True, blank=True, verbose_name="Отчество")
    clergy = models.ForeignKey(Clergy, on_delete=models.SET_NULL, null=True, blank=True,verbose_name='Степень духовенства')
    church_worker = models.ForeignKey(ChurchWorkers, null=True, blank=True, on_delete=models.SET_NULL,db_column="pries_id", verbose_name="Священнослужитель из базы")

    class Meta:
        db_table = "MarriageRecordsPriests"
        verbose_name = "Священник при браке"
        verbose_name_plural = "Священники при браке"

    def __str__(self):
        return f"{self.surname} {self.name} → брак #{self.marriage_id}"