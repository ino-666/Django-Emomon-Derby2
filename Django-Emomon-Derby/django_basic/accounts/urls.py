from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'accounts'
urlpatterns = [
    # アカウント作成機能へのパス
    path('accounts/accounts_create/', views.AccountCreateView.as_view(), name='accounts_create'),
    # ログイン機能へのパス
    path('', views.login_view, name='login'),
    # ログアウト機能へのパス
    path('accounts/logout/', views.logout_view, name='logout'),
    # ホーム画面表示機能へのパス（ログインが必要）
    path('accounts/home/', login_required(views.Home.as_view()), name='home'),
    # トレーニング機能へのパス
    path('accounts/training/', views.TrainingView.as_view(), name='training'),
    # エンディング表示機能へのパス
    path('accounts/ending/', views.Ending.as_view(), name='ending'),
    # ED購入機能へのパス
    path('accounts/ed_purchase/', views.ed_purchase, name='ed_purchase'),
    # インストラクション表示機能へのパス
    path('accounts/instruction/', views.instruction.as_view(), name='instruction'),
    # 引退馬一覧表示機能へのパス
    path('accounts/retiredHorses/', views.retiredHorses.as_view(), name='retiredHorses'),
]