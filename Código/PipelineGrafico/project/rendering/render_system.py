from geometry.transform import scale, rotation, translate
from scene.camera import World_to_camera, camera_view
from rendering.back_face_culling import back_face
from rendering.projection import perspective
from rendering.lighting import vertex_phong


import numpy as np


class RenderSystem:

    def __init__(self, rasterizer, renderer, width, height):
        self.rasterizer = rasterizer
        self.renderer = renderer

        self.width = width
        self.height = height

        self.stats={
            "vertices": 0,
            "faces": 0,
            "visible_faces": 0 
        }

    def render(self, scene, USE_LIGHTING, RENDER_MODE, VIEW_MODE):

        self.stats["vertices"] = 0
        self.stats["faces"] = 0
        self.stats["visible_faces"] = 0

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
                light_camera,
                USE_LIGHTING, 
                RENDER_MODE,
                VIEW_MODE
            )

    def render_mesh(  self, mesh, camera, light_camera, USE_LIGHTING,  RENDER_MODE, VIEW_MODE):

        transformed = self.transform_mesh( mesh )

        transformed, camera_rotation = self.to_camera_space( transformed, camera)

        normals = self.transform_normals( mesh, camera_rotation )

        visible_faces = self.compute_visibility(mesh, transformed)
        

        self.stats["vertices"] += len(mesh.vertices)

        self.stats["faces"] += len(mesh.faces)

        self.stats["visible_faces"] += len(visible_faces)


        if RENDER_MODE == 'SOLID':  # SOLID, POINT, POLYGON, AUTO, 
            self.compute_lighting(
                visible_faces,
                transformed,
                normals,
                light_camera,
                USE_LIGHTING
            )

        if VIEW_MODE =='CAMERA':
            projected = self.camera_view(transformed)
        else:    
            projected = self.project_vertices( transformed )

        if RENDER_MODE == 'SOLID':
            self.draw_mesh( projected, visible_faces)

        elif RENDER_MODE == 'POLYGON':
            self.draw_polygon(projected, visible_faces)

        elif RENDER_MODE == 'POINT': 
            self.draw_point(projected, 2)

        elif RENDER_MODE == 'AUTO':
            self.draw_face(projected, mesh.faces )

        '''elif RENDER_MODE =='CAMERA_VIEW':'''
            
    
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
    def to_camera_space( self, vertices, camera):

        return World_to_camera(
            vertices,
            camera
        )

    #transformações das normais
    def transform_normals( self, mesh, camera_rotation):

        return (
            mesh.vertex_normals
            @ camera_rotation.T
        )
    
    def compute_visibility( self, mesh, transformed):

        return back_face(
            mesh.faces,
            transformed
        )
    
    def compute_lighting( self, faces,  vertices,  normals,  light_position, USE_LIGHTING):
        
        for face in faces:
            if USE_LIGHTING== True:
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

            else:
                c0 = face.color
                c1 = face.color
                c2 = face.color

            face.vertex_colors = [c0, c1, c2]
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

    def draw_point(self, projeted, radius):
        self.renderer.draw_point(projeted, radius)

    def draw_wareframe(self, projeted, edges):
        self.renderer.draw_wireframe(projeted, edges)
    
    def draw_polygon(self, projected_vertices, faces):
        self.renderer.draw_triangle_edges(projected_vertices, faces)

    def draw_face(self, project, faces):
        self.renderer.draw_faces(project, faces)
    
    def camera_view(self, vertices ):
        return camera_view(vertices, self.width, self.height)

    
    
    
