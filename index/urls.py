from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="index-home"),
    path("add/", views.add, name="index-add"),
    path("use/", views.use, name="index-use"),
    path("storage/", views.storage, name="index-storage"),
    path("dry/", views.drystorage, name="dry"),
    path("freezer/", views.freezerstorage, name="freezer"),
    path("fridge/", views.fridgestorage, name="fridge"),
    path("delete/", views.delete, name="delete"),
    path("delete/<slug:confirmed>/<slug:storage>/<int:id>", views.deteled, name="deleted"),
    path("delete/<slug:storage>/<int:id>", views.delete_confirmation, name="delete_confitmation"),
]