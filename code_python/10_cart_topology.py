#!/usr/bin/env python 
from mpi4py import MPI

# Example for creating a cartesian topology

comm = MPI.COMM_WORLD
world_rank = comm.Get_rank()
size = comm.Get_size()

dims = MPI.Compute_dims(size, [0]*2)
cart_comm = comm.Create_cart(
        dims, periods=[True,True], reorder=True)

new_rank = cart_comm.Get_rank()

print("World rank: %d -- Cart rank: %d" %(
    world_rank, new_rank));

cart_comm.Free()
