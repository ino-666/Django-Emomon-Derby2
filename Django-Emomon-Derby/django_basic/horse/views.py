from django.contrib import messages
from django.forms import ValidationError
from django.shortcuts import redirect
from django.shortcuts import render
from .models import CPU_Horse, Horse, Trait
from .forms import HorseForm
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import HorseForm
import random
from django.http import JsonResponse
from django.http import HttpResponse


#馬の詳細を見る
def horse_detail(request, horse_id):
    horse = Horse.objects.get(pk=horse_id)
    return render(request, 'horse/horse_detail.html', {'horse': horse})

#購入画面での馬購入と馬を買った際にCPUの馬を3体追加する処理
@method_decorator(login_required, name='dispatch')
class Create_horse(FormView):
    template_name = 'horse/create_horse.html'
    form_class = HorseForm
    success_url = reverse_lazy('accounts:home')

    # お金を表示させる処理
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_money'] = self.request.user.money
        return context

    # 購入処理
    def form_valid(self, form):
        # お金が足りてるか確認
        if self.request.user.money < 300:
            messages.error(self.request, "お金が足りません。")
            return super().form_invalid(form)

        horse = form.save(commit=False)
        horse.owner = self.request.user
        horse.save()

        # 300円減らす処理
        self.request.user.money -= 300
        self.request.user.save()

        # 特性をランダムに追加
        horse.add_random_traits()

        # CPU_Horseを3体追加
        for _ in range(3):
# 名前を苗字と名前から決定
            name_parts_1 = ["かっこいい", "つよい", "ふつうの", "よわい","最強の","伝説の","面白い","タフな", "貧血気味な", "派手な", "真面目な", 
                        "短気な", "優しい", "強そうな", "弱そうな","元気な","体が柔らかい","身長の高い","最近振られた","肥満気味の","セクシーな",
                        "昔はかわいかった","未来からやってきた","イライラしている","涙もろい","寝不足な","短気な","ギンギンの","まさに","まじで",
                        "本当の","力持ちの","無口な","後輩力のある","名古屋出身の","東京生まれの","中国から来た","アメリカンな","メンヘラな","マヨラーの",
                        "強くなりそうな","近所の","幻影の","さすらいの","宇宙からやってきた","I am ","Best of ","ヘルニアの","肩が凝っている","モテ期が来た","ポジティブな","ネガティブな"
                        ,"食欲旺盛な","前向きな","就活中の","転職を考えている","代謝がいい","二日酔いの","寝相が悪い","友達思いの","ドライブが好きな"
                        ,"頑固な","関西出身の","散歩が好きな","スポーツが好きな","ハイキングが好きな","ゲームが好きな"]
            
            name_parts_2 = ["輩", "ヤンキー", "チンピラ", "魔王","モブ", "奴","お相撲さん","デブ","ガリ","小学生","中学生","高校生","大学生","社会人","小口さん",
                        "おじいさん","お母さん","先生","従業員","スパイ","警察官","熊","ヤギ","ヘビ","先輩","後輩","アルバイト","社長","運転手",
                        "エンジニア","パイロット","宇宙人","仙人","ダンゴムシ","バッタ","カブトムシ","うさぎ","かめ","縺ゅ?縺","銀行員","漁師","教授",
                        "地底人","独裁者","起業家","CTO","田中さん","騎手","KING","帝王","秘書","アーティスト","アイドル","プロデューサー","ディレクター"
                        ,"シェフ","漫画家","アシスタント","お笑い芸人","モデル","俳優","女優","しゅんしゅん","加藤さん","大口さん","中口さん","エモモンマスター"]


            # 3種類の強さをランダムに決定
            horse_type = random.choice(['strong', 'weak', 'normal'])

            # それぞれの強さに応じてステータスをランダム生成
            if horse_type == 'strong':
                stamina, speed, luck = random.randint(50, 90), random.randint(50, 90), random.randint(50, 90)
            elif horse_type == 'weak':
                stamina, speed, luck = random.randint(5, 40), random.randint(5, 40), random.randint(5, 40)
            else: # normal
                stamina, speed, luck = random.randint(10, 100), random.randint(10, 100), random.randint(10, 100)

            random_name = random.choice(name_parts_1) + random.choice(name_parts_2)

            # CPU馬を生成
            cpu_horse = CPU_Horse(
                name=random_name,
                stamina=stamina,
                speed=speed,
                luck=luck,
                emoji=random.choice(['🐴', '🐎', '🦄', '🐓', '🐒', '🐉', '🦓', '🦁', '🐈', '🐶','🦛','🦘','🐆','🐄','🐁','🐅','🐇','🐉',
                                    "👱‍♀️","🪢","💁‍♂️","🖼️","🧕","🍤","🎏","🎠","🍫","🍢","🧚‍♂️","👸","👮‍♂️","🕵️‍♂️","👩‍🎓","👨‍🌾","🧑‍⚖️","🏒","💄","👩‍⚕️",
                                    "🧝‍♂️","🧔‍♂️","🤵","🙍‍♀️","🦸‍♂️","🧑‍🚀","🛒","👨‍🎤","👩‍⚖️","🧑‍🦳","🎅","👩‍🌾","🪮","👨‍🎓","👨‍🎨","🧃","㊗️","🛻","✈️","🛸","㊙️",
                                    "🈹","🚑","🏍️","🚁","🚗","🦐","🫠","🦞","👙","🥌","🦥","🐜","🐤","🦷","🦗","🧠","⛷️","🏇","🏄‍♀️","🏊‍♀️"]),  
            )
            cpu_horse.save()
            cpu_horse.add_random_traits()

        return super().form_valid(form)

