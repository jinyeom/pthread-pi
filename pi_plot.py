import re
import subprocess
import numpy as np
from matplotlib import pyplot as plt

def plot_nthreads_time(prog, title, plot_show=False, plot_save=False, table_show=False, table_save=False):
    # plot the naive pthread implemenation of computation of pi with 1, 2, 4, 8 threads
    print("Plotting runtimes of {} with 1, 2, 4, 8 threads...".format(prog))
    times = []
    pi_vals = []
    n_threads = [1, 2, 4, 8]
    for n in n_threads:
        print("Running {} with {} thread(s)...".format(prog, n), flush=True, end="")
        result = subprocess.run([prog, str(n)], stdout=subprocess.PIPE).stdout.decode("utf-8")
        print("\x1B[32mdone\x1B[0m")
        # first line of the result should have the runtime
        t = re.search(r"elapsed process CPU time = (.*) nanoseconds", result)
        times.append(float(t.group(1)))
        # second line should have the value of pi computed
        pi_vals.append(float(result.split("\n")[1]))

    plt.figure()
    plt.title(title)
    plt.xlabel("number of threads")
    plt.ylabel("nanoseconds")
    plt.plot(n_threads, times, marker="o")
    if plot_show:
        print("Displaying the plot...")
        plt.show()
    if plot_save:
        print("Saving figure...", flush=True, end="")
        plt.savefig("{}.png".format(title))
        print("\x1B[32mdone\x1B[0m")
        plt.close()

    tbl = plt.table(cellText=np.array([times, pi_vals]).T,
                    rowLabels=n_threads, 
                    colLabels=["runtime (nanoseconds)", "pi"],
                    cellLoc="center")
    plt.title(title)
    plt.axis("off")
    plt.show()

plot_nthreads_time("./pi_naive", "Naive Parallelization with Pthread", plot_save=True)
plot_nthreads_time("./pi_mutex", "Pthread Parallelization with Mutex", plot_save=True)
plot_nthreads_time("./pi_atomic", "Pthread Parallelization with Atomic Instructions", plot_save=True)
