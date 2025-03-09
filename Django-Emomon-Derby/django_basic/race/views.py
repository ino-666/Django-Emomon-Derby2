from django.views import View
from django.shortcuts import render
from horse.models import Horse, CPU_Horse
from random import sample
from django.shortcuts import render, redirect, get_object_or_404
import random
from django.contrib import messages
from django.http import HttpResponse


# レースに出場する馬を選択する
class HorseStatusView(View):
    template_name = 'race/race_venue.html'

    # 馬とCPUの馬を取得し、テンプレートに渡す
    def get(self, request, horse_id, *args, **kwargs):
        horse = Horse.objects.get(id=horse_id)
        all_cpu_horses = list(CPU_Horse.objects.all())
        if len(all_cpu_horses) >= 3:
            cpu_horses = sample(all_cpu_horses, 3)
        else:
            cpu_horses = all_cpu_horses
        cpu_horses = sorted(cpu_horses, key=lambda horse: horse.id)
        context = {
            'horse': horse,
            'cpu_horses': cpu_horses,
        }
        request.session['cpu_horses_ids'] = [horse.id for horse in cpu_horses]
        return render(request, self.template_name, context)

    # 馬とCPUの馬を取得し、テンプレートに渡す
    def post(self, request, *args, **kwargs):
        horse_id = request.POST['horse']
        horse = Horse.objects.get(id=horse_id)
        all_cpu_horses = list(CPU_Horse.objects.all())
        if len(all_cpu_horses) >= 3:
            cpu_horses = sample(all_cpu_horses, 3)
        else:
            cpu_horses = all_cpu_horses
        cpu_horses = sorted(cpu_horses, key=lambda horse: horse.id)
        context = {
            'horse': horse,
            'cpu_horses': cpu_horses,
        }
        request.session['cpu_horses_ids'] = [horse.id for horse in cpu_horses]
        return render(request, self.template_name, context)

# レース画面へ馬の情報を渡す
def uma_uma_view(request, horse_id):
    horse = Horse.objects.get(id=horse_id)
    cpu_horses_ids = request.session.get('cpu_horses_ids', [])
    cpu_horses = CPU_Horse.objects.filter(id__in=cpu_horses_ids)
    cpu_horses = sorted(cpu_horses, key=lambda horse: horse.id)
    context = {
        'horse': horse,
        'cpu_horses': cpu_horses,
    }
    return render(request, 'race/uma_uma.html', context)


#レース終了後にhome.htmlに遷移する処理ステータスを上昇、所持金上昇の処理もここにいれています
def results(request, horse_id):
    # IDから馬を取得
    horse = get_object_or_404(Horse, id=horse_id)
    horse_position = request.session.get('horse_position', None)
    if horse_position is not None:
        horse.position = int(horse_position)
        horse.save()

    # 馬のステータスを上げる
    upper_bound = max(1, 10 - horse.stamina // 10)  # 馬のスタミナが高いほど上昇値の上限が低くなる
    horse.stamina_increase = random.randint(0, upper_bound)
    horse.increase_stamina(horse.stamina_increase)
    upper_bound = max(1, 10 - horse.speed // 10)  # 馬のスピードが高いほど上昇値の上限が低くなる
    horse.speed_increase = random.randint(0, upper_bound)
    horse.increase_speed(horse.speed_increase)
    upper_bound = max(1, 10 - horse.luck // 10)  # 馬の運が高いほど上昇値の上限が低くなる
    horse.luck_increase = random.randint(0, upper_bound)
    horse.increase_luck(horse.luck_increase)

    # ユーザーの所持金、馬の価値を増やす
    base_increase_value = 50
    if horse.position == 1:
        horse.price += 50
        horse.num_top += 1 # 優勝した回数を増やす
        base_increase_value = 700
    elif horse.position == 2:
        horse.price += 25
        base_increase_value = 350
    elif horse.position == 3:
        horse.price += 10
        base_increase_value = 150
    increase_value = base_increase_value*1.5 if horse.traits.filter(id=9).exists() else base_increase_value  # Traitのidが9の場合は150、それ以外は100
    request.user.increase_money(increase_value)

    # レース数を増やし、出場回数以上になったら引退させる
    horse.num_running += 1
    horse.save()
    if horse.num_running == horse.remaining_racings or horse.num_remaining_turns == 0:
        horse.price += horse.stamina + horse.speed + horse.luck
        horse.price *= 1.5 if horse.traits.filter(id=9).exists() else 1
        messages.success(request, f'{horse.name}はこれで引退です。お疲れ様でした🙇<br>お祝いに¥{horse.price}を受け取った。')
        request.user.increase_money(horse.price)
        horse.retire()
    else:
        messages.success(request, 'お疲れ様でした。')

    return render(request, 'race/results.html')  # results.htmlテンプレートをレンダリング

# セッション
def set_session(request):
    request.session['horse_position'] = request.POST.get('horse_position')
    return HttpResponse('Session data set')

# def select_character(request):
#     if request.method == 'POST':
#         # Assume that selected_characters is obtained from the POST data
#         selected_characters = request.POST.get('selected_characters')
#         request.session['selected_characters'] = selected_characters
#         # Continue with the rest of the view...



# def display_page(request):
#     selected_characters = request.session.get('selected_characters', default_value)
#     # Use selected_characters to generate the context for the template
#     context = {'characters': selected_characters}
#     return render(request, 'template_name.html', context)

