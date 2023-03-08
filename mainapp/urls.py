from django.urls import path
from .import views


urlpatterns=[
    path('jobs/', views.LatestJobs.as_view()),
    path("job_details/", views.DetailedPageView),
    path("filter_jobs/", views.filterjobView)
]