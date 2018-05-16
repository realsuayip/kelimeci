from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator

alpha_EN = RegexValidator(r'^[A-z]+$', 'Geçersiz karakterler içeriyor bu.')


class Kelime(models.Model):
    kelime = models.CharField(max_length=40, unique=True, error_messages={
        'unique': "Bu kelime zaten var ki"},
        validators=[alpha_EN])
    ingilizce_tanim = models.CharField(max_length=160)
    turkce_anlam = models.CharField(max_length=160)
    ingilizce_yakin = models.CharField(max_length=160)
    ornek_cumle = models.CharField(max_length=240)
    eklenme_tarihi = models.DateTimeField(auto_now_add=True)
    ekleyen_kisi = models.ForeignKey(User, on_delete=models.PROTECT, default=1)
    degistirilme_tarihi = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-degistirilme_tarihi"]

    def __str__(self):
        return f"{self.kelime}"


class Eleman(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bildikleri = models.ManyToManyField(Kelime, blank=True, related_name='bildikleri')
    favorileri = models.ManyToManyField(Kelime, blank=True)
    hepsini_al = models.BooleanField(default=False)
    bildik_privacy = models.BooleanField(default=False)
    favori_privacy = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Eleman.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.eleman.save()
