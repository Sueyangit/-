#-*- coding: utf-8 -*-
#  语音合成 WebAPI 接口调用示例 接口文档（必看）：https://doc.xfyun.cn/msc_android/%E8%AF%AD%E9%9F%B3%E5%90%88%E6%88%90.html
#  webapi 合成服务参考帖子：http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=38997&extra=
#  webapi是单次只支持1000个字节，具体看您的编码格式，计算一下具体支持多少文字
# （Very Important）创建完webapi应用添加合成服务之后一定要设置ip白名单，找到控制台--我的应用--设置ip白名单，如何设置参考：http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=41891
#  合成发音人自动添加获取测试权限使用方法：登陆开放平台https://www.xfyun.cn/后--我的应用（必须为webapi类型应用）--添加在线语音合成（已添加的不用添加）--发音人管理---添加发音人--测试代码里需修改发音人参数
#  错误码链接：https://www.xfyun.cn/document/error-code （code返回错误码时必看）
#  @author iflytek


import pyaudio
import wave
import os

    
def play_xunfei(wavfilename):

    CHUNK = 1024
    # 从目录中读取语音
#    wf = wave.open('mic4.wav', 'rb')
    wf = wave.open(wavfilename, 'rb')
    # read data
    data = wf.readframes(CHUNK)
    # 创建播放器
    p = pyaudio.PyAudio()
    # 获得语音文件的各个参数
    FORMAT = p.get_format_from_width(wf.getsampwidth())
    CHANNELS = wf.getnchannels()
    RATE = wf.getframerate()
#    print('FORMAT: {} \nCHANNELS: {} \nRATE: {}'.format(FORMAT, CHANNELS, RATE))
    # 打开音频流， output=True表示音频输出
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    frames_per_buffer=CHUNK,
                    output=True)
    # play stream (3) 按照1024的块读取音频数据到音频流，并播放
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)
        
        
        
import requests
import time
import hashlib
import base64
#  合成webapi接口地址
URL = "http://api.xfyun.cn/v1/service/v1/tts"
#  音频编码(raw合成的音频格式pcm、wav,lame合成的音频格式MP3)
AUE = "raw"
#  应用APPID（必须为webapi类型应用，并开通语音合成服务，参考帖子如何创建一个webapi应用：http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=36481
APPID = "5ce265c9"
#  接口密钥（webapi类型应用开通合成服务后，控制台--我的应用---语音合成---相应服务的apikey）
API_KEY = "dedd145d73ca0e1fd5e70a77f38365a1"

# 组装http请求头
def getHeader():
    curTime = str(int(time.time()))#1558401768
    # ttp=ssml
    param = "{\"aue\":\"" + AUE + "\",\"auf\":\"audio/L16;rate=16000\",\"voice_name\":\"xiaoyan\",\"engine_type\":\"intp65\"}"
#    print("param:{}".format(param))

    paramBase64 = str(base64.b64encode(param.encode('utf-8')), 'utf-8')
#    print("x_param:{}".format(paramBase64))

    m2 = hashlib.md5()
    m2.update((API_KEY + curTime + paramBase64).encode('utf-8'))

    checkSum = m2.hexdigest()
#    print('checkSum:{}'.format(checkSum))

    header = {
        'X-CurTime': curTime,
        'X-Param': paramBase64,
        'X-Appid': APPID,
        'X-CheckSum': checkSum,
        'X-Real-Ip': '127.0.0.1',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }
#    print(header)
    return header


def getBody(text):
    data = {'text': text}
    return data


def writeFile(file, content):
    with open(file, 'wb') as f:
        f.write(content)
    f.close()

#  待合成文本内容
#with open('t2v_test.txt','r',encoding='utf-8') as f:
#    line = f.read()
#r = requests.post(URL, headers=getHeader(), data=getBody("内容"))
#待合成文本，使用utf-8编码，需urlencode，长度小于1000字节 一个汉字两个字节
def readtxt_by_xunfei(readcontent):
    print('讯飞正在支持朗读助手')
    r = requests.post(URL, headers=getHeader(), data=getBody(readcontent))
    
    contentType = r.headers['Content-Type']
    if contentType == "audio/mpeg":
        sid = r.headers['sid']
        if AUE == "raw":
    #        print(r.content)
    #   合成音频格式为pcm、wav并保存在audio目录下
#            writeFile("audio/" + sid + ".wav", r.content)
            writeFile(sid + ".wav", r.content)
        else:
    #        print(r.content)
    #   合成音频格式为mp3并保存在audio目录下
            writeFile("audio/" + "xiaoyan" + ".mp3", r.content)
        wavfilename=sid + ".wav"
        
        print("success, sid = " + sid)
        play_xunfei(wavfilename)
        os.remove(wavfilename)
    else:
    #   错误码链接：https://www.xfyun.cn/document/error-code （code返回错误码时必看）
        print(r.text)
def readtxt_by_SAPI(content):
    print('SAPI正在支持朗读助手')
    import win32com.client
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak(content)  
    
def readtxt_by_pyttsx3(content):
    print('pyttsx3正在支持朗读助手')
    import pyttsx3
    engine = pyttsx3.init()
    volume=engine.getProperty('volume')
    engine.setProperty('volume', volume + 0.25)
    engine.say(content)
    engine.runAndWait()
    engine.stop()   
def readnews(titlelist):
    for i in titlelist:
#        readtxt_by_xunfei(i)
#        readtxt_by_SAPI(i)
        readtxt_by_pyttsx3(i)
import paqu_sina    
readnews(paqu_sina.newtitlelist())