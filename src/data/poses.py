#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 10:02:36 2024

@author: bartu
"""
import numpy as np

igl_arm_pose = np.array([
                [  # Keyframe 0 
                 [0.,0.,0.],
                 [0.,0.,0.],
                 [0., 0., 0.],
                 [0.,0.,0.],
                 [0.,0.,0.],
                 [0.,0.,0.],
                 [0.,0.,0.],
                 [0.,0.,0.],
                ],
                [  # Keyframe 1
                 [0.,0.,0.],
                 [0.,0.,0.],
                 [0., 10., 40.],
                 [0.,0.,0.],
                 [0.,0.,0.],
                 [0.,0.,0.],
                 [0.,0.,0.],
                 [0.,0.,0.],
                ],
                [  # Keyframe 2
                 [0.,0.,0.],
                 [0.,0.,0.],
                 [0., 0., 0.],
                 [0.,0.,0.],
                 [0.,0.,0.],
                 [0.,0.,0.],
                 [0.,0.,0.],
                 [0.,0.,0.],
                ],
                ])

# WARNING: I added extra  [0.,0.,0.], for the root bone
# that is actually global rotation, so once we resolve this issue
# the pose data should have 24 bones for monstera plant, instead of 25. 
monstera_rig_pose = np.array([
                            [ # Keyframe 0 
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.]
                            ],
                            [ # Keyframe 1 
                             [0.,0.,0.],
                             [40, 0., 0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.]
                            ],
                            [ # Keyframe 2 
                             [0.,0.,0.],
                             [-40.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.]
                            ],
                            [ # Keyframe 3
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.],
                             [0.,0.,0.]
                            ],
                            ])