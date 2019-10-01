#!/usr/bin/env python 
from mpi4py import MPI
import numpy as np

# Example for sending a (int32, double64) tuple

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

def definetype():
    dtypes = [MPI.INT, MPI.DOUBLE]
    dt_size = MPI.INT.size + MPI.DOUBLE.size
    displ = [0, MPI.INT.size]

    new_dtype = MPI.Datatype.Create_struct([1, 1], displ, dtypes)
    new_dtype = new_dtype.Create_resized(0, dt_size)
    new_dtype.Commit()
    return new_dtype

def fill_data(data, num):
    for i in range(num):
        data[i][0] = i + 1
        data[i][1] = 3.14 * (i + 1)

if __name__ == "__main__":
    mytype = definetype()
    num = 2
    data = np.zeros(num, dtype="int32, double")

    if rank == 0:
        comm.Recv([data, mytype], source=1, tag=0)
        print(data)
    elif rank == 1:
        fill_data(data, num)
        comm.Send([data, mytype], dest=0, tag=0)
