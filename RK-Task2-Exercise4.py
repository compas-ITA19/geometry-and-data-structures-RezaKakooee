"""
Created on Wed Oct 30 17:23:52 2019
@author: RK
Task2: Ecercise4
Using 'faces.obj'
   1. Define a function for traversing the mesh from boundary to boundary in a "straight" line.
   1. Visualise the result.

"""
#%% 
import random
#import time
import logging 
import numpy as np
import compas as cp
from compas.datastructures import Mesh
from compas_plotters import MeshPlotter

#%% # logging 
# Create and configure the logging
LOG_FORMAT = "%(message)s"
logging.basicConfig(filename="logs_exercise4.log", level=logging.DEBUG, 
                    format=LOG_FORMAT, filemode="w")
logger = logging.getLogger()

#%% get the mesh info
def get_mesh_info(object_dir='faces.obj'):
    """
    This function generates a mesh for an input object
    
    input: object_dir => the input object direction
    output: mesh_info_dict => all the detalies about the generated mesh inclding
            mesh instance, the vertices, vectecies on the boundary, and 
            non-boundary vertices
    """
    # create the mesh from .obj file
    mesh = Mesh.from_obj(cp.get(object_dir))
    # get all vertices of the mesh
    all_vertices = list(mesh.vertices())
    # get vertices on the boundary of the mesh
    on_boundry_vertices = list(mesh.vertices_on_boundary())
    # get vertices which are not on the boundary of the mesh
    non_on_boundry_vertices = list(set(all_vertices) - set(on_boundry_vertices))
    mesh_info_dict = {'mesh': mesh,
                      'all_vertices': all_vertices,
                      'on_boundry_vertices': on_boundry_vertices,
                      'non_on_boundry_vertices': non_on_boundry_vertices}
    return mesh_info_dict

#%% initial vertex
def get_current_vertex_info(mesh, current_vertex=3, previous_vertex=3):
    """
    This function identify the current vertex detailes
    
    input: mesh => the mesh of interest
           current_vertex => the curretn vertex (integer)
           previous_vertex => the previous vertex (integer)
    output: current_vertex_info_dict => all the detalies about the current vertex
            inclding the current vertex, previous vertex, vertices in the 
            neighborhood of the current vertex, neighborhood vertices which are 
            on the boundary, and neighborhood vertices which are not on the boundary
    """
    # find the neighborhood vertices of the start vectex
    neighbs_vertices = mesh.vertex_neighborhood(current_vertex)
    # find non-on-boundry neighborhood vertices
    non_on_boundry_neighbs_vertices = []
    for nbr in neighbs_vertices:
        if not mesh.is_vertex_on_boundary(nbr):
            non_on_boundry_neighbs_vertices.append(nbr)
    on_boundry_neighbs_vertices = list(set(neighbs_vertices)-set(non_on_boundry_neighbs_vertices))
    current_vertex_info_dict = {'current_vertex': current_vertex,
                                'previous_vertex': previous_vertex,
                                'neighbs_vertices': list(neighbs_vertices),
                                'on_boundry_neighbs_vertices': on_boundry_neighbs_vertices,
                                'non_on_boundry_neighbs_vertices': non_on_boundry_neighbs_vertices}
    return current_vertex_info_dict

#%% get the next vertex
def get_next_vertex(mesh_info_dict, current_vertex_info_dict):
    """
    This function identify the next vertex based on the current vertex, and the 
    neighborhood vertices. It outputs the vertex which belongs to the 
    neighborhood vertices and is not either the previous vertex nor on the sides 
    of the current vertex
    
    input: mesh_info_dict => all the detalies about the generated mesh 
           current_vertex_info_dict => all the detalies about the current vertex
           
    output: next_vertex => the next vertex which is on the stright line
    """
    previous_vertex = current_vertex_info_dict['previous_vertex']
    neighbs_vertices = current_vertex_info_dict['neighbs_vertices']
    if previous_vertex in neighbs_vertices: neighbs_vertices.remove(previous_vertex)
    # finding the next vertices on the stright line
    next_vertex = max(neighbs_vertices)
    return next_vertex
    
#%% plot mesh with all importnat detailes
def plot_mesh(mesh_info_dict, current_vertex_info_dict, edges_flag=1, faces_flag=1):
    """
    This function plot the mesh and the path dynamically. But the problem is that
    it seems that plotter.close() have not been defined in the current version
    of the COMPAS (0.10.0)
    """
    mesh = mesh_info_dict['mesh']
    # define the facecolor dictionaries for vertices
    facecolor={}
    # facecolor for all on-baoundary vertices
    facecolor.update({key: (200,200,200) for key in mesh_info_dict['non_on_boundry_vertices']})
    # facecolor for all non-on-baoundary  vertices
    facecolor.update({key: (150,150,150) for key in mesh_info_dict['on_boundry_vertices']})
    # facecolor for all on-baoundary neighborhood vertices
    facecolor.update({key: (0,255,0)     for key in current_vertex_info_dict['non_on_boundry_neighbs_vertices']})
    # facecolor for all non-on-baoundary neighborhood vertices
    facecolor.update({key: (0,0,255)     for key in current_vertex_info_dict['on_boundry_neighbs_vertices']})
    # facecolor for the current vertes
    facecolor.update({current_vertex_info_dict['current_vertex']: (255,0, 0)})
    # define important vertices
    keys = mesh_info_dict['all_vertices'] 
    
    # instantiate the MeshPlotter
    plotter = MeshPlotter(mesh=mesh, figsie=(4,4))
    # draw vertices
    plotter.draw_vertices(radius=0.3, text='key', 
                          keys=keys,
                          facecolor=facecolor)
    # draw edges
    if edges_flag==1: plotter.draw_edges()
    # draw faces
    if faces_flag==1: plotter.draw_faces()
    # show mesh plot
    plotter.show()
#    time.sleep(2)
#    plotter.close() # there is not such a method like matplotlib in COMPAS

#%% Run
if __name__ == "__main__":
    # set the object directory
    object_dir = 'faces.obj'
    # get the mesh info
    mesh_info_dict = get_mesh_info(object_dir=object_dir)
    mesh = mesh_info_dict['mesh']
    # select a non-corner vertex among vertices on the bottom boundary
    initial_state = random.randint(1,4)
    current_vertex = initial_state 
    path = [current_vertex]
    while True:
        # get the current vertex info
        current_vertex_info_dict = get_current_vertex_info(mesh_info_dict['mesh'], current_vertex=current_vertex)
        # get the mesh inf
        next_vertex = get_next_vertex(mesh_info_dict, current_vertex_info_dict)
        # update the stright path from the initial vertex to here
        path.append(next_vertex)
        # check if the next vertex is on the boundary or not
        if mesh.is_vertex_on_boundary(next_vertex):
            break
        # update the current and previous vertex
        current_vertex, previous_vertex = next_vertex, current_vertex
    
    MESSAGE = "\nThe stright path from the start vertex {} to the end vertex {} is {}"
    logger.info(MESSAGE.format(initial_state, next_vertex, path))
    
    # plot the path
    plotter = MeshPlotter(mesh, figsize=(4, 4))
    plotter.draw_vertices(radius=0.4, text='key', keys=path, facecolor=(255, 0, 0))
    plotter.draw_edges()
    plotter.draw_faces()
    plotter.show()
    
    # plot the entire mesh with all important vertices
    # plot_mesh(mesh_info_dict, current_vertex_info_dict) # please read the function definition
    
    
    
    


