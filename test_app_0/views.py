from django.views import View
from django.http import HttpResponse, JsonResponse

class IndexView(View):     # CBV
    def get(self, request):
        dummy_data = {
            'test': 'test'
            
        }
        return JsonResponse(dummy_data)

    def post(self, request):
        return HttpResponse("Post success")

    def put(self, request):
        return HttpResponse("Put success")

    def delete(self, request):
        return HttpResponse("Delete success")