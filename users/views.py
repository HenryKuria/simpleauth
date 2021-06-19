from django.views import View
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


class AccessTokenCallback(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        print(request.GET.get('code'), request.GET.get('state'))
        return HttpResponse(status=200)

    def post(self, request):
        print(request.POST)
        return HttpResponse(status=200)
