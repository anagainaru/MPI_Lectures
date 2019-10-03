#!/usr/bin/env python 
from mpi4py import MPI
import numpy as np
import sys

# Example 3: Compute multiplication of a matrix with a vector
#     - Each process gets a full row
#     - Matrix size is a multiple of number of processes
#     - Matrix has same number of rows and columns

verbose = False

if __name__ == "__main__":

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    # number of rows
    number_rows = size
    if len(sys.argv) > 1:
        number_rows = int(sys.argv[1])
     
    assert((number_rows % size) == 0),\
            "Number of rows must be multiple of total processes"
    
    # create vector data on root and broadcast it
    # create matrix on root and scatter rows to each process

    my_row_count = number_rows // size 
    local_A = np.zeros(shape=(my_row_count, number_rows), dtype='i')
    if rank==0:
        A = np.matrix([[i + 2 * j for i in range(number_rows)] for j in range(number_rows)], dtype='i')
        vect = np.array([i % 2 for i in range(number_rows)], dtype='i')
        print("Multiply matrix %s with vector %s" %(A, vect))
    else:
        A = None
        vect = np.empty(number_rows, dtype='i') 
    
    comm.Scatter([A, MPI.INT], [local_A, MPI.INT], root=0)
    comm.Bcast([vect, MPI.INT], root=0)
    
    if verbose:
        print("rank %d: matrix %s" %(rank, local_A))

    # local computation
    local_res = np.zeros(my_row_count, dtype='i')
    for i in range(my_row_count):
        local_res[i] = np.dot(local_A[i], vect)

    if verbose:
        print("rank %d: local result %s" %(rank, local_res))

    # gather the local result to root
    
    res = None
    if rank == 0:
        res = np.empty(size * my_row_count, dtype='i')

    comm.Gather([local_res, MPI.INT], [res, MPI.INT], root=0)

    if rank==0:
        print("Multiplication result %s" %(res))
