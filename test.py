import datetime

reqid = datetime.datetime.now().strftime('%d%m%Y%H%M%S%f')

print('reqid '+str(reqid))

import sched, time
s = sched.scheduler(time.time, time.sleep)
def print_time(a='default'):
    print("From print_time", time.time(), a)

def print_some_times():
    print(time.time())
    #s.enter(10, 1, print_time)
    
    #s.enter(5, 2, print_time, argument=('positional',))
    
    # despite having higher priority, 'keyword' runs after 'positional' as enter() is relative
    #s.enter(5, 1, print_time, kwargs={'a': 'keyword'})
    s.enterabs(1_650_000_000, 10, print_time, argument=("first enterabs",))
    #s.enterabs(1_650_000_000, 5, print_time, argument=("second enterabs",))
    
    s.run()
    print(time.time())

print_some_times()