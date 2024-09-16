import json
import os

def load_colors_from_json(file_path):
    try:
        with open(file_path, 'r') as file:
            colors = json.load(file)
            return colors
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f'Error: {e}')
        return {}

def generate_html(colors, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w') as file:
        file.write('<!DOCTYPE html>\n')
        file.write('<html lang="en">\n')
        file.write('<head>\n')
        file.write('  <meta charset="UTF-8">\n')
        file.write('  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
        file.write('  <title>PANTONE to HTML colour converter tool v.0.1</title>\n')
        file.write('  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap">\n')
        file.write('  <style>\n')
        file.write('    body { font-family: "Roboto", sans-serif; margin: 0; padding: 0; }\n')
        file.write('    .container { width: 80%; margin: auto; padding: 20px; }\n')
        file.write('    h1 { font-size: 2em; margin-bottom: 20px; }\n')
        file.write('    input[type="text"] { width: calc(100% - 22px); padding: 10px; margin: 10px 0; font-size: 1em; }\n')
        file.write('    button { padding: 10px 15px; margin-right: 10px; cursor: pointer; font-size: 1em; }\n')
        file.write('    table { width: 100%; border-collapse: collapse; margin-top: 20px; }\n')
        file.write('    th, td { padding: 10px; text-align: left; border: 1px solid #ddd; }\n')
        file.write('    th { background-color: #f4f4f4; }\n')
        file.write('    .color-box { width: 100px; height: 100px; display: inline-block; margin: 5px; cursor: pointer; }\n')
        file.write('    .color-name { font-size: 1.2em; text-align: center; margin-top: 5px; cursor: pointer; }\n')
        file.write('    .hidden { display: none; }\n')
        file.write('  </style>\n')
        file.write('  <script src="https://cdnjs.cloudflare.com/ajax/libs/clipboard.js/2.0.8/clipboard.min.js"></script>\n')
        file.write('</head>\n')
        file.write('<body>\n')
        file.write('  <div class="container">\n')
        file.write('    <h1>PANTONE to HTML colour converter</h1>\n')
        file.write('    <input type="text" id="search" placeholder="....">\n')
        file.write('    <button onclick="sortTable(\'name\')">By name</button>\n')
        file.write('    <button onclick="sortTable(\'pantone\')">By Pantone order</button>\n')
        file.write('    <button onclick="sortTable(\'hex\')">By HTML code</button>\n')
        file.write('    <table id="pantoneTable">\n')
        file.write('      <thead>\n')
        file.write('        <tr>\n')
        file.write('          <th>PANTONE name</th>\n')
        file.write('          <th>HTML code</th>\n')
        file.write('          <th>Test</th>\n')
        file.write('        </tr>\n')
        file.write('      </thead>\n')
        file.write('      <tbody>\n')

        for key, color in colors.items():
            hex_code = f'#{color["hex"]}'
            file.write(f'        <tr>\n')
            file.write(f'          <td class="color-name" data-clipboard-text="{hex_code}">{color["name"]}</td>\n')
            file.write(f'          <td class="color-name" data-clipboard-text="{hex_code}">{hex_code}</td>\n')
            file.write(f'          <td><div class="color-box" style="background-color: {hex_code};" data-clipboard-text="{hex_code}"></div></td>\n')
            file.write(f'        </tr>\n')

        file.write('      </tbody>\n')
        file.write('    </table>\n')
        file.write('  </div>\n')
        file.write('  <script>\n')
        file.write('    document.getElementById("search").addEventListener("input", function() {\n')
        file.write('      let search = this.value.toLowerCase();\n')
        file.write('      let rows = document.querySelectorAll("#pantoneTable tbody tr");\n')
        file.write('      rows.forEach(row => {\n')
        file.write('        let name = row.children[0].textContent.toLowerCase();\n')
        file.write('        let hex = row.children[1].textContent.toLowerCase();\n')
        file.write('        if (name.includes(search) || hex.includes(search)) {\n')
        file.write('          row.classList.remove("hidden");\n')
        file.write('        } else {\n')
        file.write('          row.classList.add("hidden");\n')
        file.write('        }\n')
        file.write('      });\n')
        file.write('    });\n')
        file.write('    function sortTable(by) {\n')
        file.write('      let table = document.querySelector("#pantoneTable tbody");\n')
        file.write('      let rows = Array.from(table.querySelectorAll("tr"));\n')
        file.write('      rows.sort((a, b) => {\n')
        file.write('        let valA = a.children[by === "name" ? 0 : by === "pantone" ? 0 : 1].textContent.toLowerCase();\n')
        file.write('        let valB = b.children[by === "name" ? 0 : by === "pantone" ? 0 : 1].textContent.toLowerCase();\n')
        file.write('        return valA.localeCompare(valB);\n')
        file.write('      });\n')
        file.write('      rows.forEach(row => table.appendChild(row));\n')
        file.write('    }\n')
        file.write('    new ClipboardJS(".color-box, .color-name");\n')
        file.write('  </script>\n')
        file.write('</body>\n')
        file.write('</html>\n')

def main():
    input_path = './pantone-colors/pantone-numbers.json'
    output_path = './Pantone-Colour-Cart-tool.html'
    colors = load_colors_from_json(input_path)
    generate_html(colors, output_path)
    print(f'Color Chartset created at {output_path}')

if __name__ == '__main__':
    main()
