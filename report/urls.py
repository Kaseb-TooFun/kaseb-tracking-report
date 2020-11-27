from django.urls import path

from . import views

urlpatterns = [
    path('total/website/<str:website_id>',
         views.website_total_report,
         name='website_total_report'
         ),
    path('total/website/<str:website_id>/action/<str:action_id>',
         views.action_total_report,
         name='action_total_report'
         ),
    path('days/website/<str:website_id>',
         views.website_days_report,
         name='website_days_report'
         ),
    path('days/website/<str:website_id>/action/<str:action_id>',
         views.action_days_report,
         name='action_days_report'
         ),
]
