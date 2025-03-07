from utils import Utils
import pandas as pd


utils = Utils()
# path_choiced = utils.wx_dirdialog()
# driver = utils.init_webdriver(default=True, headless=False, output=path_choiced)
# driver.get("https://beyblade.fandom.com/wiki/List_of_Basic_Line_parts")
site = utils.web_scrape(url="https://beyblade.fandom.com/wiki/List_of_Custom_Line_parts")
table_elements = site.find_all('table', class_='wikitable')
tables = {}
for table in table_elements:
    previous_sibling = table.previous_sibling
    while previous_sibling and previous_sibling.name is None:
        previous_sibling = previous_sibling.previous_sibling
    heading = previous_sibling.text
    # print(heading)
    tables.update({heading: table})
writer = pd.ExcelWriter('tabelas_beyblade_cx.xlsx', engine='xlsxwriter')
data_frames = []
for name, table in tables.items():
    # data_list = [[y for y in x.text.split('\n') if y if y != 'Image' if y!= 'File:Gill Shark 4-700.jpeg'] for x in table.find_all('tr') if x] 
    data_list = []
    for element in table.find_all('tr'):
        data = [y for y in element.text.split('\n') if y if y != 'Image' if y!= 'File:Gill Shark 4-700.jpeg']
        link = element.find('a', class_='')
        if link is None:
            data.extend(['Link', 'Tipo', 'Sistema', 'Ataque', 'Defesa', 'Resistência', 'Avanço', 'Eclosão'])
        else:
            # obter link
            href = f"https://beyblade.fandom.com{link.get('href')}"
            data.append(href)

            new_site = utils.web_scrape(url=href)
            #obter tipo e sistema
            new_site.find_all('div', attrs={"data-source": True})
            type_system = [x.a.text if x.a.text != '' else "N/A" for x in new_site.find_all('div', attrs={"data-source": True}) if (x.get("data-source")=="Type" or x.get("data-source")=="System")]
            data.extend(type_system)
            # obter stats ataque, defesa, resistencia e etc
            stats = [x.text if x.text != '' else "N/A"  for x in new_site.find_all('td', attrs={"data-source": True}) if x.get('data-source') != 'XStandard']
            data.extend(stats)
        data_list.append(data)

    df = pd.DataFrame(data_list)
    df.to_excel(writer, sheet_name=name, index=False, header=False)
    # print(table)

writer._save()