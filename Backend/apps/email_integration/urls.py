from django.urls import path
from .views import (
    EmailAuthView, 
    OAuth2CallbackView, 
    EmailSyncView, 
    TestEmailFetchView,
    ConnectEmailView,
    ScrapeEmailsView,
    ConfirmApplicationsView,
    ConnectionStatusView
)

app_name = 'email_integration'

urlpatterns = [
    path('auth/', EmailAuthView.as_view(), name='email-auth'),
    path('oauth2callback/', OAuth2CallbackView.as_view(), name='oauth2-callback'),
    path('sync/', EmailSyncView.as_view(), name='email-sync'),
    path('test-fetch/', TestEmailFetchView.as_view(), name='test-fetch'),
    path('connect-email/', ConnectEmailView.as_view(), name='connect-email'),
    path('scrape-emails/', ScrapeEmailsView.as_view(), name='scrape-emails'),
    path('confirm-applications/', ConfirmApplicationsView.as_view(), name='confirm-applications'),
    path('connection-status/', ConnectionStatusView.as_view(), name='connection-status'),
]