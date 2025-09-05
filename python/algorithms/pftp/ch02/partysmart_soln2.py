"""
時間の粒度に依存しないでパーティに行く時間を計算する。
有名人の滞在時間を順に選び、他の有名人で滞在時間中に
その選んだ有名人での開始時刻を含むものが何人いるかを数える。
パーティに行く時間は他の有名人が一番多くいる滞在時間の有名人の
開始時刻にすればいい。
"""

sched = [(6, 8), (6, 12), (6, 7), (7, 8), (7, 10), (8, 9), (8, 10), (9, 12),
            (9, 10), (10, 11), (10, 12), (11, 12)]
sched2 = [(6.0, 8.0), (6.5, 12.0), (6.5, 7.0), (7.0, 8.0), (7.5, 10.0), (8.0, 9.0),
          (8.0, 10.0), (9.0, 12.0), (9.5, 10.0), (10.0, 11.0), (10.0, 12.0), (11.0, 12.0)]

def bestTimeToParty(schedule):
    # 各有名人が参加する開始時刻のリストを作る
    start_times_list = []
    for c in schedule:
        start_times_list.append(c[0])
    
    # 各有名人の開始時刻が他の有名人の滞在時刻の範囲に含まれるかカウントする
    # このとき、何人の滞在時刻の範囲に含まれるかをカウントするようにする
    count_list = []
    for i in start_times_list:
        count = 0
        for c in schedule:
            if c[0] <= i < c[1]:
                count += 1
        count_list.append(count)
    
    # 最も多くの滞在時刻の範囲に含まれていた数を抽出
    maxcount = max(count_list)
    inddex_number = count_list.index(maxcount)

    time = schedule[inddex_number][0]

    print ('Best time to attend the party is at', time,\
           'o\'clock', ':', maxcount, 'celebrities will be attending!')

bestTimeToParty(sched2)
