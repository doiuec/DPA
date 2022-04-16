import os
import MyAES
import numpy as np
import matplotlib.pyplot as plt

#ハミングウェイトを計算
def hamming_distance(a):
    binary = bin(a)
    return binary.count("1")

print('start')

key = np.array([0x00, 0x01, 0x02, 0x03,
				0x04, 0x05, 0x06, 0x07,
				0x08, 0x09, 0x0a, 0x0b,
				0x0c, 0x0d, 0x0e, 0x0f])

aes = MyAES.SimpleAES128(key)

key = []

# 縦 : 時間, 横 : サンプル数
waves  = np.load('./waves_0.npy').transpose()
# 縦 : 鍵(16byte) 横 : サンプル数
hw_R10 = np.load('./correct_HW_R10.npy').transpose().astype(np.uint16)
# 平文
pt = np.load('./PTs_ui8_1000_vol0.npy')

head = 0
tail = 500

# 必要な部分だけを取り出す
waves = waves[head:tail]

# corrcoef(x, y)
# 必要な部分だけ
corrcoef = np.array(np.corrcoef(w, hw_R10)[0,1:] for w in waves)

print('hw_R10')

# 与えられた平文に対するハミングウェイトを求める
for p in pt:
    aes.encrypt(p)
    hw = []
    sb = []
    sub10 = aes.invShiftRows(aes.ct)
    for s in sub10:
        sbox = [aes.ISBOX(s^k) for k in range(256)] # sbox前まで計算し直す
        sb.appens(sbox)
    sb = np.array(sb).flatten() #sbは、平文に対するsbox前までの値
    hm = []
    for s in sb:
        humming = hamming_distance(s)
        hm.append(humming) # hmは、sbに対するハミングウェイト
    hw.append(hm)
    hw = np.array(hw) #hwには、鍵候補に対するハミングウェイトがそれぞれ入っている(16 * 256)
    np.save("'./HW_all_key_R10.npy", hw)

print('HW_all_key_R10')

hw_key = './HW_all_key_R10.npy'
hw = np.load(hw_key).transpose()

'''
ここまでで
１．波形と正解鍵に対する相関係数を求めた
２．鍵候補を用いて暗号文から10R sbox前までの値を逆算し、その結果のハミングウェイトを計算した

次に
３．波形と鍵候補からのハミングウェイトの相関係数を計算する
４．鍵が正解していれば、波形と鍵候補に相関がある
'''

wave_hw = []
for wave in waves:
    wave_hw.append(np.corrcoef(wave,hw)[0,1:])

print('correlation')

correlation = np.array(wave_hw) # numpyにする
correlation = np.abs(correlations).max(0) # 軸に対する最大値を決める、つまり相関係数の最大値

for i in range(16):
    key.append(correlation[i*256:(i+1)*256].argmax())

key = np.array(key)

print('End')
print('')
print('-------')
print(key)
print('-------')
