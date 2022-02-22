import redis
import time

r = redis.Redis(
    host='192.168.6.37',
    port=6379,
    password='mappers',
    db=0)

#result = r.geosearch('car-order', longitude=126.7981806, latitude=37.6175133, radius=10000,  unit="m", sort="ASC")
start_time = time.process_time()
counts = []
for i in range(0,100):
    for j in range(0, 10):
        car_name = "car_%i_%i"% (i*10, j*10)
        result = r.geosearch('car-order', member=car_name , radius=5000,  unit='m', sort="ASC", withdist=True)
        #print(len(result))
        counts.append(len(result))
end_time = time.process_time()
print(f"time elapsed : {int(round((end_time - start_time) * 1000))}ms")
print(f"avg=%i, max=%i, min=%i"%(sum(counts)/len(counts), max(counts), min(counts)))