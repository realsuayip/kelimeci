from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import KelimeForm, AyarDegistirForm
from .models import Kelime, Eleman
from .util import random_kelime


class Login(LoginView):
    def form_valid(self, form):
        mesaj = 'başarıyla giriş yaptınız. helal olsun'
        messages.add_message(self.request, messages.INFO, mesaj)
        return super().form_valid(form)


class Logout(LogoutView):
    def dispatch(self, form):
        mesaj = 'başarıyla çıkış yaptınız. helal olsun'
        messages.add_message(self.request, messages.INFO, mesaj)
        return super().dispatch(self.request)


class Home(ListView):
    model = Kelime
    template_name = "main.html"
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        queryset = super(Home, self).get_queryset()
        usr = self.request.user
        if usr.is_authenticated and not usr.eleman.hepsini_al:
            known = self.request.user.eleman.bildikleri.all().values_list('pk',
                                                                          flat=True)
            return queryset.exclude(pk__in=known).all()
        return queryset.all()


class KelimeEkle(LoginRequiredMixin, CreateView):
    model = Kelime
    form_class = KelimeForm
    template_name = "kelime_ekle.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.ekleyen_kisi = self.request.user
        self.object.save()
        return super(KelimeEkle, self).form_valid(form)

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO,
                             f"Kelime '{ self.object }' başarıyla eklendi.")
        return reverse_lazy("kelime_detay", args={self.object})


class KelimeDuzenle(LoginRequiredMixin, UpdateView):
    model = Kelime
    form_class = KelimeForm
    template_name = "kelime_duzenle.html"
    slug_field = "kelime"

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO,
                             f"Kelime '{ self.object }' başarıyla düzenlendi.")
        return reverse_lazy("kelime_detay", args={self.object})


class KelimeSil(LoginRequiredMixin, DeleteView):
    model = Kelime
    success_url = reverse_lazy("eklediklerim")
    slug_field = "kelime"

    def get_object(self, queryset=None):
        obj = super(KelimeSil, self).get_object()
        if not obj.ekleyen_kisi == self.request.user:
            raise Http404
        messages.add_message(self.request, messages.INFO,
                             f"Kelime '{ obj.kelime }' silindi.")
        return obj

    def get(self, *args, **kwargs):
        raise Http404


def alistirma(request):
    kelime = random_kelime(request)
    return render(request, "alistirma.html", context={'kelime': kelime})


class Profil(LoginRequiredMixin, ListView):
    model = Eleman
    template_name = "profil.html"
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        queryset = super(Profil, self).get_queryset()
        return queryset.get(user=self.request.user).bildikleri.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bilinen_ks = self.request.user.eleman.bildikleri.count()
        bilinmeyen_ks = Kelime.objects.count() - bilinen_ks
        eklenen_ks = Kelime.objects.filter(
            ekleyen_kisi=self.request.user).count()
        stats = {'bilinen': bilinen_ks,
                 'bilinmeyen': bilinmeyen_ks,
                 'eklenen': eklenen_ks}
        context['stats'] = stats
        return context


class Favorilerim(LoginRequiredMixin, ListView):
    model = Eleman
    template_name = "profil_favorilerim.html"
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        queryset = super(Favorilerim, self).get_queryset()
        return queryset.get(user=self.request.user).favorileri.all()


class Eklediklerim(LoginRequiredMixin, ListView):
    model = Kelime
    template_name = "profil_eklediklerim.html"
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        queryset = super(Eklediklerim, self).get_queryset()
        return queryset.filter(ekleyen_kisi=self.request.user)


class UserList(LoginRequiredMixin, ListView):
    model = User
    template_name = "digerleri.html"
    paginate_by = 10


class UserProfile(LoginRequiredMixin, DetailView):
    model = User
    template_name = "userprofile.html"
    slug_field = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bilinen_ks = context['user'].eleman.bildikleri.count()
        bilinmeyen_ks = Kelime.objects.count() - bilinen_ks
        eklenen_ks = Kelime.objects.filter(
            ekleyen_kisi=context['user']).count()
        stats = {'bilinen': bilinen_ks,
                 'bilinmeyen': bilinmeyen_ks,
                 'eklenen': eklenen_ks}
        context['stats'] = stats
        return context


