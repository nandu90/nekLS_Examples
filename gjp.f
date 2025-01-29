c-----------------------------------------------------------------------
      subroutine gjpsource (rhsufld,ufld,h2el)

C     Compute startresidual/right-hand-side in the pressure

      INCLUDE 'SIZE'
      INCLUDE 'TOTAL'

      real              ufld (lx1,ly1,lz1,1)
      real           rhsufld (lx1,ly1,lz1,1)

      real              h2el (2*ldim,1)

      integer              df_face(lx1*lz1*2*ldim*lelt)
      common /xcdf_arrays/ df_face
     
      integer            df_hndl,ndf_facex
      common /xcdf_ints/ df_hndl,ndf_facex

      real dU (lx1,ly1,lz1,lelt,3)
     $    ,dUdn (lx1,lz1,  6,lelt)
     $    ,udotn(lx1,lz1,  6,lelt)
     $    ,rdotn(lx1,lz1,  6,lelt)
     $    ,sdotn(lx1,lz1,  6,lelt)
     $    ,tdotn(lx1,lz1,  6,lelt)
     $    ,bm1i (lx1,ly1,lz1,lelt)

      real drdx(lx1,ly1,lz1), drdy(lx1,ly1,lz1), drdz(lx1,ly1,lz1)
     $    ,dsdx(lx1,ly1,lz1), dsdy(lx1,ly1,lz1), dsdz(lx1,ly1,lz1)
     $    ,dtdx(lx1,ly1,lz1), dtdy(lx1,ly1,lz1), dtdz(lx1,ly1,lz1)

      real wf1 (lx1,lz1,6),   wf2 (lx1,lz1,6),   wf3 (lx1,lz1,6)
     $    ,tf1 (lx1,lz1,6),   tf2 (lx1,lz1,6),   tf3 (lx1,lz1,6)

      real wa1 (lx1,ly1,lz1),   wa2 (lx1,ly1,lz1),   wa3 (lx1,ly1,lz1)
     $    ,ta1 (lx1,ly1,lz1),   ta2 (lx1,ly1,lz1),   ta3 (lx1,ly1,lz1)

      character cb*3

      integer icalld
      save    icalld
      data    icalld /0/

      nxyz1  = lx1*ly1*lz1
      ntot1  = nxyz1*nelv
      nxz1   = lx1*lz1
      nfaces = 2*ldim
      ntots  = nxz1*nfaces*nelv

      tau_gjp = 0.8/float(lx1)**4

      call rzero  (dU   ,3*ntot1)
      call rzero  (rhsufld,ntot1)
      call rzero  (   dUdn,ntots)
      call rzero  (  udotn,ntots)
      call rzero  (  rdotn,ntots)
      call rzero  (  sdotn,ntots)
      call rzero  (  tdotn,ntots)

c gradients of ufld
      !if (nid.eq.0) write(*,'(/,A)') 'Computing gradients '
      call gradm1  (dU(1,1,1,1,1),dU(1,1,1,1,2),dU(1,1,1,1,3),ufld)
      call gradm1  (dU(1,1,1,1,1),dU(1,1,1,1,2),dU(1,1,1,1,3),ufld)
      call gradm1  (dU(1,1,1,1,1),dU(1,1,1,1,2),dU(1,1,1,1,3),ufld)
      !if (nid.eq.0) write(*,'(/,A)') 'Done: Computing gradients'

      call invers2  (bm1i,bm1,ntot1)

      do iel=1,nelv

         ieg = lglel(iel)
         call col3 (drdx, rxm1(1,1,1,iel), jacmi(1,iel), nxyz1)
         call col3 (drdy, rym1(1,1,1,iel), jacmi(1,iel), nxyz1)
         call col3 (drdz, rzm1(1,1,1,iel), jacmi(1,iel), nxyz1)

         call col3 (dsdx, sxm1(1,1,1,iel), jacmi(1,iel), nxyz1)
         call col3 (dsdy, sym1(1,1,1,iel), jacmi(1,iel), nxyz1)
         call col3 (dsdz, szm1(1,1,1,iel), jacmi(1,iel), nxyz1)

         call col3 (dtdx, txm1(1,1,1,iel), jacmi(1,iel), nxyz1)
         call col3 (dtdy, tym1(1,1,1,iel), jacmi(1,iel), nxyz1)
         call col3 (dtdz, tzm1(1,1,1,iel), jacmi(1,iel), nxyz1)

         do ifc=1,nfaces

            call rzero  (wa1,  nxyz1)
            call rzero  (wa2,  nxyz1)
            call rzero  (wa3,  nxyz1)
            call rzero  (ta1,  nxyz1)
            call rzero  (ta2,  nxyz1)
            call rzero  (ta3,  nxyz1)

            call rzero  (wf1, 6*nxz1)
            call rzero  (wf2, 6*nxz1)
            call rzero  (wf3, 6*nxz1)
            call rzero  (tf1, 6*nxz1)
            call rzero  (tf2, 6*nxz1)
            call rzero  (tf3, 6*nxz1)

            cb = cbc(ifc,iel,1)
            if (cb.eq.'E  ' .or. cb.eq.'P  ') then

