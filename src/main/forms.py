from django import forms
from .models import Kelime, Eleman
from django.utils.translation import ugettext_lazy as _


class AyarDegistirForm(forms.ModelForm):
    class Meta:
        model = Eleman
        fields = ["hepsini_al", "bildik_privacy", "favori_privacy"]
        labels = {
            "hepsini_al": _('bilmediğim kelimeler de listelerde gözüksün'),
            "bildik_privacy": _('bildiklerimi kimsecikler görmesin'),
            "favori_privacy": _('favorilerimi kimsecikler görmesin'),
        }


class KelimeForm(forms.ModelForm):
    class Meta:
        model = Kelime
        fields = [
            "kelime",
            "ingilizce_tanim",
            "turkce_anlam",
            "ingilizce_yakin",
            "ornek_cumle",
        ]
        labels = {
            'kelime': _('Kelime'),
            'ingilizce_tanim': _('İngilizce Tanım'),
            'turkce_anlam': _('Türkçe Anlam'),
            'ingilizce_yakin': _('İngilizce Yakın'),
            'ornek_cumle': _('Örnek Cümle'),
        }
