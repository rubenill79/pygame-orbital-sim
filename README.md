# Pygame Orbital Simulation

Pygame Orbital Simulation is a customizable and interactive Python simulation built over Pygame that models the orbits of celestial bodies in 2D space using Newton’s law of universal gravitation.

![Orbital Simulation](link_to_image)

## Features

- Several included preset arrangements.
- Precise positioning and movement vectors obtained through built-in access to JPL’s HORIZONS system.
- Interactable objects with advanced data shown.

## Future features

- More included preset arrangements.
- Customizable simulation of celestial bodies' orbits.
- Real time zooming system to bodies to see moons, satelites, ect...
- Internationalization.
- SoundTrack
- Offline mode.

## Installation

### Dependencies

Pygame Orbital Simulation requires the following dependencies:

- Python 3
- Pygame 2.5
- Astropy
- Astroquery
- Tkinter
- CustomTkinter

### User Installation

1. Clone the repository:
git clone https://github.com/rubenill79/pygame-orbital-sim

2. Install dependencies:
pip install -r requirements.txt (doesnt work yet install manually)

3. Launch `launcher.py` and select the preset you like.

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
