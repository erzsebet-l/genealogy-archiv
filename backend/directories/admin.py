from django.contrib import admin
from .models import (
    Clergy, ChurchWorkers, Archive, Estates, Religions,
    Provinces, Yezds, Volosts, Villages, Kinship,
    Marriage, Deaths, Statuses, Persons, BirthRecords,
    Godmen, Godmothers, Husband, Wife,
    MaleGuarantors, FemaleGuarantors, Relationships
)

# Регистрация всех моделей в админке
admin.site.register(Clergy)
admin.site.register(ChurchWorkers)
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