"""
Created on Mon Oct 28 23:22:05 2019
@author: RK
Task2, Exercise3:
Define a function for computing the cross products of two arrays of vectors.
   1. The input arrays have the same length (same number of vectors).
   1. Prototype in pure Python (loop over the arrays).
   1. Make Numpy equivalent without loops.
"""
import random
import logging 
import numpy as np

#%% # logging 
# Create and configure the logging
LOG_FORMAT = "%(message)s"
logging.basicConfig(filename="logs_exercise3.log", level=logging.DEBUG, 
                    format=LOG_FORMAT, filemode="w")
logger = logging.getLogger()

#%%
# Generating two random arrays
def generate_two_random_arrays(num=5, start=-10, stop=10):
    """
    This function generates two random arrys in 3D, conaining the same number 
    of vectors. Each elements of the arrays is a random real number sampled
    from a uniform distribution in the range of start and stop points
    
    inputs: num => the number of vectors in each array
            [start, stop] => the interval we sample elements from uniformly.
    outputs: arr1 => the first generated array with the shape of num*3
             arr2 => the second generated array with the shape of num*3
    """
    arr1 = [[random.uniform(start,stop) for _ in range(3)] for _ in range(num)]
    arr2 = [[random.uniform(start,stop) for _ in range(3)] for _ in range(num)]
    return arr1, arr2

#%% Calculating the cross product of two arrays of vectors in pure Python 
# Define cross product of two vectors
def cross_product_of_two_vectors(a, b):    
    """
    This function calculates the cross product of two 3d vectors
    
    inputs: a => the first vector
            b => the second vector
    output: the cross product of the two input vectores
    """
    return list([a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]])

# Define cross product of two arrays of vectors in pure Python
def cross_product_of_two_arrays_python(arr1, arr2):
    """
    This function calculates the cross products of two arrays, which is the 
    cross products of every pair of vectors (Vi, Vj). Vis belongs to the 
    first array and Vjs belongs to the second array. Thus, here the cross 
    products of two arrays with the shape of num*3, is an array with the shape 
    of num^2 * 3.
    
    inputs: arr1 => the first generated array with the shape of num*3
            arr2 => the second generated array with the shape of num*3
    output: cross_products => the cross product of two arrays
    """
    cross_products = []
    for a in arr1:
        for b in arr2:
            cross_products.append(cross_product_of_two_vectors(a, b))
    return cross_products

#%% Calculating the cross product of two arrays of vector in numpy with for
def numpy_cross_product_of_two_arrays_with_for(arr1, arr2):
    """
    NumPy implementation of cross product uses broadcasting. So, using a for loop
    over the second array would be enough. 
    
    inputs: arr1 => the first generated array with the shape of num*3
            arr2 => the second generated array with the shape of num*3
    output: cross_prod_np_with_for => the cross product of two arrays using 
            numpy and a for loop
    """
    cross_prod_np_with_for = [np.cross(arr1, a2) for a2 in arr2]
    return cross_prod_np_with_for

#%% Calculating the cross product of two arrays of vector in numpy without for  
def numpy_cross_product_of_two_arrays_without_for(n):
    """    
    input: n => the number of vectors each array contains. We use this as the 
            recursion index
    * for simplicity, here we pass two arrays to this function as global variables
    output: cross_prod_np_without_for => the cross product of two arrays using 
            numpy without for loop using recursive function
    """
    global arr1, arr2, cross_prod_np_without_for
    if n == 0:
        return cross_prod_np_without_for
    else:
        cp = np.cross(arr1, arr2[n-1])
        cross_prod_np_without_for.append(cp)
        numpy_cross_product_of_two_arrays_without_for(n-1)

#%% Compare the results of three methods
def are_equal(cross_prod_py, cross_prod_np_with_for, cross_prod_np_without_for):
    """
    This function compares the cross products resulted from the three approches.
    
    inputs: cross_prod_py =>
            cross_prod_np_with_for =>
            cross_prod_np_without_for =>
    
    output: True (if the three cross products are equal) or False (otherwise)
    """
    # convert the inputs to numpy array
    Length = len(cross_prod_py)
    cross_prod_py_arr = np.array(cross_prod_py)
    cross_prod_np_with_for_arr = np.reshape(np.array(cross_prod_np_with_for), (Length,3))
    cross_prod_np_without_for_arr  = np.reshape(np.array(cross_prod_np_without_for), (Length,3))
    
    # sort the arrays to ease the comparision process
    cross_prod_py_arr_sort = np.sort(cross_prod_py_arr, axis=0)
    cross_prod_np_with_for_arr_sort = np.sort(cross_prod_np_with_for_arr, axis=0)
    cross_prod_np_without_for_arr_sort = np.sort(cross_prod_np_without_for_arr, axis=0)
    
    return np.equal(cross_prod_py_arr_sort, cross_prod_np_with_for_arr_sort, cross_prod_np_without_for_arr_sort).all()

#%% Run
if __name__ == '__main__':
    # generating two random arrays of vector
    arr1, arr2 = generate_two_random_arrays(num=5)
    MESSAGE = "\nThe randomly generated two arrays are: \narray1 = {0}, \n\narray2 = {1}"
    logger.info(MESSAGE.format(np.array(arr1), np.array(arr2)))
    # calculating cross product in pure python
    cross_prod_py = cross_product_of_two_arrays_python(arr1, arr2)
    # calculating cross product in numpy with for
    cross_prod_np_with_for = numpy_cross_product_of_two_arrays_with_for(arr1, arr2)
    # calculating cross product in numpy without for
    cross_prod_np_without_for = []
    numpy_cross_product_of_two_arrays_without_for(n=len(arr1))
    # compare the three results
    MESSAGE = "\nThe cross product of two arrays is equal to: \n{}"
    logger.info(MESSAGE.format(np.array(cross_prod_py)))
    print('Equality status is: ', are_equal(cross_prod_py, cross_prod_np_with_for, cross_prod_np_without_for))
    
