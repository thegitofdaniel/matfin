from math import e, log
from numpy_financial import npv
from datetime import date

class intrate():
    def __init__(self,nom_rate,nom_period,cap_period,method):
        self.nom_rate=nom_rate
        self.nom_period=nom_period
        self.cap_period=cap_period
        self.method=method
        
class produto():
    def __init__(self,v0=0,v1=0,ytm=0):
        self.v0==0
        self.v1==0
        self.ytm==0

def simple(v0=1,i=0,dt=1,ndigits=2):
    v1 = v0*(1+i*dt)
    return round(v1,ndigits=ndigits)

def compounded(v0=1,i=0,dt=1,ndigits=2):
    v1 = v0*(1+i)**dt
    return round(v1,ndigits)

def continuous(v0=1,i=0,dt=1,ndigits=2):
    v1 = v0*e**(i*dt)
    return round(v1,ndigits)

def npv_geometric(pmt=1,i=0.5,g=0,exact=False,ndigits=2):
    if exact:
        v0 = pmt/(e**i-1-g)
    else:
        v0 = pmt/(i-g)
    return round(v0,ndigits)

def equivalent(i0,f0,i1,f1):
    return (1+i0)**f0==(1+i1)**f1

def i_ltn(v0,dt,v1=1000,ndigits=4):
    # CDB 360
    # LTN/NTN -> 252
    i = (v1/v0)**(252/dt)-1
    return round(i,ndigits)
    
    
def fv_cdb(v0,i,dt,dyear=365,ndigits=2):
    v1=v0*(1+i)**(dt/dyear)
    return round(v1,ndigits)

def i_ltn(v0,dt,v1=1000,ndigits=2):
    # workdays
    i = (v1/v0)**(252/dt)-1
    return round(i,ndigits)

class ativo():
    
    def calcular(self):
        if self.v0 is None:
            self.v0 = self.v1/(1+self.ytm)**(self.t)
        
        elif self.v1 is None:
            self.v1 = self.v0*(1+self.ytm)**(self.t)
            
        elif self.t is None:
             self.t = log(self.v1/self.v0)/log(1+self.ytm)
                
        else:
            self.ytm = (self.v1/self.v0)**(1/self.t)-1
            
    def validar(self,
                ndigits=4):
        # essa funcao valida os parametros conforme v1=v0*(1+ytm)**t
        try:
            assert round(self.v0,ndigits) == round(self.v1/(1+self.ytm)**(self.t),ndigits)
            assert round(self.v1,ndigits) == round(self.v0*(1+self.ytm)**(self.t),ndigits)
            assert round(self.t,ndigits) == round(log(self.v1/self.v0)/log(1+self.ytm),ndigits)
            assert round(self.ytm,ndigits) == round((self.v1/self.v0)**(1/self.t)-1,ndigits)
        except:
            raise "Os parametros nao sao consistentes."
    
    def __init__(self,
                 v0=None,
                 v1=None,
                 ytm=None,
                 t=None,
                 nome=None,
                 i=None,
                 inome=None,
                 d=None):
        
        self.nome=nome
        
        assert [v0,v1,ytm,t].count(None)<=1
        self.v0=v0
        self.v1=v1
        self.ytm=ytm
        self.t=t
        
        if [v0,v1,ytm,t].count(None)==1:
            self.calcular()
        else:
            self.validar()
            
        #
        self.i=None
        self.inome=None
        self.d=d
        
    def __str__(self):
        text = f"nome: {self.nome}\nv0: {self.v0}\nv1: {self.v1}\nytm: {self.ytm}\nt: {self.t}"
        return text
    
class ltn(ativo):
    def __init__(self,v0=None,v1=1000,ytm=None,dias=None,t=None):
        
        self.nome="LTN - Letra do Tesouro Nacional"
        self.v1=v1
        
        assert [dias,t].count(None)==1, "Apenas dias ou t"
        if dias is not None:
            self.t=dias/252
        else:
            self.t=t
            
        self.v0=v0
        self.ytm=ytm
        if [v0,ytm].count(None)==0:
            self.validar()
        else:
            self.calcular()
        
def hpy():
    return True

if __name__ == "__main__":
    print("Hello, World!")
    assert simple(v0=1000,i=0.50,dt=1)==1500
    assert simple(v0=500000,i=0.12,dt=3)==680000
    assert continuous(v0=15000,i=0.015,dt=30)==23524.68
    assert continuous(v0=500000,i=0.05,dt=4)==610701.38
    assert npv_geometric(pmt=10,i=0.2,g=0.1)==100
    assert fv_cdb(v0=15000,i=.19,dyear=360,dt=37)==15270.59
    assert fv_cdb(v0=5000,i=.181,dyear=365,dt=32)==5073.46
    assert i_ltn(987.50,26,ndigits=4) == 0.1297
    assert i_ltn(v0=990.65,dt=26) == 0.0953
