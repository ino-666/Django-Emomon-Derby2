from django import forms
from .models import Horse

class HorseForm(forms.ModelForm):
    # 絵文字選択肢
    EMOJI_CHOICES = [
        ('🐴', '🐴'),
        ('🐎', '🐎'),
        ('🦄', '🦄'),
        ('🫡', '🫡'),
        ('😔', '😔'),
        ('😵‍💫', '😵‍💫'),
        ('😳', '😳'),
        ('🤪', '🤪'),
        ('😵', '😵'),
        ('🥴', '🥴'),
        ('🤯', '🤯'),
        ('😮‍💨', '😮‍💨'),
        ('🤕', '🤕'),
        ('🤢', '🤢'),
        ('🤧', '🤧'),
        ('🤡', '🤡'),
        ('😎', '😎'),
        ('🤩', '🤩'),
        ('😍', '😍'),
        ('😶‍🌫️', '😶‍🌫️'),
        ('🤐', '🤐'),
        ('🥰', '🥰'),
        ('😗', '😗'),
        ('😙', '😙'),
        ('🤓', '🤓'),
        ('😈', '😈'),
        ('👹', '👹'),
        ('😤', '😤'),
        ('👻', '👻'),
        ('👾', '👾'),
        # 他の絵文字をここに追加
    ]
    emoji = forms.ChoiceField(choices=EMOJI_CHOICES)  # 絵文字選択フィールド

    # 名前入力フィールド（最大10文字）
    name = forms.CharField(
        max_length=10,
        label='エモモンの名前を入力してね',
        error_messages={
            'max_length': '名前は10文字以内です',
        }
    )

    class Meta:
        model = Horse
        fields = ['name','image', 'emoji',]  # 入力フィールドの設定