#include <pthread.h>
#include <stdlib.h>
#include <math.h>
#include <stdio.h>
#include <stdint.h> /* for uint64  */
#include <time.h> /* for clock_gettime */
// #include <atomic> /*used in other parts of the assignment */

#define MAX_THREADS 512

int num_threads;
pthread_t handles[MAX_THREADS];
int short_names[MAX_THREADS];

void *compute_pi(void *);

double f(double x) {
	return (6.0 / sqrt(1 - x * x));
}

double pi = 0.0;
int numPoints = 1000000000;
double step = 0.5 / numPoints;

int main(int argc, char *argv[]) {
	if (argc != 2) {
		printf("usage: pi_naive_pthread num_threads\n");
		return -1;
	}

	pthread_attr_t attr;
	pthread_attr_init(&attr);

	// number of threads from the command line argument
	// test with 1, 2, 4, and 8 threads.
	num_threads = atoi(argv[1]);

	uint64_t execTime; /*time in nanoseconds */
	struct timespec tick, tock;

	clock_gettime(CLOCK_MONOTONIC_RAW, &tick);
	// ---------------- experiment below ----------------

	for (int i = 0; i < num_threads; ++i) {
		// create threads 0, 1, 2, ..., numThreads (round robin)
		short_names[i] = i;
		pthread_create(&handles[i], &attr, compute_pi, &short_names[i]);
	}

	// join with threads when they're done
	for (int i = 0; i < num_threads; ++i) {
		pthread_join(handles[i], NULL);
	}

	// --------------------------------------------------
	clock_gettime(CLOCK_MONOTONIC_RAW, &tock);
	execTime = 1000000000 * (tock.tv_sec - tick.tv_sec) + tock.tv_nsec - tick.tv_nsec;

	printf("elapsed process CPU time = %llu nanoseconds\n", (long long unsigned int) execTime);
	printf("%.20f\n", pi);
	return 0;
}

// function to be called by each thread
void *compute_pi(void *thread_id_ptr) {
	int tid = *(int *)thread_id_ptr;
	// for this experiment, each thread will add directly to the global sum.
	for (int i = tid; i < numPoints; i += num_threads) {
		double x = step * ((double)i);
		pi = pi + step * f(x);
	}
}
