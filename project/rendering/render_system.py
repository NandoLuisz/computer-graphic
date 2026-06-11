from geometry.transform import scale, rotation, translate
from scene.camera import World_to_camera
from rendering.back_face_culling import back_face
from rendering.projection import perspective
from rendering.lighting import vertex_phong

import numpy as np


class RenderSystem:

    def __init__(self, rasterizer, width, height):
        self.rasterizer = rasterizer

        self.width = width
        self.height = height

    def render(self, scene):

        camera = scene.camera

        if len(scene.lights) == 0:
            return

        light = scene.lights[0]

        light_camera, _ = World_to_camera(
            np.array([light.position]),
            camera
        )

        light_camera = light_camera[0]

        for mesh in scene.meshes:

            self.render_mesh(
                mesh,
                camera,
                light_camera
            )

    def render_mesh(
        self,
        mesh,
        camera,
        light_camera
    ):

        transformed = self.transform_mesh(
            mesh
        )

        transformed, camera_rotation = self.to_camera_space(
            transformed,
            camera
        )

        normals = self.transform_normals(
            mesh,
            camera_rotation
        )

        visible_faces = self.compute_visibility(
            mesh,
            transformed
        )

        self.compute_lighting(
            visible_faces,
            transformed,
            normals,
            light_camera
        )

        projected = self.project_vertices(
            transformed
        )

        self.draw_mesh(
            projected,
            visible_faces
        )

    #objeto -> mundo
    def transform_mesh(self, mesh):

        transformed = scale(
            mesh.vertices,
            mesh.scale
        )

        transformed = rotation(
            transformed,
            mesh.rotation
        )

        transformed = translate(
            transformed,
            mesh.position
        )

        return transformed
    
    # mundo -> SSC
    def to_camera_space(
        self,
        vertices,
        camera
    ):

        return World_to_camera(
            vertices,
            camera
        )

    #transformações das normais
    def transform_normals(
    self,
    mesh,
    camera_rotation
    ):

        return (
            mesh.vertex_normals
            @ camera_rotation.T
        )
    
    def compute_visibility( self, mesh, transformed):

        return back_face(
            mesh.faces,
            transformed
        )
    
    def compute_lighting( self, faces, vertices, normals, light_position):

        for face in faces:

            i0, i1, i2 = face.vertices

            c0 = vertex_phong(
                vertices[i0],
                normals[i0],
                light_position,
                face.color
            )

            c1 = vertex_phong(
                vertices[i1],
                normals[i1],
                light_position,
                face.color
            )

            c2 = vertex_phong(
                vertices[i2],
                normals[i2],
                light_position,
                face.color
            )

            face.vertex_colors = [
                c0,
                c1,
                c2
            ]
    #projeção
    def project_vertices( self, vertices ):

        return perspective(
            vertices,
            self.width,
            self.height
        ) 

    def draw_mesh( self, projected, faces ):

        self.rasterizer.draw_faces(
        projected,
        faces
        )    