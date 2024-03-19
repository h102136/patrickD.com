import tkinter as tk
import requests as req
from PIL import Image, ImageTk
import io

# get the real-time weather data from https://www.weatherapi.com/ through api
def get_weather(city_name, unit):
    api_key = 'f5e80542a7af4ad493700935241703' 
    base_url = 'https://api.weatherapi.com/v1/current.json'
    full_url = f"{base_url}?key={api_key}&q={city_name}&aqi=no" #f-string, combine key and base url
    response = req.get(full_url)
    weather_data = response.json()

    if response.status_code != 404:       # connect successfully if status_code is not 404
        if 'error' not in weather_data:   # inputted value of city_name is correct if 'error' isn't in weather_data
            result = {
                "Name":weather_data['location']['name'],
                "Latitude":weather_data['location']['lat'],
                "Longitude":weather_data['location']['lon'],
                "Country": weather_data['location']['country'],
                "Local_time": weather_data['location']['localtime'],
                "Last_updated": weather_data['current']['last_updated'],
                "Condition": weather_data['current']['condition']['text'],
                "Icon": weather_data['current']['condition']['icon'],
                "Temp": weather_data['current']['temp_f'] if unit == 'F' else weather_data['current']['temp_c'],
                # unit of temperature will show celsius or fahrenheit depend on value of Entry2 (E2) by user inputted
                "Wind_mph": weather_data['current']['wind_mph'],
                "Wind_kph":weather_data['current']['wind_kph'],
                "Wind_dir":weather_data['current']['wind_dir'],
                "Uv": weather_data['current']['uv'],
                "Pressure_mb": weather_data['current']['pressure_mb'],
                "Humidity":weather_data['current']['humidity']
            }
            return result
        else:
            return "The city could not be found."   
            # inputted value of city_name is unavailable if 'error' is in weather_data


def hit():
    city_name = E1.get()
    unit = E2.get().upper()

    if not city_name:
        info_sq.set('Please type city name')
        return
    if unit not in ['C', 'F']:
        info_sq.set('Please type unit of temperature (C or F).')
        return

    weather_info = get_weather(city_name, unit)
    if isinstance(weather_info, str):     # if returned value is string, means an error happened
        info_sq.set(weather_info)  
    elif isinstance(weather_info, dict):  # if returned value is dic (result), means inputted value is correct
        info = f"Name: {weather_info['Name']}\n"
        info += f"Latitude, Longitude: ({weather_info['Latitude']}, {weather_info['Longitude']})\n"
        info += f"Country: {weather_info['Country']}\n"
        info += f"Local Time: {weather_info['Local_time']}\n"
        info += f"Last Updated: {weather_info['Last_updated']}\n\n"
        info += f"Condition: {weather_info['Condition']}\n"
        info += f"Temperature: {weather_info['Temp']}{'F' if unit == 'F' else 'C'}\n"
        info += f"Wind MPH: {weather_info['Wind_mph']}\n"
        info += f"Wind KPH: {weather_info['Wind_kph']}\n"
        info += f"Wind Direction: {weather_info['Wind_dir']}\n" 
        info += f"UV: {weather_info['Uv']}\n"
        info += f"Pressure MB: {weather_info['Pressure_mb']}\n"
        info += f"Humidity: {weather_info['Humidity']}"

        icon_file= weather_info['Icon']
        icon_url= 'https:'+icon_file
        response_icon=req.get(icon_url)
        icon_image_data=Image.open(io.BytesIO(response_icon.content))
        weather_icon_phot=ImageTk.PhotoImage(icon_image_data)
        weather_im_canvas.create_image(35, 35, image=weather_icon_phot)
        weather_im_canvas.image = weather_icon_phot

        info_sq.set(info)
        
def reset():
    info_sq.set('')
    E1.delete(0, tk.END)
    E2.delete(0, tk.END)

window = tk.Tk()
window.title('Real-Time Global Weather Forecast')
window.geometry('500x600')

L1 = tk.Label(window, text='Real-Time Global Weather Forecast', bg='#00AAAA', font=('Arial', 15), width=45, height=3)
L1.place(x=0, y=0)

E1 = tk.Entry(window, font=('Arial', 12))
E1.place(x=370, y=78, anchor='ne')

E2 = tk.Entry(window, font=('Arial', 12))
E2.place(x=370, y=105, anchor='ne')

weather_im_canvas=tk.Canvas(window,bg='white', height=70, width=70)
weather_im_canvas.place(x=400, y=200, anchor='nw')

city_name_L = tk.Label(window, text='City Name:', font=('Arial', 12))
city_name_L.place(x=60, y=78, anchor='nw')

temperature_unit_L = tk.Label(window, text='Please type C or F:\n(Unit of Temperature)', font=('Arial', 12))
temperature_unit_L.place(x=10, y=105, anchor='nw')

info_sq = tk.StringVar()
info_sq_L = tk.Label(window, textvariable=info_sq, bg='white', fg='#003C9D', font=('Arial', 13), width=40, height=22, justify='left')
info_sq_L.place(x=20, y=150, anchor='nw')

search_B = tk.Button(window, text='Search', command=hit, width=6, height=1)
search_B.place(x=400, y=85, anchor='nw')

reset_B=tk.Button(window, text='Reset', command=reset, width=6, height=1)
reset_B.place(x=400, y=125, anchor='nw')

window.mainloop()
