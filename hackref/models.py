from __future__ import unicode_literals
import datetime

from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.contrib import messages
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import MultipleObjectsReturned
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.template.loader import render_to_string
from django.utils.encoding import smart_text
from django.utils import timezone

from .utils import model_code_generator, clean_message

COMPLETED_MESSAGE = getattr(settings, "HACKREF_COMPLETED_MESSAGE", "Referral Completed")
COMPLETED_MESSAGE_DISPLAY = getattr(settings, "HACKREF_COMPLETED_MESSAGE_DISPLAY", False)

try:
    from allauth.account.signals import user_signed_up
except ImproperlyConfigured:
    raise ImproperlyConfigured("Django All Auth is required for this project.\nDocs: \
        http://django-allauth.readthedocs.org/en/latest/")


class ReferralCodeClick(models.Model):
    user         = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    link         = models.ForeignKey("ReferralLink", null=True, blank=True)
    timestamp    = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s" %(self.link.code)
    
    def __str__(self):
        return "%s" %(self.link.code)



class ReferralLink(models.Model):
    user        = models.OneToOneField(settings.AUTH_USER_MODEL)
    code        = models.CharField(max_length=100, unique=True)
    active      = models.BooleanField(default=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.code

    def __str__(self):
        return "%s" %(self.code)


    def add_one(self, user=None):
        new_click = ReferralCodeClick.objects.create(link=self)
        if user:
            new_click.user = user
            new_click.save()
        return self.count

    @property
    def count(self):
        return self.referralcodeclick_set.count()


    def get_referred_users_by_id(self, qs=None):
        if not qs:
            qs = self.referreduser_set.all()
        id_list = [x.invitee.id for x in qs]
        return id_list

    def get_referred_users(self, qs=None):
        User = self.user.__class__
        id_list = self.get_referred_users_by_id(qs)
        return User.objects.filter(id__in=id_list)

    def get_referred_by_date(self, date_1, date_2):
        """
        Dates work like:
        yesterday = timezone.now() - datetime.timedelta(1)
        tomorrow = timezone.now() + datetime.timedelta(1)
        now = timezone.now()
        today_start = datetime.datetime.combine(now, datetime.time.min) 
        today_end = datetime.datetime.combine(now, datetime.time.max) 
        """
        try:
            datetime.datetime(date_1)
        except:
            return []
        try:
            datetime.datetime(date_2)
        except:
            return []
        qs_date1 = self.referreduser_set.filter(timestamp__gt=date_1)
        qs_date2 = self.referreduser_set.filter(timestamp__lte=date_2)
        qs = (qs_date1|qs_date2)
        users = self.get_referred_users(qs=qs)
        return users

    def get_referred_count(self):
        return self.referreduser_set.count()

    def get_referred_as_ul(self, users=None):
        if not users:
            users = self.get_referred_users()[:5]
        context = {
            "users": users
        }
        template = "hackref/snippets/referred_user_links.html"
        return render_to_string(template, context)



def create_ref_link(sender, instance, *args, **kwargs):
    if not instance.code:
        instance.code = model_code_generator(ReferralLink)

pre_save.connect(create_ref_link, sender=ReferralLink)



class ReferredUser(models.Model):
    invitee       = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='invitee')
    referrer      = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='referrer')
    link          = models.ForeignKey(ReferralLink, null=True, blank=True)
    timestamp     = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        timestamp = self.timestamp
        return timestamp.strftime('%-m/%-d/%y')






 #(request, user)

@receiver(user_signed_up)
def create_referral(sender, request, user, *args, **kwargs):
    """
    Get a ReferralLink ID based on clicked redirect.
    Use ID and created User to connect created User
    to ReferralLink User. 
    """
    referral_link_id = request.session.get("referral_link_id")
    created_user = user
    if referral_link_id:
        been_referred = ReferredUser.objects.filter(invitee=created_user).exists()
        ref_qs = ReferralLink.objects.filter(id=referral_link_id)
        if not been_referred and ref_qs.exists():
            _link_obj = ref_qs.first()
            new_referral_obj = ReferredUser()
            new_referral_obj.invitee = created_user
            new_referral_obj.referrer = _link_obj.user
            new_referral_obj.code = _link_obj
            new_referral_obj.save()
            del request.session["referral_link_id"]
            if COMPLETED_MESSAGE_DISPLAY == True:
                complete_msg = clean_message("COMPLETED_MESSAGE", COMPLETED_MESSAGE)
                messages.success(request, complete_msg)
