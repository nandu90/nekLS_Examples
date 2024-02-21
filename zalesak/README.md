# Case Notes
## AVM does not work well with ifcont.eq. .true. - due to parasitic currents entering domain
### Recommend using periodic domain with AVM for this case, otherwise one will have to increase base diffusion significantly leading to excessive diffusion near the disk region
### Perhaps increased diffusion near O boundaries is a good idea for hyperbolic problems. Assuming near O regions are far away from regions of interest. 
### Parasitic currents entering the domain is also a function of velocity field near O boundaries. If the velocity normal vector to boundary is directed inward, you can expect parasitic currents.
## Non-linear SVV requires slightly higher base diffusion coeff to avoid parasitic currents
## I have added upwind AVM. But it looks like the benefits of upwind diffusion are not seen here - possible due to a scalar diffusion coefficient (as opposed to orhtogonal tensor coefficient in SVV)
