import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

class MyFrame(customtkinter.CTkFrame):
    location_text = "LOCATION"

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        location_font = customtkinter.CTkFont(family="Century Gothic", size=30)
        forcast_font = customtkinter.CTkFont(family="Century Gothic", size=20)

        self._fg_color=("#6ea3ff","#0d182b")
        self._border_color=("#6ea3ff","#0d182b")
        self._border_width=1

        # add widgets onto the frame...
        self.location_entry = customtkinter.CTkEntry(self, placeholder_text="", fg_color="transparent", border_width=0, width=300, state="disabled")
        self.location_entry.grid(row=8, column=0, padx=30, sticky="nsew")

        self.location_label = customtkinter.CTkLabel(self, height=50, width=100, corner_radius=10, fg_color="transparent", text=self.location_text, font=location_font)
        self.location_label.grid(row=0, column=0, padx=20, columnspan=3, sticky="nsew")

        self.enable_loc_entry_button = customtkinter.CTkButton(self, fg_color="transparent", text="+", font=forcast_font, height=40, width=40, command=self.show_loc_entry)
        self.enable_loc_entry_button.grid(row=8, column=2, padx=30, sticky="nsew")

        self.change_loc_entry_button = customtkinter.CTkButton(self, fg_color="transparent", text="", state="disabled", font=forcast_font, height=40, width=40, command=self.change_location)
        self.change_loc_entry_button.grid(row=8, column=1)

        self.hourly_button = customtkinter.CTkButton(self, fg_color="#3464b3", text="Hourly Forecast", font=forcast_font, height=40, width=400, anchor="center")
        self.hourly_button.grid(row=1, column=0, padx=30, pady=10, columnspan=3, sticky="nsew")
    
    def show_loc_entry(self):
        self.location_entry.configure(state="normal")
        self.location_entry.configure(placeholder_text="Enter your current location (city or town and state)")
        self.location_entry.configure(text_color="white")
        self.location_entry.configure(border_width=1)

        self.change_loc_entry_button.configure(state="normal")
        self.change_loc_entry_button.configure(text="Go")
    
    def hide_loc_entry(self):
        self.location_entry.configure(placeholder_text="")
        self.location_entry.configure(border_width=0)

        self.change_loc_entry_button.configure(text="")

        self.location_entry.configure(state="disabled")
        self.change_loc_entry_button.configure(state="disabled")

    def change_location_text(self, new_loc_text):
        self.location_text = new_loc_text

    def change_location(self):
        temp = self.location_entry.get()
        if temp != "":
            self.location_label.configure(text=temp)
            self.change_location_text(temp)
        else:
            self.location_label.configure(text=self.location_text)
        #self.location_entry.delete(0, len(temp))
        self.location_entry.configure(text_color=("#6ea3ff","#0d182b"))
        self.hide_loc_entry()



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("550x800")
        self.resizable(False, False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        self.my_frame = MyFrame(master=self)
        self.my_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

app = App()
app.mainloop()