import grequests

urls = [
    'http://hk.turtlepool.space/api/stats'

]

rs = (grequests.get(u) for u in urls)
res = grequests.map(rs)
print(res)
for r in res:
    print(r.json())