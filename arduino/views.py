from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import WaterLevel
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from collections import defaultdict

def arduino_index(request):
    entries = WaterLevel.objects.order_by('-timestamp')

    daily_values = defaultdict(list)

    # Group values by date
    for entry in entries:
        date = timezone.localtime(entry.timestamp).date()
        daily_values[date].append(entry.level_cm)

    labels = []
    daily_consumption = []

    for date, levels in daily_values.items():
        consumption = 0
        for i in range(1, len(levels)):
            diff = levels[i - 1] - levels[i]
            if diff > 0:
                consumption += diff
        labels.append(date.strftime('%d %b'))
        daily_consumption.append(round(consumption, 2))

    data = WaterLevel.objects.order_by('-timestamp')[:10][::-1]
    latest = data[-1] if data else None
    # average = round(sum(values) / len(values), 2) if values else 0
    status = "Low" if latest and latest.level_cm < 10 else "Normal" if latest and latest.level_cm < 25 else "High"

    context = {
        'labels': labels,
        # 'values': values,
        'consumptions': daily_consumption,
        'latest_level': latest.level_cm if latest else 'N/A',
        'latest_time': timezone.localtime(latest.timestamp).strftime('%I:%M %p') if latest else 'N/A',
        # 'average_level': average,
        'status': status
    }
    print('data', context)
    return render(request, 'arduino_index.html', context)


from django.http import JsonResponse
def get_latest_data(request):
    latest = WaterLevel.objects.last()
    
    if latest:
        return JsonResponse({
            'level': latest.level_cm,
            'time': timezone.localtime(latest.timestamp).strftime('%d %b %Y %I:%M:%S %p'),
            'status': "Low" if latest and latest.level_cm < 10 else "Normal" if latest and latest.level_cm < 90 else "High"

        })
    else:
        return JsonResponse({
            'level': 0,
            'time': 'No data available',
            'status': 'NA'
        })


@csrf_exempt
def upload(request):
    if request.method == 'POST':
        level = request.POST.get('level_cm')
        print('seeeee',level)
        if level:
            WaterLevel.objects.create(level_cm=float(level))
            return HttpResponse("OK")
    return HttpResponse("Failed")
