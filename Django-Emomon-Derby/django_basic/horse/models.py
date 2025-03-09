from django.db import models
from accounts.models import User
import random

class Trait(models.Model): #特性の定義
    name = models.CharField(max_length=200)
    description = models.TextField(default='')

class BaseHorse(models.Model): #馬のベースモデル
    name = models.CharField(max_length=200)
    stamina = models.IntegerField(default=1)
    speed = models.IntegerField(default=1)
    luck = models.IntegerField(default=1)
    traits = models.ManyToManyField(Trait, blank=True) # 特性
    image = models.ImageField(upload_to='images/', null=True, blank=True)  # 画像
    emoji = models.CharField(max_length=10, default='🐴')  # 絵文字
    description = models.TextField(default='')  # キャラの説明、デフォルト値を空文字列に設定

    # ステータスの上限
    max_stamina = models.IntegerField(default=100)
    max_speed = models.IntegerField(default=100)
    max_luck = models.IntegerField(default=100)

    class Meta:
        abstract = True

    def add_random_traits(self): #特性追加
        # 全ての特性を取得します。
        all_traits = Trait.objects.all()
        # 0から2までの整数を重み付けしてランダムに選びます。
        num_traits_weights = [1, 3, 2]
        num_traits_choices = [0, 1, 2]
        num_traits = random.choices(num_traits_choices, weights=num_traits_weights, k=1)[0]
        # 特性のリストからランダムに特性を選びます。
        random_traits = random.sample(list(all_traits), num_traits)
        # Horseインスタンスにランダムな特性を追加します。
        self.traits.add(*random_traits)

class Horse(BaseHorse): #ユーザーの馬モデル
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None) #誰の馬か
    position = models.IntegerField(default=1)# 順位を取得するためのフィールド

    #上昇値の保存
    stamina_increase = models.IntegerField(default=-1)
    speed_increase = models.IntegerField(default=-1)
    luck_increase = models.IntegerField(default=-1)

    price = models.IntegerField(default=0) #値段
    num_running = models.IntegerField(default=0) #レース出場回数
    num_top = models.IntegerField(default=0) # 1位とった回数
    remaining_racings = models.IntegerField(default=10) #残りレース数
    num_remaining_turns = models.IntegerField(default=150) #残りターン数
    retired = models.BooleanField(default=False)  # 引退フィールド

    # スタミナを増やす処理
    def increase_stamina(self, increase_value):
        new_stamina = self.stamina + increase_value

        # ステータスの上限より高くならないようにする
        if new_stamina > self.max_stamina:
            over_stamina = new_stamina - self.max_stamina
            self.price += over_stamina * 5
            self.stamina = self.max_stamina
        else:
            self.stamina = new_stamina
        self.save()

    # スピードを増やす処理
    def increase_speed(self, increase_value):
        new_speed = self.speed + increase_value
        if new_speed > self.max_speed:
            over_speed = new_speed - self.max_speed
            self.price += over_speed * 5
            self.speed = self.max_speed
        else:
            self.speed = new_speed
        self.save()

    # 運を増やす処理
    def increase_luck(self, increase_value):
        new_luck = self.luck + increase_value
        if new_luck > self.max_luck:
            over_luck = new_luck - self.max_luck
            self.price += over_luck * 5
            self.luck = self.max_luck
        else:
            self.luck = new_luck
        self.save()

    # トレーニングでの上昇値を決める処理
    @staticmethod
    def weighted_random():
        weights = [2, 10, 4, 1]  # 1が出る確率を10に、他の数値の確率は1に設定
        number_list = list(range(4))  # 0～3の数値
        return random.choices(number_list, weights=weights, k=1)[0]

    def retire(self):  # 引退メソッド
        self.retired = True
        self.save()

class CPU_Horse(BaseHorse): # CPU馬
    pass
