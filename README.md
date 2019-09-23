# MPI Lectures 
### for the CS6320 class *Algorithms for parallel computing*
#### 1st and 3rd October 2019

Slides at: Link

**Table of contents**

1. Introduction to MPI
    - Library and implementation characteristics
    - MPI for python
    - Error handling

2. Blocking point-to-point communication
    - Sending and receiving with `MPI_Send` and `MPI_Recv`
    - Dynamic receiving with `MPI_Probe` and `MPI_Status`
    - Groups and communicators
    
3. Non-blocking communication

4. Collective communication
    - Synchronization (Barrier)
    - Data movement (Broadcast, Gather, Scatter, Allgather, Alltoall)
    - Collective computation (Reduce, AllReduce, Scan, Exscan, Reduce_scatter)
    - Define your own collective routine
    - Non-Blocking Collective Operations
    
5. Topology mapping and neighborhood collectives

6. Profiling MPI applications

**Code examples**
