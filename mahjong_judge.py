import random
from collections import Counter

#牌を作成
def tiles_update(tiles_data):
    # 同じものを４つ作る
    for tiles_cnt in range(TILES_CNT):
        # 牌の種類ごとに作る
        for tiles_type_cnt in range(TILES_TYPE_CNT):
            # 牌の目を1から10で生成
            for tiles_number in range(1,10):
                tiles_keep = str(tiles_number) + tiles_type[tiles_type_cnt]
                # 牌のうち1つの5の目を赤ドラにする
                if tiles_cnt == 0 and tiles_number == 5: tiles_keep += "*"
                tiles_data.append(tiles_keep)
    for i in range(4):
        tiles_data+=["東","南","西","北","白","発","中"]
    
    return tiles_data

character_and_1or9_tiles = ["東", "南", "西", "北", "白", "発", "中","1m","9m","1p","9p","1s","9s"]
character_tiles=["白", "発", "中"]
kaze=["東", "南", "西", "北"]

tiles_data=[]    # 場に出る手牌
tiles_type = ["m", "p", "s"]    #牌の種類保持
TILES_CNT = 4  #1つの牌の個数
TILES_TYPE_CNT = 3 #マンズ、ピンズ、ソウズの3つの種類

# 牌のソート
def tile_sort(tehai,tiles_type):

    # アフター
    character_keep = []
    sort_tehai=[]
    # マンズ、ピンズ、ソウズの順にソート
    for tiles_type_cnt in range(TILES_TYPE_CNT):
        sort_tehai_type=[]
        for pai in tehai:
            # 数牌なら
            if pai[0].isdigit():
                    if pai[1] == tiles_type[tiles_type_cnt]: sort_tehai_type.append(pai)
            # 字牌なら
            # 最後の繰り返し処理で通るようにする(字牌数*3追加してしまうため)
            elif tiles_type_cnt == 2:
                character_keep.append(pai)

            # 同じ種類間で数字のソート
            sort_tehai_type.sort()
        sort_tehai+=sort_tehai_type
    
    # 字牌を末尾に追加
    for character in character_keep:
        sort_tehai.append(character)
    
    return sort_tehai

def shuntsu_cnt(tehai2,mentsu_total):
    twin=[]
    twin_judge=0
    suits = ['m', 'p', 's']
    shuntsu =0
    tehai_copy=tehai2.copy()
    for suit in suits:
        suit_tiles = sorted([tile for tile in tehai_copy if len(tile) >= 2 and tile[1] == suit])
        numbers = [int(tile[0]) for tile in tehai_copy if len(tile) == 2 and tile[1] == suit]
        i=0
        while i<len(numbers)-2:
            if numbers[i]+1 in numbers and numbers[i]+2 in numbers:
                t1, t2, t3 = f'{numbers[i]}{suit}', f'{numbers[i]+1}{suit}', f'{numbers[i]+2}{suit}'
                
                mentsu_total+=[[t1,t2,t3]]
                twin+=[f"{t1,t2,t3}"]
                
                tehai_copy.remove(t1)
                tehai_copy.remove(t2)
                tehai_copy.remove(t3)
                shuntsu += 1
                suit_tiles = sorted([tile for tile in tehai_copy if len(tile) >= 2 and tile[1] == suit])
                numbers = [int(tile[0]) for tile in tehai_copy if len(tile) == 2 and tile[1] == suit]
                i = 0
            else:
                i+=1
    twin_cnt=Counter(twin)
    counts=[]
    if twin_cnt:
        values,counts=zip(*twin_cnt.most_common())
    if counts:
        if counts[0]==2:
            twin_judge+=1
        if len(counts)<=2:
            if counts[1]==2:
                twin_judge+=1
    return shuntsu,tehai_copy,twin_judge,mentsu_total

yakuhai=[]
san=[]
sushi=[]
def kotsu_cnt(tehai,mentsu_total):
    kotsu=0
    j=0
    tehai2=tehai.copy()
    while j<len(tehai2)-2:
        if tehai2[j]==tehai2[j+1] and tehai2[j+1]==tehai2[j+2]:
            kotsu+=1
            mentsu_total+=[[tehai2[j],tehai2[j+1],tehai2[j+2]]]
            if tehai2[j] in character_tiles:
                yakuhai.append(tehai2[j])
                san.append(tehai2[j])
            if tehai2[j] in kaze:
                sushi.append(tehai2[j])
            if tehai2[j]==kaze[jikaze]:
                yakuhai.append(tehai2[j])
            if tehai2[j]==kaze[bakaze]:
                yakuhai.append(tehai2[j])
            tehai2.remove(tehai2[j+2])
            tehai2.remove(tehai2[j+1])
            tehai2.remove(tehai2[j])
            j=0
        else:
            j+=1
    return kotsu,tehai2,mentsu_total

