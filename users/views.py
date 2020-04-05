from telebot import types
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import permission_required
from .bot import bot, botInfo
from dal import autocomplete
from users.models import User

from django.shortcuts import HttpResponse

# bot.delete_webhook()
# bot.polling(none_stop=True, interval=0)
# Telegram Webhook handler
@csrf_exempt
def tg_webhook(request):
    bot.process_new_updates([ types.Update.de_json(request.body.decode("utf-8")) ])
    return HttpResponse('OK')


class UsernameSelect2Autocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_staff:
            return User.objects.none()
        if not self.q:
            return User.objects.order_by('-date_reg')
        return (
            User.objects.filter(username__istartswith=self.q) |
            User.objects.filter(id__istartswith=self.q)
        ).order_by('-date_reg')[:10]
