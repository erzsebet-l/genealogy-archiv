from django.contrib import admin
from .models import (
    Clergy, Archive, Estates, Religions,
    Provinces, Yezds, Volosts, Villages, Kinship,
    Marriage, Deaths, Statuses, Persons, BirthRecords,
    Godmen, Godmothers, Husband, Wife, DeathRecordPriest,
    MaleGuarantors, FemaleGuarantors, Relationships, StatusChoice, DraftRecord, BirthRecordsPriest, MarriageRecordPriest
)
from users.models import UserManager, User 

# Регистрация всех моделей в админке
admin.site.register(Clergy)
admin.site.register(Archive)
admin.site.register(Estates)
admin.site.register(Religions)
admin.site.register(Provinces)
admin.site.register(Yezds)
admin.site.register(Volosts)
admin.site.register(Villages)
admin.site.register(Kinship)
admin.site.register(Marriage)
admin.site.register(Deaths)
admin.site.register(Statuses)
admin.site.register(Persons)
admin.site.register(BirthRecords)
admin.site.register(Godmen)
admin.site.register(Godmothers)
admin.site.register(Husband)
admin.site.register(Wife)
admin.site.register(MaleGuarantors)
admin.site.register(FemaleGuarantors)
admin.site.register(Relationships)
admin.site.register(StatusChoice)
admin.site.register(DraftRecord)
admin.site.register(BirthRecordsPriest)
admin.site.register(DeathRecordPriest)
admin.site.register(MarriageRecordPriest)
admin.site.register(User)