C     surface terms (n.u)
               call faccl3a
     $         (wf1(1,1,ifc),vx(1,1,1,iel),unx(1,1,ifc,iel),ifc)
               call faccl3a
     $         (wf2(1,1,ifc),vy(1,1,1,iel),uny(1,1,ifc,iel),ifc)
               if (ldim.eq.3)
     $          call faccl3a
     $         (wf3(1,1,ifc),vz(1,1,1,iel),unz(1,1,ifc,iel),ifc)
               call add2  (wf1(1,1,ifc),wf2(1,1,ifc),nxz1)
               if (ldim.eq.3)
     $         call add2  (wf1(1,1,ifc),wf3(1,1,ifc),nxz1)

               call add2  (udotn(1,1,ifc,iel),wf1(1,1,ifc),nxz1)

               unxmax = vlmax(unx(1,1,ifc,iel),nxz1)
               unymax = vlmax(uny(1,1,ifc,iel),nxz1)
               wf1max = vlmax(wf1(1,1,ifc),nxz1)
               wf2max = vlmax(wf1(1,1,ifc),nxz1)
               udotnmax = vlmax(udotn(1,1,ifc,iel),nxz1)
               ! write(*,*)"here",unxmax,unymax,wf1max,wf2max,udotnmax


C     surface terms (n.del r)
               call faccl3a
     $         (tf1(1,1,ifc),drdx         ,unx(1,1,ifc,iel),ifc)
               call faccl3a
     $         (tf2(1,1,ifc),drdy         ,uny(1,1,ifc,iel),ifc)
               if (ldim.eq.3)
     $          call faccl3a
     $         (tf3(1,1,ifc),drdz         ,unz(1,1,ifc,iel),ifc)
               call add2  (tf1(1,1,ifc),tf2(1,1,ifc),nxz1)
               if (ldim.eq.3)
     $         call add2  (tf1(1,1,ifc),tf3(1,1,ifc),nxz1)

               call add2  (rdotn(1,1,ifc,iel),tf1(1,1,ifc),nxz1)

C     surface terms (n.del s)
               call faccl3a
     $         (tf1(1,1,ifc),dsdx         ,unx(1,1,ifc,iel),ifc)
               call faccl3a
     $         (tf2(1,1,ifc),dsdy         ,uny(1,1,ifc,iel),ifc)
               if (ldim.eq.3)
     $          call faccl3a
     $         (tf3(1,1,ifc),dsdz         ,unz(1,1,ifc,iel),ifc)
               call add2  (tf1(1,1,ifc),tf2(1,1,ifc),nxz1)
               if (ldim.eq.3)
     $         call add2  (tf1(1,1,ifc),tf3(1,1,ifc),nxz1)

               call add2  (sdotn(1,1,ifc,iel),tf1(1,1,ifc),nxz1)

C     surface terms (n.del t)
               if (ldim.eq.3) then
                call faccl3a
     $         (tf1(1,1,ifc),dtdx         ,unx(1,1,ifc,iel),ifc)
                call faccl3a
     $         (tf2(1,1,ifc),dtdy         ,uny(1,1,ifc,iel),ifc)
                call faccl3a
     $         (tf3(1,1,ifc),dtdz         ,unz(1,1,ifc,iel),ifc)
                call add2 (tf1(1,1,ifc),tf2(1,1,ifc),nxz1)
                call add2 (tf1(1,1,ifc),tf3(1,1,ifc),nxz1)

                call add2 (tdotn(1,1,ifc,iel),tf1(1,1,ifc),nxz1)
               endif

