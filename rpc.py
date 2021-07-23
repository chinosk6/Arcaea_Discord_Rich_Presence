from pypresence import Presence
import time
import update_stat
import os

global char

client_id = "860796517240274994"
rich_presence = Presence(client_id)

def connect():
    return rich_presence.connect()

def connect_loop(lang, retries=0):
    if retries > 10:
        return
    try:
        connect()
    except:
        print("Error connecting to Discord")
        time.sleep(10)
        retries += 1
        connect_loop(lang, retries)
    else:
        update_loop(lang)

def get_data():
    return(
            {'state': "目前对立占上风",
            'small_image': "grass_2",
            'large_image': "grass_1",
            'large_text': "Tairitsu",
            'small_text': "Hikari",
            'details': "光和对立正在打架",
            'buttons': [{"label": "去劝架", "url": "http://127.0.0.1:11451/qwq"}, {"label": "我也要和她们打架!", "url": "http://127.0.0.1:11451/owo"}]
            }
            )

def update_loop(lang):
    global char
    start_time = int(time.time())
    try:
        model = str(os.popen("adb -d shell getprop ro.product.model").read())

        while True:
            rpc_data = update_stat.start(lang)
            if(rpc_data['details'] == "Device"):
                det = model.replace('\n', '')
            else:
                det = "Score:" + rpc_data['details']

            rich_presence.update(state = rpc_data['state'],
                                 small_image = char,
                                 large_image = rpc_data['large_image'],
                                 large_text = rpc_data['large_text'],
                                 #small_text = rpc_data['small_text'],
                                 details = det,
                                 #buttons = rpc_data['buttons'],
                                 start = start_time)
            print("状态已更新:" + det + ' - ' + rpc_data['state'])
            time.sleep(5)
    except Exception as sb:
        print(sb)
        rich_presence.clear()
        time.sleep(5)
        update_loop(lang)


if __name__ == '__main__':
    tstat = update_stat.check_run()
    if(tstat == "ok"):
        print("您的Arcaea系统语言是(1:非日语 2:日本語):")
        lang = str(input())
        if(lang == '2'):
            print("注意:日语部分歌曲识别准确率较低")
        print("输入角色编号:")
        char = str(input()) + "_icon"

        try:
            print("开始运行")
            connect_loop(lang)
        except KeyboardInterrupt:
            print("服务停止")
    
    else:
        print(tstat)
