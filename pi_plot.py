import re
import subprocess
import numpy as np
from matplotlib import pyplot as plt

print("Running {} in serial...".format(prog), flush=True, end="")
result = subprocess.run([prog, str(n)], stdout=subprocess.PIPE).stdout.decode("utf-8")
print("\x1B[32mdone\x1B[0m")
serial_runtime = float(re.search(r"elapsed process CPU time = (.*) nanoseconds", result).group(1))

def plot_nthreads_time(prog, title, show=False, save=False):
    # plot the naive pthread implemenation of computation of pi with 1, 2, 4, 8 threads
    print("Plotting runtimes of {} with 1, 2, 4, 8 threads...".format(prog))
    runtimes = []
    speedups = []
    pi_vals = []
    n_threads = [1, 2, 4, 8]
    for n in n_threads:
        print("Running {} with {} thread(s)...".format(prog, n), flush=True, end="")
        result = subprocess.run([prog, str(n)], stdout=subprocess.PIPE).stdout.decode("utf-8")
        print("\x1B[32mdone\x1B[0m")
        # first line of the result should have the runtime
        parallel_runtime = float(re.search(r"elapsed process CPU time = (.*) nanoseconds", result).group(1))
        runtimes.append(parallel_runtime)
        speedups.append(serial_runtime / parallel_runtime)
        # second line should have the value of pi computed
        pi_vals.append(float(result.split("\n")[1]))

    plt.figure()
    plt.title(title)
    plt.xlabel("number of threads")
    plt.ylabel("speedup")
    plt.plot(n_threads, speedups, marker="o")
    if show:
        print("Displaying the plot...")
        plt.show()
    if save:
        print("Saving plot figure...", flush=True, end="")
        plt.savefig("{}.png".format(title))
        print("\x1B[32mdone\x1B[0m")
        plt.close()
    
    plt.figure()
    plt.title(title)
    plt.xlabel("number of threads")
    plt.ylabel("runtime (nanoseconds)")
    plt.plot(n_threads, times, marker="o")
    if show:
        print("Displaying the plot...")
        plt.show()
    if save:
        print("Saving plot figure...", flush=True, end="")
        plt.savefig("{}.png".format(title))
        print("\x1B[32mdone\x1B[0m")
        plt.close()

    tbl = plt.table(cellText=np.array([times, pi_vals]).T,
                    rowLabels=n_threads, 
                    colLabels=["runtime (nanoseconds)", "pi"],
                    cellLoc="center",
                    loc="center")
    plt.title(title)
    plt.axis("off")
    if show:
        print("Displaying the table...")
        plt.show()
    if save:
        print("Saving table figure...", flush=True, end="")
        plt.savefig("{}_table.png".format(title))
        print("\x1B[32mdone\x1B[0m")
        plt.close()

plot_nthreads_time("./pi_naive", "Naive Parallelization with Pthread", save=True)
plot_nthreads_time("./pi_mutex", "Pthread Parallelization with Mutex", save=True)
plot_nthreads_time("./pi_atomic", "Pthread Parallelization with Atomic Instructions", save=True)
plot_nthreads_time("./pi_fs", "Pthread Parallelization with False-sharing", save=True)
plot_nthreads_time("./pi_local", "Pthread Parallelization with Local Sums", save=True)
