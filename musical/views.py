from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import View
from musical.models import Musicals, Categories, Genres, MainImages, MusicalSeries, MusicalReservationLink, Users, \
    Notice, TicketNotification
from .forms import SignupForm
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from .forms import LoginForm
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

class NoticeListView(View):
    def get(self, request, *args, **kwargs):
        notices = list(Notice.objects.values('notice_title', 'created_at').order_by('-created_at')[:5])
        return JsonResponse({'data': notices}, json_dumps_params={'ensure_ascii': False}, status=200)

class NoticeDetailView(View):
    def get(self, request, *args, **kwargs):
        notice_id = kwargs.get('notice_id')
        notice = Notice.objects.filter(id=notice_id).values().first()
        return JsonResponse({'data': notice}, json_dumps_params={'ensure_ascii': False}, status=200)

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
        form = LoginForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user_id']
            user_password = form.cleaned_data['user_password']

            # 사용자 인증
            try:
                user = Users.objects.get(user_id=user_id, user_password=user_password)
                # 로그인 성공 시 세션에 사용자 정보 저장
                request.session['user_id'] = user.id
                return redirect('main-page')  # main-page로 리디렉션
            except Users.DoesNotExist:
                form.add_error(None, 'Please enter a correct username and password. Note that both fields may be case-sensitive.')

    else:
        form = LoginForm()
    return render(request, 'musical/login.html', {'form': form})


def logout_view(request):
    auth_logout(request)  # Django 기본 로그아웃 처리
    request.session.flush()  # 모든 세션 데이터 제거
    return redirect('login')


class DemoMainPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'musical/main.html')


class DemoMusicalDetailView(View):

    def get(self, request, *args, **kwargs):
        musical_id = kwargs.get('musical_id')
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

        notification_exists = TicketNotification.objects.filter(musical_id=musical, user_id=int(request.session['user_id'])).exists()

        context = {
            'musical': musical,
            'series_with_reservations': series_with_reservations,
            'notification_exists': notification_exists,
        }

        return render(request, 'musical/musical_detail.html', context)

    def post(self, request, musical_id, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('login')  # 로그인 페이지로 리디렉션

        user_id = request.session['user_id']
        user = Users.objects.get(id=user_id)
        musical = Musicals.objects.get(id=musical_id)

        # 알림 존재 여부 확인
        if TicketNotification.objects.filter(musical_id=musical, user_id=user).exists():
            # 알림이 이미 존재하면 메시지 추가
            return redirect('musical_detail', musical_id=musical_id)

        # TicketNotification 객체 생성
        notification = TicketNotification.objects.create(
            musical_id=musical,
            user_id=user,
            is_notified=False
        )
        notification.save()

        return redirect('musical_detail', musical_id=musical_id)


class DemoMyPageView(View):
    def get(self, request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('login')
        return render(request, 'musical/mypage.html')