C     surface terms (n.\del u)_sum
               call faccl3a
     $         (tf1(1,1,ifc),dU(1,1,1,iel,1),unx(1,1,ifc,iel),ifc)
               call faccl3a
     $         (tf2(1,1,ifc),dU(1,1,1,iel,2),uny(1,1,ifc,iel),ifc)
               if (ldim.eq.3)
     $          call faccl3a
     $         (tf3(1,1,ifc),dU(1,1,1,iel,3),unz(1,1,ifc,iel),ifc)
               call add2   (tf1(1,1,ifc),tf2(1,1,ifc),nxz1)
               if (ldim.eq.3)
     $         call add2   (tf1(1,1,ifc),tf3(1,1,ifc),nxz1)

               call add2   ( dUdn(1,1,ifc,iel),tf1(1,1,ifc),nxz1)

            endif

         enddo

         call vecabs(udotn(1,1,1,iel),6*nxz1)

      enddo

      call fgslib_gs_op(df_hndl,dUdn,1,1,0)  ! 1 ==> +

       udotmax = glmax(udotn, ntots)
       udotmin = glmin(udotn, ntots)
       if(nid.eq.0) write(*,*)' WTF is udotmin,udotmax ',udotmin,udotmax

       rdotmax = glmax(rdotn, ntots)
       rdotmin = glmin(rdotn, ntots)
       if(nid.eq.0) write(*,*)' WTF is rdotmin,rdotmax ',rdotmin,rdotmax

       sdotmax = glmax(sdotn, ntots)
       sdotmin = glmin(sdotn, ntots)
       if(nid.eq.0) write(*,*)' WTF is sdotmin,sdotmax ',sdotmin,sdotmax

       tdotmax = glmax(tdotn, ntots)
       tdotmin = glmin(tdotn, ntots)
       ! if(nid.eq.0) write(*,*)' WTF is tdotmin,tdotmax ',tdotmin,tdotmax


       dudxmax = glmax(dU(1,1,1,1,1), ntot1)
       dudxmin = glmin(dU(1,1,1,1,1), ntot1)
       if(nid.eq.0) write(*,*)' WTF is dudxmin,dudxmax ',dudxmin,dudxmax
c
       dudymax = glmax(dU(1,1,1,1,2), ntot1)
       dudymin = glmin(dU(1,1,1,1,2), ntot1)
       if(nid.eq.0) write(*,*)' WTF is dudymin,dudymax ',dudymin,dudymax
c
       dudzmax = glmax(dU(1,1,1,1,3), ntot1)
       dudzmin = glmin(dU(1,1,1,1,3), ntot1)
       ! if(nid.eq.0) write(*,*)' WTF is dudzmin,dudzmax ',dudzmin,dudzmax
c
       dudnmax = glmax(dUdn, ntots)
       dudnmin = glmin(dUdn, ntots)
       if(nid.eq.0) write(*,*)' WTF is dudnmin,dudnmax ',dudnmin,dudnmax
c

      do iel=1,nelv

         do ifc=1,nfaces

            call rzero  (tf1, 6*nxz1)
            call rzero  (tf2, 6*nxz1)
            call rzero  (tf3, 6*nxz1)

            cb = cbc(ifc,iel,1)
            if (cb.eq.'E  ' .or. cb.eq.'P  ') then

              gjpconst = h2el(ifc,iel)*tau_gjp
              ! if(nid.eq.0) write(*,*) 'WTF is gjpconst '
      ! $                                   ,iel, ifc, gjpconst

              call col4 (tf1(1,1,ifc),udotn(1,1,ifc,iel),
     $              dUdn(1,1,ifc,iel),rdotn(1,1,ifc,iel),nxz1)
              call col4 (tf2(1,1,ifc),udotn(1,1,ifc,iel),
     $              dUdn(1,1,ifc,iel),sdotn(1,1,ifc,iel),nxz1)
              if (ldim.eq.3)
     $        call col4 (tf3(1,1,ifc),udotn(1,1,ifc,iel),
     $              dUdn(1,1,ifc,iel),tdotn(1,1,ifc,iel),nxz1)

              call cmult(tf1(1,1,ifc),gjpconst,nxz1)
              call cmult(tf2(1,1,ifc),gjpconst,nxz1)
              call cmult(tf3(1,1,ifc),gjpconst,nxz1)

              call volcl3 (rhsufld(1,1,1,iel)
     $                          ,tf1(1,1,ifc)
     $                          ,tf2(1,1,ifc)
     $                          ,tf3(1,1,ifc),area(1,1,ifc,iel),ifc)

            endif

         enddo

      enddo

