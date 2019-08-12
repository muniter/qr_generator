from PIL import Image
from pylibdmtx.pylibdmtx import encode
from jinja2 import Environment, FileSystemLoader
import random


def random_data(number: int, number_start: int, number_end: int):
    '''This function extracts unique numbers from a range of numbers'''
    data = random.sample(range(number_start, number_end), number)
    return (data)


def qr_generator(data: list, prefix='', suffix=''):
    '''Generate qr codes for data provided, returns tuple of tuples,
    with value and barcode object'''
    qrs = []
    for item in data:
        item_text = prefix + str(item) + suffix
        encoded = encode(item_text.encode('utf-8'))
        qr = Image.frombytes(
            'RGB',
            (encoded.width, encoded.height),
            encoded.pixels
        )

        qrs.append({'data': item_text, 'qr': qr})

    return(qrs)


def html_generator(manillas: list, template: str):
    '''Generate the html of the qr and values list to further
    convert to pdf'''
    file_loader = FileSystemLoader('./')
    env = Environment(loader=file_loader)
    template = env.get_template(template)
    for manilla in manillas:
        manilla["qr"].save('output/qrs/' + str(manilla["data"]) + '.png')
    result = template.render(manillas=manillas)
    return result


data = random_data(100, 100000, 1000000)
qrs = qr_generator(data)
manillas = html_generator(qrs, './templates/template.html')
with open('templates/output.html', 'w') as file:
    file.write(manillas)
