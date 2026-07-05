from django.contrib.gis.db import models


class Region(models.Model):
    fid = models.AutoField(primary_key=True)
    osm_id = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    admin_level = models.CharField(max_length=10, blank=True, null=True)
    geom = models.MultiPolygonField(srid=32628)

    class Meta:
        db_table = 'regions'
        managed = False
        verbose_name = 'Région'
        verbose_name_plural = 'Régions'

    def __str__(self):
        return self.name or f'Région {self.fid}'


class SiteMinier(models.Model):
    fid = models.AutoField(primary_key=True)
    featurenam = models.CharField(max_length=255, blank=True, null=True)
    featuretyp = models.CharField(max_length=255, blank=True, null=True)
    label1 = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    adm1 = models.CharField(max_length=255, blank=True, null=True)
    locopstat = models.CharField(max_length=255, blank=True, null=True)
    operatenam = models.CharField(max_length=255, blank=True, null=True)
    ownername1 = models.CharField(max_length=255, blank=True, null=True)
    secteur = models.CharField(
        max_length=255, blank=True, null=True, db_column='dsgattr01'
    )
    categorie = models.CharField(
        max_length=255, blank=True, null=True, db_column='dsgattr02'
    )
    substance = models.CharField(
        max_length=255, blank=True, null=True, db_column='dsgattr03'
    )
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    geom = models.PointField(srid=32628)

    class Meta:
        db_table = 'sites_miniers'
        managed = False
        verbose_name = 'Site Minier'
        verbose_name_plural = 'Sites Miniers'

    def __str__(self):
        return self.featurenam or f'Site {self.fid}'


class ExplorationMiniere(models.Model):
    fid = models.AutoField(primary_key=True)
    featurenam = models.CharField(max_length=255, blank=True, null=True)
    label1 = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    adm1 = models.CharField(max_length=255, blank=True, null=True)
    locopstat = models.CharField(max_length=255, blank=True, null=True)
    ownername = models.CharField(max_length=255, blank=True, null=True)
    substance = models.CharField(
        max_length=255, blank=True, null=True, db_column='dsgattr01'
    )
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    geom = models.PointField(srid=32628)

    class Meta:
        db_table = 'exploration_miniere'
        managed = False
        verbose_name = 'Exploration Minière'
        verbose_name_plural = 'Explorations Minières'

    def __str__(self):
        return self.featurenam or f'Exploration {self.fid}'


class GisementMineral(models.Model):
    fid = models.AutoField(primary_key=True)
    featurenam = models.CharField(max_length=255, blank=True, null=True)
    label1 = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    adm1 = models.CharField(max_length=255, blank=True, null=True)
    # locopstat = models.CharField(max_length=255, blank=True, null=True)
    substance_principale = models.CharField(
        max_length=255, blank=True, null=True, db_column='dsgattr01'
    )
    substance_secondaire = models.CharField(
        max_length=255, blank=True, null=True, db_column='dsgattr02'
    )
    substance_tertiaire = models.CharField(
        max_length=255, blank=True, null=True, db_column='dsgattr03'
    )
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    geom = models.PointField(srid=32628)

    class Meta:
        db_table = 'gisements_mineraux'
        managed = False
        verbose_name = 'Gisement Minéral'
        verbose_name_plural = 'Gisements Minéraux'

    def __str__(self):
        return self.featurenam or f'Gisement {self.fid}'





class CoursEau(models.Model):
    fid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    waterway = models.CharField(max_length=100, blank=True, null=True)
    geom = models.MultiLineStringField(srid=32628)

    class Meta:
        db_table = 'cours_eau'
        managed = False
        verbose_name = "Cours d'eau"
        verbose_name_plural = "Cours d'eau"

    def __str__(self):
        return self.name or f"Cours d'eau {self.fid}"


class AireProtegee(models.Model):
    fid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    boundary = models.CharField(max_length=100, blank=True, null=True)
    geom = models.MultiPolygonField(srid=32628)

    class Meta:
        db_table = 'aires_protegees'
        managed = False
        verbose_name = 'Aire Protégée'
        verbose_name_plural = 'Aires Protégées'

    def __str__(self):
        return self.name or f'Aire protégée {self.fid}'


class Localite(models.Model):
    fid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    place = models.CharField(max_length=100, blank=True, null=True)
    geom = models.PointField(srid=32628)

    class Meta:
        db_table = 'localites'
        managed = False
        verbose_name = 'Localité'
        verbose_name_plural = 'Localités'

    def __str__(self):
        return self.name or f'Localité {self.fid}'


class Route(models.Model):
    fid = models.AutoField(primary_key=True)
    featurenam = models.CharField(max_length=255, blank=True, null=True)
    geom = models.MultiLineStringField(srid=32628)

    class Meta:
        db_table = 'routes'
        managed = False
        verbose_name = 'Route'
        verbose_name_plural = 'Routes'

    def __str__(self):
        return self.name or f'Route {self.fid}'


class LigneElectrique(models.Model):
    fid = models.AutoField(primary_key=True)
    voltage = models.CharField(
        max_length=100, blank=True, null=True,
        db_column='dsgattr01'
    )
    voltage_classification = models.CharField(
        max_length=100, blank=True, null=True,
        db_column='dsgattr02'
    )
    geom = models.MultiLineStringField(srid=32628,dim=3)

    class Meta:
        db_table = 'lignes_electriques'
        managed = False
        verbose_name = 'Ligne Électrique'
        verbose_name_plural = 'Lignes Électriques'

    def __str__(self):
        return f'Ligne {self.voltage or self.fid}'


class Port(models.Model):
    fid = models.AutoField(primary_key=True)
    featurenam = models.CharField(max_length=255, blank=True, null=True)
    geom = models.PointField(srid=32628,dim=3)

    class Meta:
        db_table = 'ports'
        managed = False
        verbose_name = 'Port'
        verbose_name_plural = 'Ports'

    def __str__(self):
        return self.name or f'Port {self.fid}'