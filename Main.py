from random import expovariate, seed
from numpy import std
from gamma import gam
from visualise import show


# Main file for project

# Run Project modules
#   Subordinates:
#       simulate
#       Gamma test
#       Visualise


def main():
    # Generate a, N values
    # N cases
    N = {2: 2, 6: 6, 30: 30, 1000: 1000}
    # testA(N)
    test = simulate(N, 10000)
    r = results(test[0], test[1], N)
    # r = {vy, asq}
    # test gamma distribution using sim data
    #   Cases:
    #       MOM,
    #       MLE,
    #       MAT
    gammas = gam(test[0], r['asq'], N)

    show(test[0], gammas)
    return


def aVal(N):
    # produce a values for distribution of a.
    # sum(a) = 1.

    # return 3D "matrix" Rows = 4 cases, cols = len(N), depth = len(N[i])
    # cases:
    #   1 = uniform
    #   2 = low decay
    #   3 = high decay
    #   4 = extreme decay

    uni = {key: [] for key in N.keys()}
    lowV = {key: [] for key in N.keys()}
    highV = {key: [] for key in N.keys()}
    extreme = {key: [] for key in N.keys()}

    for case in uni.keys():
        for antenna in range(N[case]):
            uni[case].append(1 / (N[case] * 1.0))
            if antenna == 0:
                lowV[case].append(1.0)
                highV[case].append(1.0)
                extreme[case].append(1.0)
            else:
                lowV[case].append(lowV[case][antenna - 1] * 0.95)
                highV[case].append(highV[case][antenna - 1] * 0.65)
                extreme[case].append(extreme[case][antenna - 1] * 0.2)

    # normalise, sum(vals) == 1
    for case in uni.keys():
        alv = sum(lowV[case])
        ahv = sum(highV[case])
        EX = sum(extreme[case])
        for antenna in range(N[case]):
            lowV[case][antenna] = lowV[case][antenna] / alv
            highV[case][antenna] = highV[case][antenna] / ahv
            extreme[case][antenna] = extreme[case][antenna] / EX

    # a = the different values of a
    # each a:
    #   r cases = len(N)
    #   c antenna = len(N[i])
    return {'uni': uni, 'lowV': lowV, 'highV': highV, 'extreme': extreme}


def results(simY, a, N):
    vy = {'uni': {key: None for key in N}, 'lowV': {key: None for key in N},
          'highV': {key: None for key in N}, 'extreme': {key: None for key in N}}

    asq = {'uni': {key: None for key in N}, 'lowV': {key: None for key in N},
          'highV': {key: None for key in N}, 'extreme': {key: None for key in N}}

    # for each distribution of A.
    for dist in simY.keys():
        # for each num of antenna, N
        for case in simY[dist].keys():
            vy[dist][case] = std(simY[dist][case])
            asq[dist][case] = sum(map((lambda x: x * x), a[dist][case]))

    return {'vy': vy, 'asq': asq}


def simulate(N, simRuns):
    # simulate 1000 Y values
    # collect and return expectations, variances. E[Y], V[Y].
    # collect the a and y values and make inferences about the impact of a

    y = {'uni': {key: [] for key in N}, 'lowV': {key: [] for key in N},
         'highV': {key: [] for key in N}, 'extreme': {key: [] for key in N}}

    a = aVal(N)
    # for each simulation run
    for sim in range(simRuns):
        # for each distribution of A.
        seed(sim*2)
        for dist in y.keys():
            # for each num of antenna, N
            for case in y[dist].keys():
                temp = []
                for antenna in range(N[case]):
                    # make a random y value
                    temp.append(expovariate(1.0) * 1.0 * a[dist][case][antenna])
                y[dist][case].append(sum(temp))

    return [y, a]


def testA(N):
    # maybe test what happens for each A
    a = aVal(N)
    print "N: " + str(N)
    stee = []
    j = 0
    for dist in a.keys():

        stee.append([])
        s = dist + "\n"
        for case in a[dist].keys():
            # p.clf()
            # p.hist(a[dist][i])
            s = s + str(case) + "\n"
            # p.savefig(dist+str(i)+".png")
            s = s + str(a[dist][case]) + "\nsum: " + str(sum((a[dist][case]))) + "\nsum[A^2] = " + str(
                sum(map((lambda x: x * x), a[dist][case]))) + "\n" + "\n"

        print s
        j += 1


if __name__ == '__main__':
    print "hold up"
    main()
    #testA({2: 2, 6: 6, 10: 10})
