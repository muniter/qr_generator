import odoorpc
import unidecode
import pandas as pd
from jinja2 import Environment, FileSystemLoader

db_name = 'odoo'
username = 'graulopezjavier@gmail.com'
password = 'BmtmP73RGQsh6kHQeDCdpzfi2EQyW8f'
odoo = odoorpc.ODOO('evento.lintec.xyz', protocol='jsonrpc+ssl', port=443)

# Login
odoo.login(db_name, username, password)


def get_pd(odoo, evento):
    Attendee = odoo.env['idmji.attendee']
    attendees_id = Attendee.search([('evento', '=', evento)])
    fields = ['name', 'tipo_doc', 'num_doc', 'edad',
              'iglesia', 'categoria', 'manilla']

    # Getting the data
    data = odoo.execute('idmji.attendee', 'read', attendees_id, fields)
    # Formatting the dataframe
    df = pd.DataFrame.from_dict(data)
    df = df.set_index('id')
    df['iglesia'] = df['iglesia'].apply(lambda x: x[1])
    df['categoria'] = df['categoria'].apply(lambda x: x[1])
    # Sorting properly in the presence of unicode
    df = df.assign(name_noacc=df['name'].apply(
        lambda x: unidecode.unidecode(x)))
    df = df.sort_values(['iglesia', 'name_noacc'])
    df = df.drop('name_noacc', axis=1)  # Dropping the helper row

    # Categories pivot table
    res = df.pivot_table(index='iglesia',
                         columns=['categoria', 'manilla'],
                         values='name',
                         aggfunc='count',
                         margins=True,
                         fill_value=0,
                         margins_name='Total',
                         )

    results = [[], ]
    index = res.index
    for i in index:
        series = res.loc[i, :]
        name = series.name
        series = series[series > 0].to_dict()
        results[0].append(name)
        results.append(series)

    return([df, res, results])


def html_generator(data: list, template: str, evento: str):
    '''Generate the html of the qr and values list to further
    convert to pdf'''
    file_loader = FileSystemLoader('./')
    env = Environment(loader=file_loader)
    template = env.get_template(template)
    iglesias = data[0]
    data_iglesias = data[1:]
    data_iglesias = zip(iglesias, data_iglesias)
    result = template.render(evento=evento, data_iglesias=data_iglesias)
    return result


data = get_pd(odoo, 2)
res = html_generator(data[2],
                     'templates/base.html',
                     'Estudio Bíblico Montería')

with open('test.html', 'w') as file:
    file.write(res)
