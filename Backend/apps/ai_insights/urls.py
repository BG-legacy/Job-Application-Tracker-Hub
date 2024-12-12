from django.urls import path
from .views import AIInsightView, ApplicationInsightView

urlpatterns = [
    # Route for general AI insights
    path('insights/', AIInsightView.as_view(), name='ai-insights'),
    # Route for application-specific insights
    path('insights/application/<int:application_id>/', ApplicationInsightView.as_view(), name='application-insights'),
] 