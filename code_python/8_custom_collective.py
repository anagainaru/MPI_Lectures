from mpi4py import MPI

from Complex import Complex
# Complex class defined in a separate file

def myprod(a, b, c):
    c = Complex()
    c.real = a.real * b.real - a.img * b.img
    c.img = a.img * b.real + a.real * b.img
    return c

comm = size = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

a = Complex(rank + 1, rank)
print("Rank %d: Data %s" %(rank, a))

myop = MPI.Op.Create(myprod, True) # commute is True
res = comm.reduce(a, op=myop, root=0)

if rank==0:
    print("Product: %s" %(res))
