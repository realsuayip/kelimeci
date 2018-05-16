from .models import Kelime
import random


def kelime_listesi(request):
    kelimeler = Kelime.objects.all()
    if request.user.is_authenticated:
        if not request.user.eleman.hepsini_al:
            known = request.user.eleman.bildikleri.all().values_list('pk',
                                                                     flat=True)
            kelimeler = Kelime.objects.exclude(pk__in=known).all()
    return kelimeler


def random_kelime(request):
    k_listesi = kelime_listesi(request)
    kelime_sayisi = k_listesi.count()
    if kelime_sayisi == 0:
        return False
    rnd_kelime_idx = random.randint(0, kelime_sayisi - 1)
    return k_listesi[rnd_kelime_idx]
