"""
あなた自身が有名人だとします。
パーティに行くときの時間を自由に選ぶわけには行きません。
プロシージャに引数を追加して、与えられたystartとyendの時間内で
会える有名人の最大人数を返すようにしてください。
"""

sched = [(6, 8), (6, 12), (6, 7), (7, 8), (7, 10), (8, 9), (8, 10), (9, 12),
            (9, 10), (10, 11), (10, 12), (11, 12)]
sched2 = [(6.0, 8.0), (6.5, 12.0), (6.5, 7.0), (7.0, 8.0), (7.5, 10.0), (8.0, 9.0),
          (8.0, 10.0), (9.0, 12.0), (9.5, 10.0), (10.0, 11.0), (10.0, 12.0), (11.0, 12.0)]

def bestTimeToPartySmart(schedule, ystart, yend):
    times = []
    for c in schedule:
        times.append((c[0], 'start'))
        times.append((c[1], 'end'))

    sortlist(times)

    maxcount, time = chooseTimeConstrained(times, ystart, yend)

    print ('Best time to attend the party is at', time,\
           'o\'clock', ':', maxcount, 'celebrities will be attending!')


def sortlist(tlist):
    for index in range(len(tlist) - 1):
        ismall = index
        for i in range(index, len(tlist)):
            if tlist[ismall][0] > tlist[i][0]:
                ismall = i
        tlist[index], tlist[ismall] = tlist[ismall], tlist[index]
    return

def chooseTimeConstrained(times, ystart, yend):
    rcount = 0
    maxcount = 0
    time = 0

    for t in times:
        if t[1] == 'start':
            rcount = rcount + 1
        elif t[1] == 'end':
            rcount = rcount - 1
        if rcount > maxcount and t[0] >= ystart and t[0] < yend:
            maxcount = rcount
            time = t[0]

    return maxcount, time

bestTimeToPartySmart(sched2, 6.0, 7.0)