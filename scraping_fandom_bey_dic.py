from utils import Utils
import pandas as pd
from pathlib import Path


utils = Utils()
# path_choiced = utils.wx_dirdialog()
# driver = utils.init_webdriver(default=True, headless=False, output=path_choiced)
# driver.get("https://beyblade.fandom.com/wiki/List_of_Basic_Line_parts")
urls = {
    "tabelas_beyblade_bx": "https://beyblade.fandom.com/wiki/List_of_Basic_Line_parts",
    "tabelas_beyblade_ux": "https://beyblade.fandom.com/wiki/List_of_Unique_Line_parts",
    "tabelas_beyblade_cx": "https://beyblade.fandom.com/wiki/List_of_Custom_Line_parts",
}
index = 0
# percorrer as urls
for name, url in urls.items():
    site = utils.web_scrape(url=url)
    table_elements = site.find_all("table", class_="wikitable")
    tables = {}
    # percorrer as tabelas
    for table in table_elements:
        previous_sibling = table.previous_sibling
        while previous_sibling and previous_sibling.name is None:
            previous_sibling = previous_sibling.previous_sibling
        heading = previous_sibling.text
        tables.update({heading: table})
    writer = pd.ExcelWriter(f"{name}.xlsx", engine="xlsxwriter")
    # percorrer as informações das tabelas
    for table_name, table in tables.items():
        data_dic = {}

        if table.find("th"):
            if table_name == "Assist Blades":
                columns = ["Abbr.", "Image", "Name"]
            else:
                columns = [
                    x.text.strip()
                    for x in table.find_all("th")
                    # ignorar outros cabeçalhos
                    if x.text.strip() != "Jurassic World"
                    and x.text.strip() != "Marvel"
                    and x.text.strip() != "Star Wars"
                    and x.text.strip() != "Transformers"
                ]
        # atualiza dicionario com os nome das colunas
        data_dic.update({x: [] for x in columns if x not in data_dic.keys()})
        if (
            data_dic.get("Image Path") is None
            and data_dic.get(f"Link {table_name}") is None
        ):
            # adiciona ao dicionario a coluna que contem link da parte da bey
            data_dic.update({f"Link {table_name}": []})
            # adiciona ao dicionario a coluna que contem caminho da imagem
            data_dic.update({f"Image Path": []})


        for element in table.find_all("tr"):
            # ignorar cabeçalhos
            if element.find("th") and table_name != "Assist Blades":
                continue
            if index == 0 and table_name == "Assist Blades":
                index = 1
                continue
            # obter imagem
            if element.img:
                # verificar se eh um link de imagem
                if "data:image" not in element.img.get("src"):
                    img_link = element.img.get("src")
                else:
                    img_a = element.find("a", class_="mw-file-description image")
                    if img_a:
                        img_link = img_a.get("href")
                    else:
                        img_link = "N/A"
            else:
                img_link = "N/A"
            # adicionar link da imagem ao dicionario
            data_dic.get("Image").append(img_link)
            # realizar criação de pastas
            source_dir = Path(__file__).parent / "downloads"
            source_dir.mkdir(exist_ok=True)
            download_dir = Path(source_dir / table_name)
            download_dir.mkdir(exist_ok=True)
            # verifica se link eh válido  e realiza download
            if img_link != "N/A":
                # adicionar caminho para imagem baixada ao dicionario
                file_name = utils.download_file(img_link, download_dir)
                data_dic.get("Image Path").append(f"%USERPROFILE%/Downloads/{table_name}/{file_name}")
            else:
                data_dic.get("Image Path").append("N/A")
            # obter link da bey
            link = element.find("a", class_="")
            if link:
                link_url = "https://beyblade.fandom.com" + link.get("href")
                data_dic.get(f"Link {table_name}").append(link_url)
            else:
                link_url = "N/A"
            # obter informações parte da bey
            data_line = [
                utils.separate_words_by_capitals(x.strip())
                for x in element.text.splitlines()
                if x
                if x != "File:Quetzalcoatlus.png" and x != "File:Spinosaurus.png"
            ]
            # verifica tamanho da beyblade para adicionar nome/abreviatura ao dicionario corretamente
            if len(data_line) == 1:
                if data_dic.get("Takara Tomy Name") and data_dic.get("Hasbro Name"):
                    data_dic.get("Takara Tomy Name").append(data_line[0])
                    data_dic.get("Hasbro Name").append(data_line[0])
                else:
                    data_dic.get("Name").append(data_line[0])
            else:
                if (
                    data_dic.get("Takara Tomy Name") is not None
                    and data_dic.get("Hasbro Name") is not None
                ):
                    data_dic.get("Takara Tomy Name").append(data_line[0])
                    data_dic.get("Hasbro Name").append(data_line[1])
                else:
                    data_dic.get("Abbr.").append(data_line[0])
                    data_dic.get("Name").append(data_line[1])
            # acessa link parte da bey
            if link_url != "N/A":
                new_site = utils.web_scrape(url=link_url)
                columns_stats = [
                    "Type",
                    "SpinDirection",
                    "Weight",
                    "System",
                    "AttackStat",
                    "DefenseStat",
                    "StaminaStat",
                    "BurstResistanceStat",
                    "DashStat",
                ]

                # atualiza dicionario com as infos, sendo cada info uma coluna
                data_dic.update({x: [] for x in columns_stats if x not in data_dic.keys()})
                type_bey = new_site.find(attrs={"data-source": "Type"})
                if type_bey:
                    type_bey = type_bey.a.text if type_bey.a else "N/A"
                else:
                    type_bey = "N/A"
                if data_dic.get("Type") is not None:
                    data_dic.get("Type").append(type_bey)
                spin = new_site.find(attrs={"data-source": "SpinDirection"})
                if spin:
                    spin = spin.a.text if spin.a else "N/A"
                else:
                    spin = "N/A"
                if data_dic.get("SpinDirection") is not None:
                    data_dic.get("SpinDirection").append(spin)
                weight = new_site.find(attrs={"data-source": "Weight"})
                if weight:
                    weight = weight.span.text if weight.span else "N/A"
                else:
                    weight = "N/A"
                weight = weight.replace("grams", "").strip()
                if data_dic.get("Weight") is not None:
                    data_dic.get("Weight").append(weight)
                system_bey = new_site.find(attrs={"data-source": "System"})
                if system_bey:
                    system_bey = system_bey.a.text if system_bey.a else "N/A"
                else:
                    system_bey = "N/A"
                if data_dic.get("System") is not None:
                    data_dic.get("System").append(system_bey)

                attack = new_site.find_all(
                    lambda tag: tag.name != "th"
                    and tag.has_attr("data-source")
                    and tag["data-source"] == "AttackStat"
                )
                if attack:
                    attack = attack[0].text if attack[0].text != "" else "N/A"
                else:
                    attack = "N/A"
                if data_dic.get("AttackStat") is not None:
                    data_dic.get("AttackStat").append(attack)
                defense = new_site.find_all(
                    lambda tag: tag.name != "th"
                    and tag.has_attr("data-source")
                    and tag["data-source"] == "DefenseStat"
                )
                if defense:
                    defense = defense[0].text if defense[0].text != "" else "N/A"
                else:
                    defense = "N/A"
                if data_dic.get("DefenseStat") is not None:
                    data_dic.get("DefenseStat").append(defense)
                stamina = new_site.find_all(
                    lambda tag: tag.name != "th"
                    and tag.has_attr("data-source")
                    and tag["data-source"] == "StaminaStat"
                )
                if stamina:
                    stamina = stamina[0].text if stamina[0].text != "" else "N/A"
                else:
                    stamina = "N/A"
                if data_dic.get("StaminaStat") is not None:
                    data_dic.get("StaminaStat").append(stamina)
                if table_name == "Bits":
                    dash = new_site.find_all(
                        lambda tag: tag.name != "th"
                        and tag.has_attr("data-source")
                        and tag["data-source"] == "DashStat"
                    )
                    if dash:
                        dash = dash[0].text if dash[0].text != "" else "N/A"
                    else:
                        dash = "N/A"
                    if data_dic.get("DashStat") is not None:
                        data_dic.get("DashStat").append(dash)
                    burst = new_site.find_all(
                        lambda tag: tag.name != "th"
                        and tag.has_attr("data-source")
                        and tag["data-source"] == "BurstResistanceStat"
                    )
                    if burst:
                        burst = burst[0].text if burst[0].text != "" else "N/A"
                    else:
                        burst = "N/A"
                    if data_dic.get("BurstResistanceStat") is not None:
                        data_dic.get("BurstResistanceStat").append(burst)

        data_dic = utils.fill_list_in_dictionary(data_dic)
        df = pd.DataFrame.from_dict(data_dic)
        df.to_excel(writer, sheet_name=table_name, index=False)

    writer._save()
