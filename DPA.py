import os
import MyAES
import numpy as np
import matplotlib.pyplot as plt

key = np.array([0x00, 0x01, 0x02, 0x03,
				0x04, 0x05, 0x06, 0x07,
				0x08, 0x09, 0x0a, 0x0b,
				0x0c, 0x0d, 0x0e, 0x0f])

aes = MyAES.SimpleAES128(key)
#waves = np.load('./data/wave/waves_1250.npy', allow_pickle=True)
waves = np.load('./data/wave/waves_1.npy', allow_pickle=True)
#waves = waves[:,1920:4155]
print(waves.shape)

#waves = waves[:, 7200:7700]

#print(waves)
#print(wave)
#
#x = np.linspace(0, 1, 2235)
#plt.plot(x, waves[0])
#plt.show()
#


crypto = np.load('./data/wave/CTs_ui8_1000_vol0.npy')
plain =np.load('./data/wave/PTs_ui8_1000_vol0.npy')

'''
        鍵があっている場合：
            A_ISboxの答えも合っていて、波形の分け方も合っている
            なので、0,1で波形が分かれる
            グループごとの波形平均をとると、10Rにおける0,1の消費電力で
            分けられ、0のときの消費電力と1のときの消費電力がわかる
            0,1で消費電力が明らかに違うため、大きな差になる
        鍵が間違っている場合：
            A_ISboxの答えが間違っていて、波形の分け方も間違っている
            なので、0,1ではなくランダムに波形が分かれる
            グループごとの波形平均をとると、ランダムに分けられる
            ランダムなため、差も少ない
'''
column, row = crypto.shape

for a in range(16):
    guess = []
    for i in range(256):
        count = 0
        set0 = []
        set1 = []
        for j in range(column):
            #Plain = plain[j]
            #cry_result = aes.encrypt(Plain)
            #print(cry_result)
            #print("---")
            #print(crypto[j])
            #print("-----")
            #print(np.all(cry_result == crypto[j]))
            #print("-------")
            P_ISBOX = crypto[j, a]^i  #最初のAddRoundKeyとXOR
            A_ISBOX = aes.ISBOX[P_ISBOX]  #IShitRowsを飛ばして, ISBox
            if A_ISBOX & 0x1 == 0:  #ISbox後の最後1ビットを抽出し, 0,1 を判定
                set0.append(waves[count])
            else:
                set1.append(waves[count])
            count += 1

        set0 = np.array(set0)
        set0 = np.mean(set0, axis = 0)
        set1 = np.array(set1)
        set1 = np.mean(set1, axis = 0)

        d = abs(set0 - set1)
        #x = np.linspace(0, 1, 7992)
        #plt.plot(x, d)
        #plt.show()
        dmax = np.max(d)
        guess.append(dmax)
        #print(i)
        #x = np.linspace(0, 1, 7992)
        #plt.plot(x, waves[0])
        #plt.show()


        
        ##################guess the key(R10)############################
    guess_sorted = np.sort(guess)[::-1]
    #print(guess_sorted)
    rightkeys = [0x13, 0x11, 0x1d, 0x7f, 0xe3, 0x94, 0x4a, 0x17, 0xf3, 0x7, 0xa7, 0x8b, 0x4d, 0x2b, 0x30, 0xc5]
    print('right key is ' + str(rightkeys[a]))
    right_key = rightkeys[a]
    wave_value = guess[right_key]
    #print(guess[19])

    x = np.linspace(0, 1, 256)
    plt.plot(x, guess)
    plt.show()

    for i in range(256):
        if wave_value == guess_sorted[i]:
            print("guess key is " + str(i) + ' th')
            break
