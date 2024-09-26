from PIL import Image

def getImage(img_type, piece_color = None):
    if piece_color != None:
        return piece_images[piece_color][img_type]
    else:
        return ui_images[img_type]

ui_images = {
    'null': Image.new('RGBA', (100, 100)),
    'dot': Image.open('img/dot.png').convert('RGBA')
}

piece_images = {
    'white': {
        'King': Image.open('img/wh-king.png').convert('RGBA'),
        'Queen': Image.open('img/wh-queen.png').convert('RGBA'),
        'Rook': Image.open('img/wh-rook.png').convert('RGBA'),
        'Bishop': Image.open('img/wh-bishop.png').convert('RGBA'),
        'Knight': Image.open('img/wh-knight.png').convert('RGBA'),
        'Pawn': Image.open('img/wh-pawn.png').convert('RGBA')
    },
    'black': {
        'King': Image.open('img/bl-king.png').convert('RGBA'),
        'Queen': Image.open('img/bl-queen.png').convert('RGBA'),
        'Rook': Image.open('img/bl-rook.png').convert('RGBA'),
        'Bishop': Image.open('img/bl-bishop.png').convert('RGBA'),
        'Knight': Image.open('img/bl-knight.png').convert('RGBA'),
        'Pawn': Image.open('img/bl-pawn.png').convert('RGBA')
    }
}


