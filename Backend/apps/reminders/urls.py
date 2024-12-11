from django.urls import path
from .views import ReminderListCreateView

urlpatterns = [
    path('', ReminderListCreateView.as_view(), name='reminders-list-create'),
] 