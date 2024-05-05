import matplotlib
matplotlib.use('module://pygame_matplotlib.backend_pygame')
import matplotlib.pyplot as plt
import numpy as np
import math

fig, axes = plt.subplots(1, 1,)
axes.plot([1,2], [1,2], color='green', label='test')
fig.canvas.draw()

def normalize_angle(angle):
    # Normalize the angle to the range [0, 360)
    return (angle + 360) % 360

def second_highest(arr):
    # Edge case: check if there are at least two unique values in the array
    if len(set(arr)) < 2:
        raise ValueError("Array must contain at least two unique values.")

    # Initialize the largest and second-largest values
    first = second = float('-inf')

    # Traverse through the array to find the largest and second-largest
    for num in arr:
        if num > first:
            # If current number is greater than the largest, update first and second
            second = first
            first = num
        elif first > num > second:
            # If current number is between largest and second-largest, update second
            second = num

    return second

def draw(graphic, entity):
    try:
        # Create a figure with two subplots
        fig, ax = plt.subplots(figsize=(1, 1,), subplot_kw={'polar': True})
        if graphic == 'pygame-gui.Attraction_forces':
            # Separar los datos de la lista
            
            nombres = [item[0] for item in entity.attraction_forces]
            magnitudes = np.array([item[1] for item in entity.attraction_forces])
            angulos = np.array([item[2] for item in entity.attraction_forces])
            #print(magnitudes, angulos)
            
            width = 1 / len(magnitudes)
            colors = plt.cm.viridis(magnitudes / np.max(magnitudes))
            
            second = second_highest(magnitudes)
            
            ax.bar(angulos, magnitudes, width=width, bottom=0.0, color=colors, alpha=0.5)
            ax.set_ylim(0, second)
            
            # Ensure the figure redraws
            fig.canvas.draw()
            plt.close()

            return fig
    except Exception: 
        ax.text(0.5, 0.5, 'Error: Datos Inválidos', fontsize=16, ha='center', va='center', color='red')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')  # Ocultar ejes para solo mostrar el mensaje
        # Título para indicar el error
        ax.set_title('Error en el Gráfico')
        fig.canvas.draw()
        return fig