from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size() 

A = [i * rank for i in range(5)]

print("My rank %d of %d" %(rank, size));
print("My values for A: %s" %(A));
