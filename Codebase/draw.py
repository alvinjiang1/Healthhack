import io
from PIL import Image, ImageDraw, ImageFont
from google.cloud import vision

def draw_vertices(image_source, vertices, colour="green"):
    with Image.open(image_source) as pillow_img:                           
        draw = ImageDraw.Draw(pillow_img)
        for vertex in vertices:                        
            for i in range(len(vertex) - 1):
                x, y = vertex[i].x, vertex[i].y
                next_x, next_y = vertex[i + 1].x, vertex[i + 1].y
                draw.line(((x, y), (next_x, next_y)), fill=colour, width=3)
            n = len(vertex)
            draw.line(((vertex[n-1].x, vertex[n-1].y), (vertex[0].x, vertex[0].y)), fill=colour, width=3)

    return pillow_img
    
    
