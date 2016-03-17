import re

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse, NoReverseMatch

from django.views.generic import RedirectView, View
from django.shortcuts import render, get_object_or_404

# Create your views here.


from .models import ReferredUser, ReferralLink
from .utils import get_redirect_path, clean_message

CODE_DNE_REDIRECT = getattr(settings, "HACKREF_CODE_DOES_NOT_EXIST_REDIRECT", "/") #Referral Code does not exist
CODE_DNE_MESSAGE =getattr(settings, "HACKREF_CODE_DOES_NOT_EXIST_MESSAGE", "This code does not exist")
CODE_DNE_DISPLAY = getattr(settings, "HACKREF_CODE_DOES_NOT_EXIST_MESSAGE_DISPLAY", False)
USER_EXISTS_REDIRECT = getattr(settings, "HACKREF_USER_EXISTS_REDIRECT", "/" )
USER_EXISTS_MESSASE = getattr(settings, "HACKREF_USER_EXISTS_MESSASE", "You are already logged in.")
USER_EXISTS_MESSASE_DISPLAY = getattr(settings,"HACKREF_USER_EXISTS_MESSASE_DISPLAY", False)
REDIRECT_SUCCESS_NAME = getattr(settings, "HACKREF_REDIRECT_SUCCESS_NAME", "account_signup")
REDIRECT_SUCCESS_MESSSAGE = getattr(settings, "HACKREF_REDIRECT_SUCCESS_MESSSAGE", "Referral Counted")
REDIRECT_SUCCESS_MESSSAGE_DISPLAY = getattr(settings, "HACKREF_REDIRECT_SUCCESS_MESSSAGE_DISPLAY", False)
COMPLETED_MESSAGE = getattr(settings, "HACKREF_COMPLETED_MESSAGE", "Referral Completed")
COMPLETED_MESSAGE_DISPLAY = getattr(settings, "HACKREF_COMPLETED_MESSAGE_DISPLAY", False)


class CodeTrackingView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'ref-code-redirect'

    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated():
            """
            Error: User exists. Ignore Referral
            """
            if USER_EXISTS_MESSASE_DISPLAY == True:
                messages.error(self.request, clean_message("USER_EXISTS_MESSASE", USER_EXISTS_MESSASE))
            return get_redirect_path("USER_EXISTS_REDIRECT", USER_EXISTS_REDIRECT)
        code = self.kwargs.get("code")
        link_qs = ReferralLink.objects.filter(code=code)
        if not code or link_qs.count() != 1:
            """
            Error: Referral code does not exists. Do Redirect
            """
            if CODE_DNE_DISPLAY == True:
                messages.error(self.request, clean_message("CODE_DNE_MESSAGE", CODE_DNE_MESSAGE))
            return get_redirect_path("CODE_DNE_REDIRECT", CODE_DNE_REDIRECT)

        if link_qs.count() == 1:
            """
            Successs: Referral Code Exists.
            """
            link_obj = link_qs.first()
            self.request.session['referral_link_id'] = link_obj.id
            link_obj.add_one(user)
            if REDIRECT_SUCCESS_MESSSAGE_DISPLAY == True:
                messages.success(self.request, clean_message("REDIRECT_SUCCESS_MESSSAGE", REDIRECT_SUCCESS_MESSSAGE))
        return get_redirect_path("REDIRECT_SUCCESS_NAME", REDIRECT_SUCCESS_NAME)



