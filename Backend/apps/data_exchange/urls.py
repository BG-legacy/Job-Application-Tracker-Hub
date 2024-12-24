from django.urls import path
from .views import ExcelImportView, ExcelExportView

urlpatterns = [
    path('import/excel/', ExcelImportView.as_view(), name='import-excel'),
    path('export/excel/', ExcelExportView.as_view(), name='export-excel'),
] 