from pylab import plot, clf, hist, savefig, title, figure
from numpy import linspace


def show(Y, gammas):
    # take MOM, MLE curves
    x = linspace(1E-6, 10, 1000)
    for dist in Y.keys():
        for case in Y[dist].keys():
            clf()
            t = dist+str(case)+".png"
            title(dist+" dist, "+str(case)+" antennas.")
            plot(x, gammas['MOM'][dist][case], 'r-', x, gammas['MLE'][dist][case], 'b-', x, gammas['MAT'][dist][case], 'g-')
            hist(Y[dist][case],normed=1,alpha=.3)
            savefig(t, bbox_inches='tight')
    # show and save