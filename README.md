# Pygame Orbital Simulation

Pygame Orbital Simulation is a customizable and interactive Python simulation built over Pygame that models the orbits of celestial bodies in 2D space using Newton’s law of universal gravitation.

![Orbital Simulation](link_to_image)

## Features

- Customizable simulation of celestial bodies' orbits.
- Several included preset arrangements for quick setup.
- Precise positioning and movement vectors obtained through built-in access to JPL’s HORIZONS system.

## Installation

### Dependencies

Pygame Orbital Simulation requires the following dependencies:

- Python 3
- Pygame
- Astropy
- Astroquery

### User Installation

1. Clone the repository:
git clone https://https://github.com/rubenill79/pygame-orbital-sim

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

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the [MIT License](https://github.com/rubenill79/pygame-orbital-sim/blob/main/LICENSE).