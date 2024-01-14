FPS = 120

WIDTH, HEIGHT = 500, 500

vert_shader = '''
#version 330 core

in vec2 vert;
in vec2 texcoord;
out vec2 uvs;

void main() {
    gl_Position = vec4(vert, 0.0, 1.0); 
    uvs = texcoord;                             
    }
'''




