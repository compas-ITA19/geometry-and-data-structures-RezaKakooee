"""
Created on Sun Oct 27 19:13:32 2019
@author: Reza Kakooee, kakooee@arch.ethz.ch for ITA19
Task2, Exercise1: 
Use the cross product to compute the area of a convex, 2D polygon
"""
#%% # Import dependencies
import numpy as np
import logging 
import matplotlib.pyplot as plt

#%% # logging 
# Create and configure the logging
LOG_FORMAT = "%(message)s"
logging.basicConfig(filename="logs_exercise2.log", level=logging.DEBUG, 
                    format=LOG_FORMAT, filemode="w")
logger = logging.getLogger()
    
# Making a random convex 2D polygon
def get_some_2d_cordinates(num_vertices=4, radius=5):
    """ 
    Here fisrt we generate some random theta in polar cordinates to be sure
    that the vertices shape a CONVEX polygon, then we convert them to cartesian
    
    inputs: num_vertices => number of vertices of the polygon
            rradius => the radius of the circle on which the polygon vertices lie
    outpus: vertices => (x,y) cordinates of the polygon's vertices        
    """
    # generating random angles 
    thetas = [np.random.uniform(0, 2*np.pi) for _ in range(num_vertices)]
    # sort the angles
    thetas = np.sort(thetas)
    # converting the polar cordinates to cartesian
    X, Y = [radius*np.cos(t) for t in thetas], [radius*np.sin(t) for t in thetas]
    # tha vertices of the polygon are:
    vertices = np.array([[x,y] for x,y in zip(X,Y)])
    return vertices

# Finding a point inside the polyogn
def get_a_point_inside_polygon(vertices):
    """
    This function findes a point inside the polygon. It can be any arbitrary 
    point inside the polygon but here we get approximately the center of the polygon.
    We define the approximate center of the polygon as the mean of its 
    vertices' cordinates. This approximate center is always inside the polygon,
    because we assumed that the polygon is convex.
    
    inputs: vertices => the polygon vertices cordinates
    outputs: approximate_center => (x, y) coordinats of the approximate center of the polygon
    """
#    # get two non-consecutive vertices
#    x0, y0 = vertices[0]
#    x2, y2 = vertices[2]
#    m = (y2-y0)/(x2-x0)
#    f = lambda x: m*(x-x0) + y0
#    xc = np.mean([x0,x2])
#    yc = f(xc)
    # calculating the sudo-center of polygon _APPROXIMATELY_
    xc, yc = np.mean(vertices[:,0], axis=0), np.mean(vertices[:,1], axis=0)
    approximate_center = (xc, yc)
    return approximate_center

# calculating vectors from the approximate center to all vertices
def vectors_from_center_to_vertices(approximate_center, vertices):
    """ 
    We need these vectors, because the area of the polygon is the sum of the 
    ares of triagnulars constructed by the center and all vertices
    
    inputs: approximate_center => (x,y) coordinats of the approximate center of the polygon
            vertices => the polygon vertices cordinates
    output: internal_vectors => all vectors from the center to vertices
    
    """
    xc, yc = approximate_center[0], approximate_center[1]
    internal_vectors = [[x-xc, y-yc] for x,y in vertices]
    return internal_vectors

def cross_product(a, b):    
    """
    This function calculates the cross product of two 2d vectors
    
    inputs: a => the first vector
            b => the second vector
    output: the cross product of the two input vectores
    """
    return a[0]*b[1]-a[1]*b[0]

# plotting the polygon, and all internal vectors
def plotting_polygon(approximate_center, num_vertices, vertices, internal_vectors):
    X, Y = list(vertices[:,0]), list(vertices[:,1])
    xc, yc = approximate_center[0], approximate_center[1]
    X.append(X[0])
    Y.append(Y[0])
    fig, ax = plt.subplots()
    ax.plot(X, Y)
    ax.plot([0],[0],'ob')
    ax.plot([xc],[yc],'or')
    for i in range(num_vertices):
        ax.arrow(xc, yc, internal_vectors[i][0], internal_vectors[i][1])
    plt.show()

# calculating the polygon area
def calculating_polygon_area(num_vertices, internal_vectors):
    """
    We already splited the polygon to triangulars. Now, the area of the polygon
    is the sum of the all triangulars' area. A triangular area is equal to the 
    half of the cross products of it's two edges.
    
    inputs: num_vertices => number of vertices of the polygon
            internal_vectors => all vectors from the center to vertices
    output: polygon_area => the polygon's area
    """
    internal_vectors.append(internal_vectors[0])
    triangles_area = []
    # calculating each triangular's area by a for loop
    for i in range(num_vertices):
        triangles_area.append(0.5*np.abs(cross_product(internal_vectors[i],internal_vectors[i+1])))
    polygon_area = np.sum(triangles_area)
    return polygon_area

#%% Run
if __name__ == '__main__':
    # set the number of vertices arbitrary
    num_vertices = 10
    # generate vertices for a convex polygon
    vertices = get_some_2d_cordinates(num_vertices=num_vertices)
    MESSAGE = "\nRandom generated vertices are: \nvertices = {}"
    logger.info(MESSAGE.format(vertices))
    # find the approximate center of the polygon
    approximate_center = get_a_point_inside_polygon(vertices)
    MESSAGE = "\nThe approximate center of the convex polygon is: \napproximate_center = [{0:2.5f}, {0:2.5f}]"
    logger.info(MESSAGE.format(approximate_center[0], approximate_center[1]))
    # calculating the internal vectors from center to vertices
    internal_vectors = vectors_from_center_to_vertices(approximate_center, vertices)
    # plotting the polygon and internal vectors
    plotting_polygon(approximate_center, num_vertices, vertices, internal_vectors)
    # calculating the polygon's area
    polygon_area = calculating_polygon_area(num_vertices, internal_vectors)
    MESSAGE = "\nThe polygon area is: \npolygon_area = {0:2.5f}"
    logger.info(MESSAGE.format(polygon_area))
    print("The polygon area is: ", polygon_area)
