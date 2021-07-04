import os, time
import random, string
import catch_stat
import subprocess
 
def popen(com, is_out = False):
    ex = subprocess.Popen(com, stdout=subprocess.PIPE, shell=True)
    out = 'f'
    try:
        out = ex.stdout.read().decode("GBK")
    except:
        out = ex.stdout.read().decode("utf-8")
    return out

def generate_randstring(num = 5):
    value = ''.join(random.sample(string.ascii_letters + string.digits, num))
    return(value)

def check_run():
    res = os.popen("adb shell \"dumpsys window | grep mCurrentFocus\"")
    now_run = res.read()
    #print(now_run)
    if("moe.low.arc" not in now_run):
        if("mCurrentFocus" in now_run):
            return("未检测到Arcaea运行")
        elif("no devices" in now_run):
            return("您没有连接设备,或者没有打开USB调试")
        elif("adb" in now_run):
            return("您的电脑没有安装ADB")

    else:
        return("ok")

def start(lang):
    #print("您的Arcaea系统语言是(1:非日语 2:日本語):")
    #lang = str(input())
    #if(lang == '2'):
    #    print("注意:日语部分歌曲识别准确率较低")

    #tstat = check_run()
    #if(tstat == "ok"):
        #while True:
    iname = generate_randstring(5)
    fstat = popen("adb shell /system/bin/screencap -p /sdcard/%s.png" % iname)
    fstat = popen("adb pull /sdcard/%s.png /temp/%s.png" % (iname, iname))
    fstat = popen("adb shell rm /sdcard/%s.png" % iname)

    if(os.path.isfile("/temp/%s.png" % iname) == False):
        print("游玩数据获取失败")
    else:
        now_info = catch_stat.stat_identify(("/temp/%s.png" % iname), lang)
        now_stat = now_info[0]
        now_score = now_info[1]
        os.remove("/temp/%s.png" % iname)
        #print(now_stat)

        #time.sleep(2)
    if(now_stat != "In Menu"):
        now_stat = "Playing " + now_stat

    if(now_score == "0"):
        now_score = "Device"
    else:
        try:
            now_score = str("%.8d" % int(now_score))
            now_score = now_score[0:2] + '\'' + now_score[2:5] + '\'' + now_score[5:8]
        except Exception as sb:
            print(sb)
            now_score = "Device"

    return(
            {'state': now_stat,
            'small_image': "grass_2",
            'large_image': "main_icon",
            'large_text': "Arcaea",
            'small_text': "Hikari",
            'details': now_score,
            'buttons': [{"label": "去劝架", "url": "http://127.0.0.1:11451/qwq"}, {"label": "我也要和她们打架!", "url": "http://127.0.0.1:11451/owo"}]
            }
            )

    #else:
        #print(tstat)
        #return(None)
