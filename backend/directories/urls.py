from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import (
    ArchiveViewSet, ClergyViewSet, EstateViewSet, ReligionViewSet,
    ProvinceViewSet, YezdViewSet, VolostViewSet, VillageViewSet,
    ChurchWorkerViewSet, PersonViewSet, BirthRecordsViewSet,
    GodmenViewSet, GodmothersViewSet, BirthRecordsPriestViewSet,
    StatusesViewSet, MyPersonsView, StatusChoiceViewSet,
    HomeView, DraftViewSet, ScanUploadView, 
    KinshipViewSet, DeathRecordsViewSet, DeathRecordPriestViewSet, RelationshipsViewSet,
    MarriageViewSet, MarriageRecordPriestViewSet, HusbandViewSet, WifeViewSet, 
    MaleGuarantorViewSet, FemaleGuarantorViewSet, ChangePasswordView
)


router = DefaultRouter()
router.register(r'archives', ArchiveViewSet)
router.register(r'clergy', ClergyViewSet)
router.register(r'estates', EstateViewSet)
router.register(r'religions', ReligionViewSet)
router.register(r'provinces', ProvinceViewSet)
router.register(r'yezds', YezdViewSet)
router.register(r'volosts', VolostViewSet)
router.register(r'villages', VillageViewSet)
router.register(r'church-workers', ChurchWorkerViewSet)
router.register(r'persons', PersonViewSet)
router.register(r'birth-records', BirthRecordsViewSet)
router.register(r'godmen', GodmenViewSet)
router.register(r'godmothers', GodmothersViewSet)
router.register(r'birth-record-priests', BirthRecordsPriestViewSet)
router.register(r'status-choices', StatusChoiceViewSet)
router.register(r'statuses', StatusesViewSet)
router.register(r'drafts', DraftViewSet, basename='draft')
router.register(r'kinship', KinshipViewSet)
router.register(r'death-records', DeathRecordsViewSet)
router.register(r'death-record-priests', DeathRecordPriestViewSet)
router.register(r'relationships', RelationshipsViewSet)
router.register(r'marriage-records', MarriageViewSet)  
router.register(r'marriage-record-priests', MarriageRecordPriestViewSet)
router.register(r'husbands', HusbandViewSet)
router.register(r'wives', WifeViewSet)
router.register(r'male-guarantors', MaleGuarantorViewSet)
router.register(r'female-guarantors', FemaleGuarantorViewSet)
router.register(r'marriage-record-priests', MarriageRecordPriestViewSet)



urlpatterns = [
    path('api/auth/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
    path('persons-search/', MyPersonsView.as_view(), name='persons-search'),
    path('home/', HomeView.as_view(), name='home'),
    path('marriage-records/<int:pk>/upload-scan/', ScanUploadView.as_view(), {'record_type': 'marriage'}, name='marriage-upload-scan'),
    path('death-records/<int:pk>/upload-scan/', ScanUploadView.as_view(), {'record_type': 'death'}, name='death-upload-scan'),
]