from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    sdata = np.array([i for i in range(5)])
    comm.Send(sdata, dest=1, tag=11)
elif rank == 1:
    rdata = np.array([0 for i in range(5)])
    comm.Recv(rdata, source=0, tag=11)
    print(rdata)
