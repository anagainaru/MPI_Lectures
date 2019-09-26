from mpi4py import MPI

rank = MPI.COMM_WORLD.Get_rank()
print("rank %d: before barrier" %(rank))

MPI.COMM_WORLD.barrier()

print("rank %d: after barrier" %(rank))
