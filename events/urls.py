from django.urls import path

from events import views

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('e/<int:event_id>/', views.EventView.as_view(), name='event'),
    path('e/<int:event_id>/admin/', views.EventAdminView.as_view(), name='event_admin'),
    path('e/<int:event_id>/enter/', views.EventEnterView.as_view(), name='event_enter'),
    path('e/<int:event_id>/results/', views.EventResultsView.as_view(), name='event_results'),
    path('e/<int:event_id>/participants/', views.EventParticipantsView.as_view(), name='event_participants'),
    path('e/<int:event_id>/registration/', views.EventRegistrationView.as_view(), name='event_registration'),


    path('ajax/check_pin_code/', views.check_pin_code, name='check_pin_code'),
]
