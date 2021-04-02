from django.views import View
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# TODO: uncomment 
# from telega.client import dispatcher, bot


@method_decorator(csrf_exempt, name='dispatch')
class TelegramWebhookView(View):

    def post(self, request, *args, **kwargs):
        print(request.POST)
        bot.send_text(str(dict(request.POST)), chat_id='@tempfc_alerts')
        # dispatcher.process_update(update)
        return HttpResponse('test')
