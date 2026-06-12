from rest_framework import serializers

from .models import (
    Archive, Estates,Religions,Provinces,Yezds,Volosts,Villages,Persons,BirthRecords,Godmen,Godmothers,BirthRecordsPriest,
    ChurchWorkers,Statuses,StatusChoice,Clergy,DraftRecord,Kinship,Deaths,DeathRecordPriest,Relationships,Marriage,
    MarriageRecordPriest,Husband, Wife, MaleGuarantors, FemaleGuarantors,
)


class MarriageRecordPriestSerializer(serializers.ModelSerializer):
    clergy_name = serializers.CharField(source='clergy.name', read_only=True)
    
    class Meta:
        model = MarriageRecordPriest
        fields = '__all__'


class RelationshipsSerializer(serializers.ModelSerializer):
    who_name = serializers.SerializerMethodField()
    whom_name = serializers.SerializerMethodField()
    kinship_name = serializers.CharField(source='kinship.name', read_only=True)
    
    class Meta:
        model = Relationships
        fields = '__all__'
    
    def get_who_name(self, obj):
        if obj.who:
            return f"{obj.who.surname} {obj.who.name} {obj.who.patronymic}".strip()
        return None
    
    def get_whom_name(self, obj):
        if obj.whom:
            return f"{obj.whom.surname} {obj.whom.name} {obj.whom.patronymic}".strip()
        return None


class ArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Archive
        fields = '__all__'


class EstateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estates
        fields = '__all__'


class ReligionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Religions
        fields = '__all__'


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provinces
        fields = '__all__'


class YezdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Yezds
        fields = '__all__'


class VolostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volosts
        fields = '__all__'


class VillageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Villages
        fields = '__all__'


class ClergySerializer(serializers.ModelSerializer):
    class Meta:
        model = Clergy
        fields = ['clergy_id', 'name']


class ChurchWorkerSerializer(serializers.ModelSerializer):
    clergy_name = serializers.CharField(source='clergy.name', read_only=True)
    clergy_id = serializers.IntegerField(source='clergy.clergy_id', read_only=True)

    class Meta:
        model = ChurchWorkers
        fields = [
            'pries_id',
            'name', 'surname', 'patronymic',
            'clergy',
            'clergy_id',
            'clergy_name',
        ]


class PersonSerializer(serializers.ModelSerializer):
    patronymic = serializers.CharField(allow_blank=True, required=False)
    estate_name = serializers.SerializerMethodField()
    creed_name = serializers.SerializerMethodField()
    village_name = serializers.SerializerMethodField()

    class Meta:
        model = Persons
        fields = '__all__'
        extra_kwargs = {
            'sex': {'required': False, 'allow_blank': True, 'allow_null': True},  # временно
        }

    def get_estate_name(self, obj):
        return obj.estate.name if obj.estate else None

    def get_creed_name(self, obj):
        return obj.creed.name if obj.creed else None

    def get_village_name(self, obj):
        return obj.village.name if obj.village else None


class DeathRecordPriestSerializer(serializers.ModelSerializer):
    clergy_name = serializers.CharField(source='clergy.name', read_only=True)
    
    class Meta:
        model = DeathRecordPriest
        fields = '__all__'


class PersonSearchSerializer(serializers.ModelSerializer):
    province_name = serializers.CharField(source='province.name', read_only=True)
    yezd_name = serializers.CharField(source='yezd.name', read_only=True)
    volost_name = serializers.CharField(source='volost.name', read_only=True)
    village_name = serializers.CharField(source='village.name', read_only=True)
    estate_name = serializers.CharField(source='estate.name', read_only=True)
    creed_name = serializers.CharField(source='creed.name', read_only=True)

    class Meta:
        model = Persons
        fields = [
            'person_id', 'surname', 'name', 'patronymic', 'sex', 'date',
            'province_id', 'province_name', 'yezd_id', 'yezd_name',
            'volost_id', 'volost_name', 'village_id', 'village_name',
            'estate_id', 'estate_name', 'creed_id', 'creed_name',
            'duplicate', 'comment'
        ]


