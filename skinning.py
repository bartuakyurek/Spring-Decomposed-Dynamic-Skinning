#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

IMPORTANT NOTES:
- Q: are SMPL's rotations in degrees or in radians?


"""
import igl
import numpy as np
from scipy.spatial.transform import Rotation

from skeleton import Skeleton
from linalg_utils import get_rotation_mats, compose_transform_matrix

# ---------------------------------------------------------------------------------
# Helper routine to obtain posed mesh vertices
# ---------------------------------------------------------------------------------
def get_skel_points(skeleton, theta, trans, degrees, exclude_root, combine_points=True):
   
    bone_locations = skeleton.pose_bones(theta, trans, degrees=degrees, exclude_root=exclude_root)
    
    skel_mesh_points = bone_locations
    if combine_points:
        skel_mesh_points = np.reshape(bone_locations, (-1,3)) # Combine all the 3D points into one dimension
   
    return skel_mesh_points

def _get_mesh_points(mode):
    
    if mode == "Rigid":
        posed_mesh_points = None
    else:
        posed_mesh_points = None
        print("Warning: skinning not implemented yet...")
    return posed_mesh_points

def bind_weights(mesh_verts, skel_verts): 
    """
    Find the set of weights that will be the
    skinning weights for the provided mesh vertices. Usually this method
    is called at the T-pose, such that skinning function can take these 
    T-pose binding weights to map the mesh from T-pose to the desired 
    deformation. 

    Parameters
    ----------
    mesh_verts : np.ndarray
        Vertices of the mesh, has shape (n_verts, 3).
    skel_verts : np.ndarray
        Endpoint locations of the skeleton that has shape (n_bones * 2, 3).
        It's assumed every bone has 2 endpoints such that every consecutive
        [i][i+1] where i is an even number, represents a bone.
        
        Note that you need to convert SMPL joints to Skeleton class in your
        pipeline before using this method; otherwise the input data will not
        match with the implementation.

    Returns
    -------
    weights : np.ndarray.
        Binding weights has shape (n_verts, n_bones). Every row belongs to
        a vertex in the mesh, and every column is dedicated to the bones, 
        (be careful, bones not joints, those are used interchangibly in skeletal 
        animation but in this pipeline every bone has 2 joints). 
        
        Every entry w=(v, b) is the weight w that is bound to vertex v and bone b. 
        Meaning that vertex v, will inherit the transformation of bone b at
        w amount. Usually w is in range [0.0, 1.0] for smooth vertex blending.
        However setting it outside of this range is still theoretically possible.
    """
    assert type(mesh_verts) == np.ndarray
    assert type(skel_verts) == np.ndarray
    
    weights = None
    print(">> WARNING: Bind_weigths() is not implemented yet...")
    return weights


def LBS(V, W, abs_rot, abs_trans):
    assert W.shape[0] == V.shape[0], f"Expected weights and verts to have same length at dimension 0, i.e. weights has shape (n_verts, n_bones)\
                                                 and verts has shape (n_verts, 3), got shape {W.shape} and {V.shape}."
    n_verts, n_bones = W.shape
    assert abs_rot.shape == (n_bones, 4), f"Expected absolute rotations in quaternions to have shape ({n_bones}, 4), got {abs_rot.shape}."
    assert abs_trans.shape == (n_bones, 3), f"Expected absolute translations to have shape ({n_bones}, 3), got {abs_trans.shape}."

    V_posed = np.zeros_like(V)    
        
    Ms = []
    for bone in range(n_bones):
        rot = Rotation.from_quat(abs_rot[bone])
        M = compose_transform_matrix(abs_trans[bone], rot)
        Ms.append(M)
    
    for vertex in range(n_verts):
        v_homo = np.ones(4)
        v_homo[:3] = V[vertex]
        for bone in range(n_bones):
            transformed_vert = Ms[bone] @ v_homo # or np.matmul(v_homo, M.T) also works
            assert np.abs(Ms[bone][-1,-1] - 1.0) < 1e-12, f"Matrix has to have 1.0 at the last dimension, got matrix {Ms[bone]}."
            assert np.abs(v_homo[-1] - 1) < 1e-12, f"Homogeneous coordinates are expected to have 1.0 at the last dimension, got vector {v_homo}."
            #assert np.abs(transformed_vert[-1] - 1.0) < 1e-3, f"transformed_vert has to have 1.0 at the last dimension, got vector {transformed_vert}"
            V_posed[vertex] += W[vertex, bone] * transformed_vert[:3]
            
    # TODO: convert for loops into matrix multiplications
    #tmp = V @ R_mat (n_bones,n_verts,3)
    #tmp2 = W.T @ tmp (n_bones,n_bones,3)
    #tmp3 = tmp2 + abs_trans
        
    V_posed = np.array(V_posed)
    assert V_posed.shape == V.shape
    return V_posed
    

def skinning(verts, abs_rot, abs_trans, weights, skinning_type="LBS"):
    """
    Deform the vertices by provided transformations and selected skinning
    method.

    Parameters
    ----------
    verts : np.ndarray
        Vertices to be deformed by provided transformations.
    abs_rot : np.ndarray
        Absolute rotation transformation quaternions of shape (n_bones, 4)
    abs_trans : np.ndarray
        Absolute translation vec3 of shape (n_bones, 3)
    weights : np.ndarray
        Binding weights between vertices and bone transformation of shape
        (n_verts, n_bones). Note that to deform the skeleton, set weights of 
        shape (n_bones * 2, n_bones) with 1.0 weights for every couple rows.
        e.g. for a two bones it is 
                                    [[1.0, 0.0],
                                     [1.0, 0.0],
                                     [0.0, 1.0],
                                     [0.0, 1.0]] 
    skinning_type : str, optional
        DESCRIPTION. The default is "LBS".

    Returns
    -------
    V_deformed : np.ndarray
        Deformed vertices of shape (n_verts, 3)
    """
    
   
    if skinning_type == "LBS" or skinning_type == "lbs":
        # Deform vertices based on Linear Blend Skinning
        return LBS(V         = verts, 
                   W         = weights,
                   abs_rot   = abs_rot, 
                   abs_trans = abs_trans)
    else:
        raise ValueError(f">> ERROR: This skinning type \"{skinning_type}\" \
                         is not supported yet.")

"""
# todo:  taken https://github.com/Dou-Yiming/Pose_to_SMPL/blob/main/smplpytorch/pytorch/rodrigues_layer.py
def quat2mat(quat):
    Convert quaternion coefficients to rotation matrix.
    Args:
        quat: size = [batch_size, 4] 4 <===>(w, x, y, z)
    Returns:
        Rotation matrix corresponding to the quaternion -- size = [batch_size, 3, 3]
    
    norm_quat = quat
    norm_quat = norm_quat / norm_quat.norm(p=2, dim=1, keepdim=True)
    w, x, y, z = norm_quat[:, 0], norm_quat[:, 1], norm_quat[:,
                                                             2], norm_quat[:,
                                                                           3]

    batch_size = quat.size(0)

    w2, x2, y2, z2 = w.pow(2), x.pow(2), y.pow(2), z.pow(2)
    wx, wy, wz = w * x, w * y, w * z
    xy, xz, yz = x * y, x * z, y * z

    rotMat = torch.stack([
        w2 + x2 - y2 - z2, 2 * xy - 2 * wz, 2 * wy + 2 * xz, 2 * wz + 2 * xy,
        w2 - x2 + y2 - z2, 2 * yz - 2 * wx, 2 * xz - 2 * wy, 2 * wx + 2 * yz,
        w2 - x2 - y2 + z2
    ],
                         dim=1).view(batch_size, 3, 3)
    return rotMat
