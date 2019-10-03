#!/usr/bin/env python 
from mpi4py import MPI
import numpy as np

# Example for measuring the Bcast time

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

comm.barrier();
local_wt = MPI.Wtime();

data = np.array([rank * i for i in range(10)])
comm.Bcast(data, root=0); 
local_wt = MPI.Wtime() - local_wt;

wt = comm.reduce(local_wt, op=MPI.MAX, root=0);

if rank == 0:
    print("Bcast time %f" %(wt))
