from django.views import generic, View
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView
from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
#from .models import Race, Training
from horse.models import Horse
from accounts.models import User
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from horse.models import Horse
from django.db.models import F
from django.db import transaction
import random
from django.contrib import messages


#アカウント作成の処理
class AccountCreateView(generic.CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'accounts/accounts_create.html'

    def get_success_url(self):
        return reverse('accounts:login')  # アカウント作成後ログインページにリダイレクトします

#ログインの処理
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password) # type: ignore
        
        if user is not None:
            login(request, user) # type: ignore
            return redirect('accounts:home')  # ログイン成功時のリダイレクト先
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid login credentials'})  # ログイン失敗時のエラーメッセージ

    return render(request, 'accounts/login.html')

#ログアウトの処理
def logout_view(request):
    logout(request)
    return redirect('accounts:login')  # ログアウト後、ログインページにリダイレクトする

#トレーニングの処理
class TrainingView(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user = self.request.user
        user.refresh_from_db()  # Fetch the latest data from the database

        # remaining daysがなくなったら、10にリセットしてセレクト画面へリダイレクト
        if user.remaining_days <= 1:
            user.remaining_days = 10
            user.save()
            return redirect('horse:select_horse')

        # トレーニングの種類を取得
        training_type = request.POST.get('training_type')

        # ユーザーの引退していない馬をすべて取得
        horses = Horse.objects.filter(owner=user, retired=False)

        if training_type == 'elevation':# 高地トレーニングの処理
            for horse in horses:
                horse.stamina_increase = Horse.weighted_random() # 上昇値を決める処理
                # その他のステータスの上昇値は-1にすることで非表示
                horse.speed_increase = -1
                horse.luck_increase = -1
                horse.increase_stamina(horse.stamina_increase) # 上昇値分ステータスを上げる
        elif training_type == 'dash':# ダッシュトレーニングの処理
            for horse in horses:
                horse.speed_increase = Horse.weighted_random()
                horse.stamina_increase = -1
                horse.luck_increase = -1
                horse.increase_speed(horse.speed_increase)
        elif training_type == 'prayer':# お参りトレーニングの処理
            for horse in horses:
                horse.luck_increase = Horse.weighted_random()
                horse.speed_increase = -1
                horse.stamina_increase = -1
                horse.increase_luck(horse.luck_increase)

        # レースまでの残り日数を減らす
        user.remaining_days -= 1
        user.save()

        # 各馬の残りトレーニング回数を減らす処理
        for horse in horses:
            horse.num_remaining_turns -= 1
            horse.save()

            # 残りトレーニング回数が0の時、引退額を決定する。
            if horse.num_remaining_turns == 0 and user.remaining_days != 0 and not horse.retired:
                horse.price += horse.stamina + horse.speed + horse.luck
                horse.price *= 1.5 if horse.traits.filter(id=9).exists() else 1
                messages.success(request, f'{horse.name}はこれで引退です🫂<br>お祝いに¥{horse.price}を受け取った。')

            # 残りトレーニング回数が-1の時、馬を引退させ、引退祝いを金額に足す。
            if horse.num_remaining_turns == -1 and not horse.retired:
                horse.price += horse.stamina + horse.speed + horse.luck
                horse.price *= 1.5 if horse.traits.filter(id=9).exists() else 1
                horse.save()
                request.user.increase_money(horse.price)
                horse.retire()

        return redirect('accounts:home')

#ホーム画面に自分の持っている🐎を表示する処理
class Home(TemplateView):
    template_name = 'accounts/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:  # ユーザーがログインしているかを確認
            context['user'] = self.request.user  # ログインしていれば、そのユーザーオブジェクトをテンプレートに渡す
            context['user_horses'] = Horse.objects.filter(owner=self.request.user, retired=False)  # ログインユーザーが所有する馬を取得
        #context['race'] = Race.objects.first()  # raceオブジェクトをテンプレートに渡す
        return context

# ED購入の処理
def ed_purchase(request):
    # お金が足りないとき
    if request.user.money < 5000:
        messages.error(request, "お金が足りません。")
        return redirect('accounts:home')

    request.user.increase_money(-5000)
    request.user.enable_ending() # エンディングボタンを開放する
    messages.success(request, "エンディングが解放されました。")
    return redirect('accounts:home')

# エンディング画面の表示
class Ending(TemplateView):
    template_name = 'accounts/ending.html'

# 遊び方画面の表示
class instruction(TemplateView):
    template_name = 'accounts/instruction.html'

# 引退馬一覧の表示
class retiredHorses(TemplateView):
    template_name = 'accounts/retiredHorses.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['retired_horses'] = Horse.objects.filter(owner=self.request.user, retired=True)  # ユーザーの所有した引退馬を取得

        return context