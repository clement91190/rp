import subprocess
import sys
import time
import rp.optim_server.optim_server.endpoints.worker_endpoints as end


def stop_pool(pool):
    for p in pool:
        p.terminate()
    time.sleep(1)


def start_pool(num_process, cmd):
    pool = []
    for i in range(num_process):
        pool.append(subprocess.Popen(cmd))


def main():
    cmd = ["python", "-m", "rp.scripts.test_with_server"]

    try:
        num_process = sys.argv
        print num_process[1]
        num_process = int(num_process[-1] )
    except:
        num_process = 1
    pool = []
    end.clean_data()
    start_pool(num_process, cmd)
    t = time.time()

    while(True):
        if time.time() - t > 25:
            print "stoping  !"
            #stop_pool(pool)
            end.clean_data()
            start_pool(num_process, cmd)
            t = time.time()

if __name__ == "__main__":
    main()
