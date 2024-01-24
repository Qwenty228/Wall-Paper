FPS = 60

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

VID_FILE_TYPES = [".webm", ".mkv", '.flv', '.vob', 
                    '.ogg', '.ogv', '.drc', '.gif',
                    '.gifv', '.mng', '.avi', '.MTS',
                    '.M2TS', ".TS", '.mov', '.qt',
                    '.yuv', '.rm', '.rmvb', '.viv',
                    '.asf', '.amv', '.mp4', '.m4v',
                    '.mpg', '.mp2', '.mpeg', '.mpe',
                    '.mpv', '.m2v', '.svi', '.3gp',
                    '.3g2', '.mxf', '.roq', '.nsv',
                    '.f4v', '.f4p', '.f4a', '.f4b']



