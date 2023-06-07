import os
import shutil

log = 'change_logs.txt'  # 用于记录重命名结果


def rename(fi):
    # srt/ass -> del (删除字幕文件)
    if fi.endswith('.srt') or fi.endswith('.ass'):
        return 'DEL'

    # S1/S01 -> empty
    # HEVC-Main10 -> HEVC-10bit
    # 包含可不用识别直接替换字符的字典
    wo_dict = {'S1 ': '',
               'S01 ': '',
               'S1': '',
               'S01': '',
               'HEVC-Main10': 'HEVC-10bit',
               'HEVC Main10': 'HEVC-10bit',
               'HEVC 10bit': 'HEVC-10bit'}
    for k, v in wo_dict.items():
        fi = fi.replace(k, v)

    # SN -> S0N
    pos = 0
    while pos != len(fi) -1:
        if fi[pos] == 'S' and fi[pos + 1:pos + 2].isnumeric() and not fi[pos + 1: pos + 3].isnumeric():
            fi = fi.replace(fi[pos:pos+2], 'S{:>02d}'.format(int(fi[pos + 1:pos + 2])))
        pos += 1

    # S0NO -> S0N 0
    pos = 0
    while pos != len(fi) - 1:
        if fi[pos] == 'S' and fi[pos + 1: pos + 3].isnumeric():
            if fi[pos + 3] != ' ':
                fi = fi.replace(fi[pos:pos + 3], f'{fi[pos:pos + 3]} ')
            break
        pos += 1

    # NCOPSP -> [NCOP SP]
    if fi.find('NCOP SP') != -1:
        fi = fi.replace('NCOPSP', '[NCOP SP]')

    # - NN -> [NN]
    pos = fi.find('- ')
    if pos != -1 and fi[pos + 2: pos + 4].isnumeric():
        fi = fi.replace(fi[pos: pos + 4], fi[pos + 2: pos + 4])

    e_list = ['NCOP', 'NCED', 'OVA', 'SP']
    pos = -1
    for e in e_list:
        pos = fi.find(e)
        if pos != -1:
            break

    if pos != -1:
        # eN -> eNN
        if fi[pos + len(e): pos + len(e) + 1].isnumeric() and not fi[pos + len(e): pos + len(e) + 2].isnumeric():
            fi = fi.replace(fi[pos: pos + len(e) + 1], '{}{:>02d}'.format(e, int(fi[pos + len(e): pos + len(e) + 1])))

        if fi[pos - 1] != '[':
            # e -> [e]
            if not fi[pos + 1 + len(e)].isnumeric():
                fi = fi.replace(e, f'[{e}]')

            # eNN -> [e NN]
            if fi[pos + len(e): pos + len(e) + 2].isnumeric():
                fi = fi.replace(fi[pos: pos + len(e) + 2],
                                f'[{fi[pos: pos + len(e)]} {fi[pos + len(e): pos + len(e) + 2]}]')

    # e]END -> [e] END
    pos = fi.find(e)
    if pos != -1:
        end = pos
        while fi[end] != ']' and end != len(fi) - 1:
            end += 1
        if fi[end + 1] != ' ':
            fi = fi.replace(fi[pos: end + 1], f'{fi[pos: end + 1]} ')

    # ENN -> [NN]
    pos = 0
    while pos != len(fi):
        if fi[pos] == 'E' and fi[pos + 1: pos + 3].isnumeric():
            fi = fi.replace(fi[pos: pos + 3], f'[{fi[pos + 1: pos + 3]}]')
            break
        pos += 1

    # [NN]END -> [NN] END
    pos = 0
    while pos != len(fi) - 1:
        if fi[pos] == '[' and fi[pos + 1: pos + 3].isnumeric():
            if fi[pos + 4] == '[':
                fi = fi.replace(fi[pos: pos + 4], f'{fi[pos: pos + 4]} ')
            else:
                fi = fi.replace(fi[pos: pos + 5], f'{fi[pos: pos + 4]} ')
            break
        pos += 1

    # NNNNxCCCC -> CCCCp
    pos = 4
    while pos != len(fi) - 5:
        if fi[pos - 4: pos].isnumeric() and fi[pos + 1: pos + 5].isnumeric():
            fi = fi.replace(fi[pos - 4: pos + 5], f'{fi[pos + 1: pos + 5]}p')
            break
        pos += 1

    # [SRVFI-Raws] -> start
    if not fi.startswith('[SRVFI-Raws]'):
        fi = '[SRVFI-Raws] ' + fi.replace('[SRVFI-Raws]', '')

    return fi


# 遍历深层目录
def search(x, out=[]):
    if os.path.isdir(x):
        res = [os.path.join(x, f) for f in os.listdir(x)]
        if len(res) > 0:
            out += res
            for r in res:
                search(r, out)
    return out


# 去掉开头的 .\\ 以让shutil识别相对文件路径
files = [f[2:] for f in search(os.curdir) if os.path.isfile(f)]

with open(log, 'w+') as fp:
    for src in files:
        bn = os.path.basename(src)  # 得到 文件名.扩展名 进行重命名识别
        # 不对log和俩脚本进行重命名识别
        if bn.find('rename_python') != -1 or bn.find('withdraw_python') != -1 or bn.find(log) != -1:
            continue

        r = rename(bn)  # 重命名后的结果

        #  删除字幕文件
        if r == 'DEL':
            try:
                os.remove(src)
            except:
                continue
            continue

        dst = src[:src.rfind('\\') + 1] + r
        try:
            shutil.move(src, dst)
            fp.write(f'{src} -> {dst}, succ\r')
        except:
            fp.write(f'{src} -> {dst}, failed\r')
