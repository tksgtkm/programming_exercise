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
    
    if forward < backward:
        flip = 'F'
    else:
        flip = 'B'
    for t in intervals:
        if t[2] == flip:
            if t[0] == t[1]:
                print('Person at position', t[0], 'flip your cap!')
            else:
                print('People in positions', t[0], 'through', t[1], 'flip your caps!')


pleaseConform(caps)