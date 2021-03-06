# Simple reader for Google Sheets exported to HTML

import bs4

def encode(tag):
    if isinstance(tag, bs4.NavigableString):
        return tag.encode('utf8').replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    else:
        return tag.encode('utf8')

def read_sheet(filename):
    with open(filename) as infile:
        soup = bs4.BeautifulSoup(infile.read())
    [table] = soup.find_all('tbody')
    result = []
    for tr in table.find_all('tr'):
        row = []
        for td in tr.find_all(['td']):
            # The border between the header rows/columns and body
            # are actually little tds
            if 'freezebar-cell' in td['class']: continue
            # No idea what this is, but delete it
            for div in td.find_all("div", class_="softmerge-inner"):
                div.replaceWithChildren()
            cell = ''.join(map(encode, td.contents))
            # Fix what appears to be a bug in Google Sheets
            cell = cell.replace('\n', '<br>')
            row.append(cell)
        if row: result.append(row)

    return result
