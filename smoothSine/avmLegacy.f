c---------------------------------------------------------------------
      subroutine evm_setvisc(u, visc)
      include 'SIZE'
      include 'TOTAL'

      parameter (lt=lx1*ly1*lz1*lelt)
      real u(lt)
      common /scruz/  h0(lt),uf(lt),r(lt),diag(lx1)
      real  h0, uf, r, diag

      common /screvm/ h1(lt), h2(lt), dtmp(lt)
      real  h1, h2, dtmp

      integer ibuild,e
      save    ibuild
      data    ibuild / 0 /

      real    visum 
      save    visum 
      data    visum  / 0. /
      integer ncut, nc

      integer trantyp ! changes transfer function
      integer ncuttyp           ! changes cut-off modes number

      real visc(lx1,ly1,lz1,nelv)
      
      ncuttyp = 3               ! 1/5 of lx1
      if(ncuttyp.eq.1) then
        nc = lx1-3
        if(lx1.le.3) then
          write(6,*) 'evm: lx1=',lx1,'<=3, set nc=1'
          nc = 1
        endif
      elseif(ncuttyp.eq.2) then
        nc   = int((3./4.)*lx1)
      elseif(ncuttyp.eq.3) then
        nc   = int((4./5.)*lx1)
      endif
      ncut = lx1 - nc

      n = nx1*ny1*nz1*nelv
      dinv=1./ldim
      do i=1,n
         h0(i)=bm1(i,1,1,1)**dinv ! Local length scale
         v2   =vx(i,1,1,1)**2+vy(i,1,1,1)**2+vz(i,1,1,1)**2
         v    =sqrt(v2)
         visc(i,1,1,1)=0.5*v*h0(i)  ! This is the max possible viscosity
         !gamma=0.5
      enddo

      
      nxyz=nx1*ny1*nz1
      call copy     (uf,u,n)
      
      alpha = 0.5
      
      call rone(diag,nx1)
      trantyp = 1 ! linear

      if(trantyp.eq.1) then    ! linear dropdown
        do k=1,ncut
          j = nx1-k + 1
          w = alpha*(float(ncut+1-k)/float(ncut))
          diag(j) = 1.-w
        enddo
      elseif(trantyp.eq.2) then ! quadratic rolldown
        do k=1,ncut
          j = nx1-k + 1
          w = alpha*((float(ncut+1-k)/float(ncut))**2)
          diag(j) = 1.-w
        enddo
      endif

      ifld=2
      call evm_g_filter1(uf,diag,ifld,ibuild)
      call sub2         (uf,u,n)
      ! call convop       (r,uf)              ! Residual
      call convect_new(r,uf,.false.,vx,vy,vz,.false.)
      call invcol2(r,bm1,n)

      call rone (uf,n)
      uavg = gl2norm(u, n) / gl2norm(uf, n)
      call cmult(uf,uavg,n)
      call sub2 (uf, u, n)
      uinf = glamax (uf, n)

      icapcnt = 0
      do i=1,n        ! evaluate viscosity
        const = 1.0 ! Tuning factor c_E
        ent_visc = const*abs(r(i))*(h0(i)**2) / uinf
        cap = visc(i,1,1,1)
        visc(i,1,1,1)  = min(visc(i,1,1,1),ent_visc)
        visc(i,1,1,1) = max(visc(i,1,1,1),1e-20)
        if(abs(visc(i,1,1,1)-cap).le.1e-8) icapcnt = icapcnt + 1
      enddo
      icapsum = iglsum(icapcnt,1)
      nsum = iglsum(n,1)

      do e=1,nelv
        vmax=vlmax(visc(1,1,1,e),nxyz)
        call cfill(visc(1,1,1,e),vmax,nxyz)
      enddo

      
      vismx = glamax(visc,n)
      vismn = glamin(visc,n)
      visav = glsc2(visc,bm1,n)/volvm1

      visum = visum + vlsc2(visc,bm1,n)*dt
      vsum  = glsum(visum,1)

      if(nio.eq.0 .and. istep.le.1) write(6,*) 'Modes:',ncut
     $            ,', transfer type(1-linear,2-quad)',trantyp
     $            ,', alpha=',alpha

      if(nio.eq.0)write(6,10) istep,vismx,vismn,visav,icapsum,nsum,vsum
  10  format(i6,1p3e12.5,2i9,1p1e12.5' evm')

      
      return
      end
c---------------------------------------------------------------------
      subroutine evm_g_filter1(u,diag,ifld,ibuild)
c
c     Generalized filter: F(u) with F = J^T D J, where D=diag(diag)
c
      include 'SIZE'
      include 'TOTAL'

      real u(1),diag(1)

      parameter (lxx=lx1*lx1,lxyz=lx1*ly1*lz1)
      common /cgflt1/ f(lxx),wk1(lxyz),wk2(lxyz),wk3(lxyz)

      ifldt  = ifield
      ifield = ifld

      if (ibuild.eq.0) call build_filter(f,diag,nx1)
      ibuild=1

      call filterq(u,f,nx1,nz1,wk1,wk2,wk3,if3d,umax)

      ifield = ifldt

      return
      end
c---------------------------------------------------------------------      
