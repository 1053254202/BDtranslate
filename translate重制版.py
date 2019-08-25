# ���߳�
import threading
# �߳�˯��
import time
# GUI
import tkinter
# md5
import hashlib
# �����
import random
# ���������װѡ��װ·����ģ��
from tkinter.filedialog import *
# ��ȡ���а�����ģ��
import pyperclip
# html����ģ��
import requests
# ����json��ʽ��ģ��
import json
# �ƶ��ļ�
import shutil

# ȫ��·��
path = ''


class Window(object):
    # ��ʼ��
    window = tkinter.Tk()
    # ����
    window.title("����")
    # �޸�ͼ��
    window.iconbitmap('favicon.ico')

    # ���ô��ڴ�С�������ô��ڴ�������ĳ�ʼλ��
    width = 200
    height = 120
    # ��ȡ����ĳߴ�
    screenHeight = window.winfo_screenheight()
    screenWidth = window.winfo_screenwidth()
    align = '%dx%d+%d+%d' % (width, height, screenWidth - 1.1 * width, screenHeight - 2.1 * height)
    # print(align)
    window.geometry(align)

    # ���ô����Ƿ������,True�ɱ䣬False���ɱ�
    window.resizable(width=False, height=False)

    # �����
    txt = tkinter.Entry(window)
    txt.grid(row=0, column=0, sticky=tkinter.W + tkinter.E + tkinter.N + tkinter.S, padx=5, pady=5)
    # ���¼�
    txt.bind("<Return>", fanyi)
    # �����
    result = tkinter.Entry(window)
    result.grid(row=1, column=0, sticky=tkinter.W + tkinter.E + tkinter.N + tkinter.S, padx=5, pady=5)
    # ��ʾ��ǰ��־�ļ����Ŀ¼�������
    var = tkinter.StringVar()
    var.set(path)
    pt = tkinter.Entry(window, textvariable=var)
    pt.grid(row=2, column=0, sticky=tkinter.W + tkinter.E + tkinter.N + tkinter.S, padx=5, pady=5)

    # ���밴ť
    btn = tkinter.Button(window, text="����", command=fanyi)
    btn.grid(row=0, column=1, sticky=tkinter.W + tkinter.E + tkinter.N + tkinter.S, padx=5, pady=5)
    # �򿪶�ȡ��־�ļ�
    folder = tkinter.Button(window, text='Ŀ¼', command=openFolder)
    folder.grid(row=1, column=1, sticky=tkinter.W, padx=5, pady=5)
    # �޸���־���Ŀ¼
    change = tkinter.Button(window, text='�޸�', command=lambda: changeFolder(pat=path))
    change.grid(row=2, column=1, sticky=tkinter.W, padx=5, pady=5)


# ���ļ���·��
def openFolder():
    os.system('explorer.exe /n,%s' % path)


# �޸���־�ļ����·��
def changeFolder(pat):
    # filepath = askopenfilename(title="�޸Ĵ����־�ļ���",initialdir=path)
    pt.delete(0, tkinter.END)
    filepath = askdirectory(title="�޸Ĵ����־�ļ���", initialdir=pat)
    # print(filepath)
    # ����path��ȫ�ֱ���path
    global path
    # Ĭ�ϵ�Ŀ¼�ָ��/,������Ҫ����תΪ\������\Ҫת��\\
    path = filepath.replace('/', '\\')
    # ����ǰ��־·����ʾ��pt��
    pt.insert(10, path)
    # �ƶ�֮ǰ����־�ļ���������ļ������ڣ�����Ϊ�ǵ�һ�δ�������־�ļ�
    if (os.path.exists(pat + "\\translate.log")):
        # ���Ŀ��Ŀ¼�и�ͬ���ļ�����ɾ��
        if (os.path.exists(filepath + "\\translate.log")):
            os.remove(filepath + "\\translate.log")
        # Ȼ���ƶ�ԴĿ¼��log�ļ�
        shutil.move(pat + "\\translate.log", filepath + "\\translate.log")


# ����־�ļ��鿴��־
def openFile():
    os.system('cmd /c %s' % (path + "\\translate.log"))


