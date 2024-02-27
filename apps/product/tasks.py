import os
from apps.product.celery import app
from PIL import Image
from lameli_2 import settings


@app.task
def process_image(image_path):

    abs_image_path = os.path.join(settings.BASE_DIR, image_path)

    # Проверка существования файла
    if os.path.exists(abs_image_path):
        try:
            with Image.open(abs_image_path) as img:
                if img.width == 200 and img.height == 200:
                    pass
                else:
                    new_img = img.crop((0,0,img.width,img.width)).resize((200, 200)).transpose(Image.FLIP_LEFT_RIGHT)
                    new_img.save(abs_image_path)
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print(f"File not found: {abs_image_path}")
