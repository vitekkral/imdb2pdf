from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('imdb2pdf.html')


@app.route('/link', methods=['POST'])
def get_link():
    imdb = request.form.get('imdb_link')
    return render_template('imdb2pdf.html', imdb_res=imdb_scrape(imdb))


def imdb_scrape(imdb_link_in):
    from bs4 import BeautifulSoup as BS
    import requests

    r = requests.get(imdb_link_in)
    soup = BS(r.text, "html.parser")
    imdb_filmography = soup.find_all('div', {'class': 'filmo-category-section'})
    title = str(soup.find("title").text)
    credit_list = {'credit list': title}

    for role in imdb_filmography:  # pozice u filmu
        item_in_role = role.find_all('div')
        for each_item in item_in_role:  # jednotlive filmy
            production_statut = each_item.find('a', {'class': 'in_production'})  # in production?
            name_tagged = each_item.find('b')
            try:
                if name_tagged is not None:
                    name = str(name_tagged.text).strip()
                    year_tagged = each_item.find('span')
                    year_tagged.text.strip()
                    year = (str(year_tagged.text).strip())[:4]
                    if year is '':
                        year = 'year n/a'
                        if production_statut is not None:  # if in production
                            year = 'filming'
                    if year in credit_list.keys():
                        temp_val = credit_list.pop(year)
                        temp_val.append(name)
                        credit_list[year] = temp_val
                    else:
                        credit_list[str(year)] = [str(name)]
            except AttributeError:
                pass
    return credit_list


app.run(port=3336, debug=True)


if __name__ == "__main__":
    main()
