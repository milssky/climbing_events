from django.contrib import admin

from events.models import Event, Participant, Route, Accent

admin.site.register(Event)
admin.site.register(Participant)
admin.site.register(Route)
admin.site.register(Accent)
