import datetime
from django.contrib import admin
from django.utils import timezone


now = timezone.now()
today_start = datetime.datetime.combine(now, datetime.time.min) 
today_end = datetime.datetime.combine(now, datetime.time.max) 

# Register your models here.


from .models import ReferralLink, ReferredUser, ReferralCodeClick


admin.site.register(ReferralCodeClick)


class ReferralLinkAdmin(admin.ModelAdmin):
    readonly_fields = ["code", "referred_users", "todays_users", "clicks"]
    class Meta:
        model = ReferralLink


    def referred_users(self, obj):
        html = obj.get_referred_as_ul()
        return html
    referred_users.allow_tags = True

    def todays_users(self, obj):
        users = obj.get_referred_by_date(today_start, today_end)
        html = obj.get_referred_as_ul(users=users)
        return html
    todays_users.allow_tags = True

    def clicks(self, obj):
        return obj.count


admin.site.register(ReferralLink, ReferralLinkAdmin)

admin.site.register(ReferredUser)
