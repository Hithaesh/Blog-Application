from django.urls import path, include

urlpatterns = [
    path('account/', include('account.urls')),
    # path("blog/", include('blogs.urls'))
]