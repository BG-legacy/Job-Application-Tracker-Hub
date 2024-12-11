from rest_framework.generics import ListCreateAPIView
from .models import Reminder
from .serializers import ReminderSerializer

class ReminderListCreateView(ListCreateAPIView):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer 