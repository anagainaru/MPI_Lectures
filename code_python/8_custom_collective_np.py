#!/usr/bin/env python 
from mpi4py import MPI
import numpy as np

# Example of implementing a custom reduction operation
# that identifies array indexes with odd numbers
# in any of the processors

def unpack_array(array_mem, dt):
    a = array_mem.tobytes()
    itemsize = dt.Get_size()
    array_len = int(array_mem.shape[0])
    unpack_array = []
    for i in range(int(array_len/itemsize)):
        unpack_array.append(int(np.frombuffer(a[itemsize*i:itemsize*(i+1)],
                            dtype=np.int64)))
    return np.array(unpack_array)

def myprod(xmem, ymem, dt):
    a = unpack_array(xmem, dt)
    b = unpack_array(ymem, dt)

    c = np.array([0] * len(a))
    for i in range(len(a)):
        c[i] = a[i] % 2 | b[i] % 2
    
    ymem[:] = memoryview(bytearray(c))[:]


comm = size = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

a = np.array([rank * (i + 1) for i in range(3)])
b = np.array([0] * 3)
print("Rank %d: Data %s" %(rank, a))

myop = MPI.Op.Create(myprod, True) # commute is True
comm.Reduce([a, MPI.DOUBLE], [b, MPI.DOUBLE], op=myop, root=0)

if rank==0:
    print("Contains odd numbers: %s" %(b))
