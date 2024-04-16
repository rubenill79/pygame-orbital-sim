import matplotlib
matplotlib.use('module://pygame_matplotlib.backend_pygame')
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 1,)
axes.plot([1,2], [1,2], color='green', label='test')
fig.canvas.draw()