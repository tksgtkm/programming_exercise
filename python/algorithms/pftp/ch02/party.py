"""
あなたは一般人としてあるパーティに出席しますが1時間しか出席できないものとします。
そのパーティには有名人も多く参加しますが、参加する時間帯はバラバラであるとします。
schedはパーティに参加する有名人が来場する時間と退場する時間を表します。
有名人の来場時間はschedに記載の時間のとおりですが、退場の時間はその時間までに
退場するものとします。なので、退場の時間にパーティに出席してもその有名人には会えない
ものとします。
どの時間帯に行けば一番多くの有名人に合うことができるでしょうか？
"""
# 有名人が滞在する各時刻
sched = [(6, 8), (6, 12), (6, 7), (7, 8), (7, 10), (8, 9), (8, 10), (9, 12),
            (9, 10), (10, 11), (10, 12), (11, 12)]

# 各時刻の有名人の人数を数えて、最大数を取り出す
def bestTimeToParty(schedule):
    # 有名人が最初にパーティに来る時刻と最後の有名人が帰る時刻を決める
    start = schedule[0][0]
    end = schedule[0][1]
    for c in schedule:
        start = min(c[0], start)
        end = max(c[1], end)
    
    # startとendの間の各時刻に有名人が何人いるかという情報を取得
    count = celebrityDensity(schedule, start, end)

    # 有名人が最も多い時間帯を決める
    maxcount = 0
    for i in range(start, end + 1):
        if count[i] > maxcount:
            maxcount = count[i]
            time = i

    # 27 ~ 31は下記でも代用できる。
    # maxcount = max(count[start:end + 1])
    # time = count.index(maxcount)

    print('Best time to attend the party is at', time,\
          'o\'clock', ':', maxcount, 'celebrities will be attending!')

def celebrityDensity(sched, start, end):

    count = [0] * (end + 1)
    # 時間のイテレーション
    for i in range(start, end + 1):
        count[i] = 0
        for c in sched:
            if c[0] <= i and c[1] > i:
                count[i] += 1

    return count

bestTimeToParty(sched)