c      call col2 (rhsufld,bm1i,ntot1)

      return
      end

c-----------------------------------------------------------------------
      subroutine vecabs(a,n)
      real a(1)

      do i=1,n
         a(i)=abs(a(i))
      enddo

      return
      end
C
      subroutine faccl3a(a,b,c,iface1)
C
C     Collocate B with A on the surface IFACE1 of element IE.
C
C         A is a (NX,NY,IFACE) data structure
C         B is a (NX,NY,NZ) data structure
C         C is a (NX,NY,IFACE) data structure
C         IFACE1 is in the preprocessor notation 
C         IFACE  is the dssum notation.
C         5 Jan 1989 15:12:22      PFF
C
      include 'SIZE'
      include 'TOPOL'
      DIMENSION A(LX1,LY1),B(LX1,LY1,LZ1),C(LX1,LY1)
C
C     Set up counters
C
      CALL DSSET(lx1,ly1,lz1)
      IFACE  = EFACE1(IFACE1)
      JS1    = SKPDAT(1,IFACE)
      JF1    = SKPDAT(2,IFACE)
      JSKIP1 = SKPDAT(3,IFACE)
      JS2    = SKPDAT(4,IFACE)
      JF2    = SKPDAT(5,IFACE)
      JSKIP2 = SKPDAT(6,IFACE)
C
      I = 0
      DO 100 J2=JS2,JF2,JSKIP2
      DO 100 J1=JS1,JF1,JSKIP1
         I = I+1
         A(I,1) = B(J1,J2,1)*C(I,1)
  100 CONTINUE
C
      return
      end
C
c-----------------------------------------------------------------------
C
      subroutine volcl3 (a,b1,b2,b3,c,iface1)
C
C     Collocate B with A on the surface IFACE1 of element IE.
C
C         A is a (NX,NY,IFACE) data structure
C         B is a (NX,NY,NZ) data structure
C         C is a (NX,NY,IFACE) data structure
C         IFACE1 is in the preprocessor notation 
C         IFACE  is the dssum notation.
C         5 Jan 1989 15:12:22      PFF
C
      include 'SIZE'
      include 'TOPOL'
      include 'DXYZ'
      DIMENSION A(LX1,LY1,LZ1)
     $         ,B1(LX1,LY1),B2(LX1,LY1),B3(LX1,LY1),C(LX1,LY1)
C
C     Set up counters
C
      CALL DSSET(lx1,ly1,lz1)
      IFACE  = EFACE1(IFACE1)
      JS1    = SKPDAT(1,IFACE)
      JF1    = SKPDAT(2,IFACE)
      JSKIP1 = SKPDAT(3,IFACE)
      JS2    = SKPDAT(4,IFACE)
      JF2    = SKPDAT(5,IFACE)
      JSKIP2 = SKPDAT(6,IFACE)
C

      if    (IFACE.eq.1 .or. IFACE.eq.2) then

           ixt= 1
           if(IFACE.eq.2) ixt= lx1
           I = 0
           sumA = 0.
           do J2=JS2,JF2,JSKIP2
              iz = 1 + (J2-1)/ly1
              do J1=JS1,JF1,JSKIP1
                 I = I+1
                 sumA       =sumA       +              B1(I,1)*C(I,1)
                 iy = 1 + (J1-ixt)/lx1
                 do ix=1,lx1
                    A(ix,iy,iz)=A(ix,iy,iz)+dxtm1(ix,ixt)*B1(I,1)*C(I,1)
                 enddo
c          if(nid.eq.0) write(*,*) 'WTF iz, iy, ix iface 1 2'
c     $                                               , iz, iy, ix, iface
              enddo
           enddo
