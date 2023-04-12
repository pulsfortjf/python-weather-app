import customtkinter
import requests
import json
from datetime import datetime
from geopy.geocoders import Nominatim

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

class MyFrame(customtkinter.CTkFrame):
    location_text = "LOCATION"

    tutorial_showing = True

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        location_font = customtkinter.CTkFont(family="Century Gothic", size=30)
        forecast_font = customtkinter.CTkFont(family="Century Gothic", size=20)
        tutorial_font = customtkinter.CTkFont(family="Century Gothic", size=14)

        self._fg_color=("#6ea3ff","#0d182b")
        self._border_color=("#6ea3ff","#0d182b")
        self._border_width=1

        # add widgets onto the frame...
        self.location_label = customtkinter.CTkLabel(self, height=50, width=100, corner_radius=10, fg_color="transparent", text=self.location_text, font=location_font, anchor="center")
        self.location_label.grid(row=0, column=0, padx=30, columnspan=3, sticky="nsew")

        self.forecast_button = customtkinter.CTkButton(self, fg_color="#3464b3", text="Forecast", font=forecast_font, height=40, width=400, anchor="center", command=self.find_weather)
        self.forecast_button.grid(row=1, column=0, padx=30, pady=10, columnspan=3, sticky="nsew")

        self.fbutton_tutorial_label = customtkinter.CTkLabel(self, height=100, width=400, corner_radius=10, fg_color="transparent", justify="left",
                                                             text="When location and units have been selected,\nclick Forecast to see the weather for that location", font=tutorial_font, anchor="nw")
        self.fbutton_tutorial_label.grid(row=2, column=0, columnspan=3, padx=30, sticky="nsew")

        self.forecast_label = customtkinter.CTkLabel(self, height=200, width=400, corner_radius=10, fg_color="transparent", text="", font=forecast_font, anchor="w", justify="left")
        self.forecast_label.grid(row=3, column=0, padx=30, columnspan=3, sticky="nsw")

        self.ubutton_tutorial_label = customtkinter.CTkLabel(self, height=100, width=150, corner_radius=10, fg_color="transparent", justify="left",
                                                             text="The letter shown is\nthe temperature units\n(C or F). Click the button\nto change the units", font=tutorial_font, anchor="e")
        self.ubutton_tutorial_label.grid(row=7, column=0, columnspan=2, sticky="nse")

        self.plus_button_tutorial_label = customtkinter.CTkLabel(self, height=100, width=100, corner_radius=10, fg_color="transparent", text="Click + to\nchange\nthe location", font=tutorial_font, anchor="w", justify="left")
        self.plus_button_tutorial_label.grid(row=7, column=2, sticky="nse")

        self.location_entry = customtkinter.CTkEntry(self, placeholder_text="Enter your current location (city or town and state)", fg_color="transparent", border_width=1, width=300, state="normal")
        self.location_entry.grid(row=8, column=0, padx=30, sticky="nsew")

        self.units_button = customtkinter.CTkButton(self, fg_color="transparent", text="C", font=forecast_font, height=40, width=40, command=self.change_units, anchor="center")
        self.units_button.grid(row=8, column=1, padx=0, sticky="ns")

        self.enable_loc_entry_button = customtkinter.CTkButton(self, fg_color="transparent", text="+", font=forecast_font, height=40, width=40, command=self.change_location, anchor="center")
        self.enable_loc_entry_button.grid(row=8, column=2, padx=30, sticky="ns")

    def change_units(self):
        curr_units = self.units_button.cget("text")

        if curr_units == "C":
            self.units_button.configure(text="F")
        else:
            self.units_button.configure(text="C")

    def change_location_text(self, new_loc_text):
        self.location_text = new_loc_text

    def change_location(self):
        if self.tutorial_showing:
            self.close_tutorial()
        
        temp = self.location_entry.get()
        if temp != "":
            self.location_label.configure(text=temp)
            self.forecast_label.configure(text="")
            self.change_location_text(temp)
        else:
            self.location_label.configure(text=self.location_text)
        #self.location_entry.delete(0, len(temp))
        #self.location_entry.configure(text_color=("#6ea3ff","#0d182b"))
        #self.hide_loc_entry()
    
    def city_lat_long(self, location_name):
        geolocator = Nominatim(user_agent="MyApp")

        location_coords = geolocator.geocode(location_name)

        return (str(location_coords.latitude), str(location_coords.longitude))

    def time_format_for_location(self, utc_with_tz):
        local_time = datetime.utcfromtimestamp(utc_with_tz)
        return local_time.time()

    def close_tutorial(self):
        self.fbutton_tutorial_label.configure(text="")
        self.ubutton_tutorial_label.configure(text="")
        self.plus_button_tutorial_label.configure(text="")

        self.fbutton_tutorial_label.configure(height=0)
        self.ubutton_tutorial_label.configure(height=0)
        self.plus_button_tutorial_label.configure(height=0)

        self.forecast_label.configure(height=360)

    def find_weather(self):
        api_key = "42fdbb39807f01a6f203d839aeb80cef"

        location_name = self.location_label.cget("text")

        units_str = self.units_button.cget("text")
        if units_str == "C":
            units = "metric"
        else:
            units = "imperial"

        #split_location = location_name.split(', ')
        #city_name = split_location[0]
        #state_code = split_location[1]
        #print(city_name, state_code)

        lat_long = self.city_lat_long(location_name)
        print(lat_long[0], lat_long[1])

        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat_long[0]}&lon={lat_long[1]}&units={units}&appid={api_key}')
        #response = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?lat={lat_long[0]}&lon={lat_long[1]}&appid={api_key}')
        #response = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?q={city_name},{state_code},us&appid={api_key}')

        forecast_info = response.json()

        if forecast_info['cod'] == 200:
            kelvin = 273 # value of kelvin

            #Storing the fetched values of weather of a city
            #temp = int(forecast_info['main']['temp'] - kelvin)                                     #converting default kelvin value to Celcius
            temp = int(forecast_info['main']['temp'])
            feels_like_temp = int(forecast_info['main']['feels_like'])
            pressure = forecast_info['main']['pressure']
            humidity = forecast_info['main']['humidity']
            wind_speed = forecast_info['wind']['speed'] * 3.6
            sunrise = forecast_info['sys']['sunrise']
            sunset = forecast_info['sys']['sunset']
            timezone = forecast_info['timezone']
            cloudy = forecast_info['clouds']['all']
            description = forecast_info['weather'][0]['description']
    
            sunrise_time = self.time_format_for_location(sunrise + timezone)
            sunset_time = self.time_format_for_location(sunset + timezone)
         
            weather_str = f"Temperature ({units_str}): {temp}°\nFeels like ({units_str}): {feels_like_temp}°\nPressure: {pressure} hPa\nHumidity: {humidity}%\nSunrise at {sunrise_time} and Sunset at {sunset_time}\nCloud: {cloudy}%\nInfo: {description}"
        else:
            weather_str = f"Weather for '{location_name}' not found!\nPlease enter a valid city name"
        
        self.forecast_label.configure(text=weather_str)
        self.forecast_label.configure(anchor="w")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("550x600")
        self.resizable(False, False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        self.my_frame = MyFrame(master=self)
        self.my_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

app = App()
app.mainloop()