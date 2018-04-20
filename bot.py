import os
import psutil
import telegram
from emoji import emojize
from modules.wvgrabber import app as wvgrabber

default_keypad = [
    [telegram.KeyboardButton(emojize(":clapper: Grab video link", use_aliases=True)),
     telegram.KeyboardButton(emojize(":bar_chart: System info", use_aliases=True))]
]


class ApiState:
    """
    State store

    active_state
    active_func
    """
    pass


class BotAPI:
    def __init__(self, cmd):
        try:
            if getattr(ApiState, 'active_state'):
                func = getattr(ApiState, 'active_func')
                self.answ, self.keypad = func(cmd)
                return
        except AttributeError:
            pass

        cmd_dict = {
            emojize(":clapper: Grab video link", use_aliases=True): self.watch_video,
            emojize(":bar_chart: System info", use_aliases=True): self.sysinfo,
        }
        func = cmd_dict.get(cmd)

        if func:
            self.answ, self.keypad = func()
        else:
            self.answ = 'Command not found'
            self.keypad = default_keypad

    def watch_video(self, video_link=None):
        if not video_link:
            setattr(ApiState, 'active_state', True)
            setattr(ApiState, 'active_func', self.watch_video)
            answ = 'Insert link on page with video player...'
            keypad = ''
        else:
            answ = wvgrabber.url_reader(video_link)
            keypad = default_keypad
            delattr(ApiState, 'active_state')
            delattr(ApiState, 'active_func')
        return answ, keypad

    @staticmethod
    def sysinfo():
        common_info = "Used RAM: {} %\n" \
                      "Used HDD: {} %\n" \
                      "Used CPU: {} %\n".format(psutil.virtual_memory().percent,
                                                psutil.disk_usage('/').percent,
                                                psutil.cpu_percent())
        try:

            cputemp_raw = os.popen('vcgencmd measure_temp').readline()
            cputemp = cputemp_raw.replace("temp=", "").replace("\n", "")
            rpi_specific = "Temp CPU: {}\n".format(cputemp)
        except Exception as e:
            rpi_specific = ''

        try:
            import Adafruit_DHT
            humidity, temperature = Adafruit_DHT.read_retry(22, 2)
            dht_specific = "--------\nAir temp: {} C\n" \
                           "Humidity: {} %\n".format(int(temperature), int(humidity))
        except Exception as e:
            dht_specific = ''

        common_info += rpi_specific
        common_info += dht_specific

        keypad = default_keypad
        return common_info, keypad

    def reboot(self):
        return 'Nope :/', default_keypad
