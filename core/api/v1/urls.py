from django.urls import include
from django.urls import path

urlpatterns = [
    path("showcase/", include("api.v1.showcase.urls")),
    path("token/", include("api.v1.auth.urls")),
    path("schema/", include("api.v1.schema.urls")),
]