class Ayarlar(LoginRequiredMixin, UpdateView):
    model = Eleman
    form_class = AyarDegistirForm
    template_name = "profil_ayarlar.html"

    def get_object(self):
        return Eleman.objects.get(user=self.request.user)

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO,
                             f"Ayarlar kaydedilmiştir.")
        return reverse_lazy("ayarlar")


@login_required
def kelimecikar(request):
    if request.POST.get('kelime'):
        y = get_object_or_404(Eleman, user=request.user).bildikleri
        cikan_kelime = request.POST.get('kelime')
        if not y.filter(kelime=cikan_kelime).exists():
            raise Http404
        x = get_object_or_404(Kelime, kelime=cikan_kelime)
        y.remove(x)
        messages.add_message(request, messages.INFO,
                             f"{cikan_kelime} bildiklerinden çıkarıldı.")
        next = request.POST.get('next', 'profil')
        return redirect(next)
    raise Http404


def arama(request):
    if request.method == "GET":
        aranan = request.GET.get('kelime')
        if aranan:
            iceren = Kelime.objects.filter(kelime__icontains=aranan)
            pn_rq = True
            if iceren.count() < 10:
                pn_rq = False
            pnt = Paginator(iceren, 10)
            page = request.GET.get('sayfa')
            data = pnt.get_page(page)
            return render(request, "arama.html", context={"data": data,
                                                          "aranan": aranan,
                                                          "pn_rq": pn_rq})
    raise Http404


class KelimeDetay(DetailView):
    model = Kelime
    slug_field = "kelime"
    template_name = "kelime_detay.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bilinme = False
        favorilenme = False
        if self.request.user.is_authenticated:
            if context['kelime'] in self.request.user.eleman.bildikleri.all():
                bilinme = True
            if context['kelime'] in self.request.user.eleman.favorileri.all():
                favorilenme = True
        context['favorilenme'] = favorilenme
        context['bilinme'] = bilinme
        return context


@login_required
def _addknown(request):
    if request.method == "POST" and request.POST['kelime']:
        known = request.POST['kelime']
        usr_bilinen = get_object_or_404(Eleman, user=request.user).bildikleri
        kelime_obj = get_object_or_404(Kelime, kelime=known)
        next = request.POST.get('next', 'profil')
        if kelime_obj in usr_bilinen.all():
            raise Http404
        else:
            usr_bilinen.add(kelime_obj)
            messages.add_message(request, messages.INFO,
                                 f"{known} bildiklerinize eklendi.")
            return redirect(next)
    raise Http404


@login_required
def _addfavori(request):
    if request.method == "POST" and request.POST['favori']:
        favori = request.POST['favori']
        usr_favori = get_object_or_404(Eleman, user=request.user).favorileri
        kelime_obj = get_object_or_404(Kelime, kelime=favori)
        next = request.POST.get('next', 'profil')
        if kelime_obj in usr_favori.all():
            return redirect(next)
        else:
            usr_favori.add(kelime_obj)
            messages.add_message(request, messages.INFO,
                                 f"{kelime_obj} favorilerinize eklendi.")
            return redirect(next)
    raise Http404


@login_required
def favoricikar(request):
    if request.POST.get('favori'):
        next = request.POST.get('next', 'profil')
        y = get_object_or_404(Eleman, user=request.user).favorileri
        cikan_kelime = request.POST.get('favori')
        if not y.filter(kelime=cikan_kelime).exists():
            return redirect(next)
        x = get_object_or_404(Kelime, kelime=cikan_kelime)
        y.remove(x)
        messages.add_message(request, messages.INFO,
                             f"{cikan_kelime} favorilerinden çıkarıldı.")
        return redirect(next)
    raise Http404


def about(request):
    return render(request, "about.html")
