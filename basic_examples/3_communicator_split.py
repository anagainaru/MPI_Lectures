#!/usr/bin/env python 
from mpi4py import MPI

# Example for splitting the processes in two groups

# Get the rank and size in the original communicator
world_rank = MPI.COMM_WORLD.Get_rank()
world_size = MPI.COMM_WORLD.Get_size()

# Determine color based on even/odd ranks
color = world_rank % 2; 

# Split the communicator based on the color and use the
# original rank for ordering
new_comm = MPI.COMM_WORLD.Split(color, world_rank)

new_rank = new_comm.Get_rank()
new_size = new_comm.Get_size()

print("World rank/size: %d/%d -- New rank/size: %d/%d" %(
                world_rank, world_size, new_rank, new_size));

new_comm.Free()
