import json
import os

def generate_html(colors, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w') as file:
        file.write('<!DOCTYPE html>\n')
        file.write('<html lang="en">\n')
        file.write('<head>\n')
        file.write('  <meta charset="UTF-8">\n')
        file.write('  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
        file.write('  <title>Pantone Cards Viewer</title>\n')
        file.write('  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap">\n')
        file.write('  <style>\n')
        file.write('    body { font-family: "Roboto", sans-serif; background-color: #f0f0f0; margin: 0; padding: 20px; }\n')
        file.write('    header { text-align: center; margin-bottom: 20px; }\n')
        file.write('    .search-bar input { padding: 10px; width: 50%; font-size: 16px; border: 1px solid #ccc; border-radius: 4px; margin-bottom: 10px; }\n')
        file.write('    #htmlCodeDisplay { padding: 10px; width: 50%; font-size: 16px; border: 1px solid #ccc; border-radius: 4px; background-color: #fff; }\n')
        file.write('    .grid-container { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; justify-items: center; }\n')
        file.write('    .card { width: 200px; height: 300px; background-color: white; box-shadow: 0 4px 8px rgba(0,0,0,0.2); display: flex; flex-direction: column; justify-content: flex-end; }\n')
        file.write('    .color-block { height: 60%; display: flex; align-items: center; justify-content: center; font-size: 18px; font-weight: bold; color: #fff; cursor: pointer; }\n')
        file.write('    .card-info { height: 40%; padding: 10px; text-align: center; background-color: #fff; border-top: 1px solid #ddd; }\n')
        file.write('    .pantone-family { font-size: 16px; font-weight: bold; margin-bottom: 5px; color: #000; }\n')
        file.write('    .pantone-name { font-size: 14px; margin: 5px 0; color: #555; }\n')
        file.write('    .pantone-hex { font-size: 16px; margin: 5px 0; color: #555; }\n')
        file.write('    .selected-colors { display: flex; justify-content: center; gap: 10px; margin-bottom: 10px; flex-wrap: wrap; }\n')
        file.write('    .selected-color-box { width: 100px; height: 100px; border: 1px solid #ccc; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: bold; }\n')
        file.write('  </style>\n')
        file.write('</head>\n')
        file.write('<body>\n')

        file.write('  <header>\n')
        file.write('    <div class="selected-colors" id="selectedColors">\n')
        for _ in range(7):
            file.write('      <div class="selected-color-box" data-hex=""></div>\n')
        file.write('    </div>\n')
        file.write('    <div class="search-bar">\n')
        file.write('      <input type="text" id="search" placeholder="by name, by number, by code, ....">\n')
        file.write('    </div>\n')
        file.write('    <div>\n')
        file.write('      <input type="text" id="htmlCodeDisplay" readonly placeholder="Click to copy code...">\n')
        file.write('    </div>\n')
        file.write('    <div>\n')
        file.write('      <button onclick="saveAsPNG()">Save as PNG</button>\n')
        file.write('      <button onclick="resetSelection()">Reset charset</button>\n')
        file.write('    </div>\n')
        file.write('  </header>\n')

        file.write('  <div class="grid-container" id="cardContainer">\n')

        for code, color in colors.items():
            hex_code = f'#{color["hex"]}'
            family = code
            name = color["name"]

            file.write(f'    <div class="card" data-name="{name}" data-family="{family}" data-hex="{hex_code}">\n')
            file.write(f'      <div class="color-block" style="background-color: {hex_code};" data-clipboard-text="{hex_code}" title="Click to copy {hex_code}">\n')
            file.write('      </div>\n')
            file.write('      <div class="card-info">\n')
            file.write(f'        <p class="pantone-family">PANTONE {family}</p>\n')
            file.write(f'        <p class="pantone-name">{name}</p>\n')
            file.write(f'        <p class="pantone-hex">{hex_code}</p>\n')
            file.write('      </div>\n')
            file.write('    </div>\n')

        file.write('  </div>\n')

        file.write('<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>\n')
        file.write('<script>\n')

        file.write('document.getElementById("search").addEventListener("input", function() {\n')
        file.write('  var filter = this.value.toLowerCase();\n')
        file.write('  var cards = document.querySelectorAll(".card");\n')
        file.write('  cards.forEach(function(card) {\n')
        file.write('    var name = card.getAttribute("data-name").toLowerCase();\n')
        file.write('    var family = card.getAttribute("data-family").toLowerCase();\n')
        file.write('    var hex = card.getAttribute("data-hex").toLowerCase();\n')
        file.write('    if (name.includes(filter) || family.includes(filter) || hex.includes(filter)) {\n')
        file.write('      card.style.display = "flex";\n')
        file.write('    } else {\n')
        file.write('      card.style.display = "none";\n')
        file.write('    }\n')
        file.write('  });\n')
        file.write('});\n')

        file.write('document.querySelectorAll(".color-block").forEach(function(block) {\n')
        file.write('  block.addEventListener("click", function() {\n')
        file.write('    var hexValue = this.getAttribute("data-clipboard-text");\n')
        file.write('    var selectedColors = document.querySelectorAll(".selected-color-box");\n')
        file.write('    var hexExists = false;\n')

        file.write('    selectedColors.forEach(function(box) {\n')
        file.write('      if (box.getAttribute("data-hex") === hexValue) {\n')
        file.write('        hexExists = true;\n')
        file.write('      }\n')
        file.write('    });\n')

        file.write('    if (!hexExists) {\n')
        file.write('     \n')
        file.write('      var added = false;\n')
        file.write('      selectedColors.forEach(function(box) {\n')
        file.write('        if (!box.getAttribute("data-hex") && !added) {\n')
        file.write('          box.style.backgroundColor = hexValue;\n')
        file.write('          box.setAttribute("data-hex", hexValue);\n')
        file.write('          box.innerHTML = hexValue;\n')
        file.write('          added = true;\n')
        file.write('        }\n')
        file.write('      });\n')
        file.write('    }\n')

        file.write('    document.getElementById("htmlCodeDisplay").value = hexValue;\n')
        file.write('  });\n')
        file.write('});\n')

        file.write('function saveAsPNG() {\n')
        file.write('  html2canvas(document.body).then(function(canvas) {\n')
        file.write('    var link = document.createElement("a");\n')
        file.write('    link.href = canvas.toDataURL("image/png");\n')
        file.write('    link.download = "pantone_colors.png";\n')
        file.write('    link.click();\n')
        file.write('  });\n')
        file.write('}\n')

        file.write('function resetSelection() {\n')
        file.write('  var selectedColors = document.querySelectorAll(".selected-color-box");\n')
        file.write('  selectedColors.forEach(function(box) {\n')
        file.write('    box.style.backgroundColor = "white";\n')
        file.write('    box.setAttribute("data-hex", "");\n')
        file.write('    box.innerHTML = "";\n')
        file.write('  });\n')
        file.write('  document.getElementById("htmlCodeDisplay").value = "Click to copy code ...";\n')
        file.write('}\n')

        file.write('</script>\n')
        file.write('</body>\n')
        file.write('</html>\n')

if __name__ == "__main__":
    with open('./pantone-colors/pantone-numbers.json') as f:
        data = json.load(f)
    generate_html(data, './PANTONE_Card_Tool.html')
