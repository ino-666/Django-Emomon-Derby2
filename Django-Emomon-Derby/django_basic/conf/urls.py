from django.contrib import admin
from django.urls import path, include
 
urlpatterns = [
    path('', include('accounts.urls')),
    path('horse/', include('horse.urls')),  # horseアプリのURL設定を追加
    path('race/', include('race.urls')),  # raceアプリのURL設定を追加
    path('admin/', admin.site.urls),
]