c           if(nid.eq.0) write(*,*) 'WTF area face 1 2 ', iface, sumA

      elseif(IFACE.eq.3 .or. IFACE.eq.4) then

           iyt= 1
           if(IFACE.eq.4) iyt= ly1
           I = 0
           sumA = 0.
           do J2=JS2,JF2,JSKIP2
              iz = (J2-1)/ly1 + 1
              do J1=JS1,JF1,JSKIP1
                 I = I+1
                 sumA       =sumA       +              B2(I,1)*C(I,1)
                 ix = J1-(iyt-1)*lx1
                 do iy=1,ly1
                    A(ix,iy,iz)=A(ix,iy,iz)+dytm1(iy,iyt)*B2(I,1)*C(I,1)
                 enddo
c          if(nid.eq.0) write(*,*) 'WTF iz, iy, ix iface 3 4'
c     $                                               , iz, iy, ix, iface
              enddo
           enddo
c           if(nid.eq.0) write(*,*) 'WTF area face 3 4 ', iface, sumA

      elseif(IFACE.eq.5 .or. IFACE.eq.6) then

           izt= 1
           if(IFACE.eq.6) izt= lz1
           I = 0
           sumA = 0.
           do J2=JS2,JF2,JSKIP2
              iy = J2
              do J1=JS1,JF1,JSKIP1
                 I = I+1
                 sumA       =sumA       +              B3(I,1)*C(I,1)
                 ix = J1-(izt-1)*lx1*ly1
                 do iz=1,lz1
                    A(ix,iy,iz)=A(ix,iy,iz)+dztm1(iz,izt)*B3(I,1)*C(I,1)
                 enddo
c          if(nid.eq.0) write(*,*) 'WTF iz, iy, ix iface 5 6'
c     $                                               , iz, iy, ix, iface
              enddo
           enddo
c           if(nid.eq.0) write(*,*) 'WTF area face 5 6 ', iface, sumA

      endif
C
      return
      end

c-----------------------------------------------------------------------

      subroutine df_setup
      include 'SIZE'
      include 'TOTAL'

      integer              df_face(lx1*lz1*2*ldim*lelt)
      common /xcdf_arrays/ df_face
     
      integer            df_hndl,ndf_facex
      common /xcdf_ints/ df_hndl,ndf_facex

      common /ivrtx/ vertex ((2**ldim)*lelt)
      common /ctmp1/ qs(lx1*ly1*lz1*lelt)
      integer vertex

      call setup_df_gs(df_hndl,lx1,ly1,lz1,nelt,nelgt,vertex)
      call df_set_fc_ptr

c      param(59)=1
c      call geom_reset(1)
c      call set_unr

      return
      end

c-----------------------------------------------------------------------
      subroutine df_set_fc_ptr

c     Set up pointer to restrict u to faces ! NOTE: compact

      include 'SIZE'
      include 'TOTAL'

      integer              df_face(lx1*lz1*2*ldim*lelt)
      common /xcdf_arrays/ df_face
     
      integer            df_hndl,ndf_facex
      common /xcdf_ints/ df_hndl,ndf_facex

      integer e,f,ef

      call dsset(lx1,ly1,lz1) ! set skpdat

      nxyz  = lx1*ly1*lz1
      nxz   = lx1*lz1
      nface = 2*ldim
      nxzf  = lx1*lz1*nface ! red'd mod to area, unx, etc.

      k = 0

      do e=1,nelv
      do ef=1,nface  ! EB notation

         f      = eface1(ef)
         js1    = skpdat(1,f)
         jf1    = skpdat(2,f)
         jskip1 = skpdat(3,f)
         js2    = skpdat(4,f)
         jf2    = skpdat(5,f)
         jskip2 = skpdat(6,f)

         i = 0
         do j2=js2,jf2,jskip2
         do j1=js1,jf1,jskip1

            i = i+1
            k = i+nxz*(ef-1)+nxzf*(e-1)           ! face   numbering
            df_face(k) = j1+lx1*(j2-1)+nxyz*(e-1) ! global numbering

         enddo
         enddo

      enddo
      enddo
      ndf_facex = nxzf*nelv

      return
      end

