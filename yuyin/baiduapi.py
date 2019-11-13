import pyaudio
import wave
from aip import AipSpeech
import time
import requests
import json

DEV_PID = "1537"


# 用Pyaudio库录制音频
#   out_file:输出音频文件名
#   rec_time:音频录制时间(秒)
def audio_record(out_file, rec_time):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16  # 16bit编码格式
    CHANNELS = 1  # 单声道
    RATE = 16000  # 16000采样频率

    p = pyaudio.PyAudio()
    # 创建音频流
    stream = p.open(format=FORMAT,  # 音频流wav格式
                    channels=CHANNELS,  # 单声道
                    rate=RATE,  # 采样率16000
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Start Recording...")

    frames = []  # 录制的音频流
    # 录制音频数据
    for i in range(0, int(RATE / CHUNK * rec_time)):
        data = stream.read(CHUNK)
        frames.append(data)

    # 录制完成
    stream.stop_stream()
    stream.close()
    p.terminate()

    print("Recording Done...")

    # 保存音频文件
    wf = wave.open(out_file, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


# 读取paudio录制好的音频文件, 调用百度语音API, 设置api参数, 完成语音识别
#    client:AipSpeech对象
#    afile:音频文件
#    afmt:音频文件格式(wav)
def aip_get_asrresult(client, afile, afmt):
    # 选项参数:
    # cuid    String  用户唯一标识，用来区分用户，填写机器 MAC 地址或 IMEI 码，长度为60以内
    # dev_pid String  语言类型(见下表), 默认1537(普通话 输入法模型)
    # 识别结果已经被SDK由JSON字符串转为dict
    result = client.asr(get_file_content(afile), afmt, 16000, {"dev_pid": DEV_PID})
    # print(result)
    # 如果err_msg字段为"success."表示识别成功, 直接从result字段中提取识别结果, 否则表示识别失败
    if result["err_msg"] == "success.":
        # print(result["result"])
        return result["result"]
    else:
        # print(result["err_msg"])
        return ""


def xiaosi(strtxt):
    try:
        xiaosiid = "e1fd6a1f977549f4a28e42c65ca9e61e"
        userid = "1005268416@qq.com"
        url = "https://api.ownthink.com/bot?appid={}&userid={}&spoken={}".format(xiaosiid, userid, strtxt)
        jsondate = json.loads(requests.get(url).text)
        if jsondate["message"] == "success":
            return jsondate["data"]["info"]["text"]
    except Exception as e:
        return "出现错误。"

def yaya(strtxt):
    try:
        url = "http://api.qingyunke.com/api.php?key=free&appid=0&msg={}".format(strtxt)
        jsondate = json.loads(requests.get(url).text)
        if jsondate["result"] == 0:
            return jsondate["content"]
    except Exception as e:
        return "出现错误。"


# 控制鼠标滚动
# def mouse_control(dir_tr):
#     MOVE_DX = 5 # 每次滚动行数
#     ms = PyMouse()
#     horizontal = 0
#     vertical = 0
#     if dir_tr.find("上") != -1: # 向上移动
#         vertical = MOVE_DX
#         #print("vertical={0}, 向上".format(vertical))
#     elif dir_tr.find("下") != -1: # 向下移动
#         vertical = 0 - MOVE_DX
#         #print("vertical={0}, 向下".format(vertical))
#     elif dir_tr.find("左") != -1: # 向左移动
#         horizontal = 0 - MOVE_DX
#         #print("horizontal={0}, 向左".format(horizontal))
#     elif dir_tr.find("右") != -1: # 向右移动
#         horizontal = MOVE_DX
#         #print("horizontal={0}, 向右".format(horizontal))
#
#     #print("horizontal, vertical=[{0},{1}]".format(horizontal, vertical))
#     # 通过scroll(vertical, horizontal)函数控制页面滚动
#     # 另外PyMouse还支持模拟move光标,模拟鼠标click,模拟键盘击键等
#     ms.scroll(vertical, horizontal)
APP_ID = "17765747"
API_KEY = "6akzMKQZ6fTTmSTvpQdiMpA8"
SECRET_KEY = "pG8oB6vmWcmH5vtVtaYXtjHOGdiGUKRX"
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
AUDIO_FORMAT = 'pcm'
while (True):
    AUDIO_OUTPUT = "my.pcm"
    # 请说出语音指令，例如["向上", "向下", "向左", "向右"]
    print("\n\n==================================================")
    print("Please tell me the command(limit within 3 seconds):")
    # print("Please tell me what you want to identify(limit within 10 seconds):")
    audio_record(AUDIO_OUTPUT, 3)  # 录制语音指令
    # print("Identify On Network...")
    asr_result = aip_get_asrresult(client, AUDIO_OUTPUT, AUDIO_FORMAT)  # 识别语音指令
    if len(asr_result) != 0:  # 语音识别结果不为空，识别结果为一个list
        print("我:", asr_result[0])
        # print("Start Control...")
        xi = yaya(asr_result[0])
        # mouse_control(asr_result[0]) # 根据识别结果控制页面滚动
        print("小思", xi)
        if asr_result[0].find("退出") != -1:  # 如果是"退出"指令则结束程序
            break;
        time.sleep(1)  # 延时1秒
