# Water Tank Level Estimation Project

This project estimates the water level in a tank using an **Ultrasonic Sensor (HC-SR04)** connected to an **Arduino UNO**, with data visualized on a **Django web dashboard**. It features real-time water level monitoring, alerts for low/high levels, and data logging with interactive charts.

## 📦 Components Used
- Arduino UNO
- Ultrasonic Sensor (HC-SR04)
- Buzzer (for alerts)
- Jumper wires
- (Optional) LCD Display (initially used, removed later)

## ⚙️ Working Principle
The ultrasonic sensor measures the distance between itself and the water surface. The tank height is predefined (e.g., 30 cm), so the water level is calculated as:

```math
Water Level = Tank Height - Distance from Sensor
```

## 🧠 Features
- Live sensor data upload via serial port
- Django backend for data storage and visualization
- Realistic animated water tank chart with wave motion
- Daily water consumption graph (based on level difference)
- API endpoint for dynamic JS chart updates

## 🖥️ Arduino Code (Final Version)
```cpp
#define trigPin 9
#define echoPin 10
#define buzzerPin 8
#define tankHeight 30  // cm

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(buzzerPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH);
  float distance = duration * 0.034 / 2;
  float level = tankHeight - distance;

  Serial.println(level);

  if (level < 5 || level > 27) {
    digitalWrite(buzzerPin, HIGH);
  } else {
    digitalWrite(buzzerPin, LOW);
  }

  delay(2000);
}
```

## 🐍 Python Script (Serial to Django)
```python
import serial
import requests
import time

SERIAL_PORT = 'COM3'
BAUD_RATE = 9600
DJANGO_URL = 'http://127.0.0.1:8000/upload/'

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)

while True:
    try:
        line = ser.readline().decode().strip()
        if line:
            print("Sending:", line)
            requests.post(DJANGO_URL, data={'level_cm': line})
    except Exception as e:
        print("Error:", e)
```

## 🌐 Django Views Sample
```python
from django.http import JsonResponse
from django.utils import timezone
from collections import defaultdict
from .models import WaterLevel

def get_latest_data(request):
    entries = WaterLevel.objects.order_by('timestamp')
    daily_values = defaultdict(list)
    for entry in entries:
        date = timezone.localtime(entry.timestamp).date()
        daily_values[date].append(entry.level_cm)

    labels = []
    consumptions = []
    for date, levels in daily_values.items():
        diff = sum(max(0, levels[i - 1] - levels[i]) for i in range(1, len(levels)))
        labels.append(date.strftime('%d %b'))
        consumptions.append(round(diff, 2))

    return JsonResponse({
        'labels': labels,
        'consumptions': consumptions,
    })
```

## 📊 Chart.js (Dynamic Chart)
```html
<script>
fetch('/api/latest/').then(res => res.json()).then(data => {
    // Initialize Chart.js here with data.labels and data.consumptions
});
</script>
```

## 📅 Submission Deadline
**Date:** 31st May 2025

---

## 👨‍💻 Developed By
Group of Engineering Students based on hands-on IoT + Web Development training.

If you have questions or want to contribute, open an issue or PR!

---

✔️ *Real-time water monitoring made simple and visual.*
