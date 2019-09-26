from mpi4py import MPI
import numpy

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
assert comm.size == 2

sdata = numpy.array([(rank+1) * i for i in range(10)])
rdata = numpy.array([0] * 10)

if comm.rank == 0:
    target = 1
else:
    target = 0

print("rank %d: initial data: %s" %(rank, sdata))

request = comm.Isend([sdata, MPI.INT], dest=target, tag=10)
comm.Recv([rdata, MPI.INT], source=target, tag=MPI.ANY_TAG)
request.Wait()

print("rank %d: received data %s" %(rank, rdata))
