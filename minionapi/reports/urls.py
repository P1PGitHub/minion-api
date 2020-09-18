from django.urls import path

from . import views

app_name = "reports"
urlpatterns = [
    path("", views.ReportList.as_view(), name="list"),
    path("customer_service/", views.CustomerServiceList.as_view(),
         name="customer-service-list"
         ),
    path("customer_service/simple/", views.CustomerServiceSimpleList.as_view(),
         name="customer-service-simple-list"
         ),
    path("customer_service/drafts/", views.CustomerServiceSimpleDraftsList.as_view(),
         name="customer-service-drafts-list"),
    path("customer_service/drafts/recent/", views.CustomerServiceRecentDraftsList.as_view(),
         name="customer-service-recent-drafts-list"),
    path("customer_service/recent/", views.CustomerServiceRecentList.as_view(),
         name="customer-service-drafts-list"),
    path("customer_service/<pk>/", views.CustomerServiceRetrieveUpdate.as_view(),
         name="customer-service-retrieve-delete"),
    path("sign/", views.SignatureCreate.as_view(), name="signature-create"),
    path("sign/<signature_id>/", views.SignatureRetreiveDelete.as_view(),
         name="signature-upload"),
    path("<report_id>/",
         views.ReportDetail.as_view(), name="report-detail"
         ),
    path("<report_id>/publish/",
         views.ReportPublish.as_view(), name="report-publish"
         ),
    path("<report_id>/inventory/",
         views.InventoryCheckOutListCreate.as_view(), name="inventory-list"
         ),
    path("<report_id>/inventory/clear/",
         views.InventoryClear.as_view(), name="inventory-clear"),
    path("<report_id>/time_entry/",
         views.TimeEntryListCreate.as_view(), name="time-entry-list"
         ),
    path("<report_id>/time_entry/clear/",
         views.TimeEntryClear.as_view(), name="time-entry-clear"),

]
