from bs4 import BeautifulSoup

with open('pantone-colors.html', 'r') as file:
    soup = BeautifulSoup(file, 'html.parser')

cells = soup.find_all('td')

with open('pantone_colors.txt', 'w') as file:
    for i in range(0, len(cells), 2):
        color_name = cells[i].get('class', [''])[0]
        color_code = cells[i].get('data-clipboard-text', '')

        file.write(f"{color_name} - {color_code}\n")

print("Data saved at pantone_colors.txt")
