# import threading

import traceback

# from utils.gui import App
from utils.renderer import Renderer
from data.shaders.circular import Anim
# from data.template.doomfire import Anim
# from data.videos.videos import Anim



if __name__ == "__main__":
    # try:
    #     app = App()
    #     r = Renderer(debug=False, animation=Anim(), app=None)

    #     t1 = threading.Thread(target=r.animate)
    #     t1.start()
    #     app.mainloop()
    #     print('done')

    # except Exception:
    #     print(traceback.format_exc())
    # finally:
    #     r.wm.kill_workerw()
    #     r.running = False
    #     quit()

    try:
        r = Renderer(debug=False, animation=Anim(), app=None)
        r.animate()
    except Exception:
        print(traceback.format_exc())
    finally:
        r.wm.kill_workerw()
        quit()
    

