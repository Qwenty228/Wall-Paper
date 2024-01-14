from data.base import BaseAnim

class Anim(BaseAnim):
    mode = 'clear'
    frag_shader = '''
#version 330 core

uniform float time;
uniform float aspect_ratio;
uniform sampler2D tex;  // same for every process running in parallel
                        // sampler2D is a 2D texture
in vec2 uvs;            // comes from quad buffer
out vec4 f_color;

vec3 pallete(float t) {
    vec3 a = vec3(0.500, 0.328, 0.500);
    vec3 b = vec3(-0.802, 0.260, 0.908);
    vec3 c = vec3(1.018, 0.177, 1.321);
    vec3 d = vec3(1.506, 5.597, 0.671);
    return a + b*cos(6.28318*(c*t + d));
}

void main(){
    vec3 finalColor = texture(tex, uvs).rgb;  // base pygame texture color(black)
    vec2 uv = uvs*2 - 1; // normalize uvs
    uv.x *= aspect_ratio;
    vec2 uv0 = uv;
    
    for (float i = 0.0; i< 3.; i++){
        uv = fract(uv *1.5) -0.5;

        float d = length(uv) * exp(-length(uv0));
        vec3 col = pallete(length(uv0) + (time + i)*0.4);

        d = sin(d*8. + time)/8.;
        d = abs(d);

        d = 0.005/d;

        finalColor += col * d;
    }

    f_color = vec4(finalColor, 1.0); // sample texture, uvs use color from the texture to asign to the fragment
}
'''

    def set_uniforms(self, program, **kwargs):
        program['time'] = kwargs['time']
        program['aspect_ratio'] = kwargs['aspect_ratio']