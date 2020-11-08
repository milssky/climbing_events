from django import views
from django.forms import formset_factory
from django.http import JsonResponse
from django.shortcuts import render, redirect

from events.forms import ParticipantRegistrationForm, EventAdminForm, AccentForm, AccentParticipantForm, \
    EventAdminServiceForm
from events.models import Event, Participant, Route, Accent
from events import services


class MainView(views.View):
    @staticmethod
    def get(request):
        events = Event.objects.all()
        return render(
            request=request,
            template_name='events/index.html',
            context={
                'events': events,
            }
        )


class EventView(views.View):
    @staticmethod
    def get(request, event_id):
        event = Event.objects.get(id=event_id)
        return render(
            request=request,
            template_name='events/event.html',
            context={
                'event': event,
            }
        )


class EventAdminView(views.View):
    @staticmethod
    def get(request, event_id):
        event = Event.objects.get(id=event_id)
        return render(
            request=request,
            template_name='events/event-admin.html',
            context={
                'event': event,
                'form': EventAdminForm(instance=event, prefix='admin_form'),
                'service_form': EventAdminServiceForm(prefix='service_form'),
            }
        )

    @staticmethod
    def post(request, event_id):
        event = Event.objects.get(id=event_id)
        service_form = EventAdminServiceForm(request.POST, prefix='service_form')
        form = EventAdminForm(request.POST, prefix='admin_form')
        print(service_form)
        if 'clear_event' in request.POST:
            services.clear_event(event=event)
        elif 'create_participant' in request.POST:
            services.create_participant_with_default_accents(
                event=event,
                first_name=services.get_random_string(4),
                last_name=services.get_random_string(6)
            )
        elif 'create_routes' in request.POST:
            services.create_event_routes(event=event)
        elif 'update_score' in request.POST:
            services.update_participants_score(event=event)
        else:
            pass
        return redirect('event_admin', event_id)


class EventEnterView(views.View):
    @staticmethod
    def get(request, event_id):
        event = Event.objects.get(id=event_id)
        initial = [{'label': i} for i in range(event.routes_num)]
        # print(initial)
        AccentFormSet = formset_factory(AccentForm, extra=0)
        formset = AccentFormSet(initial=initial, prefix='accents')
        return render(
            request=request,
            template_name='events/event-enter.html',
            context={
                'event': event,
                'formset': formset,
                'participant_form': AccentParticipantForm(prefix='participant'),
            }
        )

    @staticmethod
    def post(request, event_id):
        event = Event.objects.get(id=event_id)
        participant_form = AccentParticipantForm(request.POST, prefix='participant')
        AccentFormSet = formset_factory(AccentForm)
        accent_formset = AccentFormSet(request.POST, prefix='accents')
        if participant_form.is_valid() and accent_formset.is_valid():
            pin = participant_form.cleaned_data['pin']
            try:
                participant = Participant.objects.get(pin=int(pin))
            except Participant.DoesNotExist:
                pass
                participant = services.create_participant_with_default_accents(
                    event=event,
                    first_name=participant_form.cleaned_data['first_name'],
                    last_name=participant_form.cleaned_data['last_name'],
                )
            participant_accents = Accent.objects.filter(participant=participant, event=event)
            print(participant_accents)
            for index, accent in enumerate(participant_accents):
                accent.accent = accent_formset.cleaned_data[index]['accent']
                accent.route = Route.objects.get(event=event, number=index + 1)
                accent.save()
            # Accent.objects.bulk_update(participant_accents, ['accent', 'route', ])
            services.update_routes_points(event=event)
            services.update_participants_score(event=event)

            return redirect('event_results', event_id=event_id)
        return render(
            request=request,
            template_name='events/event-enter.html',
            context={
                'event': event,
                'formset': accent_formset,
                'participant_form': participant_form,
            }
        )


class EventResultsView(views.View):
    @staticmethod
    def get(request, event_id):
        event = Event.objects.get(id=event_id)
        return render(
            request=request,
            template_name='events/event-results.html',
            context={
                'event': event,
                'participants': event.participant.all(),
            }
        )


class EventParticipantsView(views.View):
    @staticmethod
    def get(request, event_id):
        event = Event.objects.get(id=event_id)
        participants = Participant.objects.filter(event__id=event_id)
        return render(
            request=request,
            template_name='events/event-participants.html',
            context={
                'event': event,
                'participants': participants,
            }
        )


class EventRegistrationView(views.View):
    @staticmethod
    def get(request, event_id):
        event = Event.objects.get(id=event_id)
        return render(
            request=request,
            template_name='events/event-registration.html',
            context={
                'event': event,
                'form': ParticipantRegistrationForm(),
            }
        )

    @staticmethod
    def post(request, event_id):
        form = ParticipantRegistrationForm(request.POST, request.FILES)
        event = Event.objects.get(id=event_id)
        if form.is_valid():
            services.create_participant_with_default_accents(
                event=event,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                birth_year=form.cleaned_data['birth_year'],
                city=form.cleaned_data['city'],
                team=form.cleaned_data['team'],
                grade=form.cleaned_data['grade'],
            )
            return redirect('event_participants', event_id=event_id)
        return render(
            request=request,
            template_name='events/event-registration.html',
            context={
                'event': event,
                'form': form,
            }
        )


def check_pin_code(request):
    print('in check_pin_code')
    print(request.GET)
    pin = request.GET.get('pin')
    event_id = request.GET.get('event_id')
    try:
        participant = Participant.objects.get(pin=pin, event__id=event_id)
        print(participant)
        response = {'response': f'Found: {str(participant)}'}
    except Participant.DoesNotExist:
        response = {'response': 'Participant not found'}
    return JsonResponse(response)