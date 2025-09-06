"""
各有名人に対してその人がどれだけ好ましいかという重みが付属するものとする。
これには、スケジュールを(6.0, 8.0, 3)のような3要素のタプルとして表す
開始時刻は6.0終了時刻は8.0重みが3となる。
有名人の重みを足し合わせた最大重みの時刻を求めよ。
"""

sched2 = [(6.0, 8.0, 2), (6.5, 12.0 , 1), (6.5, 7.0, 2), (7.0, 8.0, 2), 
          (7.5, 10.0, 3), (8.0, 9.0, 2), (8.0, 10.0, 1), (9.0, 12.0, 2), 
          (9.5, 10.0, 4), (10.0, 11.0, 2), (10.0, 12.0, 3), (11.0, 12.0, 7)]

# sched2 = [(6.5, 7.0, 2), (6.5, 12.0 , 1), (6.0, 8.0, 2) ]

def bestTimeToParty(schedule):
    start_times_list = []
    for c in schedule:
        start_times_list.append(c[0])
    
    count_list = []
    for i in start_times_list:
        count = 0
        for c in schedule:
            if c[0] <= i < c[1]:
                count += c[2]
        count_list.append(count)

    maxcount = max(count_list)
    inddex_number = count_list.index(maxcount)

    time = schedule[inddex_number][0]

    print(time, maxcount)

bestTimeToParty(sched2)