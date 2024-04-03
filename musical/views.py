

from django.http import JsonResponse
from django.utils import timezone
from django.views.generic import View
from musical.models import Musicals, Categories, Genres, MainImages

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