def toitsu_cnt(tehai,mentsu_total):
    toi=0
    j=0
    sho=False
    sho2=False
    while j<len(tehai)-1:
        if tehai[j]==tehai[j+1]:
            mentsu_total+=[[tehai[j],tehai[j+1]]]
            if tehai[j] in character_tiles:
                sho=True
            elif tehai[j] in kaze:
                sho2=True
            toi+=1
            tehai.remove(tehai[j+1])
            tehai.remove(tehai[j])
            j=0
        else:
            j+=1
    return toi,tehai,sho,sho2,mentsu_total

def hora(hand):
    toitoi=False
    pinfu=False
    mentsu_total=[]
    shuntsu,tehai2,twin_judge,mentsu_total= shuntsu_cnt(hand.copy(),mentsu_total)
    kotsu,head,mentsu_total=kotsu_cnt(tehai2.copy(),mentsu_total)
    toi,tehai3,sho,sho2,mentsu_total=toitsu_cnt(head.copy(),mentsu_total)
    if shuntsu+kotsu==4 and toi==1:
        if kotsu==4:
            toitoi=True
        if shuntsu==4:
            pinfu=True
        return True,toitoi,pinfu,head,twin_judge,sho,sho2,mentsu_total
    else:
        return False,False,False,[],False,False,False


    
def is_tanyao(tehai):
    for tile in tehai:
        if tile in character_and_1or9_tiles:
            return False
    if len(yakuhai)!=0:
        return False
    return True

def is_honro(tehai):
    for tile in tehai:
        if len(tile)==2 and tile[0] in "2345678":
            return False
    return True

def is_chinitsu(tehai):
    suits = ['m', 'p', 's']
    for ji in character_tiles:
        for tile in tehai:
            if ji==tile:
                return False
    for tile in tehai:
        for ji in kaze:
            if ji==tile:
                return False
    for suit in suits:
        cnt=0
        for tile in tehai:
            if tile[1] == suit:
                cnt+=1
        if cnt==len(tehai):
            return True
    return False

def is_honitsu(tehai):
    cnt=0
    remove=[]
    i=0
    for tile in tehai:
        for ji in character_tiles:
            if ji==tile:
                cnt+=1
                remove.append(ji)
    for tile in tehai:
        for ji in kaze:
            if ji==tile:
                cnt+=1
                remove.append(ji)
        i+=1
    if cnt==0:
        return False
    for r in remove:
       tehai.remove(r)
    suits = ['m', 'p', 's']
    for suit in suits:
        cnt=0
        for tile in tehai:
            if tile[1]==suit:
                cnt+=1
        if len(tehai)==cnt:
            return True
    return False

def is_ittsu(tehai):
    suits = ['m', 'p', 's']
    for suit in suits:
        cnt=0
        for i in range(1,10):
            if f"{i}{suit}" in tehai:
                cnt+=1
        if cnt==9:
            return True
    return False

def is_sanshoku(tehai):
    suits=['m','p','s']
    for i in range(1,8):
            if f"{i}{suits[0]}" in tehai and f"{i+1}{suits[0]}" in tehai and f"{i+2}{suits[0]}" in tehai:
                if f"{i}{suits[1]}" in tehai and f"{i+1}{suits[1]}" in tehai and f"{i+2}{suits[1]}" in tehai:
                    if f"{i}{suits[2]}" in tehai and f"{i+1}{suits[2]}" in tehai and f"{i+2}{suits[2]}" in tehai:
                        return True
    return False

def is_honro(tehai):
    for tile in tehai:
        if len(tile)==2 and tile[0] not in "19":
            return False
    return True

def is_ryuiso(tehai):
    green=["2s", "3s", "4s", "6s", "8s", "発"]
    for tile in tehai:
        if tile not in green:
            return False
    return True

def is_junchan(mentsu):
    for tiles in mentsu:
        cnt=0
        for tile in tiles:
            if len(tile)==2 and tile[0] in "19":
                cnt+=1
        if cnt==0:
            return False
    return True

def is_chanta(mentsu):
    for tiles in mentsu:
        cnt=0
        for tile in tiles:
            if len(tile)==2 and tile[0] in "19":
                cnt+=1
            elif (tile in kaze) or (tile in character_tiles):
                cnt+=1
        if cnt==0:
            return False
    return True
def rare_yaku_judge(tehai):
    cnt=0
    for tile in character_and_1or9_tiles:
        if tile in tehai:
            cnt+=1
    toi,tiles_data,sho,sho2=toitsu_cnt(tehai.copy())
    if toi==7:
        print("七対子")
        return True
    if cnt==13 and toi ==1:     
        print("国士無双")
        return True
   
