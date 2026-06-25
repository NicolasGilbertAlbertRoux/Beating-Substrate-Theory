# -*- coding: utf-8 -*-
"""
BST Appendix Stage KG04 — waves -> contacts: are the localization sites of a wave GEOMETRIC/TOPOLOGICAL
events, not added axioms? Build a generic wave field (random superposition of plane waves) and
identify its intrinsic geometric singularities:
  (1) PHASE SINGULARITIES (optical vortices): points where psi=0 and the phase winds by +/-2pi.
      These are TOPOLOGICAL defects -- the SAME vorticity objects as magnetism (S59). At intensity ZEROS.
  (2) FLUX CONCENTRATIONS (caustics / intensity maxima): where |psi|^2 is high -- the CONTACT-likely
      sites (Born-relevant). Geometric (catastrophe-type) concentrations of the ray flow.
Honest status (per the trio): same geometric GRAMMAR for classical contacts and measurement-localization;
it remains to show how far it reproduces QM quantitatively. The FORM is |psi|^2 (wave intensity); the
probability RULE (intensity -> frequency) stays the scale-wall residue.
"""
import numpy as np
np.random.seed(1)
N=256; L=40.0; dx=L/N
x=(np.arange(N))*dx; X,Y=np.meshgrid(x,x,indexing='ij')

# generic random wave field: sum of M plane waves, fixed |k| (monochromatic isotropic) = standard model
M=40; k0=2.0
psi=np.zeros((N,N),complex)
for _ in range(M):
    th=np.random.uniform(0,2*np.pi); ph=np.random.uniform(0,2*np.pi)
    kx,ky=k0*np.cos(th),k0*np.sin(th)
    psi+=np.exp(1j*(kx*X+ky*Y+ph))
psi/=np.sqrt(M)
I=np.abs(psi)**2; phase=np.angle(psi)

# (1) locate phase singularities: plaquette phase winding = +/-2pi
def winding(ph):
    def d(a,b):
        x=b-a; return (x+np.pi)%(2*np.pi)-np.pi
    w=( d(ph[:-1,:-1],ph[:-1,1:]) + d(ph[:-1,1:],ph[1:,1:])
       + d(ph[1:,1:],ph[1:,:-1]) + d(ph[1:,:-1],ph[:-1,:-1]) )
    return w
W=winding(phase)
charge=np.round(W/(2*np.pi)).astype(int)
nplus=int((charge==1).sum()); nminus=int((charge==-1).sum())
# intensity AT the vortices vs the field mean
vmask=(charge!=0)
I_at_vort=I[:-1,:-1][vmask].mean(); I_mean=I.mean(); I_max=I.max()

print("="*70)
print("WAVE FIELD: %d plane waves, |k|=%.1f, grid %d^2"%(M,k0,N))
print("="*70)
print("(1) PHASE SINGULARITIES (topological vortices = the S59 vorticity objects):")
print("    count: +charge=%d, -charge=%d, total=%d ; net charge=%d (should be ~0)"%(nplus,nminus,nplus+nminus,nplus-nminus))
print("    density n_v = %.4f /area  (theory k^2/4pi = %.4f)"%((nplus+nminus)/(L*L),k0**2/(4*np.pi)))
print("    <intensity> AT vortices = %.4f   vs field mean = %.4f   => vortices sit at intensity %s"
      %(I_at_vort,I_mean,"MINIMA (zeros)" if I_at_vort<0.3*I_mean else "?"))
print("\n(2) FLUX CONCENTRATIONS (contact-likely sites = Born-relevant, high |psi|^2):")
hi=I> (I_mean+2*I.std())
print("    high-intensity fraction of area = %.3f ; max/mean intensity = %.1f"%(hi.mean(),I_max/I_mean))
print("    => contacts (high flux) and vortices (zero flux) are DISTINCT geometric features of one wave.")
print("    [NB: max/mean is a DIMENSIONLESS ratio set by M, threshold, seed, mesh -- it is NOT g;")
print("     any resemblance to 9.81 m/s^2 is pure coincidence/numerology, not physics.]")

print("\nREADING (honest):")
print(" - The wave is intrinsically organized by GEOMETRIC singularities: topological vortices (S59")
print("   vorticity, at zeros) AND flux concentrations/caustics (high |psi|^2, contact-likely).")
print(" - 'Contacts/definiteness' = a resolution event at the flux-concentration geometry; its FORM")
print("   follows |psi|^2 (wave intensity). Same geometric grammar as classical contacts.")
print(" - RESIDUE unchanged: the probability RULE (intensity->frequency) = scale wall. NOT closed here.")
print(" - STATUS: BST offers ONE geometric grammar for contacts and measurement events; how far it")
print("   reproduces QM quantitatively remains to be shown. (No claim that measurement is 'explained'.)")
