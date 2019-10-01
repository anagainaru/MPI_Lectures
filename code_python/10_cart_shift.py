from mpi4py import MPI

comm = MPI.COMM_WORLD
world_rank = comm.Get_rank()
size = comm.Get_size()

ndim = 2

dims = MPI.Compute_dims(size, [0]*ndim)
cart_comm = comm.Create_cart(
        dims, periods=[True,True], reorder=True)

new_rank = cart_comm.Get_rank()
if new_rank==0:
    print("Cart dim: %s" %(dims))

for i in range(ndim):
    for d in (-1, +1):
        source, dest = cart_comm.Shift(i, d)
        if new_rank == 0:
            print("Dir %d, disp %d - Src %d - Dest %d" %(
                i, d, source, dest));

cart_comm.Free()
