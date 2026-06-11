import pygame
import numpy as np

class Rasterizer:

    def __init__(self, screen):
        self.screen = screen

        #inicializando o buffer
        width = screen.get_width()
        height = screen.get_height()
        self.zbuffer = np.full((height, width), np.inf)
    
    def clear_zbuffer(self):
        self.zbuffer.fill(np.inf)

    def draw_faces(self, projected_vertices, faces):

        for face in faces:

            points = []

            for i in face.vertices:

                if projected_vertices[i] is None:
                    break

                points.append(projected_vertices[i])

            if len(points) != 3:
                continue

            p0, p1, p2 = points

            self.draw_triangle( p0, p1, p2, face )

    def draw_triangle(self, A, B, C, face):

        width = self.screen.get_width()
        height = self.screen.get_height()

        min_y = max( 0, int(min(A[1], B[1], C[1])))

        max_y = min( height - 1, int(max(A[1], B[1], C[1])) )

        denom = (
            (B[1]-C[1])*(A[0]-C[0])
            +
            (C[0]-B[0])*(A[1]-C[1])
        )

        if abs(denom) < 1e-6:
            return
        c0, c1, c2 = face.vertex_colors
        if len(face.vertex_colors) != 3:
            print(face.vertex_colors)
            print(c0, c1, c2)

        for y in range(min_y, max_y + 1):

            intersections = self.scanline_intersections( y, A, B, C )

            if len(intersections) < 2:
                continue

            intersections.sort()

            for i in range( 0, len(intersections)-1, 2 ):

                x_start = max( 0, int(intersections[i]) )

                x_end = min( width - 1, int(intersections[i+1]) )

                for x in range( x_start, x_end + 1 ):

                    a,b,c = self.barycentric(
                        x + 0.5,
                        y + 0.5,
                        A,
                        B,
                        C,
                        denom
                    )

                    z = (
                        a*A[2]
                        +
                        b*B[2]
                        +
                        c*C[2]
                    )

                    current_z = self.zbuffer[y, x]

                    if z < current_z:

                        self.zbuffer[y, x] = z

                        r = (
                            a*c0[0]
                            +
                            b*c1[0]
                            +
                            c*c2[0]
                        )

                        g = (
                            a*c0[1]
                            +
                            b*c1[1]
                            +
                            c*c2[1]
                        )

                        b_color = (
                            a*c0[2]
                            +
                            b*c1[2]
                            +
                            c*c2[2]
                        )

                        pixel_color = (
                            max(0, min(255, int(r))),
                            max(0, min(255, int(g))),
                            max(0, min(255, int(b_color)))
                        )

                        try:
                            self.screen.set_at(
                                (x,y),
                                pixel_color
                            )

                        except Exception as e:

                            print("ERRO DE COR")
                            print("pixel_color =", pixel_color)
                            print("c0 =", c0)
                            print("c1 =", c1)
                            print("c2 =", c2)
                            print("a,b,c =", a,b,c)

                            raise

    def scanline_intersections( self, y, A, B, C ):

        intersections = []

        edges = [
            (A,B),
            (B,C),
            (C,A)
        ]

        for P1, P2 in edges:

            y1 = P1[1]
            y2 = P2[1]

            if y1 == y2:
                continue

            if (
                min(y1,y2)
                <= y
                <
                max(y1,y2)
            ):

                t = (
                    (y - y1)
                    /
                    (y2 - y1)
                )

                x = (
                    P1[0]
                    +
                    t*(P2[0]-P1[0])
                )

                intersections.append(x)

        return intersections

    def barycentric( self, px, py, A, B, C, denom ):

        alpha = (
            (B[1]-C[1])*(px-C[0])
            +
            (C[0]-B[0])*(py-C[1])
        ) / denom

        beta = (
            (C[1]-A[1])*(px-C[0])
            +
            (A[0]-C[0])*(py-C[1])
        ) / denom

        gamma = (
            1
            -
            alpha
            -
            beta
        )

        return alpha,beta,gamma