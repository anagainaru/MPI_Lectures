#!/usr/bin/env python 
from mpi4py import MPI
import numpy as np
import sys

# Example 1: Compute pi using numerical integration
#     - Input parameter: number of slices 
#     - Number of slices must be a multiple of the total processes
#     - By default number of slices = number of processes

verbose = False

if __name__ == "__main__":

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    # number of slices
    n = size
    if len(sys.argv) > 1:
        n = int(sys.argv[1])

    # 
    assert((n % size) == 0),\
            "Number of slices must be multiple of total processes"

    w = 1.0 / n
    mypi = 0.0

    for i in range(rank + 1, n + 1, size):
        mypi += w * np.sqrt(1 - np.power(i / n, 2))

    if verbose:
        print("rank %d: my local pi %5.3f" %(rank, mypi))

    pi = comm.reduce(mypi, op=MPI.SUM, root=0)

    if rank==0:
        print("PI: %f" %(4 * pi))
