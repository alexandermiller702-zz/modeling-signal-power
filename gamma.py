from scipy.stats import gamma, kstest
from numpy import mean, std, linspace
import csv


def gam(Y, asq, N):
    x = linspace(1E-6, 10, 1000)

    mx = {'uni': {key: None for key in N}, 'lowV': {key: None for key in N},
          'highV': {key: None for key in N}, 'extreme': {key: None for key in N}}
    MOM = {'uni': {key: None for key in N}, 'lowV': {key: None for key in N},
           'highV': {key: None for key in N}, 'extreme': {key: None for key in N}}
    mat = {'uni': {key: None for key in N}, 'lowV': {key: None for key in N},
           'highV': {key: None for key in N}, 'extreme': {key: None for key in N}}

    with open('results.csv', 'wb') as wr:
        wr.write("dist,case,E[Y],sum(ASQ),Var(Y),MATks,MAT%,MLEks,MLE%,MOMks,MOM%\n")
        for dist in Y.keys():
            for case in Y[dist].keys():
                matparam = Moms(1, asq[dist][case])
                mat[dist][case] = gamma.pdf(x, matparam['alpha'], loc=0, scale=matparam['beta'])
                one = kstest(Y[dist][case], 'gamma', [matparam['alpha'], 0, matparam['beta']])

                mxparam = gamma.fit(Y[dist][case])
                mx[dist][case] = gamma.pdf(x, mxparam[0], loc=mxparam[1], scale=mxparam[2])
                two = kstest(Y[dist][case], 'gamma', [mxparam[0], mxparam[1], mxparam[2]])

                momparam = Moms(mean(Y[dist][case]), std(Y[dist][case])**2)
                MOM[dist][case] = gamma.pdf(x, momparam['alpha'], loc=0, scale=momparam['beta'])
                three = kstest(Y[dist][case], 'gamma', [momparam['alpha'], 0, momparam['beta']])

                wr.write(dist+","+str(case)+","+str(round(mean(Y[dist][case]), 4))+"," +
                                 str(round(asq[dist][case], 4))+","+str(round(std(Y[dist][case])**2, 4))+"," +
                                 str([round(one[0], 4), round(one[1], 4)])+"," +
                                 str([round(two[0], 4), round(two[1], 4)])+"," +
                                 str([round(three[0], 4), round(three[1], 4)])+"\n")

    return {'MOM': MOM, 'MLE': mx, 'MAT': mat}


def Moms(mu, var):
    # take mean and variance,
    # return alpha, beta
    a = mu ** 2 / var
    b = 1.0/(mu / var)
    return {'alpha': a, 'beta': b}

