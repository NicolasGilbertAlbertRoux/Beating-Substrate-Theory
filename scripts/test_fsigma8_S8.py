import numpy as np
from scipy.special import erfc
from scipy.integrate import solve_ivp
Om0,OD0,dc = 0.315,0.685,1.686
N=np.linspace(np.log(0.02),np.log(1.0),700); a=np.exp(N); z=1/a-1

def growth(Eofa):
    lnE=np.log(Eofa); dlnE=np.gradient(lnE,N)
    def Om_a(x): ai=np.exp(x); E=np.interp(x,N,Eofa); return Om0*ai**-3/E**2
    def rhs(x,y): D,Dp=y; return [Dp,-(2+np.interp(x,N,dlnE))*Dp+1.5*Om_a(x)*D]
    s=solve_ivp(rhs,[N[0],N[-1]],[a[0],a[0]],t_eval=N,rtol=1e-7,atol=1e-9)
    D=s.y[0]; f=np.gradient(np.log(D),N)
    return D,f

def bst_E(sig0):
    E=np.sqrt(Om0*a**-3+OD0)
    for _ in range(30):
        D,_=growth(E); sig=sig0*D/np.interp(0.0,N,D)
        R=erfc(dc/(np.sqrt(2)*np.clip(sig,1e-3,None))); flux=np.clip(np.gradient(R,N),1e-6,None)
        rhoDE=OD0*flux/np.interp(0.0,N,flux)
        Enew=np.sqrt(Om0*a**-3+rhoDE); E=0.5*E+0.5*Enew
    return E

E_L=np.sqrt(Om0*a**-3+OD0); D_L,f_L=growth(E_L)
sig8_0=0.81
print("="*68); print("f*sigma8(z) et S8 : BST (auto-coherent) vs LCDM. Meme primordial."); print("="*68)
for sig0 in [1.3,1.6,2.0]:
    E_B=bst_E(sig0); D_B,f_B=growth(E_B)
    ratio=np.interp(0.0,N,D_B)/np.interp(0.0,N,D_L)
    s8_B=sig8_0*ratio
    S8_L=sig8_0*np.sqrt(Om0/0.3); S8_B=s8_B*np.sqrt(Om0/0.3)
    sig=sig0*D_B/np.interp(0.0,N,D_B); R=erfc(dc/(np.sqrt(2)*np.clip(sig,1e-3,None)))
    fl=np.clip(np.gradient(R,N),1e-6,None); rhoDE=OD0*fl/np.interp(0.0,N,fl)
    w=-1-(1/3)*np.gradient(np.log(rhoDE),N); w0=w[np.argmin(abs(z))]
    print(f"sig0={sig0}:  w0={w0:+.2f}  D_BST(0)/D_LCDM(0)={ratio:.3f}  sigma8_0(BST)={s8_B:.3f}  S8={S8_B:.3f} (LCDM {S8_L:.3f})")
