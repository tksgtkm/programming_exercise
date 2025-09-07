"""
あるカードマジックを行なう。
助手が52枚一組のトランプを持って、観客の席を回る。
そのあいだ、マジシャンは部屋の外で待つ。
観客のうち、5人がトランプカードの中から1枚ずつ選ぶ。
助手は5枚のカードを集め、観客全員に4枚のカードを1枚ずつ見せる。
数秒後、マジシャンにその4枚のカードを見せる。
その後、助手は最後の1枚のカードを観客に見せて、マジシャンには
最後の1枚を当ててもらう。

当て方：
hurt_10 dia_9  hurt_3 spade_Q dia_J
を選んだとする。

助手は同じスートのカードを2枚選ぶ。
5枚のカードがあり、スートは4種類だから同じスートのカードは
少なくとも2枚含まれる。
今回はhurt_3とhurt_10を選ぶ。

この2枚のカードをA ~ Kの順で円周上で時計回りになるように考える

この円周上の2つの値は時計回りで必ず1から6だけ離れている。
たとえばhurt_10からhurt_3までは6離れている。

この2枚のカードの片方をまず示す。
残りを秘密のカードにする。
今回だとhurt_10を示して、hurt_3を秘密のカードとする。
・秘密のカードは最初に示したカードを同じスート
・秘密のカードは最初に示したカードから時計回りで1から6の間の値

1〜6の値はどうやって伝えるか。
(小、中、大) = 1
(小、大、中) = 2
(中、小、大) = 3
(中、大、小) = 4
(大、小、中) = 5
(大、中、小) = 6

今回は6と伝えたいので。
残りの3枚を[spade_Q dia_J dia_9]の順序にする。

よって助手がマジシャンに見せるカードは[hurt_10 spade_Q dia_J dia_9]の順序になり、
そこからマジシャンはhurt_6を当てる。
"""

# カードの小さいのから大きいのまで全順序を示す
deck = ['A_C', 'A_D', 'A_H', 'A_S', '2_C', '2_D', '2_H', '2_S', '3_C', '3_D', '3_H', '3_S',
        '4_C', '4_D', '4_H', '4_S', '5_C', '5_D', '5_H', '5_S', '6_C', '6_D', '6_H', '6_S',
        '7_C', '7_D', '7_H', '7_S', '8_C', '8_D', '8_H', '8_S', '9_C', '9_D', '9_H', '9_S',
        '10_C', '10_D', '10_H', '10_S', 'J_C', 'J_D', 'J_H', 'J_S',
        'Q_C', 'Q_D', 'Q_H', 'Q_S', 'K_C', 'K_D', 'K_H', 'K_S']

def AssistantOrdersCards():

    print('Cards are character strings as shown below')
    print('Ordering is:', deck)

    # 変数を初期化
    cards, cind, cardsuits, cnumbers = [], [], [], []
    numsuits = [0, 0, 0, 0]

    # 5枚のカードに対応するキーボード入力を求めるforループ
    for i in range(5):
        # カードが何番目であるかを表示する
        # end = ' 'は空白を表示させる
        print('Please give card', i+1, end = ' ')
        # 入力された文字を受取り、変数cardに書き込み
        card = input('in above format:')
        cards.append(card)
        # カードの文字列を取って、リストdeckで対応するカードのインデックスを求める
        # インデックスは2枚のカードの比較で使う
        n = deck.index(card)
        # 各種データ構造の設定
        # 5枚のカードのインデックスをcindに格納する
        cind.append(n)
        # 5枚のスートをcardsuitsに格納する
        # 各カードのインデックスからスートがモジュロ4で求まる。
        # クラブ(スート0)のカードは、4の倍数、ダイヤ(スート1)のカードは
        # 4の倍数+1のインデックスとなる。
        cardsuits.append(n % 4)
        # カードの値、すなわちA(1)からK(13)を得るには
        # インデックス4で整数除算(//)する。
        cnumbers.append(n // 4)
        numsuits[n % 4] += 4
        if numsuits[n % 4] > 1:
            pairsuit = n % 4

    cardh = []
    for i in range(5):
        if cardsuits[i] == pairsuit:
            cardh.append(i)

    hidden, other, encode = outputFirstCard(cnumbers, cardh, cards)

    reminders = []
    for i in range(5):
        if i != hidden and i != other:
            reminders.append(cind[i])
    
    sortList(reminders)

    outputNext3Cards(encode, reminders)

    return

def outputFirstCard(numbers, oneTwo, cards):
    encode = (numbers[oneTwo[0]] - numbers[oneTwo[1]]) % 13
    if encode > 0 and encode <= 6:
        hidden = oneTwo[0]
        other = oneTwo[1]
    else:
        hidden = oneTwo[1]
        other = oneTwo[0]
        encode = (numbers[oneTwo[1]] - numbers[oneTwo[0]]) % 13

    print('First card is:', cards[other])
    return hidden, other, encode

def outputNext3Cards(code, ind):
    if code == 1:
        second, third, fourth = ind[0], ind[1], ind[2]
    elif code == 2:
        second, third, fourth = ind[0], ind[2], ind[1]
    elif code == 3:
        second, third, fourth = ind[1], ind[0], ind[2]
    elif code == 4:
        second, third, fourth = ind[1], ind[2], ind[0]
    elif code == 5:
        second, third, fourth = ind[2], ind[0], ind[0]
    else:
        second, third, fourth = ind[2], ind[1], ind[2]

    print('Second card is:', deck[second])
    print('Third card is:', deck[third])
    print('Fourth card is:', deck[fourth])

def sortList(tlist):
    for index in range(0, len(tlist) - 1):
        ismall = index
        for i in range(index, len(tlist)):
            if tlist[ismall] > tlist[i]:
                ismall = i
        tlist[index], tlist[ismall] = tlist[ismall], tlist[index]
    return