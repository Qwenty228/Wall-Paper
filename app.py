import traceback

from ui.gui import App



if __name__ == "__main__":
    try:
        app = App()        
       
        app.mainloop()
        print('done')
        

    except Exception:
        print(traceback.format_exc())
    finally:
        quit()
        

   