"""
Created on Tue Oct 27 18:03:15 2019
@author: Reza Kakooee, kakooee@arch.ethz.ch
Task2, Exercise1: 
Given two vectors, use the cross product to create a set of three orthonormal vectors.
"""
#%% # Import dependencies
import random
import logging 
import numpy as np

#%% # logging 
# Create and configure the logging
LOG_FORMAT = "%(message)s"
logging.basicConfig(filename="logs_exercise1.log", level=logging.DEBUG, 
                    format=LOG_FORMAT, filemode="w")
logger = logging.getLogger()

#%% Generating two random 3d vectors which are independent to each other
def get_two_vectors(dim=3, start=-10, stop=10):
    """
    This function generates random vector which are linearly independent
    
    inputs: DIM => a scalar showing the dimention of the working space
            INTERVAL => the interval in which we want to generate the vectors' element
    output: two random linear independent vectors
    """
    # Generating two random vector in the DIM dimention and in the interval of [-INTERVAL, INTERVAL]
    v1 = [random.uniform(start, stop) for i in range(dim)]
    v2 = [random.uniform(start, stop) for i in range(dim)]
    # Checking the liner independency of the two vectors
    rank = np.linalg.matrix_rank(np.array([v1, v2]))
    # Generate two vectors again in the case the pervious vectors are linrearly dependent
    if rank < 2:
        get_two_vectors()
    return v1, v2

# Define cross product of two vectors
def cross_product(a, b):    
    """
    This function calculates the cross product of two 3d vectors
    
    inputs: a => the first vector
            b => the second vector
    output: the cross product of the two input vectores
    """
    return list([a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]])

# Define projection of vector vj on vector ui
def projection(vj, ui):
    """
    This function calculates the projection of a vector of another vector
    
    inputs: vj => the vector we want to project to the second vector
            ui => the vector we want to project the first vector on it
    output: the projected vector vj on ui
    """
    return np.multiply(np.dot(vj,ui)/np.dot(ui,ui), ui)

# Define vector normalization with norm-2
def normalize(u):
    """
    This function normalizes a vector. The normal vector has the magnitude 1
    
    inputs: u => the vector we want to normalize
    output: the normalized vector
    """
    return np.divide(u, np.sqrt(np.dot(u,u)))

# A simple Gram-Schmidt algorithm for 3d space
# Gram-Schmidt algorithm is an algorith which outputs n orthonormal vectors 
# for enery n linear independent input vectors. here we develope the algorithm 
# for just 3d space
def Gram_Schmidt(v1, v2, v3):
    """
    Given a set of linearly independent vectors, this function converts them
    into an orthonormal set of vectors.
    
    inputs: the set os vectors we want to orthonormalize
    output: orthonormalized set of vectors
    """
    u1 = v1
    u2 = v2 - projection(v2, u1)
    u3 = v3 - projection(v3, u1) - projection(v3, u2)
    return normalize(u1), normalize(u2), normalize(u3)

# Test if the algorithm orthogonolize the input vectors corectly
def is_orthogonal(e1, e2, e3):
    flag_orth = np.dot(e1,e2) + np.dot(e1,e3) + np.dot(e2,e3)
    return True if np.abs(flag_orth)<=0.000001 else False # np.finfo(float).eps

# Test if the algorithm normalize the input vectors corectly
def is_normal(e1, e2, e3):
    flag_norm = np.dot(e1,e1) + np.dot(e2,e2) + np.dot(e3,e3)
    return True if np.abs(flag_norm-3)<=0.000001 else False

#%% Run
if __name__ == '__main__':
    # Generate two randomly 3d vectors which are linearly independent
    v1, v2 = get_two_vectors()
    MESSAGE = "\nThe main two vectors are: \nv1 = [{0:5.2f}, {1:2.5f}, {2:2.5f}], \nv2 = [{3:2.5f}, {4:2.5f}, {5:2.5f}]"
    logger.info(MESSAGE.format(v1[0], v1[1], v1[2], v2[0], v2[1], v2[2]))
    # Using corss product for generating the third vector
    v3 = cross_product(v1, v2)
    MESSAGE = "\nThe third vector perpendicular on the plain passing from the main two vectors is: \nv3 = [{0:5.2f}, {1:5.2f}, {2:5.2f}]"
    logger.info(MESSAGE.format(v3[0], v3[1], v3[2]))
    # Using Gram-Schmidt algorithm for orthonormalizing the three vectores
    e1, e2, e3 = Gram_Schmidt(v1, v2, v3)
    MESSAGE = "\nThe resulted three orthonormalvectors are: \ne1 = [{0:5.2f}, {1:5.2f}, {2:5.2f}], \ne2 = [{3:5.2f}, {4:5.2f}, {5:5.2f}], \ne3 = [{3:5.2f}, {4:5.2f}, {5:5.2f}]"
    logger.info(MESSAGE.format(e1[0], e1[1], e1[2], e2[0], e2[1], e2[2], e3[0], e3[1], e3[2]))
    
    # Test if the algorithm works correctly or not
    print("Check orthogonal: ", is_orthogonal(e1, e2, e3))
    print("Check normal: ", is_normal(e1, e2, e3))
    print("Check orthonormal: ", is_orthogonal(e1, e2, e3) and is_normal(e1, e2, e3))