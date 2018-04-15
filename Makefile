# Makefile for building all experiments...
CC=g++
CFLAGS=-std=c++11
LDFLAGS=-lpthread
SOURCES=pi_seq.cc pi_naive.cc pi_mutex.cc pi_atomic.cc pi_fs.cc
BINARIES=$(patsubst %.cc,%,$(SOURCES))

all: seq naive mutex atomic fs

seq: pi_seq.cc
	$(CC) $(CFLAGS) -o pi_seq pi_seq.cc
naive: pi_naive.cc
	$(CC) $(CFLAGS) -o pi_naive pi_naive.cc $(LDFLAGS)
mutex: pi_mutex.cc
	$(CC) $(CFLAGS) -o pi_mutex pi_mutex.cc $(LDFLAGS)
atomic: pi_atomic.cc
	$(CC) $(CFLAGS) -o pi_atomic pi_atomic.cc $(LDFLAGS)
fs: pi_fs.cc
	$(CC) $(CFLAGS) -o pi_fs pi_fs.cc $(LDFLAGS)

clean:
	rm -f $(BINARIES)
