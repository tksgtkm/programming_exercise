"""
FかBの文字を含む配列があり、もしFとBの両方の文字を含む配列がある場合は
どちらかの文字のみを含む配列にしたいとする。
F: forward 前向き
B: backward 後ろ向き

例
'F', 'F', 'B', 'B', 'B', 'F', 'B', 'B', 'B', 'F', 'F', 'B', 'F'

上記のような配列の場合、FをBに変換する場合は[0:2], [5], [9:11], [12]
の4回変換する必要がある。
しかし同様の方法でBを変換する場合は[2:5], [6:9], [11]の3回で済む。
このようにFかBの文字を含む配列が与えられたときどちらかの文字のみを
含む配列に変換するのを最小回数で行うにはどうすればいいか?

並んでいる文字の集合に対する文字の種類のリストがあるとする。
文字の種類が続いている区間のリストを計算する。
区間は開始位置、終了位置、a<bとして[a,b]で表せる。
aとbを含めたaからbまでのすべての位置が区間に含まれる。
各区間にはFかBかのラベルがあるので、区間は3要素、開始位置、終了位置、
FかBかのラベルからなる。
よって、[0,1]: F [2,4]: B [5,5]: F のように区間が求まる。
"""

caps = ['F', 'F', 'B', 'B', 'B', 'F', 'B', 'B', 'B', 'F', 'F', 'B', 'F' ]
cap2 = ['F', 'F', 'B', 'B', 'B', 'F', 'B', 'B', 'B', 'F', 'F', 'F', 'F' ]

def pleaseConform(caps):
    start = 0
    # forwardとbackwardは前向き区間と後ろ向き区間の個数を数える
    forward = 0
    backward = 0
    # 区間タプルのリスト
    intervals = []

    # FかBの区間を計算する
    for i in range(1, len(caps)):
        # Trueだと一つの区間が終わる
        if caps[start] != caps[i]:
            intervals.append((start, i - 1, caps[start]))

            if caps[start] == 'F':
                forward += 1
            else:
                backward += 1
            start = i

    # [(0, 1, 'F'), (2, 4, 'B'), (5, 5, 'F'), (6, 8, 'B'), (9, 10, 'F'), (11, 11, 'B')]
    # print(intervals)

    # 最後の区間をintervalsに追加する
    intervals.append((start, len(caps) - 1, caps[start]))
    if caps[start] == 'F':
        forward += 1
    else:
        backward += 1
    # [(0, 1, 'F'), (2, 4, 'B'), (5, 5, 'F'), (6, 8, 'B'), (9, 10, 'F'), (11, 11, 'B'), (12, 12, 'F')]
    # print(intervals)
    
    print(forward) # 4
    print(backward) # 3
    if forward < backward:
        flip = 'F'
    else:
        flip = 'B'
    for t in intervals:
        if t[2] == flip:
            print('People in positions', t[0], 'through', t[1], 'flip your caps!')


pleaseConform(caps)