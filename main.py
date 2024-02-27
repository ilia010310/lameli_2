from PIL import Image, ImageChops
from rembg import remove

SOURCE_DIR = 'media/images/avatars/'

open_image = Image.open(SOURCE_DIR + 'ava.jpg')
output_dir = SOURCE_DIR + 'ava_new.png'

output = remove(open_image)
output.save(output_dir)







# See PyCharm help at https://www.jetbrains.com/help/pycharm/
