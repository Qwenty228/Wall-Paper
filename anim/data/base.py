
class BaseAnim:
    """Base class for animations"""
    mode = 'image'
    frag_shader = '''
#version 330 core
uniform sampler2D tex;

in vec2 uvs;            // comes from quad buffer
out vec4 f_color;

void main(){
    f_color = vec4(texture(tex, uvs).rgb, 1.0); // sample texture, uvs use color from the texture to asign to the fragment
}
'''
    def __init__(self, **kwargs):
        """Initialization of the animation
        kwargs: dict of arguments
        """
        pass

    def update(self, **kwargs):
        """Updating pygame render surface
        could be used for pygame simulation,
        or video extraction rendering
        kwargs: dict of arguments
        """
        pass


    def set_uniforms(self, program, **kwargs):
        """Set the uniforms for the shader program, shader rendering
        program: moderngl program
        kwargs: dict of uniforms
        """

        pass