from presets import EarthMoon, InnerSolarSystem, SolarSystem, EnhancedSolarSystem
import customtkinter
import tkinter
import pickle

class Data():
    def __init__(self, scenario, language, fullscreen):
        self.scenario = scenario
        self.language = language
        self.fullscreen = fullscreen

def load_data():   
    # Load the dictionary back
    try:
        with open('launcher_options.dat', 'rb') as file:
            loaded_attributes = pickle.load(file)
    except FileNotFoundError:
        return
    except pickle.UnpicklingError:
        label_3.configure(text = "Fallo al cargar la configuración")
        return
    # Create a new object using the loaded attributes
    loaded_object = Data(
        scenario=loaded_attributes['scenario'],
        language=loaded_attributes['language'],
        fullscreen=loaded_attributes['fullscreen']
    )
        
    optionmenu_1.set(loaded_object.scenario)
    radiobutton_var.set(loaded_object.language)
    if loaded_object.fullscreen is False:
        switch_1.toggle()
        
def save_data(scenario, language, fullscreen):
    data = Data(scenario, language, fullscreen)
    # Extract relevant attributes into a dictionary
    attributes_to_save = {
        'scenario': data.scenario,
        'language': data.language,
        'fullscreen': data.fullscreen
    }
    # Save the dictionary to a file using pickle
    with open('launcher_options.dat', 'wb') as file:
        pickle.dump(attributes_to_save, file)

customtkinter.set_ctk_parent_class(tkinter.Tk)

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.title("Launcher")

font = customtkinter.CTkFont('',20)

def button_callback():
    if optionmenu_1.get().__eq__("Tierra - Luna"):
        text_scenario = "Tierra - Luna"
        label_3.configure(text = "Lanzando simulación . . . ")
        app.update()
        s = EarthMoon()
        s.scenario = 1
    elif optionmenu_1.get().__eq__("Sistema Solar Interno"):
        text_scenario = "Sistema Solar Interno"
        label_3.configure(text = "Lanzando simulación . . . ")
        app.update()
        s = InnerSolarSystem()
        s.scenario = 2
    elif optionmenu_1.get().__eq__("Sistema Solar Completo"):
        text_scenario = "Sistema Solar Completo"
        label_3.configure(text = "Lanzando simulación . . . ")
        app.update()
        s = SolarSystem()
        s.scenario = 3
    elif optionmenu_1.get().__eq__("Sistema Solar Ampliado"):
        text_scenario = "Sistema Solar Ampliado"
        label_3.configure(text = "Lanzando simulación . . . ")
        app.update()
        s = EnhancedSolarSystem()
        s.scenario = 4
    else:
        label_3.configure(text = "Escoge un escenario para comenzar")
        return
    
    s.language = radiobutton_var.get()
    s.fullscreen = bool(switch_1.get())
    
    save_data(text_scenario, s.language, s.fullscreen)
    
    app.destroy()
    s.start()

frame_1 = customtkinter.CTkFrame(master=app)
frame_1.pack(pady=20, padx=60, fill="both", expand=True)

label_1 = customtkinter.CTkLabel(master=frame_1, justify=customtkinter.LEFT, text="Parámetros de Simulación", font=font)
label_1.pack(pady=10, padx=10)

optionmenu_1 = customtkinter.CTkOptionMenu(frame_1, values=["Tierra - Luna", "Sistema Solar Interno", "Sistema Solar Completo", "Sistema Solar Ampliado"])
optionmenu_1.pack(pady=10, padx=10)
optionmenu_1.set("Escoger Escenario")

label_1 = customtkinter.CTkLabel(master=frame_1, justify=customtkinter.LEFT, text="")
label_1.pack(pady=10, padx=10)

label_2 = customtkinter.CTkLabel(master=frame_1, justify=customtkinter.LEFT, text="")
label_2.pack(pady=10, padx=10)

label_3 = customtkinter.CTkLabel(master=frame_1, justify=customtkinter.LEFT, text="")
label_3.pack(pady=10, padx=10)

switch_1 = customtkinter.CTkSwitch(master=frame_1, text="Pantalla completa")
# para que comience activo
switch_1.toggle()
switch_1.pack(pady=10, padx=10)

label_4 = customtkinter.CTkLabel(master=frame_1, justify=customtkinter.LEFT, text="Idioma / Language")
label_4.pack(pady=10, padx=10)

radiobutton_var = customtkinter.IntVar(value=1)

radiobutton_1 = customtkinter.CTkRadioButton(master=frame_1, variable=radiobutton_var, value=1, text="Español")
radiobutton_1.pack(pady=10, padx=10)

radiobutton_2 = customtkinter.CTkRadioButton(master=frame_1, variable=radiobutton_var, value=2, text="English")
radiobutton_2.pack(pady=10, padx=10)

button_1 = customtkinter.CTkButton(master=frame_1, command=button_callback, text="Lanzar Simulación")
button_1.pack(pady=10, padx=10)

# Obtener el ancho y alto de la pantalla
ancho_pantalla = app.winfo_screenwidth()
alto_pantalla = app.winfo_screenheight()

# Obtener el ancho y alto de la ventana
ancho_ventana = 400  # Puedes ajustar el ancho de la ventana
alto_ventana = 520  # Puedes ajustar el alto de la ventana

# Calcular la posición para centrar la ventana
x = (ancho_pantalla / 2) - (ancho_ventana / 2)
y = (alto_pantalla / 2) - (alto_ventana / 2)

# Establecer la posición de la ventana en el centro
app.geometry(f'{ancho_ventana}x{alto_ventana}+{int(x)}+{int(y)}')

app.iconbitmap('resources\icon.ico')

load_data()

app.mainloop()