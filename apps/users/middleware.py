from datetime import timedelta

from django.utils import timezone

ACTIVITY_INTERVAL = timedelta(minutes=5)


class LastActivityMiddleware:
    ''' Мидлвейр, который срабатывает каждый раз при получение запроса от пользователя '''
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            now = timezone.now()
            if user.last_activity is None or now - user.last_activity > ACTIVITY_INTERVAL:
                User.objects.filter(pk=user.pk).update(last_activity=now)
        return response