c-----------------------------------------------------------------------
      subroutine df_face2full(vol_ary, faceary)

      include 'SIZE'
      include 'TOTAL'

      integer              df_face(lx1*lz1*2*ldim*lelt)
      common /xcdf_arrays/ df_face
     
      integer            df_hndl,ndf_facex
      common /xcdf_ints/ df_hndl,ndf_facex

      real     faceary(lx1*lz1,2*ldim,lelt)
      real     vol_ary(lx1,ly1,lz1,lelt)
      integer  i,j

      n=lx1*ly1*lz1*nelfld(ifield)
      call rzero(vol_ary,n)

c      write(*,*) 'WTF is ndf_facex ', ndf_facex
      do j=1,ndf_facex
         i=df_face(j)
c         write(*,*) 'WTF is df_face ', i, j
         vol_ary(i,1,1,1) = vol_ary(i,1,1,1)+faceary(j,1,1)
      enddo

      return
      end

c-----------------------------------------------------------------------
      subroutine setup_df_gs(dfh,nx,ny,nz,nel,melg,vertex)

c     Global-to-local mapping for gs

      include 'SIZE'
      include 'TOTAL'

      integer   dfh,vertex(1)

      parameter(lf=lx1*lz1*2*ldim*lelt)
      common /c_is1/ glo_num_vol((lx1+2)*(ly1+2)*(lz1+2)*lelt)
     $             , glo_num_face(lf)
      integer*8 glo_num_face,glo_num_vol,ngv

      common /nekmpi/ mid,mp,nekcomm,nekgroup,nekreal

      integer icalld
      save    icalld
      data    icalld /0/

      mx = nx +2
      ! if(nid.eq.0) write(*,*) 'WTF calling set_vert from setup_df_gs'
      call set_vert(glo_num_vol,ngv,mx,nel,vertex,.true.)

      mxyz1 = mx*mx*mx
      mxy1  = mx*mx
      if(icalld.eq.0) then
         if(nid.eq.0) then
            do ie=1,nelv
               ifs = (ie-1)*2**ldim +        1
               ifl = (ie-1)*2**ldim +  2**ldim
c               write(*,'(A,11(1X,I8))') 'WTF is vertex ',
c     $                       (vertex(ii), ii=ifs, ifl)
            enddo
               
            do ie=1,nelv
               do kk=1,mx
                 do jj=1,mx
                    iis = (ie-1)*mxyz1 + (kk-1)*mxy1 + (jj-1)*mx +  1
                    iil = (ie-1)*mxyz1 + (kk-1)*mxy1 + (jj-1)*mx + mx
c                    write(*,'(A,13(1X,I8))') 'WTF is glo_num ',iis,iil,
c     $                       (glo_num_vol(ii), ii=iis,iil)
                 enddo 
               enddo 
            enddo 
         endif
         icalld = 1
      endif

      mz0 = 1
      mz1 = 1
      if (if3d) mz0 = 0
      if (if3d) mz1 = lz1+1
      call iface_vert_int8 (glo_num_face,glo_num_vol,mz0,mz1,nelt)

      nf = lx1*lz1*2*ldim*nelt !total number of points on faces
      call fgslib_gs_setup(dfh,glo_num_face,nf,nekcomm,np)

      return
      end

c-----------------------------------------------------------------------
      subroutine get_h2el (h2el)

C     Compute startresidual/right-hand-side in the pressure

      INCLUDE 'SIZE'
      INCLUDE 'TOTAL'

      real              h2el (2*ldim,1)

      nfaces = 2*ldim

      do iel=1,nelv

         xe1 = xm1(  1,  1,  1,iel)
         xe2 = xm1(nx1,  1,  1,iel)
         ye1 = ym1(  1,  1,  1,iel)
         ye2 = ym1(  1,ny1,  1,iel)
         ze1 = zm1(  1,  1,  1,iel)
         ze2 = zm1(  1,  1,nz1,iel)

         do iface=1,nfaces

            if(iface.eq.2 .or. iface.eq.4) h_el = xe2-xe1
            if(iface.eq.1 .or. iface.eq.3) h_el = ye2-ye1
            if(iface.eq.5 .or. iface.eq.6) h_el = ze2-ze1

            h2el (iface,iel) = h_el*h_el
c            if(nid.eq.0) write(*,*) 'WTF is e f h_el h2el ',
c     $                   iel, iface, h_el, h2el(iface,iel)

         enddo

      enddo

      return
      end

c-----------------------------------------------------------------------
