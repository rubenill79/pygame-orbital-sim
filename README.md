# Pygame Orbital Simulation

Pygame Orbital Simulation is a customizable and interactive Python simulation built over Pygame that models the orbits of celestial bodies in 2D space using Newton’s law of universal gravitation.

![Orbital Simulation](link_to_image)

## Features

- Several included preset arrangements.
- Create your own preset arrangements.
- Precise positioning and movement vectors obtained through built-in access to JPL’s HORIZONS system.
- Real time zooming system to bodies to see moons, satelites, ect... (In progress)
- Interactable objects with advanced data shown.
- Camera center in the entity you click so you can look how it will look if you were in that place.
- Internationalization.

## Future features

- More included preset arrangements.

- SoundTrack
- Offline mode.

## Installation

### Dependencies

Pygame Orbital Simulation requires the following dependencies:

- Python 3
- Pygame-ce
- Pygame-gui
- Astropy
- Astroquery

### User Installation

1. Clone the repository:
git clone https://github.com/rubenill79/pygame-orbital-sim

2. Install dependencies:
pip install -r requirements.txt

3. Launch `main.py` positioning vscode or other ide in the app folder.

## Usage

Once the simulation starts, you can control and interact with it using the following keys:

| Key(s) | Action(s)                            |
|--------|--------------------------------------|
| SPACE  | Pause/play simulation                |
| W S A D| Move window view; pan about          |
| +/-    | Zoom in and out respectively         |
| Mouse  | Mouse wheel and dragging for zooming |
| r      | Reset zoom and position              |
| ./,    | Speed up and slow down simulation   |
| l      | Toggle labels on the selected entity|
| ESC    | Quit the simulation                  |

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request or contact me via email.

## License

This project is licensed under the [MIT License](https://github.com/rubenill79/pygame-orbital-sim/blob/main/LICENSE).
