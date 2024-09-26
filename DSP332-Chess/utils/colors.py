from dataclasses import dataclass

@dataclass
class Colors:
    # Default UI colors
    DARK_GRAY = "#131516"
    LIGHT_GRAY = "#1d2021"
    WHITE = "#e1e1e1"
    
    # Default square colors
    DARK_VIOLET = "#474554"
    LIGHT_VIOLET = "#9F9BBC"
    
    # Square colors for an attacked piece
    LIGHT_ATTACKING = "#BC9B9B"
    DARK_ATTACKING = "#4C3A3A"
    
    # Square colors for the previous move
    LIGHT_MOVE = "#CCB2D7"
    DARK_MOVE = "#50475E"

    # Result colors
    LIGHT_YELLOW = "#F7DC6F"
    LIGHT_RED = "#EC7063"
    LIGHT_GREEN = "#82E0AA"
