from django.db import models

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
        db_table = "Estates"

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
    patronymic = models.CharField(max_length=255, verbose_name="Отчество")
    clergy = models.ForeignKey(Clergy, on_delete=models.PROTECT, verbose_name="Духовенство", db_column="clergy_id")
    
    class Meta:
        verbose_name="Священнослужитель"
        verbose_name_plural = "Священнослужители"
        db_table = "ChurchWorkers"


    def __str__(self):
        return f"{self.clergy.name}: {self.surname} {self.name} {self.patronymic}"



class Marriage(models.Model):
    marriage_id = models.BigAutoField(primary_key=True, verbose_name="Код брака")
    archive = models.ForeignKey(Archive, on_delete=models.PROTECT, db_column="archive_id", verbose_name="Код архива")
    page = models.IntegerField(verbose_name="Лист")
    page_turn = models.BooleanField(default=False, verbose_name="Оборот")
    number_record = models.IntegerField(verbose_name="Номер записи")
    date = models.DateField(verbose_name="Дата бракосочетания")
    pries = models.ForeignKey(ChurchWorkers, on_delete=models.PROTECT, db_column="pries_id", verbose_name="Код церковнослужиетля")
    comment = models.TextField(null=True, blank=True, verbose_name="Комментарий")

    class Meta:
        verbose_name = "Брак"
        verbose_name_plural = "Браки"
        ordering = ['date']
        db_table = "Marriage"



class Deaths(models.Model):
    death_id = models.BigAutoField(primary_key=True, verbose_name="Код смерти")
    archive = models.ForeignKey(Archive, on_delete=models.PROTECT, db_column="archive_id", verbose_name="Код архива")
    page = models.IntegerField( verbose_name="Лист")
    page_turn = models.BooleanField(default=False, verbose_name="Оборот")
    number_record = models.IntegerField(verbose_name="Номер записи")
    date = models.DateField(verbose_name="Дата смерти")
    age = models.IntegerField(verbose_name="Возраст")
    reason = models.CharField(max_length=255, null=True, blank=True, verbose_name="Причина смерти")
    pries = models.ForeignKey(ChurchWorkers, null=True, blank=True, on_delete=models.PROTECT, db_column="pries_id", verbose_name="Код священнослужителя")
    place = models.CharField(max_length=255, null=True, blank=True, db_column="burial_place", verbose_name="Место погребения")


    class Meta:
        verbose_name = "Смерть"
        verbose_name_plural = "Смерти"
        ordering = ['date']
        db_table = "Deaths"



