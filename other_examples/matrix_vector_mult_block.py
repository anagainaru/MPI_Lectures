#!/usr/bin/env python 
from mpi4py import MPI
import numpy as np
import sys

# Example 3: Compute multiplication of a matrix with a vector
#     - Each process gets a chunk of the vector and of a row
#     - Number of elements in a row are a multiple of the chunk size
#     - Matrix has same number of elements on rows and columns

verbose = False

if __name__ == "__main__":

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    # number of rows
    number_rows = size
    if len(sys.argv) > 1:
        number_rows = int(sys.argv[1]) 

    assert((size % number_rows) == 0),\
            "Total number of chunks must be multiple of total processes"

    chunk_per_row = size // number_rows
    chunk_size = number_rows // chunk_per_row

    if verbose and rank==0:
        print("Each process receives %d elements from one row of %d elements" %(
            chunk_size, number_rows))
    
    # create vector and matrix data on root and
    # send corresponding chunks to each process

    local_A = np.zeros(chunk_size, dtype='i')
    local_vect = np.zeros(chunk_size, dtype='i')
    if rank==0:
        A = np.matrix([[i + 2 * j for i in range(number_rows)] for j in range(number_rows)], dtype='i')
        vect = np.array([i % 2 for i in range(number_rows)], dtype='i')
        print("Multiply matrix %s with vector %s" %(A, vect))

        for i in range(size):
            offset = (i % chunk_per_row) * chunk_size
            row_offset = i // chunk_per_row
            comm.Send([vect[offset:offset+chunk_size], MPI.INT], dest=i, tag=1)
            comm.Send([A[row_offset, offset:offset+chunk_size], MPI.INT], dest=i, tag=2)
    
    comm.Recv([local_vect, MPI.INT], source=0, tag=1)
    comm.Recv([local_A, MPI.INT], source=0, tag=2)
    
    if verbose:
        print("rank %d: matrix %s, vect %s" %(rank, local_A, local_vect))


    # local computation
    local_res = np.dot(local_A, local_vect)

    if verbose:
        print("rank %d: local result %s" %(rank, local_res))

    # reduce data for all ranks sharing a row
    color = rank // chunk_per_row
    new_comm = MPI.COMM_WORLD.Split(color, rank)
    local_res = new_comm.reduce(local_res, root=0)

    if new_comm.Get_rank() == 0:
        if verbose:
            print("rank %d: row %d result %d" %(rank, color, local_res))
        
        # send the local result to root
        comm.send(local_res, dest=0, tag=3)
    
    res = np.zeros(number_rows, dtype='i')
    if rank == 0:
        for i in range(number_rows):
            status = MPI.Status()
            ret = comm.recv(source=MPI.ANY_SOURCE, tag=3, status=status)
            rnk = status.Get_source()
            res[rnk // chunk_per_row] = ret

        print("Multiplication result %s" %(res))

