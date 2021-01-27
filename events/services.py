import random
import string

from events.models import Event, Route, Accent, Participant


def get_random_string(length):
    # Random string with the combination of lower and upper case
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))


def create_event_routes(event: Event) -> None:
    for i in range(event.routes_num):
        Route.objects.create(
            number=i + 1,
            event=event,
        )


def create_default_accents(event: Event, participant: Participant) -> None:
    for route in event.route.all():
        Accent.objects.create(
            accent=Accent.ACCENT_NO,
            route=route,
            participant=participant,
            event=event,
        )


def clear_event(event: Event) -> None:
    event.participant.all().delete()
    event.route.all().delete()


def create_participant_with_default_accents(event: Event, first_name: str, last_name: str,
                                            birth_year: int = 2000, city: str = '', team: str = '',
                                            grade: Participant.GRADES = Participant.GRADE_BR,
                                            ) -> Participant:
    participant = Participant.objects.create(
        first_name=first_name,
        last_name=last_name,
        birth_year=birth_year,
        city=city,
        team=team,
        grade=grade,
        event=event,
        pin=random.randint(1000, 9999),
    )

    create_default_accents(event=event, participant=participant)

    return participant


def update_routes_points(event: Event) -> None:
    for route in event.route.all():
        if event.score_type == Event.SCORE_PROPORTIONAL:
            c = len(event.accent.filter(route=route).exclude(accent=Accent.ACCENT_NO))
            try:
                route.points = 1 / c
            except ZeroDivisionError:
                pass
        else:
            route.points = 1
        route.save()


def update_participants_score(event: Event) -> None:
    for participant in event.participant.all():
        participant.score = 0
        print(participant)
        score_type = event.score_type
        for index, accent in enumerate(participant.accent.all()):
            if accent.accent == Accent.ACCENT_FLASH:
                if score_type == Event.SCORE_SIMPLE_SUM:
                    participant.score += event.flash_points
                else:
                    participant.score += event.flash_points * accent.route.points
            if accent.accent == Accent.ACCENT_REDPOINT:
                if score_type == Event.SCORE_SIMPLE_SUM:
                    participant.score += event.redpoint_points
                else:
                    participant.score += event.redpoint_points * accent.route.points
        participant.save()
