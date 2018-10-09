from galpy.potential import MWPotential2014
from galpy.actionAngle import actionAngleAdiabatic
from galpy.df import quasiisothermaldf

if __name__ == '__main__':
    # mp = MiyamotoNagaiPotential(a=0.5, b=0.0375, normalize=.1)
    # p = mp.plotRotcurve(Rrange=[0.01,10.],grid=1001)
    # # fig = plt.figure()
    # # fig.lines.extend(p)
    # plt.show()
    aA= actionAngleAdiabatic(pot=MWPotential2014,c=True)
    qdf = quasiisothermaldf(1. / 3., 0.2, 0.1, 1., 1., pot=MWPotential2014, aA=aA, cutcounter=True)
