from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    sdata = {'a': 7, 'b': 3.14}
    comm.send(sdata, dest=1, tag=11)
elif rank == 1:
    rdata = comm.recv(source=0, tag=11)
    print(rdata)
