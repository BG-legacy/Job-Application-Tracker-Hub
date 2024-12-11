from django.urls import path
from .views import ApplicationListCreateView, ApplicationDetailView, DashboardSummaryView

urlpatterns = [
    path('', ApplicationListCreateView.as_view(), name='application-list-create'),
    path('<int:pk>/', ApplicationDetailView.as_view(), name='application-detail'),
    path('dashboard/', DashboardSummaryView.as_view(), name='application-dashboard'),
] 