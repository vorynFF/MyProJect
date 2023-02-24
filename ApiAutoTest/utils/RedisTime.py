import redis
import time
start_time = time.time()
print(start_time)
redis_conn = redis.Redis(host='3.131.210.71', port=6378)
res = redis_conn.hgetall("superior_q")
print(res)
end_time = time.time()
print(str(end_time - start_time))


