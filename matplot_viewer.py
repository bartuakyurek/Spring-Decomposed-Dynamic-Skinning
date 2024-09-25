#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 12:57:13 2024

@author: bartu
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from viewer import Viewer


class Matplot_Viewer(Viewer):
    def __init__(self):
        super().__init__()
        
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(projection='3d')
        
    def run(self):
        
        for node_key in self.nodes:
            node = self.nodes[node_key]
            verts = node.vertices
            faces = node.faces
            
            self.render_node(verts, faces)
        
        # TODO: update the same plot?
        # or save it and once the viewer is done, convert saved images to video (in main)
        plt.show()
        

    def render_node(self, verts, faces):
        mesh = Poly3DCollection(verts[faces], alpha=0.2)
        face_color = (141 / 255, 184 / 255, 226 / 255)
        edge_color = (50 / 255, 50 / 255, 50 / 255)
        mesh.set_edgecolor(edge_color)
        mesh.set_facecolor(face_color)
        self.ax.add_collection3d(mesh)
    
    
    
if __name__ == "__main__":
    print(f"INFO: Running tests for {__file__}")
    import numpy as np
    from scene_node import Mesh
    
    ### Manual Spring Data 
    P = np.array([
                    [0.5, 3.0, 0.5],
                    [2.0, 3.0, 0.0],
                    [1.0, 2.0, 1.0],
                    [1.0, 1.0, 0.0],
                    [0.0, 1.0, 0.0],
                ])
    S = np.array([
                    [0, 2],
                    [1, 2],
                    [2, 4],
                    [2, 3],
                    [3, 4]
                ])
       
    viewer = Matplot_Viewer()

    for i in range(10):
        mass_spring_sys_node = Mesh(P, S)
        viewer.add_scene_node(mass_spring_sys_node)
    viewer.run()