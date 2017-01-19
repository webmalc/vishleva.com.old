from django.conf.urls import url
from pages.views import ReviewList, CreateReview

urlpatterns = [
    url(r'^review/create', CreateReview.as_view(), name='review_create'),
    url(r'^review/list', ReviewList.as_view(), name='review_list'),
]
