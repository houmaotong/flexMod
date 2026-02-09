# Resources

This directory contains all application resources.

## Directory Structure

```
resources/
├── icons/          # Application icons (window icons, button icons, etc.)
│   └── logo_128.png
└── images/         # Other images (backgrounds, illustrations, etc.)
```

## Usage

Use the `ResourceManager` class to access resources:

```python
from refactor.utils.resource_manager import resource_manager

# Get application icon
app_icon = resource_manager.get_app_icon()

# Get specific icon
icon = resource_manager.get_icon("filename.png")

# Get image pixmap
pixmap = resource_manager.get_pixmap("filename.jpg")
```

## Adding New Resources

1. Place icon files in the `icons/` directory
2. Place image files in the `images/` directory
3. Access them using the ResourceManager

## Supported Formats

- Icons: PNG, ICO, SVG
- Images: PNG, JPG, JPEG, SVG
