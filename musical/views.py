from django.http import JsonResponse
from django.views.generic import View
from musical.models import Musicals

class MusicalListView(View):
    def get(self, request, *args, **kwargs):
        musicals = list(Musicals.objects.values())
        return JsonResponse(musicals, safe=False)
