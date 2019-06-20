from .models import Profile


class CheckProfileMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        return self.get_response(request)

    def process_request(self, request):
        user = request.user
        if user.is_authenticated:
            prof = Profile.objects.get(user=user)
            username = ''
            if user.first_name != '':
                username += user.first_name
                if user.last_name != '':
                    username += ' ' + user.last_name
            else:
                username = user.username
        else:
            prof = None
            username = None
        # print("yo")
        request.profile = prof
        request.username = username
        return None