# レースに出場する馬を選択する
class select_horse(TemplateView):
    template_name = 'horse/select_horse.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['race'] = Race.objects.first()  # raceオブジェクトをテンプレートに渡す
        context['horses'] = Horse.objects.filter(owner=self.request.user, retired=False)  # ログインユーザーが所有する馬を取得
        return context

#馬の名前と絵文字を変更する処理、一応画像も変えられます。
def edit_name(request, horse_id):
    horse = Horse.objects.get(pk=horse_id)
    form = HorseForm(instance=horse)
    if request.method == 'POST':
        new_name = request.POST.get('new_name')
        new_emoji = request.POST.get('emoji')
        if new_name:
            horse.name = new_name
        if new_emoji:
            horse.emoji = new_emoji
        horse.save()
        return redirect('accounts:home')
    return render(request, 'horse/horse_detail.html', {'form': form, 'horse': horse})

#馬を逃がす処理
def release(request, horse_id):
    horse = Horse.objects.get(pk=horse_id)
    horse.price += horse.stamina + horse.speed + horse.luck
    horse_name = horse.name   #馬の名前を保存
    horse_price = horse.price   #馬の価格を保存

    request.user.money += horse.price
    request.user.save()

    horse.retire()

    messages.success(request, f"{horse_name}を戦力外通告しました。バイバイ👋<br>おや？¥{horse_price}落としていったようだ。")
    return redirect('accounts:home')

# 特別合宿
@login_required
def train_stamina(request, horse_id):
    return do_special_training(request, horse_id, 'stamina')

@login_required
def train_speed(request, horse_id):
    return do_special_training(request, horse_id, 'speed')

@login_required
def train_luck(request, horse_id):
    return do_special_training(request, horse_id, 'luck')

def do_special_training(request, horse_id, stat):
    horse = Horse.objects.get(pk=horse_id)
    training_cost = 800

    # Check if the horse belongs to the logged in user
    if horse.owner != request.user:
        messages.error(request, "このエモモンはあなたのエモモンではありません。")
        return redirect('horse:horse_id', horse_id=horse.id)

    # Check if the user has enough money
    if request.user.money < training_cost:
        messages.error(request, "お金が足りません。")
        return redirect('horse:horse_id', horse_id=horse.id)

    # トレーニングの型に応じて20～40ランダムに上昇させる
    if stat == 'stamina':
        horse.increase_stamina(random.randint(20, 40))
    elif stat == 'speed':
        horse.increase_speed(random.randint(20, 40))
    elif stat == 'luck':
        horse.increase_luck(random.randint(20, 40))

    # ターン数を10減らす
    horse.num_remaining_turns -= 10
    horse.save()

    # お金を減らす
    request.user.money -= training_cost
    request.user.save()

    messages.success(request, "特別合宿が完了しました！")
    return redirect('horse:horse_id', horse_id=horse.id)

# キャリア延長処理
def extend_career(request, horse_id):
    horse = Horse.objects.get(pk=horse_id)
    training_cost = 1000

    if request.user.money < training_cost:
        messages.error(request, "お金が足りません。")
        return redirect('horse:horse_id', horse_id=horse.id)

    # ターン数と試合数を増やす
    horse.num_remaining_turns += 10
    horse.remaining_racings += 1
    horse.save()

    request.user.money -= training_cost
    request.user.save()

    messages.success(request, "キャリアが延長されました！")
    return redirect('horse:horse_id', horse_id=horse.id)

# 特性を追加する処理
def add_traits(request, horse_id):
    horse = Horse.objects.get(id=horse_id)
    training_cost = 2000

    if request.user.money < training_cost:
        messages.error(request, "お金が足りません。")
        return redirect('horse:horse_id', horse_id=horse.id)

    all_traits = Trait.objects.exclude(id__in=horse.traits.values_list('id', flat=True))
    if len(all_traits) >= 2:
        random_traits = random.sample(list(all_traits), 2)
        horse.traits.add(*random_traits)
    horse.save()

    request.user.money -= training_cost
    request.user.save()

    messages.success(request, "特性が増えました")
    return redirect('horse:horse_id', horse_id=horse.id)

def get_horse_count(request):
    count = Horse.objects.filter(owner=request.user, retired=False).count()
    return JsonResponse({'count': count})

# お金を追加する処理
def add_money(request):
    training_cost = 50

    request.user.money += training_cost
    request.user.save()
    return redirect('horse:create_horse')
