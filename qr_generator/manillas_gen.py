from PIL import Image
from weasyprint import HTML
from pylibdmtx.pylibdmtx import encode
from jinja2 import Environment, FileSystemLoader
import random


def random_data(number: int, number_start: int, number_end: int):
    '''This function extracts unique numbers from a range of numbers'''
    sample = random.sample(range(number_start, number_end), number)
    data = []
    for item in sample:
        data.append(format(item, '>07'))

    return (data)


def qr_generator(data: list, prefix='', suffix=''):
    '''Generate qr codes for data provided, returns tuple of tuples,
    with value and barcode object'''
    qrs = []
    for item in data:
        item_text = prefix + item + suffix
        encoded = encode(item_text.encode('utf-8'))
        qr = Image.frombytes(
            'RGB',
            (encoded.width, encoded.height),
            encoded.pixels
        )

        qrs.append({'data': item_text, 'qr': qr})

    return(qrs)


def html_generator(manillas: list, template: str, eb: str):
    '''Generate the html of the qr and values list to further
    convert to pdf'''
    file_loader = FileSystemLoader('./')
    env = Environment(loader=file_loader)
    template = env.get_template(template)
    for manilla in manillas:
        manilla["qr"].save('output/qrs/' + str(manilla["data"]) + '.png')
    result = template.render(manillas=manillas, eb=eb)
    return result


# Ask for input
num_manillas = input("Número de Manillas: ")
eb = input("Estudio Bíblico: ")

output = eb.lower()
template = 'templates/template.html'
data = random_data(int(num_manillas), 5000000, 6000000)
qrs = qr_generator(data)
manillas = html_generator(qrs, template=template, eb=eb)

with open(output + '.html', 'w') as file:
    file.write(manillas)

with open(eb.lower() + '.txt', 'w') as file:
    for item in data:
        file.write(f"{item}\n")

HTML(filename=output + '.html').write_pdf(output + '.pdf')
