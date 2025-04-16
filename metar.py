import requests
from datetime import datetime
import re
import time
from datetime import datetime, timezone
station = "LTAC"  # ICAO kodu (örneğin: LTAC - Ankara Esenboğa)

def fetch_and_save_wx():
    try:
        url = f"https://tgftp.nws.noaa.gov/data/observations/metar/stations/{station}.TXT"
        response = requests.get(url)
        lines = response.text.strip().split("\n")

        now = datetime.now(timezone.utc)
        time_str = now.strftime("%b %d %Y %H:%M")

        metar = lines[1]

        wind_match = re.search(r"(\d{3})(\d{2,3})G?(\d{2,3})?KT", metar)
        temp_match = re.search(r"M?(\d{2})/M?(\d{2})", metar)
        press_match = re.search(r"A(\d{4})", metar)

        humidity = 50
        rain_1h = 0
        rain_24h = 0
        rain_midnight = 0

        if wind_match:
            wind_dir = int(wind_match.group(1))
            wind_spd = int(wind_match.group(2))
            wind_gust = int(wind_match.group(3)) if wind_match.group(3) else wind_spd
        else:
            wind_dir = wind_spd = wind_gust = 0

        if temp_match:
            temp = int(temp_match.group(1))
            temp = -temp if 'M' in metar[temp_match.start()] else temp
            temp_f = int(temp * 9 / 5 + 32)
        else:
            temp_f = 70

        if press_match:
            inhg = int(press_match.group(1)) / 100.0
            pressure = int(inhg * 33.8639 * 10)
        else:
            pressure = 10150

        wx_line = f"{wind_dir:03d}/{wind_spd:03d}g{wind_gust:03d}t{temp_f:03d}r{rain_1h:03d}p{rain_24h:03d}P{rain_midnight:03d}h{humidity:02d}b{pressure:05d}"

        with open("wxnow.txt", "w") as f:
            f.write(f"{time_str}\n")
            f.write(f"{wx_line}\n")

        print(f"[{time_str}] wxnow.txt güncellendi.")

    except Exception as e:
        print("Hata oluştu:", e)

# Her 10 dakikada bir çalıştır
while True:
    fetch_and_save_wx()
    time.sleep(600)  # 600 saniye = 10 dakika
