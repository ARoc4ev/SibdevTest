from django.urls import path
from .views import  AplPost, AplGet

urlpatterns = [
    # path('/apl-get/', ),
    path('apl-post/',  AplPost.as_view({'post': 'create'})),
    path('apl-get/',  AplGet.as_view()),
]