# �ٶȽӿ�
def baiduInterface(q):
    # ����ȥ�ٶȹ������뿪֮ͨ���ṩ�Ĳ���
    appid = "20190808000325167"
    orilan = "auto"
    to = ""
    # �ж�ԭ�����ԣ���Ϊԭ����������Ϊauto�������Ӣ�ľ�����toֵΪzh������to��ת��Ϊen
    # ord���ڽ�һ����ĸת����ASCLL��Ӧ������
    if (65 <= ord(q[0].upper()) <= 90):
        to = "zh"
    else:
        to = "en"
    # ���ɹٷ�Ҫ���һ�������
    salt = str(random.randint(1235467890, 9087654321))
    # �ٷ��ṩ����Կ
    secretKey = "msPayCcPEK0QRwRYwXRt"
    # combination��ϵ���˼
    com = appid + q + salt + secretKey
    # md5ת��
    sign = hashlib.md5(com.encode(encoding='UTF-8')).hexdigest()
    # ���ǰ��չٷ�Ҫ��ƴ�ӵõ�����������
    url = "http://api.fanyi.baidu.com/api/trans/vip/translate?q=" + q + "&from=" + orilan + "&to=" + to + "&appid=" + appid + "&salt=" + salt + "&sign=" + sign
    html = requests.get(url)
    # ������ʾ�������Ѻ�
    # showinfo("����",json.loads(html.text)["trans_result"][0]["dst"])
    # ��Ϊ���������ͨ����ڣ�һ�������Ʒ���һ�Σ���������ѵģ�����֤��һ�����ڿɷ���10�Σ�����һ�����ڳ���200W�η��룬�����Ĳ����շ�
    # ���Ե��̫Ƶ��ʱ���᷵��error_code���ж�json�Ƿ���ڸü������ھ͸�����ʾ���ݣ��������쳣�������
    # if ("error_code" in json.loads(html.text)):
    #     result.insert(10, "����ô�죡��")
    # else:
    #     src = json.loads(html.text)["trans_result"][0]["src"]
    #     dst = json.loads(html.text)["trans_result"][0]["dst"]
    #     result.insert(10, dst)
    # �쳣�������ⳬ��ʹ��Ƶ��
    # ������ʾ�û��ķ�ʽ�����Ѻã�������ʾ�������
    try:
        # ԭ��
        src = json.loads(html.text)["trans_result"][0]["src"]
        # ����
        dst = json.loads(html.text)["trans_result"][0]["dst"]
        # ���������ʾ��
        result.delete(0, tkinter.END)
        # д������
        result.insert(10, dst)
        # ׷��д���ļ��������򴴽�,���ļ�����׷������
        if (path != ''):
            with open(path + "/translate.log", "at+") as file:
                file.write(src + "\t\t\t" + dst + '\n')
    # �鿴�쳣��Ϣ
    except Exception as msg:
        result.delete(0, tkinter.END)
        # error_code�ǹٷ�json�ļ�����ʧ�ܷ��صĴ�����Ϣ��ʾjson�������
        if ("error_code" in json.loads(html.text)):
            # print(html.text)
            # python���õĲ����쳣����ӡ�쳣��ʾ
            # print(msg)
            if (path != ""):
                # ��error_msg��ӡ����־��
                with open(path + "/translate.log", "at+") as file:
                    file.write(json.loads(html.text)["error_code"] + "\t\t\t" + json.loads(html.text)["error_msg"])
            if json.loads(html.text)["error_code"] == "54003":
                # ��ʾ���ݣ�һ�������󳬹�����
                result.insert(10, "����ô�죡��")
            else:
                # ԭ������+�Ŵ�����BUG�������ҵĴ���BUG����������ҳ���ε�BUG��Ӧ���ǵ����ַ���ƴ�ӵķ���
                result.insert(10, "ԭ�Ĳ��ܰ���+��")


# ��ѡ����event��Ϊ���û�����س���ִ�з���󶨵��¼����󣬵����ť����ʱ������Ҫ����
def fanyi(*event):
    # ��ȡԭ������������
    q = txt.get()
    if (q == ""):
        result.insert(10, "�����롣����")
    else:
        baiduInterface(q)


# ���������̵߳��õĺ����������̺߳�������а������Ƿ�ı䣬�ı���ִ�������������ݣ����ı���ִ��
def run():
    # ��ǰ���а��ֵ
    curValue = ""
    # ��һ�μ��а��ֵ
    lastValue = ""
    while True:
        curValue = pyperclip.paste()  # ��ȡ���а帴�Ƶ�����
        try:
            if curValue != lastValue:  # �����⵽���а������иĶ�����ô�ͽ����ı����޸�
                lastValue = curValue
                q = curValue
                baiduInterface(q)
            # ���sleep�����һЩBUG����Ҳ��֪��Ϊʲô���о����߳��������еĺ���Ҫ�Ӹ�sleep����������˭�ܸ�����Ϊʲô
            # ���ſ���ע����������
            time.sleep(0.1)
        except KeyboardInterrupt:  # �����ctrl+c����ô���˳��������  ����������û���á����˴��ţ�
            break




# �������а����ݱ仯�߳̿���
threading.Thread(target=run).start()
# ������Ϣѭ��
window.mainloop()