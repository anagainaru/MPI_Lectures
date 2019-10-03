#!/usr/bin/env python 
from mpi4py import MPI
import numpy as np
import random
import sys
from heapq import merge 

# Example 2: Merge Sort
#     - Number of processes are a power of 2
#     - Global array is 4 times number of processes

verbose = False

def merge_sort(max_height, rank, start_array, comm):
    local_array = np.copy(start_array)

    for height in range(max_height):
        parent = rank & (~(1 << height))
        if rank == parent:
            child = rank | (1 << height)
            # receive data from the right child
            if verbose:
                print("At height %d, rank %d receive from %d" %(height, rank, child))
            data = np.array([0] * len(local_array))
            comm.Recv([data, MPI.INT], source=child, tag=height)
            # merge the array with your own data
            local_array = np.array(list(merge(local_array, data)))
        else:
            # send your data to the parent
            if verbose:
                print("At height %d, rank %d sends to %d" %(height, rank, parent))
            comm.Send([local_array, MPI.INT], dest=parent, tag=height)
            break

    return local_array

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # allow only size equal to power of 2
    assert((size & (size - 1)) == 0),\
            "Number of processes must be power of 2"

    global_array_size = size * 4
    if len(sys.argv)>1:
        global_array_size = int(sys.argv[1])
        assert (global_array_size % size ==0)

    # calculate total height of tree
    height = int(np.log2(size))

    if rank==0:
        # create input array
        global_data = list(range(global_array_size))
        random.shuffle(global_data)
        global_data = np.array(global_data)
        if verbose:
            print("Global data %s" %(global_data))
            print("Tree of hight %d" %(height))
    else:
        global_data = None

    comm.barrier();
    local_wt = MPI.Wtime();

    local_array_size = global_array_size // size
    local_data = np.array([0] * local_array_size)
    comm.Scatter([global_data, MPI.INT], [local_data, MPI.INT], root=0)    

    if verbose:
        print("Rank %d: data %s" %(rank, local_data))

    local_data.sort()
    
    if verbose:
        print("Rank %d: local data sorted %s" %(rank, local_data))

    res = merge_sort(height, rank, local_data, comm)

    local_wt = MPI.Wtime() - local_wt;
    wt = comm.reduce(local_wt, op=MPI.MAX, root=0);

    if rank == 0:
        if verbose:
            print("Sorted array %s" %(res))
        assert(all(res[i] <= res[i+1] for i in range(len(res)-1)))
        print("Time to sort %d elements on %d processes: %f" %(
            global_array_size, size, wt))
