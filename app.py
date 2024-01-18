import threading

import traceback

from utils.gui import App
from utils.renderer import Renderer
from data.shaders.fullspectrumcyber import Anim
# from data.template.doomfire import Anim
# from data.videos.videos import Anim



if __name__ == "__main__":
    try:
        app = App()
        r = Renderer(debug=True, animation=Anim(), app=None)

        t1 = threading.Thread(target=r.animate)
        t1.start()
        app.mainloop()
        r.running = False
        print('done')
        

    except Exception:
        print(traceback.format_exc())
    finally:
        r.wm.kill_workerw()
        quit()
        

   