class GodmenSerializer(serializers.ModelSerializer):
    estate_name = serializers.CharField(source='estate.name', read_only=True)
    creed_name = serializers.CharField(source='creed.name', read_only=True)
    province_name = serializers.CharField(source='province.name', read_only=True)
    yezd_name = serializers.CharField(source='yezd.name', read_only=True)
    volost_name = serializers.CharField(source='volost.name', read_only=True)
    village_name = serializers.CharField(source='village.name', read_only=True)

    class Meta:
        model = Godmen
        fields = [
            'godmen_id', 'name', 'patronymic', 'surname',
            'estate', 'estate_name',
            'creed', 'creed_name',
            'province', 'province_name',
            'yezd', 'yezd_name',
            'volost', 'volost_name',
            'village', 'village_name',
            'birth', 'person'
        ]


class GodmothersSerializer(serializers.ModelSerializer):
    estate_name = serializers.CharField(source='estate.name', read_only=True)
    creed_name = serializers.CharField(source='creed.name', read_only=True)
    province_name = serializers.CharField(source='province.name', read_only=True)
    yezd_name = serializers.CharField(source='yezd.name', read_only=True)
    volost_name = serializers.CharField(source='volost.name', read_only=True)
    village_name = serializers.CharField(source='village.name', read_only=True)
    status_name = serializers.CharField(source='status.name', read_only=True)

    class Meta:
        model = Godmothers
        fields = [
            'godmother_id', 'name', 'patronymic', 'surname',
            'estate', 'estate_name',
            'creed', 'creed_name',
            'province', 'province_name',
            'yezd', 'yezd_name',
            'volost', 'volost_name',
            'village', 'village_name',
            'status', 'status_name',
            'birth', 'person'
        ]


class BirthRecordsPriestSerializer(serializers.ModelSerializer):
    clergy_name = serializers.CharField(source='clergy.name', read_only=True)
    church_worker_name = serializers.CharField(source='church_worker.full_name', read_only=True)

    class Meta:
        model = BirthRecordsPriest
        fields = [
            'id', 'name', 'surname',
            'clergy', 'clergy_name',
            'church_worker', 'church_worker_name',
            'birth'
        ]


class BirthRecordsSerializer(serializers.ModelSerializer):
    person_data = PersonSerializer(source='person', read_only=True)
    priests = BirthRecordsPriestSerializer(many=True, read_only=True)
    godmen = GodmenSerializer(many=True, read_only=True)
    godmothers = GodmothersSerializer(many=True, read_only=True)
    archive_name = serializers.SerializerMethodField()
    father_estate_name = serializers.SerializerMethodField()
    father_village_name = serializers.SerializerMethodField()

    class Meta:
        model = BirthRecords
        fields = '__all__'

    def get_archive_name(self, obj):
        return obj.archive.name if obj.archive else None

    def get_father_estate_name(self, obj):
        return obj.father_estate.name if obj.father_estate else None

    def get_father_village_name(self, obj):
        return obj.father_village.name if obj.father_village else None


