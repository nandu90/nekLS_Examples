# nekLS_Examples

## Some troubleshooting tips

### Dam Break Problem

- More frequent CLSR makes for better stability (lower div errors)
- Some high fluctuations in div are expected at the start of the simulation
- No need to increase TLSR frequency
- Stable upto CFL=0.2
- ifvvisp T/F does not seem to make a measurable difference
- BDF1/2 does not seem to make an effect on the CFL stability limit. Stable upto CFL=0.2
