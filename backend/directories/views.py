from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
import os
from pathlib import Path
from django.conf import settings
from rest_framework.parsers import MultiPartParser
from django.contrib.auth import authenticate, update_session_auth_hash

from .models import (
    Archive, Clergy, Estates, Religions, Provinces, Yezds, Volosts,
    Villages, Persons, BirthRecords, Godmen, Godmothers, BirthRecordsPriest,
    ChurchWorkers, StatusChoice, Statuses, Marriage, Deaths, DraftRecord,
    Kinship, DeathRecordPriest, Relationships, MarriageRecordPriest,
    Husband, Wife, MaleGuarantors, FemaleGuarantors,
)

from .serializers import (
    ArchiveSerializer, ClergySerializer, EstateSerializer, ReligionSerializer,
    ProvinceSerializer, YezdSerializer, VolostSerializer, VillageSerializer, PersonSerializer, BirthRecordsSerializer,
    GodmenSerializer, GodmothersSerializer, BirthRecordsPriestSerializer, ChurchWorkerSerializer,
    StatusChoiceSerializer, StatusesSerializer, DraftRecordSerializer, KinshipSerializer,
    DeathRecordsSerializer, DeathRecordPriestSerializer, RelationshipsSerializer, MarriageSerializer,
    MarriageRecordPriestSerializer, HusbandSerializer, WifeSerializer, MaleGuarantorSerializer, FemaleGuarantorSerializer,
)

