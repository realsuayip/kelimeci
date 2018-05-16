from django.urls import path
from main import views
urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('alistirma/', views.alistirma, name="alistirma"),
    path('login/', views.Login.as_view(template_name='login.html',
                                       redirect_authenticated_user=True),
         name="login"
         ),
    path('logout/', views.Logout.as_view(), name="logout"),
    path('kelime_ekle/', views.KelimeEkle.as_view(), name="kelime_ekle"),
    path('profil/', views.Profil.as_view(), name="profil"),
    path('kelime_cikar/', views.kelimecikar, name="kelimecikar"),
    path('_addknown/', views._addknown, name="addknown"),
    path('ara/', views.arama, name="arama"),
    path('kelime/<slug:slug>/', views.KelimeDetay.as_view(),
         name="kelime_detay"),
    path('about/', views.about, name="about"),
    path('kelime_sil/<slug:slug>/', views.KelimeSil.as_view(),
         name="kelimesil"),
    path('profil/eklediklerim/', views.Eklediklerim.as_view(),
         name="eklediklerim"),
    path('profil/ayarlar/', views.Ayarlar.as_view(), name="ayarlar"),
    path('kelime_duzenle/<slug:slug>/', views.KelimeDuzenle.as_view(),
         name="kelime_duzenle"),
    path('_addfavori', views._addfavori, name="addfavori"),
    path('_favoricikar/', views.favoricikar, name="favoricikar"),
    path('profil/favorilerim/', views.Favorilerim.as_view(),
         name="favorilerim"),
    path('digerleri/', views.UserList.as_view(), name="digerleri"),
    path('birisi/<slug:slug>', views.UserProfile.as_view(),
         name="userprofile"),
]
