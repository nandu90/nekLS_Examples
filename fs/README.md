# Orr-Sommerfeld instability in two phases flow
Based on this Nek5000 example [fs_hydro](https://github.com/Nek5000/Nek5000/tree/master/short_tests/fs_hydro) 
and [fs_hydro.pdf](https://github.com/Nek5000/NekExamples/blob/35bac75238bf3e7abb6f621615be1f5b3b2bed04/fs_2/README.pdf).

The input file `u2.txt` contains all the properties, mean velocity profile, forcing, eigenvalue and mode. The eigenmodes
are calculated from solving Orr-Sommerfeld equation and interpolate to the mesh. The solver can be found 
[here](https://github.com/khanhn201/orr-sommerfeld/tree/main).

To check if the growth rate is correct, `grep AMP logfile`. The last value is the relative error.
