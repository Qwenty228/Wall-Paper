from utils.renderer import Renderer
from data.template.box import Anim




if __name__ == "__main__":
    try:
        r = Renderer(debug=False, animation=Anim())
        r.animate()
    except Exception as e:
        print(e)
    finally:
        r.wm.kill_workerw()
        quit()