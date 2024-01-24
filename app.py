import threading

import traceback

from utils.gui import App
from utils.renderer import Renderer




if __name__ == "__main__":
    try:
        e = threading.Event()
        r = Renderer(debug=True, event=e)
        app = App(r, e)        
       
        app.mainloop()
        if r.on_pause:
            e.set()
        r.running = False
        print('done')
        

    except Exception:
        print(traceback.format_exc())
    finally:
        r.wm.kill_workerw()
        quit()
        

   