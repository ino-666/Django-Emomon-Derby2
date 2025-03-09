from django.urls import path
from . import views

app_name = 'horse'
urlpatterns = [
    # 馬データ作成ページへのパス
    path('create_horse_date/', views.Create_horse.as_view(), name='create_horse'),
    # 馬選択ページへのパス
    path('select_horse/', views.select_horse.as_view(), name='select_horse'),
    # 馬の名前編集ページへのパス
    path('horse/<int:horse_id>/', views.edit_name, name='edit_name'),
    # 馬詳細ページへのパス
    path('horse/<int:horse_id>/', views.horse_detail, name='horse_id'),
    # 馬解放機能へのパス
    path('horse/<int:horse_id>/release/', views.release, name='release'),
    # スタミナトレーニング機能へのパス
    path('horse/<int:horse_id>/train_stamina/', views.train_stamina, name='train_stamina'),
    # スピードトレーニング機能へのパス
    path('horse/<int:horse_id>/train_speed/', views.train_speed, name='train_speed'),
    # 運トレーニング機能へのパス
    path('horse/<int:horse_id>/train_luck/', views.train_luck, name='train_luck'),
    # 経歴拡張機能へのパス
    path('extend_career/<int:horse_id>/', views.extend_career, name='extend_career'),
    # 特性追加機能へのパス
    path('add_traits/<int:horse_id>/', views.add_traits, name='add_traits'),
    
    path('get_horse_count', views.get_horse_count, name='get_horse_count'),
    path('add_money/', views.add_money, name='add_money'),
    # 必要に応じて他のURLパターンをここに追加します。
]