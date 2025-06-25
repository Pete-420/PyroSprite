# 🔥 PyroSprite - Fire Particle System

A real-time fire particle system built with Python and Pygame, featuring animated backgrounds and realistic flame effects using sprite atlases.


## ✨ Features

- **Real-time Fire Simulation**: Dynamic particle system with realistic fire behavior
- **Animated Backgrounds**: Support for animated sprite atlas backgrounds
- **Interactive Controls**: Mouse-controlled emitter positioning and real-time parameter adjustment
- **Sprite Atlas Support**: Efficient rendering using texture atlases for both particles and backgrounds
- **Configurable System**: Easy-to-modify configuration files for customization


## 🖼️ Screenshots

The system features:
- flame particles with life-cycle based animation
- Animated forest background with seamless looping
- Interactive fire emitter that follows mouse movement
- Debug information display for performance monitoring

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd PyroSprite
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

## 🎮 Controls

| Key/Action | Description |
|------------|-------------|
| `ESC` | Exit application |
| `SPACE` | Pause/Resume simulation |
| `+` / `=` | Increase emit rate |
| `-` | Decrease emit rate |
| `D` | Toggle debug information |
| `G` | Toggle mouse grab mode |
| `Mouse Movement` | Move fire emitter (when grab mode is on) |

## 🛠️ Configuration

The system is highly configurable through the `src/config.py` file:

### Particle Configuration
```python
PARTICLE_CONFIG = {
    'atlas_path': 'textures/j.png',
    'frame_width': 219,
    'frame_height': 1024,
    'atlas_cols': 7,
    'atlas_rows': 1,
}
```

### Background Configuration
```python
BACKGROUND_ATLAS_CONFIG = {
    'atlas_background_path': 'textures/background_atlas.png',
    'frame_width': 773,
    'frame_height': 765,
    'atlas_cols': 4,
    'atlas_rows': 2,
}
```

### Screen Configuration
```python
SCREEN_CONFIG = {
    'width': 773,
    'height': 765,
    'title': 'PyroSprites - Fire Particle System',
}
```

## 📁 Project Structure

```
PyroSprite/
├── main.py                 # Main application entry point
├── README.MD               # Project documentation
├── requirements.txt        # Python dependencies
├── src/                   # Source code directory
│   ├── background.py      # Animated background system
│   ├── config.py          # Configuration settings
│   ├── emitter.py         # Particle emitter logic
│   ├── particle.py        # Individual particle behavior
│   └── particleAtlas.py   # Sprite atlas management
└── textures/              # Asset directory
    ├── background_atlas.png  # Animated background sprite sheet
    ├── fire_background.png   # Static background (fallback)
    └── j.png                 # Fire particle sprite atlas
```

## 🔧 Technical Details

### Architecture

- **Modular Design**: Separated concerns with dedicated classes for particles, emitters, backgrounds, and atlases
- **Sprite Atlas System**: Efficient texture management using sprite sheets
- **Delta Time Animation**: Smooth animation independent of frame rate
- **Configurable Parameters**: External configuration for easy tweaking

### Particle System

- **Life-cycle Animation**: Particles change appearance based on their remaining life
- **Physics Simulation**: Realistic movement with gravity and wind effects
- **Ember Effects**: Special particle types for enhanced realism
- **Alpha Blending**: Smooth transparency effects for realistic fire appearance

## 🎨 Customization

### Adding New Particle Effects

1. Create new sprite atlas in the `textures/` directory
2. Update `PARTICLE_CONFIG` in `config.py`
3. Modify rendering logic in `main.py` if needed

### Creating Custom Backgrounds

1. Prepare sprite atlas with consistent frame dimensions
2. Update `BACKGROUND_ATLAS_CONFIG` settings
3. Adjust animation speed as desired

## 🐛 Troubleshooting

### Common Issues

**Missing textures**: Ensure all texture files are in the `textures/` directory
**Performance issues**: Reduce emit rate or particle count in debug mode
**Import errors**: Verify all dependencies are installed with `pip install -r requirements.txt`

### Debug Mode

Enable debug mode with the `D` key to monitor:
- Particle count
- Emit rate
- FPS
- Emitter position
- Ember count

## 📦 Dependencies

- **pygame>=2.0.0**: Main game engine and graphics
- **PyOpenGL>=3.1.0**: OpenGL bindings for hardware acceleration

## 👥 Authors

- **Bartosz Berezowski** - Lead Developer
- **Piotr Truszkowski** - Graphics & Animation
- **Adam Ożański** - System Architecture

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! 

**Enjoy creating beautiful fire effects with PyroSprite!** 🔥