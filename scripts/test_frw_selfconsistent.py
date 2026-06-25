import numpy as np
from scipy.special import erfc
from scipy.integrate import solve_ivp
# FRW AUTO-COHERENT : rho_DE(flux de collapse) -> H -> D(croissance) -> flux -> itere.
Om0,OD0,dc = 0.315,0.685,1.686
sig0 = 2.0
N = np.linspace(np.log(0.02), np.log(1.25), 800); a=np.exp(N)
def growth_D(Eofa):
    lnE=np.log(Eofa); dlnE=np.gradient(lnE,N)
    def Om_a(x): ai=np.exp(x); E=np.interp(x,N,Eofa); return Om0*ai**-3/E**2
    def rhs(x,y): D,Dp=y; return [Dp,-(2+np.interp(x,N,dlnE))*Dp+1.5*Om_a(x)*D]
    sol=solve_ivp(rhs,[N[0],N[-1]],[a[0],a[0]],t_eval=N,rtol=1e-7,atol=1e-9)
    D=sol.y[0]; return D/np.interp(0.0,N,D)
def rhoDE_from_D(D):
    sig=sig0*D; R=erfc(dc/(np.sqrt(2)*np.clip(sig,1e-3,None)))
    flux=np.clip(np.gradient(R,N),1e-6,None)
    return OD0*flux/np.interp(0.0,N,flux)
E=np.sqrt(Om0*a**-3+OD0)
for it in range(40):
    D=growth_D(E); rhoDE=rhoDE_from_D(D); Enew=np.sqrt(Om0*a**-3+rhoDE)
    diff=np.max(np.abs(Enew-E)/E); E=0.5*E+0.5*Enew
    if diff<1e-6: break
z=1/a-1; rhoDE=rhoDE_from_D(growth_D(E))
w=-1-(1/3)*np.gradient(np.log(rhoDE),N); ODE=rhoDE/(Om0*a**-3+rhoDE)
i0=np.argmin(abs(z)); w0=w[i0]; wa=-np.gradient(w,a)[i0]
m=(z>-0.2)&(z<3); zc=z[m][np.argmin(abs(w[m]+1))]
print("="*60); print(f"FRW AUTO-COHERENT (sig0={sig0}, converge {it+1} iter, diff={diff:.1e})"); print("="*60)
print(f"{'z':>6} {'H/H0':>7} {'rho_DE':>8} {'Om_DE':>7} {'w(z)':>8}")
for zz in [1.5,1.0,0.5,0.3,0.0]:
    i=np.argmin(abs(z-zz)); print(f"{z[i]:>6.2f} {E[i]:>7.3f} {rhoDE[i]:>8.4f} {ODE[i]:>7.4f} {w[i]:>8.3f}")
print(f"\n  croisement w=-1 a z~{zc:.2f} ; rho_DE pique a z~{z[np.argmax(rhoDE)]:.2f}")
print(f"  w0={w0:+.3f}  wa~{wa:+.2f}  Omega_DE(0)={ODE[i0]:.3f}")
