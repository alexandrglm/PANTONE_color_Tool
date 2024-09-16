import json
import os

def generate_html(colors, output_path):
    if not output_path or os.path.dirname(output_path) == '':
        raise ValueError("Output path is invalid. Please provide a valid path.")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w') as file:
        file.write('<!DOCTYPE html>\n')
        file.write('<html lang="en">\n')
        file.write('<head>\n')
        file.write('  <meta charset="UTF-8">\n')
        file.write('  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
        file.write('  <title>Pantone Cards Viewer</title>\n')
        file.write('  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap">\n')
        file.write('  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&display=swap">\n')
        file.write('  <style>\n')
        file.write('    body { font-family: "Roboto", sans-serif; background-color: #f0f0f0; margin: 0; padding: 20px; }\n')
        file.write('    header { text-align: center; margin-bottom: 20px; }\n')
        file.write('    .search-bar input { padding: 10px; width: 50%; font-size: 16px; border: 1px solid #ccc; border-radius: 4px; margin-bottom: 10px; }\n')
        file.write('    .controls { text-align: center; margin-bottom: 20px; }\n')
        file.write('    .controls button { padding: 10px 20px; font-size: 16px; margin: 0 10px; cursor: pointer; }\n')
        file.write('    .selected-colors { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin-bottom: 20px; }\n')
        file.write('    .selected-color { width: 100px; height: 100px; border: 2px solid #ccc; cursor: pointer; position: relative; }\n')
        file.write('    .selected-color:hover { border-color: #000; }\n')
        file.write('    .selected-color .remove { position: absolute; top: 2px; right: 2px; background: #fff; border: 1px solid #ccc; border-radius: 50%; cursor: pointer; padding: 2px; }\n')
        file.write('    .grid-container { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; justify-items: center; margin-top: 20px; }\n')
        file.write('    .card { width: 200px; height: 250px; background-color: white; box-shadow: 0 4px 8px rgba(0,0,0,0.2), 0 0 15px rgba(255,255,255,0.7) inset; display: flex; flex-direction: column; justify-content: flex-end; border-radius: 10px; position: relative; overflow: hidden; }\n')
        file.write('    .color-block { height: 60%; display: flex; align-items: center; justify-content: center; font-size: 18px; font-weight: bold; color: #fff; cursor: pointer; border-bottom: 1px solid rgba(0,0,0,0.1); position: relative; z-index: 1; }\n')
        file.write('    .color-block::after { content: \'\'; position: absolute; bottom: 0; left: 0; width: 100%; height: 50px; background: linear-gradient(to top, rgba(255,255,255,0.6), rgba(255,255,255,0)); z-index: -1; }\n')
        file.write('    .card-info { height: 40%; padding: 10px; text-align: center; background-color: #fff; border-top: 1px solid #ddd; }\n')
        file.write('    .pantone-family { font-family: "Playfair Display", serif; font-size: 16px; font-weight: bold; margin: 5px 0; color: #000; text-transform: capitalize; }\n')
        file.write('    .pantone-name { font-size: 14px; margin: 5px 0; color: #555; text-transform: capitalize; }\n')
        file.write('    .pantone-hex { font-size: 16px; margin: 5px 0; color: #555; }\n')
        file.write('    .pantone-cmyk { font-size: 14px; margin: 5px 0; color: #555; }\n')
        file.write('    .pantone-cmyk span { display: inline; }\n')
        file.write('  </style>\n')
        file.write('</head>\n')
        file.write('<body>\n')

        file.write('  <header>\n')
        file.write('    <div class="search-bar">\n')
        file.write('      <input type="text" id="search" placeholder="Search by name, number, or code...">\n')
        file.write('    </div>\n')
        file.write('  </header>\n')

        file.write('  <div class="controls">\n')
        file.write('    <div class="selected-colors" id="selectedColors"></div>\n')
        file.write('    <button id="savePNG">Save as PNG</button>\n')
        file.write('    <button id="resetSelection">Reset</button>\n')
        file.write('  </div>\n')

        file.write('  <div class="grid-container" id="cardContainer">\n')

        for code, color in colors.items():
            hex_code = f'#{color["hex"].upper()}'
            family = color["name"]
            name = code
            cmyk = color.get("cmyk", [0.0, 0.0, 0.0, 0.0])

            if len(cmyk) != 4:
                cmyk = [0.0, 0.0, 0.0, 0.0]

            cmyk_percent = [f"{val:.1f}%" for val in cmyk]

            file.write(f'    <div class="card" data-name="{name}" data-family="{family}" data-hex="{hex_code}" data-cmyk="{",".join(cmyk_percent)}">\n')
            file.write(f'      <div class="color-block" style="background-color: {hex_code};" data-clipboard-text="{hex_code}" title="Click to copy {hex_code}">\n')
            file.write('      </div>\n')
            file.write('      <div class="card-info">\n')
            file.write(f'        <p class="pantone-family">PANTONE {family}</p>\n')
            file.write(f'        <p class="pantone-name">{name}</p>\n')
            file.write(f'        <p class="pantone-hex">{hex_code}</p>\n')
            file.write(f'        <p class="pantone-cmyk">C: <span>{cmyk_percent[0]}</span> M: <span>{cmyk_percent[1]}</span> Y: <span>{cmyk_percent[2]}</span> K: <span>{cmyk_percent[3]}</span></p>\n')
            file.write('      </div>\n')
            file.write('    </div>\n')

        file.write('  </div>\n')

        file.write('<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>\n')
        file.write('<script>\n')

        file.write('let selectedColors = [];\n')

        file.write('function updateSelectedColors() {\n')
        file.write('  const container = document.getElementById("selectedColors");\n')
        file.write('  container.innerHTML = "";\n')
        file.write('  selectedColors.forEach(color => {\n')
        file.write('    const colorDiv = document.createElement("div");\n')
        file.write('    colorDiv.classList.add("selected-color");\n')
        file.write('    colorDiv.style.backgroundColor = color.hex;\n')
        file.write('    colorDiv.innerHTML = "<div class=\'remove\'>&times;</div>";\n')
        file.write('    colorDiv.addEventListener("click", () => {\n')
        file.write('      selectedColors = selectedColors.filter(c => c.hex !== color.hex);\n')
        file.write('      updateSelectedColors();\n')
        file.write('    });\n')
        file.write('    container.appendChild(colorDiv);\n')
        file.write('  });\n')
        file.write('}\n')

        file.write('function handleCardClick(event) {\n')
        file.write('  const card = event.currentTarget;\n')
        file.write('  const color = {\n')
        file.write('    name: card.dataset.name,\n')
        file.write('    family: card.dataset.family,\n')
        file.write('    hex: card.dataset.hex,\n')
        file.write('    cmyk: card.dataset.cmyk.split(",").map(val => parseFloat(val))\n')
        file.write('  };\n')
        file.write('  if (!selectedColors.find(c => c.hex === color.hex)) {\n')
        file.write('    selectedColors.push(color);\n')
        file.write('    updateSelectedColors();\n')
        file.write('  }\n')
        file.write('}\n')

        file.write('document.querySelectorAll(".card").forEach(card => {\n')
        file.write('  card.addEventListener("click", handleCardClick);\n')
        file.write('});\n')

        file.write('document.getElementById("resetSelection").addEventListener("click", () => {\n')
        file.write('  selectedColors = [];\n')
        file.write('  updateSelectedColors();\n')
        file.write('});\n')

        file.write('document.getElementById("savePNG").addEventListener("click", () => {\n')
        file.write('  html2canvas(document.getElementById("cardContainer")).then(canvas => {\n')
        file.write('    const link = document.createElement("a");\n')
        file.write('    link.href = canvas.toDataURL("image/png");\n')
        file.write('    link.download = "pantone_cards.png";\n')
        file.write('    link.click();\n')
        file.write('  });\n')
        file.write('});\n')

        file.write('document.getElementById("search").addEventListener("input", function() {\n')
        file.write('  const query = this.value.toLowerCase();\n')
        file.write('  document.querySelectorAll(".card").forEach(card => {\n')
        file.write('    const name = card.dataset.name.toLowerCase();\n')
        file.write('    const family = card.dataset.family.toLowerCase();\n')
        file.write('    const hex = card.dataset.hex.toLowerCase();\n')
        file.write('    const matches = name.includes(query) || family.includes(query) || hex.includes(query);\n')
        file.write('    card.style.display = matches ? "block" : "none";\n')
        file.write('  });\n')
        file.write('});\n')

        file.write('</script>\n')
        file.write('</body>\n')
        file.write('</html>\n')

pantone_file_path = './engine/pantone-html-cmyk.json'
output_path = './output/PANTONE_CHART_Viewer_0001.html'

with open(pantone_file_path) as f:
    pantone_data = json.load(f)

generate_html(pantone_data, output_path)
