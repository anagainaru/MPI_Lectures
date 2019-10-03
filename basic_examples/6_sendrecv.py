#!/usr/bin/env python 
from mpi4py import MPI

# Example for using sendrecv

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

to = (rank + 1) % size
fr = (rank - 1) % size

sdata = rank
rdata = comm.sendrecv(sdata, dest=to, source=fr)

print("rank %d got data from %d" %(rank, rdata))