ALLOWED_SCAN_EXTS = {'.jpg', '.jpeg', '.png', '.tiff', '.tif'}

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')

        if not current_password or not new_password:
            return Response(
                {'error': 'Текущий и новый пароль обязательны'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Проверяем текущий пароль
        if not user.check_password(current_password):
            return Response(
                {'error': 'Текущий пароль указан неверно'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Проверяем длину нового пароля
        if len(new_password) < 8:
            return Response(
                {'error': 'Новый пароль должен содержать не менее 8 символов'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Устанавливаем новый пароль
        user.set_password(new_password)
        user.save()

        # Обновляем сессию (чтобы пользователь не вышел)
        update_session_auth_hash(request, user)

        return Response(
            {'message': 'Пароль успешно изменён'},
            status=status.HTTP_200_OK
        )


class MarriageRecordPriestViewSet(viewsets.ModelViewSet):
    queryset = MarriageRecordPriest.objects.select_related('clergy', 'church_worker').all()
    serializer_class = MarriageRecordPriestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        marriage_id = self.request.query_params.get('marriage')
        if marriage_id:
            queryset = queryset.filter(marriage_id=marriage_id)
        return queryset

 
class KinshipViewSet(viewsets.ModelViewSet):
    queryset = Kinship.objects.all()
    serializer_class = KinshipSerializer
    permission_classes = [IsAuthenticated]


class ScanUploadView(APIView):
    parser_classes     = [MultiPartParser]
    permission_classes = [IsAuthenticated]
 
    def post(self, request, pk, record_type):
        scan_file = request.FILES.get('scan')
        if not scan_file:
            return Response({'error': 'Файл не передан'}, status=400)
 
        ext = Path(scan_file.name).suffix.lower()
        if ext not in ALLOWED_SCAN_EXTS:
            return Response({'error': f'Недопустимый формат: {ext}'}, status=400)
 
        # jpeg → jpg
        if ext == '.jpeg':
            ext = '.jpg'
 
        scan_dir = Path(settings.MEDIA_ROOT) / 'scans' / record_type
        scan_dir.mkdir(parents=True, exist_ok=True)
 
        # Удаляем предыдущий скан этой записи (любое расширение)
        for old_ext in ALLOWED_SCAN_EXTS | {'.jpg'}:
            old = scan_dir / f'{pk}{old_ext}'
            if old.exists():
                old.unlink()
 
        # Сохраняем: {id}.jpg / {id}.png / …
        save_path = scan_dir / f'{pk}{ext}'
        with open(save_path, 'wb+') as f:
            for chunk in scan_file.chunks():
                f.write(chunk)
 
        media_url = getattr(settings, 'MEDIA_URL', '/media/')
        return Response({'scan_url': f'{media_url}scans/{record_type}/{pk}{ext}'}, status=200)


class ArchiveViewSet(viewsets.ModelViewSet):
    queryset = Archive.objects.all().order_by('-year')
    serializer_class = ArchiveSerializer
    permission_classes = [permissions.IsAuthenticated]


class ClergyViewSet(viewsets.ModelViewSet):
    queryset = Clergy.objects.all().order_by('name')
    serializer_class = ClergySerializer
    permission_classes = [permissions.IsAuthenticated]


class EstateViewSet(viewsets.ModelViewSet):
    queryset = Estates.objects.all().order_by('name')
    serializer_class = EstateSerializer
    permission_classes = [permissions.IsAuthenticated]


class ReligionViewSet(viewsets.ModelViewSet):
    queryset = Religions.objects.all().order_by('name')
    serializer_class = ReligionSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProvinceViewSet(viewsets.ModelViewSet):
    queryset = Provinces.objects.all().order_by('name')
    serializer_class = ProvinceSerializer
    permission_classes = [permissions.IsAuthenticated]


class YezdViewSet(viewsets.ModelViewSet):
    queryset = Yezds.objects.all().order_by('name')
    serializer_class = YezdSerializer
    permission_classes = [permissions.IsAuthenticated]


class VolostViewSet(viewsets.ModelViewSet):
    queryset = Volosts.objects.all().order_by('name')
    serializer_class = VolostSerializer
    permission_classes = [permissions.IsAuthenticated]


class VillageViewSet(viewsets.ModelViewSet):
    queryset = Villages.objects.all().order_by('name')
    serializer_class = VillageSerializer
    permission_classes = [permissions.IsAuthenticated]


class ChurchWorkerViewSet(viewsets.ModelViewSet):
    queryset = ChurchWorkers.objects.select_related('clergy').all()
    serializer_class = ChurchWorkerSerializer
    permission_classes = [permissions.IsAuthenticated]


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Persons.objects.none()
    serializer_class = PersonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Persons.objects.select_related('estate', 'creed', 'village').all()
        surname = self.request.query_params.get('surname')
        name    = self.request.query_params.get('name')
        sex     = self.request.query_params.get('sex')
        if surname: qs = qs.filter(surname__iexact=surname)
        if name:    qs = qs.filter(name__iexact=name)
        if sex:     qs = qs.filter(sex=sex)
        return qs


class DraftViewSet(viewsets.ModelViewSet):
    serializer_class   = DraftRecordSerializer
    permission_classes = [IsAuthenticated]
 
    def get_queryset(self):
        # Пользователь видит только свои черновики
        return DraftRecord.objects.filter(
            created_by=self.request.user
        ).order_by('-updated_at')
    
    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser])
    def upload_scan(self, request, pk=None):
        return ScanUploadView().post(request, pk=pk, record_type='draft')
 
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        draft = self.get_object()
 
        if draft.published_record_id:
            return Response(
                {'detail': 'Черновик уже опубликован.'},
                status=status.HTTP_400_BAD_REQUEST
            )
 
        return Response({
            'detail':  'Готово к публикации.',
            'payload': draft.payload,
            'draft_id': draft.draft_id,
        }, status=status.HTTP_200_OK)


class BirthRecordsViewSet(viewsets.ModelViewSet):
    serializer_class = BirthRecordsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = BirthRecords.objects.select_related(
        'archive',
        'person',
        'father_estate',
        'father_village',
    ).prefetch_related(
        'priests',
        'godmen',
        'godmothers',
    ).order_by('-birth_id')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def last(self, request):
        archive_id = request.query_params.get('archive_id')
        if not archive_id:
            return Response(
                {'detail': 'archive_id required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        last_record = BirthRecords.objects.filter(
            archive_id=archive_id,
            created_by=request.user,
        ).order_by('-number_record').first()

        if not last_record:
            return Response(None)

        serializer = self.get_serializer(last_record)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser])
    def upload_scan(self, request, pk=None):
        return ScanUploadView().post(request, pk=pk, record_type='birth')


class DeathRecordsViewSet(viewsets.ModelViewSet):
    serializer_class = DeathRecordsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Deaths.objects.select_related(
        'archive', 'person', 'village', 'estate', 'kinship', 'pries'
    ).prefetch_related(
        'priests',
        'priests__clergy',
        'priests__church_worker',
    ).order_by('-date')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        # При обновлении не меняем created_by
        serializer.save()

    @action(detail=False, methods=['get'])
    def last(self, request):
        archive_id = request.query_params.get('archive_id')
        sex = request.query_params.get('sex')
        
        if not archive_id:
            return Response(
                {'detail': 'archive_id required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = Deaths.objects.filter(
            archive_id=archive_id, 
            created_by=request.user
        )
        
        if sex:
            queryset = queryset.filter(sex=sex)
        
        last_record = queryset.order_by('-number_record').first()
        
        if not last_record:
            return Response(None)
        
        serializer = self.get_serializer(last_record)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser])
    def upload_scan(self, request, pk=None):
        """Загрузить скан для записи о смерти"""
        return ScanUploadView().post(request, pk=pk, record_type='death')


class RelationshipsViewSet(viewsets.ModelViewSet):
    queryset = Relationships.objects.select_related('who', 'whom', 'kinship').all()
    serializer_class = RelationshipsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Фильтрация по параметрам запроса
        who_id = self.request.query_params.get('who')
        whom_id = self.request.query_params.get('whom')
        if who_id:
            queryset = queryset.filter(who_id=who_id)
        if whom_id:
            queryset = queryset.filter(whom_id=whom_id)
        return queryset


class GodmenViewSet(viewsets.ModelViewSet):
    queryset = Godmen.objects.all()
    serializer_class = GodmenSerializer
    permission_classes = [permissions.IsAuthenticated]


class GodmothersViewSet(viewsets.ModelViewSet):
    queryset = Godmothers.objects.all()
    serializer_class = GodmothersSerializer
    permission_classes = [permissions.IsAuthenticated]


class BirthRecordsPriestViewSet(viewsets.ModelViewSet):
    queryset = BirthRecordsPriest.objects.all()
    serializer_class = BirthRecordsPriestSerializer
    permission_classes = [permissions.IsAuthenticated]


class MyPersonsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Persons.objects.all()
        q = request.query_params.get('q', '').strip()
        if q:
            queryset = queryset.filter(
                Q(surname__icontains=q) |
                Q(name__icontains=q) |
                Q(patronymic__icontains=q)
            )
        serializer = PersonSerializer(queryset, many=True)
        return Response({
            'user': request.user.username,
            'persons': serializer.data,
        })


class StatusChoiceViewSet(viewsets.ModelViewSet):
    queryset = StatusChoice.objects.all().order_by('name')
    serializer_class = StatusChoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
 
 
class StatusesViewSet(viewsets.ModelViewSet):
    queryset = Statuses.objects.select_related('status_choice', 'person', 'marriage').all()
    serializer_class = StatusesSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        person_id = self.request.query_params.get('person')
        if person_id:
            queryset = queryset.filter(person_id=person_id)
        marriage_id = self.request.query_params.get('marriage')
        if marriage_id:
            queryset = queryset.filter(marriage_id=marriage_id)
        return queryset


class HomeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        records = []

        # Рождения
        births = (
            BirthRecords.objects
            .filter(created_by=user)
            .select_related('person', 'archive')
            .order_by('-date_of_baptism')
        )
        for b in births:
            p = b.person
            records.append({
                "type":          "birth",
                "type_label":    "Рождение",
                "id":            b.birth_id,
                "date":          str(b.date_of_baptism),
                "description":   f"{p.surname} {p.name} {p.patronymic}".strip(),
                "archive":       _archive_label(b.archive),
                "page":          b.page,
                "number_record": b.number_record,
                "person_id":     p.person_id if p else None,
            })

        marriages = (
            Marriage.objects
            .filter(created_by=user)
            .select_related('archive')
            .prefetch_related('husbands__person', 'wives__person')  
            .order_by('-date')
        )
        for m in marriages:
            husband = m.husbands.first()  
            wife    = m.wives.first()     
            parts   = []
            
            person_id = None
            if husband:
                parts.append(f"{husband.person.surname} {husband.person.name}")
                person_id = husband.person.person_id
            if wife:
                parts.append(f"{wife.person.surname} {wife.person.name}")
                if not person_id:
                    person_id = wife.person.person_id
                    
            records.append({
                "type":          "marriage",
                "type_label":    "Брак",
                "id":            m.marriage_id,
                "date":          str(m.date),
                "description":   " и ".join(parts) or f"Брак #{m.marriage_id}",
                "archive":       _archive_label(m.archive),
                "page":          m.page,
                "number_record": m.number_record,
                "person_id":     person_id,
            })

        deaths = (
            Deaths.objects
            .filter(created_by=user)
            .select_related('archive', 'person')
            .order_by('-date')
        )
        for d in deaths:
            person_obj = d.person
            if person_obj:
                desc = f"{person_obj.surname} {person_obj.name} {person_obj.patronymic}".strip()
                person_id = person_obj.person_id
            else:
                desc = f"Смерть #{d.death_id}"
                person_id = None
                
            records.append({
                "type":          "death",
                "type_label":    "Смерть",
                "id":            d.death_id,
                "date":          str(d.date),
                "description":   desc,
                "archive":       _archive_label(d.archive),
                "page":          d.page,
                "number_record": d.number_record,
                "person_id":     person_id,
            })

        records.sort(key=lambda r: r["date"], reverse=True)

        return Response({
            "user": user.full_name or user.email,
            "user_role": "admin" if user.is_staff else "user",
            "records": records,
            "counts": {
                "birth":    births.count(),
                "marriage": marriages.count(),
                "death":    deaths.count(),
            },
        })


class DeathRecordPriestViewSet(viewsets.ModelViewSet):
    queryset = DeathRecordPriest.objects.select_related('clergy', 'church_worker').all()
    serializer_class = DeathRecordPriestSerializer
    permission_classes = [permissions.IsAuthenticated]


class MarriageViewSet(viewsets.ModelViewSet):
    serializer_class = MarriageSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Marriage.objects.select_related('archive', 'pries').all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def perform_destroy(self, instance):
        MarriageRecordPriest.objects.filter(marriage=instance).delete()
        Husband.objects.filter(marriage=instance).delete()
        Wife.objects.filter(marriage=instance).delete()
        MaleGuarantors.objects.filter(marriage=instance).delete()
        FemaleGuarantors.objects.filter(marriage=instance).delete()
        Statuses.objects.filter(marriage=instance).update(marriage=None)
        instance.delete()
    
    @action(detail=False, methods=['get'])
    def last(self, request):
        archive_id = request.query_params.get('archive_id')
        if not archive_id:
            return Response(
                {'detail': 'archive_id required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        last_record = Marriage.objects.filter(
            archive_id=archive_id,
            created_by=request.user,
        ).order_by('-number_record').first()
        if not last_record:
            return Response(None)
        serializer = self.get_serializer(last_record)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser])
    def upload_scan(self, request, pk=None):
        return ScanUploadView().post(request, pk=pk, record_type='marriage')
        

class HusbandViewSet(viewsets.ModelViewSet):
    queryset = Husband.objects.select_related('person', 'marriage').all()
    serializer_class = HusbandSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        marriage_id = self.request.query_params.get('marriage')
        if marriage_id:
            queryset = queryset.filter(marriage_id=marriage_id)
        person_id = self.request.query_params.get('person')
        if person_id:
            queryset = queryset.filter(person_id=person_id)
        return queryset


class WifeViewSet(viewsets.ModelViewSet):
    queryset = Wife.objects.select_related('person', 'marriage').all()
    serializer_class = WifeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        marriage_id = self.request.query_params.get('marriage')
        if marriage_id:
            queryset = queryset.filter(marriage_id=marriage_id)
        person_id = self.request.query_params.get('person')
        if person_id:
            queryset = queryset.filter(person_id=person_id)
        return queryset


class MaleGuarantorViewSet(viewsets.ModelViewSet):
    queryset = MaleGuarantors.objects.select_related('person', 'marriage').all()
    serializer_class = MaleGuarantorSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        marriage_id = self.request.query_params.get('marriage')
        if marriage_id:
            queryset = queryset.filter(marriage_id=marriage_id)
        person_id = self.request.query_params.get('person')
        if person_id:
            queryset = queryset.filter(person_id=person_id)
        return queryset


class FemaleGuarantorViewSet(viewsets.ModelViewSet):
    queryset = FemaleGuarantors.objects.select_related('person', 'marriage').all()
    serializer_class = FemaleGuarantorSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        marriage_id = self.request.query_params.get('marriage')
        if marriage_id:
            queryset = queryset.filter(marriage_id=marriage_id)
        person_id = self.request.query_params.get('person')
        if person_id:
            queryset = queryset.filter(person_id=person_id)
        return queryset


def _archive_label(archive) -> str:
    if not archive:
        return "—"
    return f"{archive.name} — {archive.number_case} ({archive.year})"