"""
"""
def batch_rodrigues(axisang):
    
    #axisang N x 3
    axisang_norm = torch.norm(axisang + 1e-8, p=2, dim=1)
    angle = torch.unsqueeze(axisang_norm, -1)
    axisang_normalized = torch.div(axisang, angle)
    angle = angle * 0.5
    v_cos = torch.cos(angle)
    v_sin = torch.sin(angle)
    quat = torch.cat([v_cos, v_sin * axisang_normalized], dim=1)
    rot_mat = quat2mat(quat)
    rot_mat = rot_mat.view(rot_mat.shape[0], 9)
    return rot_mat
"""
"""
def batch_axsang_to_quats(rot):
    assert rot.shape[1] == 3

    roll = rot[:, 0] / 2.
    pitch = rot[:, 1] / 2.
    yaw = rot[:, 2] / 2.
    
    if type(rot) == np.ndarray:
        sin = np.sin
        cos = np.cos
        stack = np.stack
    else: 
        sin = torch.sin
        cos = torch.cos
        stack = torch.stack
        
    qx = sin(roll) * cos(pitch) * cos(yaw)
    qy = cos(roll) * sin(pitch) * cos(yaw)
    qz = cos(roll) * cos(pitch) * sin(yaw)
    qw = cos(roll) * cos(pitch) * cos(yaw)
    
    return stack((qx, qy, qz, qw)).transpose()

