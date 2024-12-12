from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Reminder
from .serializers import ReminderSerializer
from rest_framework.permissions import IsAuthenticated

class ReminderListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReminderSerializer

    def get_queryset(self):
        return Reminder.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReminderDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer 