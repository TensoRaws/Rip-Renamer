import os
import mediainfomini
import shutil

def getinfo(file):
    height, depth, v_codec, a_codec = 0, 0, 'NA', 'NA'
    l_info = mediainfomini.get_media_info(file, 'a', 'b')
    max_a_bitrate = 0
    for i in range(len(l_info)):
        if 'RESOLUTION' in l_info[i]:
            height = l_info[i][l_info[i].find("x") + 1 :]
        if 'BIT.DEPTH' in l_info[i]:
            depth = l_info[i][l_info[i].find(":") + 2:l_info[i].find("bits") - 1]
        if 'VIDEO' in l_info[i]:
            end = l_info[i].find(', ')
            v_codec = l_info[i][l_info[i].find(":") + 2: end if end != -1 else 0]
        if 'AUDIO' in l_info[i]:
            if eval(l_info[i + 2]) > max_a_bitrate:
                max_a_bitrate = eval(l_info[i + 2])
                start = l_info[i + 3].rfind(',') + 2
                a_codec = l_info[i + 3][start if start != -1 else 0:]

    return height, depth, v_codec, a_codec


fn = input('名称输入(例Yosuga no Sora):')

sp_format_list = ['.mkv']

files = [os.path.join(os.curdir, f) for f in os.listdir(os.curdir) if f[f.rfind('.'):] in sp_format_list]
files.sort()
pack = files[0][files[0].rfind('.'):]  # 封装

with open('change_logs.txt', 'w+') as fp:
    for i in range(1, len(files) + 1):         # media info
        h, d, v, a = getinfo(files[i - 1])
        output = f'[SRVFI-Raws] {fn}' + ' [{:>02d}] '.format(i) + f'[{h}p {v}-{d}bit {a}]{pack}'
        src, dst = files[i - 1], output
        try:
            shutil.move(src, dst)
            fp.write(f'{src} -> {dst}, succ\r')
        except:
            fp.write(f'{src} -> {dst}, failed\r')

print("程序运行结果已记录在change_logs.txt中")
print("程序结束,输入任意内容退出...", end='')
_ = input("")