class Statuses(models.Model):
    status_id = models.AutoField(primary_key=True, verbose_name="Код статуса")
    name = models.CharField(max_length=255,  verbose_name="Статус")
    date_start = models.DateField(verbose_name="Начало действия статуса")
    date_end = models.DateField(null=True, blank=True, verbose_name="Окончание действия статуса")
    marriage = models.ForeignKey(Marriage, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Код брака", db_column="marriage_id")


    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
        db_table = "Statuses"

    def __str__(self):
        return f"{self.name} {self.date_start} - {self.date_end}"



class Persons(models.Model):
    GENDER_CHOICES = [('М', 'Мужской'),('Ж', 'Женский')]

    person_id = models.BigAutoField(primary_key=True, verbose_name="Код персоны")
    name = models.CharField(max_length=255, verbose_name="Имя")
    surname = models.CharField(max_length=255, verbose_name="Фамилия")
    patronymic = models.CharField(max_length=255, verbose_name="Отчество")
    date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    sex = models.CharField(max_length=1, choices=GENDER_CHOICES)
    status = models.ForeignKey(Statuses, on_delete=models.PROTECT, db_column="status_id", verbose_name="Код статуса")
    estate = models.ForeignKey(Estates, on_delete=models.PROTECT, db_column="estate_id", verbose_name="Код сословия")
    creed = models.ForeignKey(Religions, on_delete=models.PROTECT, db_column="creed_id", verbose_name="Код веры")
    death = models.ForeignKey(Deaths, null=True, blank=True, on_delete=models.SET_NULL, db_column="death_id", verbose_name="Код смерти")
    province = models.ForeignKey(Provinces, on_delete=models.PROTECT, db_column="province_id", verbose_name="Губерния")
    yezd = models.ForeignKey(Yezds, on_delete=models.PROTECT, db_column="yezd_id", verbose_name="Уезд")
    volost = models.ForeignKey(Volosts, on_delete=models.PROTECT, db_column="volost_id", verbose_name="Волость")
    village = models.ForeignKey(Villages, on_delete=models.PROTECT, db_column="village_id", verbose_name="Село")
    duplicate = models.IntegerField(default=0, verbose_name="Дубликат")
    comment = models.TextField(null=True, blank=True, verbose_name="Комментарий")


    class Meta:
        verbose_name = "Персона"
        verbose_name_plural = "Персоны"
        ordering = ['surname', 'name', 'patronymic']
        db_table = "Persons"

    def __str__(self):
        return f"{self.name} {self.surname} {self.patronymic} ({self.duplicate})"




class BirthRecords(models.Model):
    GENDER_CHOICES = [('М', 'Мужской'),('Ж', 'Женский')]
    
    birth_id = models.BigAutoField(primary_key=True, verbose_name="Код рождения")
    archive = models.ForeignKey(Archive, on_delete=models.PROTECT, db_column="archive_id", verbose_name="Код архива")
    page = models.IntegerField(verbose_name="Лист")
    page_turn = models.BooleanField(default=False, verbose_name="Оборот")
    number_record = models.IntegerField(verbose_name="Номер записи")
    person = models.ForeignKey(Persons, on_delete=models.PROTECT, db_column="person_id", verbose_name="Код персоны")
    sex = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Пол")
    date_of_baptism = models.DateField(verbose_name="Дата крещения")
    comment = models.TextField(null=True, blank=True, verbose_name="Комментарий")
    pries = models.ForeignKey(ChurchWorkers, on_delete=models.PROTECT, db_column="pries_id", verbose_name="Код священнослужителя")


    class Meta:
        verbose_name = "Рождение"
        verbose_name_plural = "Рождения"
        db_table = "BirthRecords"

    def __str__(self):
        return f"{self.person.name} {self.person.patronymic} {self.person.surname}"




    
class Godmen(models.Model):
    godmen_id = models.BigAutoField(primary_key=True, verbose_name="Код восприемника-мужчины")
    person = models.ForeignKey(Persons, on_delete=models.PROTECT, db_column="person_id", verbose_name="Код персоны")
    birth = models.ForeignKey(BirthRecords, on_delete=models.PROTECT, db_column="birth_id", verbose_name="Код рождения")

    class Meta:
        verbose_name = "Восприемник - мужчина"
        verbose_name_plural = "Восприемники - мужчины"
        db_table = "Godmen"

    def __str__(self):
        return f"{self.person.name} {self.person.patronymic} {self.person.surname} в рождении № {self.birth.birth_id}"
    



class Godmothers(models.Model):
    godmother_id = models.BigAutoField(primary_key=True, verbose_name="Код восприемника-женщины")
    person = models.ForeignKey(Persons, on_delete=models.PROTECT, db_column="person_id", verbose_name="Код персоны")
    birth = models.ForeignKey(BirthRecords, on_delete=models.PROTECT, db_column="birth_id", verbose_name="Код рождения")

    class Meta:
        verbose_name = "Восприемник - женщина"
        verbose_name_plural = "Восприемники - женщины"
        db_table = "Godmothers"

    def __str__(self):
        return f"{self.person.name} {self.person.patronymic} {self.person.surname} в рождении № {self.birth.birth_id}"
    


class Husband(models.Model):
    man_id = models.BigAutoField(primary_key=True, verbose_name="Код жениха")
    person = models.ForeignKey(Persons, on_delete=models.PROTECT, db_column="person_id", verbose_name="Код персоны")
    marriage = models.ForeignKey(Marriage, on_delete=models.PROTECT,  db_column="marriage_id", verbose_name="Код брака")
    number_marriage = models.IntegerField( verbose_name="Номер брака")
    age = models.IntegerField(verbose_name="Возраст")

    class Meta:
        verbose_name = "Жених"
        verbose_name_plural = "Женихи"
        db_table = "Husband"
    
    def __str__(self):
        return f"{self.person.name} {self.person.patronymic} {self.person.surname} в браке № {self.marriage.marriage_id}"



class Wife(models.Model):
    wife_id = models.BigAutoField(primary_key=True, verbose_name="Код невесты")
    person = models.ForeignKey(Persons, on_delete=models.PROTECT, db_column="person_id", verbose_name="Код персоны")
    marriage = models.ForeignKey(Marriage, on_delete=models.PROTECT, db_column="marriage_id", verbose_name="Код брака")
    number_marriage = models.IntegerField(verbose_name="Номер брака")
    age = models.IntegerField(verbose_name="Возраст")

    class Meta:
        verbose_name = "Невеста"
        verbose_name_plural = "Невесты"
        db_table = "Wife"
    
    def __str__(self):
        return f"{self.person.name} {self.person.patronymic} {self.person.surname} в браке № {self.marriage.marriage_id}"



class MaleGuarantors(models.Model):
    guarantors_id = models.BigAutoField(primary_key=True, verbose_name="Код поручителя-мужчины")
    person = models.ForeignKey(Persons, on_delete=models.PROTECT, db_column="person_id", verbose_name="Код персоны")
    marriage = models.ForeignKey(Marriage, on_delete=models.PROTECT, db_column="marriage_id", verbose_name="Код брака")


    class Meta:
        verbose_name = "Поручитель - мужчина"
        verbose_name_plural = "Поручители - мужчины"
        db_table = "MaleGuarantors"

    def __str__(self):
        return f"{self.person.name} {self.person.patronymic} {self.person.surname} в браке № {self.marriage.marriage_id}"




class FemaleGuarantors(models.Model):
    guarantors_id = models.BigAutoField(primary_key=True, verbose_name="Код поручителя-женщины")
    person = models.ForeignKey(Persons, on_delete=models.PROTECT, db_column="person_id", verbose_name="Код персоны")
    marriage = models.ForeignKey(Marriage, on_delete=models.PROTECT, db_column="marriage_id", verbose_name="Код брака")


    class Meta:
        verbose_name = "Поручитель - женщина"
        verbose_name_plural = "Поручители - женщины"
        db_table = "FemaleGuarantors"

    def __str__(self):
        return f"{self.person.name} {self.person.patronymic} {self.person.surname} в браке № {self.marriage.marriage_id}"



class Relationships(models.Model):
    relationship_id = models.BigAutoField(primary_key=True, verbose_name="Код отношений")
    who = models.ForeignKey(Persons, on_delete=models.PROTECT, related_name='relations_from', db_column="person1_id", verbose_name="Код персоны - кто")
    whom = models.ForeignKey(Persons, on_delete=models.PROTECT, related_name='relations_to', db_column="person2_id", verbose_name="Код персоны - кому")
    kinship = models.ForeignKey(Kinship, on_delete=models.PROTECT,  db_column="kinship_id", verbose_name="Код родства")
    birth = models.ForeignKey(BirthRecords, on_delete=models.PROTECT, null=True, blank=True, db_column="birth_id", verbose_name="Код рождения")
    marriage = models.ForeignKey(Marriage, on_delete=models.PROTECT, null=True, blank=True, db_column="marriage_id", verbose_name="Код брака")

    class Meta:
        verbose_name = "Отношение"
        verbose_name_plural = "Отношения"
        db_table = "Relationships"

    def __str__(self):
        return f"{self.who.name} {self.who.patronymic} {self.who.surname} - {self.kinship.name} для {self.whom.name} {self.whom.patronymic} {self.whom.surname}"