class DeathRecordsSerializer(serializers.ModelSerializer):
    priests = DeathRecordPriestSerializer(many=True, read_only=True)
    archive_name = serializers.CharField(source='archive.name', read_only=True)
    person_data = PersonSerializer(source='person', read_only=True)
    estate_name = serializers.CharField(source='estate.name', read_only=True)
    kinship_name = serializers.CharField(source='kinship.name', read_only=True)
    pries_name = serializers.CharField(source='pries.name', read_only=True)
    pries_surname = serializers.CharField(source='pries.surname', read_only=True)

    # Названия — только для чтения
    province_name = serializers.CharField(source='province.name', read_only=True)
    yezd_name = serializers.CharField(source='yezd.name', read_only=True)
    volost_name = serializers.CharField(source='volost.name', read_only=True)
    village_name = serializers.CharField(source='village.name', read_only=True)

    # ID — читаются и пишутся (убираем read_only)
    province = serializers.PrimaryKeyRelatedField(queryset=Provinces.objects.all(), allow_null=True, required=False)
    yezd = serializers.PrimaryKeyRelatedField(queryset=Yezds.objects.all(), allow_null=True, required=False)
    volost = serializers.PrimaryKeyRelatedField(queryset=Volosts.objects.all(), allow_null=True, required=False)
    village = serializers.PrimaryKeyRelatedField(queryset=Villages.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Deaths
        fields = '__all__'
        # Добавляем extra_kwargs для полей, которые не должны быть обязательными
        extra_kwargs = {
            'person': {'required': False, 'allow_null': True},
            'page': {'required': False},
            'number_record': {'required': False},
            'date': {'required': False},
            'sex': {'required': False},
        }

    def get_relatives(self, obj):
        if not obj.person:
            return []
        relationships = Relationships.objects.filter(whom=obj.person).select_related('who', 'kinship')
        return [
            {
                'name': rel.who.name or '',
                'patronymic': rel.who.patronymic or '',
                'surname': rel.who.surname or '',
                'kinship_id': rel.kinship_id,
                'kinship_name': rel.kinship.name if rel.kinship else '',
            }
            for rel in relationships if rel.who
        ]


class StatusChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusChoice
        fields = ['status_choice_id', 'name']


class StatusesSerializer(serializers.ModelSerializer):
    status_name = serializers.CharField(source='status_choice.name', read_only=True)
    person_name = serializers.CharField(source='person.name', read_only=True)
    person_surname = serializers.CharField(source='person.surname', read_only=True)

    class Meta:
        model = Statuses
        fields = ['status_id', 'person', 'person_name', 'person_surname', 'status_choice', 'status_name', 'date_start', 'date_end', 'marriage']


class DraftRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftRecord
        fields = [
            'draft_id', 'record_type', 'payload',
            'created_at', 'updated_at', 'published_record_id',
        ]
        read_only_fields = ['draft_id', 'created_at', 'updated_at', 'published_record_id']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class KinshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kinship
        fields = ['kinship_id', 'name']


class MarriageSerializer(serializers.ModelSerializer):
    archive_name = serializers.CharField(source='archive.name', read_only=True)
    pries_name = serializers.CharField(source='pries.name', read_only=True)
    pries_surname = serializers.CharField(source='pries.surname', read_only=True)
    priests = MarriageRecordPriestSerializer(many=True, read_only=True)
    
    class Meta:
        model = Marriage
        fields = '__all__'


class HusbandSerializer(serializers.ModelSerializer):
    person_name = serializers.CharField(source='person.name', read_only=True)
    person_surname = serializers.CharField(source='person.surname', read_only=True)
    person_patronymic = serializers.CharField(source='person.patronymic', read_only=True)
    
    class Meta:
        model = Husband
        fields = [
            'man_id', 'person', 'person_name', 'person_surname', 'person_patronymic',
            'marriage', 'number_marriage', 'age'
        ]
        read_only_fields = ['man_id']


class WifeSerializer(serializers.ModelSerializer):
    person_name = serializers.CharField(source='person.name', read_only=True)
    person_surname = serializers.CharField(source='person.surname', read_only=True)
    person_patronymic = serializers.CharField(source='person.patronymic', read_only=True)
    
    class Meta:
        model = Wife
        fields = [
            'wife_id', 'person', 'person_name', 'person_surname', 'person_patronymic',
            'marriage', 'number_marriage', 'age'
        ]
        read_only_fields = ['wife_id']


class MaleGuarantorSerializer(serializers.ModelSerializer):
    person_name = serializers.CharField(source='person.name', read_only=True)
    person_surname = serializers.CharField(source='person.surname', read_only=True)
    person_patronymic = serializers.CharField(source='person.patronymic', read_only=True)
    
    class Meta:
        model = MaleGuarantors
        fields = [
            'guarantors_id', 'person', 'person_name', 'person_surname', 'person_patronymic',
            'marriage'
        ]
        read_only_fields = ['guarantors_id']


class FemaleGuarantorSerializer(serializers.ModelSerializer):
    person_name = serializers.CharField(source='person.name', read_only=True)
    person_surname = serializers.CharField(source='person.surname', read_only=True)
    person_patronymic = serializers.CharField(source='person.patronymic', read_only=True)
    
    class Meta:
        model = FemaleGuarantors
        fields = [
            'guarantors_id', 'person', 'person_name', 'person_surname', 'person_patronymic',
            'marriage'
        ]
        read_only_fields = ['guarantors_id']


class MarriageRecordPriestSerializer(serializers.ModelSerializer):
    clergy_name = serializers.CharField(source='clergy.name', read_only=True)
    church_worker_name = serializers.CharField(source='church_worker.surname', read_only=True)
    
    class Meta:
        model = MarriageRecordPriest
        fields = [
            'id', 'marriage', 'name', 'surname', 'patronymic',
            'clergy', 'clergy_name', 'church_worker', 'church_worker_name'
        ]
        read_only_fields = ['id']