def batch_axsang_to_quats2(axisang):
    # TODO: assert axisang is type torch array
   
    axisang_norm = torch.norm(axisang + 1e-8, p=2, dim=1)
    angle = torch.unsqueeze(axisang_norm, -1)
    axisang_normalized = torch.div(axisang, angle)
    angle = angle * 0.5
    v_cos = torch.cos(angle)
    v_sin = torch.sin(angle)
    quat = torch.cat([v_cos, v_sin * axisang_normalized], dim=1)
    
    return quat

def forward_kin(joint_pos, 
                joint_edges, 
                joint_parents, 
                relative_rot, # axis angle representation
                relative_trans=None):
    
    relative_rot_q = batch_axsang_to_quats(relative_rot)
    
    if relative_trans is None:
        relative_trans = np.zeros_like(relative_rot_q)[:,:3]
        
    absolute_rot, absolute_trans = igl.forward_kinematics(joint_pos, 
                                                          joint_edges, 
                                                          joint_parents, 
                                                          relative_rot_q,
                                                          relative_trans)
    
    return absolute_rot, absolute_trans
   """ 
"""
def LBS(V, W, J, JE, theta):

    P = igl.directed_edge_parents(JE)
    abs_rot, abs_t = forward_kin(J, JE, P, theta)
    
    R_mat = np.array(quat2mat(torch.from_numpy(abs_rot)))
    num_bones = abs_t.shape[0]
    
    V_posed = np.zeros_like(V)
    for vertex in range(V_posed.shape[0]):
        for bone in range(num_bones):
            if bone == 0:
                pass # TODO: decide your notation! use only joints or edges! SMPL uses joint notation... but idk.
            # tmp = W[vertex, bone] * np.matmul(V[vertex], R_mat[bone]) + abs_t[bone]
            # TODO: remove for loop!
            V_posed[vertex] += W[vertex, bone] * np.matmul(V[vertex], R_mat[bone]) + abs_t[bone]
            
    # TODO: where's the T you promised in return?...
    return V_posed

def inverse_LBS(V_posed, W, J, JE, theta):
    
    unposed_V = LBS(V_posed, W, J, JE, -theta)
    return unposed_V
"""
if __name__ == "__main__":
    print(">> Testing skinning.py...")
    
    """
    from smpl_torch_batch import SMPLModel
    from skeleton_data import get_smpl_skeleton

    training_data = torch.load('./data/50004_dataset.pt')
    data_loader = torch.utils.data.DataLoader(training_data, batch_size=1, shuffle=False)

    device = "cpu"
    smpl_model = SMPLModel(device=device, model_path='./body_models/smpl/female/model.pkl')
    kintree = get_smpl_skeleton()
    F = smpl_model.faces

    for data in data_loader:
       beta_pose_trans_seq = data[0].squeeze().type(torch.float64)
       betas, pose, trans = beta_pose_trans_seq[:,:10], beta_pose_trans_seq[:,10:82], beta_pose_trans_seq[:,82:] 
       target_verts = data[1].squeeze()
       smpl_verts, joints = smpl_model(betas, pose, trans)
       break
       
    V = smpl_verts.detach().cpu().numpy()
    J = joints.detach().cpu().numpy()
    n_frames, n_verts, n_dims = target_verts.shape
    """
    
    
    
