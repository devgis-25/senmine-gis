from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegionViewSet, SiteMiniérViewSet, ExplorationMiniereViewSet,
    GisementMineralViewSet, CoursEauViewSet, AireProtegeeViewSet,
    LocaliteViewSet, RouteViewSet, LigneElectriqueViewSet,
    PortViewSet, StatsViewSet, ConflitUsageViewSet, PredictionViewSet,ImpactEnvironnementalViewSet
)

router = DefaultRouter()
router.register(r'regions', RegionViewSet, basename='regions')
router.register(r'sites-miniers', SiteMiniérViewSet, basename='sites-miniers')
router.register(r'explorations', ExplorationMiniereViewSet, basename='explorations')
router.register(r'gisements', GisementMineralViewSet, basename='gisements')
router.register(r'cours-eau', CoursEauViewSet, basename='cours-eau')
router.register(r'aires-protegees', AireProtegeeViewSet, basename='aires-protegees')
router.register(r'localites', LocaliteViewSet, basename='localites')
router.register(r'routes', RouteViewSet, basename='routes')
router.register(r'lignes-electriques', LigneElectriqueViewSet, basename='lignes-electriques')
router.register(r'ports', PortViewSet, basename='ports')
router.register(r'stats', StatsViewSet, basename='stats')
router.register(r'conflits-usage', ConflitUsageViewSet, basename='conflits-usage')
router.register(r'predictions', PredictionViewSet, basename='predictions')
router.register(r'impact-environnemental', ImpactEnvironnementalViewSet, basename='impact-environnemental')

urlpatterns = [
    path('', include(router.urls)),
]