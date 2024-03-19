from queue import Queue
import time

q = Queue(maxsize=10000000000000000000000000000000000)
st = time.time()
q.put(1465264263624562642523524634634562345234)
q.put(2)
q.put(377654)

print(q.get())
print(q.get())
print(q.get())
print(time.time() - st)

