import qrcode
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import random

# This program will generate a set of random numbers
# And use then return them in a qrcode list


def random_data(number: int, number_start: int, number_end: int):
    data = random.sample(range(number_start, number_end), number)
    return (data)


def qr_gen(data: list):

    qr_list = [[], []]
    for code in data:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=5,
            border=3,
        )
        qr.add_data(code)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="transparent")
        qr_list[0].append(img)
        qr_list[1].append(code)

    return(qr_list)


def qr_write(base_img: str, qrs: list, size=[75, 75],
             initial_left=[600, 13], t_initial_left=[400, 25], y_increment=88):

    # Font to use
    font = ImageFont.truetype("OpenSans-Regular.ttf", 30)
    # Background Image
    for i in range(0, len(qrs[0]), 10):
        with Image.open(base_img) as image:
            image_copy = image.copy()
            draw = ImageDraw.Draw(image_copy)
            pos = [initial_left[0], initial_left[1]]
            t_pos = [t_initial_left[0], t_initial_left[1]]

            for qr, code in zip(qrs[0][i:i+10], qrs[1][i:i+10]):
                qr = qr.resize(size)
                image_copy.paste(qr, tuple(pos))
                image_copy.paste(qr, tuple([pos[0] - 400, pos[1]]))
                draw.text(t_pos, str(code), (0, 0, 0), font=font)

                # Incremating location
                pos[1] += y_increment
                t_pos[1] += y_increment

            image_copy.save(f"output/{i}-{i+10}.png")


data = random_data(110, 100000, 1000000)
qrs = qr_gen(data)
r_write('base/lines.png', qrs=qrs)