def yaku_judge(tehai):
        if tehai==["1m","1m","1m","2m","3m","4m","5m","6m","7m","8m","9m","9m","9m"] or tehai==["1p","1p","1p","2p","3p","4p","5p","6p","7p","8p","9p","9p","9p"] or tehai==["1s","1s","1s","2s","3s","4s","5s","6s","7s","8s","9s","9s","9s"]:
            print("九蓮宝燈")
            return
        if is_ryuiso(tehai):
            print("緑一色")
            return
        if (len(san)+len(sushi)==4) and (sho or sho2):
            print("字一色")
            if len(sushi)==4:
                print("大四喜")
                return
            if len(san)==3:
                print("大三元")
                return
            if kan==4:
                print("四槓子")
                return
            if ankou==4:
                print("四暗刻",end="")
                if tanki:
                    print("単騎")
                else:
                    print()
                return
            if tenho:
                print("天和")
                return
            elif chiho:
                print("地和")
                return
            else:
                return
        if len(sushi)==4:
            print("大四喜")
            if kan==4:
                print("四槓子")
                return
            elif ankou==4:
                print("四暗刻",end="")
                if tanki:
                    print("単騎")
                else:
                    print()
                return
            if tenho:
                print("天和")
                return
            elif chiho:
                print("地和")
                return
            else:
                return
        if len(san)==3:
            print("大三元")
            if kan==4:
                print("四槓子")
                return
            else:
             if ankou==4:
                print("四暗刻",end="")
                if tanki:
                    print("単騎")
                else:
                    print()
                return
            if tenho:
                print("天和")
                return
            elif chiho:
                print("地和")
                return
            else:
                return
        if kan==4:
            print("四槓子")
            if ankou==4:
                print("四暗刻",end="")
                if tanki:
                    print("単騎")
                else:
                    print()
                return
            if tenho:
                print("天和")
                return
            elif chiho:
                print("地和")
                return
            else:
                return
        if ankou==4:
            print("四暗刻",end="")
            if tanki:
                print("単騎")
            else:
                print()
            return
        elif reach:
            if tenho:
                print("天和")
                return
            elif chiho:
                print("地和")
                return
            if double:
                print("ダブルリーチ")
            else:
                print("リーチ")
        if dora!=0:
            for _ in range(dora):
                print("ドラ")
        if tsumo==1 and state==1:
            print("門前清自摸和")
        if pinhu and head[0]!=kaze[jikaze] and head[0]!=kaze[bakaze] and head[0] not in character_tiles:
            print("平和")
        if sho and len(san)==2:
            print("小三元")
        if sho2 and len(sushi)==3:
            print("小四喜")
        if twin_judge==2:
            print("二盃口")
        elif twin_judge==1:
            print("一盃口")
        if kan==3:
            print("三槓子")
        if ankou==3:
            print("三暗刻")
        if is_honro(tehai):
            print("混老頭")
        if is_junchan(mentsu_total):
            print("純全帯么九")
        elif is_chanta(mentsu_total):
            print("混全帯么九")
        if toitoi:
            print("対々和")
        if len(yakuhai)!=0:
            print("役牌:"+",".join(yakuhai))
        if is_chinitsu(tehai):
            print("清一色")
        if is_honitsu(tehai):
            print("混一色")
        if is_honro(tehai):
            print("混老頭")
        if is_ittsu(tehai):
            print("一気通貫")
        if is_sanshoku(tehai):
            print("三色同順")
        if is_tanyao(tehai):
            print("タンヤオ")
        if haitei:
            print("海底")
        elif houtei:
            print("河底")
        if rinshan:
            print("嶺上開花")
        if chankan:
            print("槍槓")

jikaze=int(input("字風牌 東:0/南:1/西:2/北:3"))
bakaze=int(input("場風牌 東:0/南:1/西:2/北:3"))
state=int(input("門前:1/副露:0"))
if state:
    reach=int(input("リーチ有:1/無:0"))
    if reach:
        double=int(input("ダブルリーチ:1/その他:0"))
    else:
        double=0
else:
    reach=0
dora=int(input("ドラの枚数"))
tsumo=int(input("ツモ:1/ロン:0"))
if tsumo:
    tenho=int(input("天和"))
    chiho=int(input("地和"))
else:
    tenho=0
    chiho=0
ryan=int(input("両面:1/その他:0"))
tanki=int(input("単騎:1/その他:0"))
ankou=int(input("暗刻の数を入力"))
kan=int(input("槓子の数を入力"))
haitei=int(input("海底:1/その他:0"))
houtei=int(input("河底:1/その他:0"))
chankan=int(input("槍槓:1/その他:0"))
rinshan=int(input("嶺上開花:1/その他:0"))
first=int(input("一発:1/その他:0"))

hand=["東","東","東","1p","2p","3p","7s","8s","9s","7m","8m","9m","9m","9m"]
hand=tile_sort(hand,tiles_type)
hora_result=False
hora_result,toitoi,pinhu,head,twin_judge,sho,sho2,mentsu_total=hora(hand.copy())
if hora_result or rare_yaku_judge(hand.copy()):
                    yaku_judge(hand.copy())
                    print("和了!")