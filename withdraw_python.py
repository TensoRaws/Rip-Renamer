import shutil

with open('change_logs.txt', 'r') as fp:
    x = fp.readline()
    while x:
        src = x[:x.find('->') - 1]
        dst = x[x.find('->') + 3:x.rfind(', succ')]
        try:
            shutil.move(dst, src)
        except:
            print('err')
        x = fp.readline()