from PIL import Image

def newImg(int):
    img = Image.new('RGB', (400, 400))
    img.putpixel((int, 60), (156, 156, 55))
    img.save('sqr.png')
    return img

for each in range(0, 60):

    image = newImg(each)
    image.save('/Users/johnmogielnicki/code/evolve/media/images/{}.png'.format(each), 'PNG')
