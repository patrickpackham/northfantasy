from .models import League
from django.urls import reverse
from django.http import HttpResponseRedirect

class AdminCheckMixin(object):
    def dispatch(self, *args, **kwargs):
        league = League.objects.get(name__icontains=self.kwargs['league_name'])
        if self.request.user != league.admin:
            return HttpResponseRedirect(
                reverse('league_home',
                        kwargs={'league_name': kwargs['league_name']}))
        return super(AdminCheckMixin, self).dispatch(*args, **kwargs)