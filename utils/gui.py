import tkinter
import tkinter.messagebox
import customtkinter


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


def button_callback():
    print("button pressed")



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1100}x{580}")


        button = customtkinter.CTkButton(self, text="my button", command=button_callback)
        button.grid(row=0, column=0, padx=20, pady=20)



if __name__ == "__main__":
    app = App()
    app.mainloop()
    print("done")