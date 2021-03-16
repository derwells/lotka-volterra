import numpy as np
import matplotlib.pyplot as plt
import os

e = 1e-6
x_center = 50
y_center = 40

def preyPred(x, y, K):
    '''
    Output of Predator-Prey differential equation

    Args:
        x   (float): x-coordinate
        y   (float): y-coordinate
        K   (float): Calculated K-value of differnetial equation
    '''

    return np.log(pow(y, 0.2)*pow(x, 0.5)) - 0.005*y - 0.01*x - K

def findK(x, y):
    '''
    Wrapper for finding K value.

    Args:
        x   (float): Initial x-coordinate
        y   (float): Initial y-coordinate
    '''

    return preyPred(x, y, 0)

def falsePosition(t0, t1, f):
    '''
    Regula-Falsi on function f over bounds t0, t1.

    Args:
        t0  (float): Starting x-coordinate bound 
        t1  (float): Ending x-coordinate bound 
        f   (function): Lambda function of bounded region

    Returns:
        t_next  (float): Estimated root below threshold epsilon (e)
    '''

    condition = True
    while condition:
        f_t0 = f(t0)
        f_t1 = f(t1)

        t_next = (t0*f_t1 - t1*f_t0) / (f_t1 - f_t0)
        f_t_next = f(t_next)
        
        if f_t0*f_t_next < 0:
            t1 = t_next
        else:
            t0 = t_next

        condition = abs(f_t_next) > e

    return(t_next)

def solveRegion(dom, ran, f):
    '''
    Performs Regula-falsi on specified range.

    Args:
        dom (list): Corresponding x-values of range (ran)
        ran (list): y-values to perform Regula-Falsi on

    Returns:
        (list) : Corresponding x-values with solved y-values
    '''

    dom_values, ran_values = [], []
    
    d = round(dom[0], 2)
    while d <= dom[1]:
        r = falsePosition(ran[0], ran[1], lambda t : f(d, t))

        if ran[0] <= r <= ran[1]:
            dom_values.append(d)
            ran_values.append(r)

        d = round(d + 1e-2, 2)

    return [dom_values, ran_values]

def getPlot(x, y, name):
    '''
    Function for plotting solved points

    Args:
        x       (list): All x-coordinates
        y       (list): All y-coordinates
        name    (string): Desired filename of plot
    '''

    plt.clf()
    plt.scatter(x, y, s = 0.25)
    plt.xlabel('Prey population')
    plt.ylabel('Predator population')
    plt.title('Predator (y) vs Prey (x)')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.draw()

    current_path = os.path.abspath('plots')

    plt.savefig(os.path.join(current_path, '{}.png'.format(name)))


def run(x0, y0):
    '''
    Starts Regula-falsi solution given initial values x0, y0.
    Begins by estimating boundaries.

    Args:
        x0  (float): Initial x-value
        y0  (float): Initial y-value

    Returns:
        (tuple): x-values with solved y-value on same index
    '''

    K = findK(x0, y0)
    print("K:", K)

    x_bound = lambda x : preyPred(x, y_center, K)
    x_min = falsePosition(1e-4, x_center, x_bound)
    x_max = falsePosition(x_center, pow(x0, 2), x_bound)
    print("x boundaries:", x_min, x_max)

    y_bound = lambda y : preyPred(x_center, y, K)
    y_min = falsePosition(1e-4, y_center, y_bound)
    y_max = falsePosition(y_center, pow(y0, 2), y_bound)
    print("y boundaries:", y_min, y_max)

    region_boundaries = [
        [[x_center, x_max], [y_center, y_max]],
        [[x_min, x_center], [y_center, y_max]],
        [[x_min, x_center], [y_min, y_center]],
        [[x_center, x_max], [y_min, y_center]]
    ]

    q = lambda d, r : preyPred(d, r, K)
    
    # Populate with known values
    x_values = [x_center, x_center, x_min, x_max]
    y_values = [y_min, y_max, y_center, y_center]

    i = 1
    for b in region_boundaries:
        x, y = solveRegion(b[0], b[1], q)
        x_values.extend(x)
        y_values.extend(y)

        # Get region plot
        getPlot(x, y, "x{}y{}-{}".format(x0, y0, i))
        i += 1

    # Get whole plot
    getPlot(x_values, y_values, "x{}y{}".format(x0, y0))

    return (x_values, y_values)

if __name__ == "__main__":
    if not os.path.exists('plots'):
        os.makedirs('plots')

    x, y = [], []

    init_values = [
        [20, 50],
        [20, 150],
        [200, 50],
    ]

    for x0, y0 in init_values:
        x_i, y_i = run(x0, y0)
        x.extend(x_i)
        y.extend(y_i)

    getPlot(x, y, 'combined-plot')
