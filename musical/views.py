from django.http import JsonResponse
from django.utils import timezone
from django.views.generic import View
from musical.models import Musicals, Categories, Genres, MainImages, MusicalSeries, MusicalReservationLink
from .forms import SignupForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
class MusicalListView(View):
    def get(self, request, *args, **kwargs):
        musicals = list(Musicals.objects.values())
        return JsonResponse({'data': musicals}, json_dumps_params={'ensure_ascii':False}, status=200)

class MusicalDetailView(View):
    def get(self, request, *args, **kwargs):
        musical_id = kwargs.get('musical_id')

        if musical_id is not None:
            musical = Musicals.objects.filter(id=musical_id).values().first()

            if musical:
                return JsonResponse({'data': musical}, json_dumps_params={'ensure_ascii': False}, status=200)
            else:
                return JsonResponse({'error': 'Musical not found'}, status=404)


class CategoryListView(View):
    def get(self, request, *args, **kwargs):
        categories = list(Categories.objects.values())
        return JsonResponse({'data': categories}, json_dumps_params={'ensure_ascii':False}, status=200)

class GenreListView(View):
    def get(self, request, *args, **kwargs):
        genres = list(Genres.objects.values())
        return JsonResponse({'data': genres}, json_dumps_params={'ensure_ascii':False}, status=200)

class PopularMusicalListView(View):
    def get(self, request, *args, **kwargs):

        popular_musicals = list(Musicals.objects.values('id', 'title')[:5])

        return JsonResponse({'data': popular_musicals}, json_dumps_params={'ensure_ascii': False}, status=200)

class UpcomingMusicalListView(View):
    def get(self, request, *args, **kwargs):
        upcoming_musicals = Musicals.objects.filter(open_from__gte=timezone.now()).order_by('-open_from')[:5]

        upcoming_musicals_data = [{'id': musical.id,'title': musical.title} for musical in upcoming_musicals]
        return JsonResponse({'data': upcoming_musicals_data}, json_dumps_params={'ensure_ascii': False}, status=200)

class MainImageListView(View):

    def get(self, request, *args, **kwargs):
        main_images = list(MainImages.objects.order_by('sequence').values('image_url', 'sequence'))
        return JsonResponse({'data': main_images}, json_dumps_params={'ensure_ascii': False}, status=200)

class CategoryMusicalListView(View):
    def get(self, request, *args, **kwargs):
        category_id = kwargs.get('category_id')
        musicals = Musicals.objects.filter(category_id=category_id).values()
        return JsonResponse({'data': list(musicals)}, json_dumps_params={'ensure_ascii': False}, status=200)

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'musical/signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'musical/login.html', {'form': form})

class DemoMainPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'musical/main.html')


class DemoMusicalDetailView(View):

    def get(self, request, musical_id, *args, **kwargs):
        musical = Musicals.objects.get(id=musical_id)
        musical_series = MusicalSeries.objects.filter(musical_id=musical_id).values()

        series_with_reservations = []
        for series in musical_series:
            series_id = series['id']
            reservations = MusicalReservationLink.objects.filter(series_id=series_id).values()
            series_with_reservations.append({
                'series': series,
                'reservations': list(reservations)
            })

        context = {
            'musical': musical,
            'series_with_reservations': series_with_reservations
        }
        return render(request, 'musical_detail.html', context)
