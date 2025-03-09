from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'race'
urlpatterns = [
    # レース待機ページへのパス
    path('race_venue/', views.HorseStatusView.as_view(), name='race_venue'),
    # レースページへのパス
    path('uma_uma/<int:horse_id>', views.uma_uma_view, name='uma_uma'),
    # 結果ページへのパス
    path('results/<int:horse_id>/', views.results, name='results'),
    # セッション設定機能へのパス
    path('set_session/', views.set_session, name='set_session'),
]