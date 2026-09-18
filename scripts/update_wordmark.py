import re

# 1. Update index.html
index_path = 'www.alethia.earth/index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

svg_pattern = r'<svg width="1384" height="322" viewBox="0 0 1384 322" fill="none" id="svg-955778784_3154">.*?</svg>'
new_svg = (
    '<svg width="1384" height="322" viewBox="0 0 1384 322" fill="none" id="svg-955778784_3154">\n'
    '<text x="692" y="240" text-anchor="middle" font-family="\'Plus Jakarta Sans\', -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, sans-serif" font-size="250" font-weight="700" fill="#D5EEBC" letter-spacing="0.06em">PRAKRITI</text>\n'
    '</svg>'
)

if re.search(svg_pattern, html, re.DOTALL):
    html = re.sub(svg_pattern, new_svg, html, count=1, flags=re.DOTALL)
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Updated index.html svg-955778784_3154 successfully.")
else:
    print("Checked index.html (already updated or matching).")

# 2. Update script_main.CPsdJQ5r.mjs
mjs_path = 'framerusercontent.com/sites/6AN2yDPkGAirmFqcg2kbn3/script_main.CPsdJQ5r.mjs'
with open(mjs_path, 'r', encoding='utf-8') as f:
    mjs = f.read()

# Update A=()=>g==="Jqc8zl2f2" and ne=()=>g!=="Jqc8zl2f2"
mjs = mjs.replace('A=()=>g===`Jqc8zl2f2`,ne=()=>g!==`Jqc8zl2f2`', 'A=()=>!1,ne=()=>!0')

idx_start = mjs.find('intrinsicWidth:1384,layoutDependency:D,layoutId:`N6pw9HjCS`,svg:`<svg width="1384" height="322"')
if idx_start != -1:
    idx_end = mjs.find('withExternalLayout', idx_start)
    old_block = mjs[idx_start:idx_end]
    new_block = (
        'intrinsicWidth:1384,layoutDependency:D,layoutId:`N6pw9HjCS`,svg:`<svg width="1384" height="322" viewBox="0 0 1384 322" fill="none" xmlns="http://www.w3.org/2000/svg">\\n'
        '<text x="692" y="240" text-anchor="middle" font-family="\'Plus Jakarta Sans\', -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, sans-serif" font-size="250" font-weight="700" fill="#D5EEBC" letter-spacing="0.06em">PRAKRITI</text>\\n'
        '</svg>\\n`,'
    )
    mjs = mjs[:idx_start] + new_block + mjs[idx_end:]
    with open(mjs_path, 'w', encoding='utf-8') as f:
        f.write(mjs)
    print("Updated script_main.CPsdJQ5r.mjs successfully.")
else:
    print("Checked script_main.CPsdJQ5r.mjs (already updated or not found).")

# 3. Update gXbnnzqqN.js
gx_path = 'framerusercontent.com/sites/6AN2yDPkGAirmFqcg2kbn3/https/framerusercontent.com/modules/7HH7w3Vp5VLoUtBw66f7/tIajzIluFNbxLoujxvW7/gXbnnzqqN.js'
with open(gx_path, 'r', encoding='utf-8') as f:
    gx = f.read()

idx_start_gx = gx.find('intrinsicWidth: 1384,\n                        layoutDependency: layoutDependency,\n                        layoutId: "N6pw9HjCS",\n                        svg:')
if idx_start_gx != -1:
    idx_end_gx = gx.find('withExternalLayout', idx_start_gx)
    new_gx_block = (
        'intrinsicWidth: 1384,\n'
        '                        layoutDependency: layoutDependency,\n'
        '                        layoutId: "N6pw9HjCS",\n'
        '                        svg: \'<svg width="1384" height="322" viewBox="0 0 1384 322" fill="none" xmlns="http://www.w3.org/2000/svg">\\n'
        '<text x="692" y="240" text-anchor="middle" font-family="\\\'Plus Jakarta Sans\\\', -apple-system, BlinkMacSystemFont, \\\'Segoe UI\\\', Roboto, sans-serif" font-size="250" font-weight="700" fill="#D5EEBC" letter-spacing="0.06em">PRAKRITI</text>\\n'
        '</svg>\\n\',\n                        '
    )
    gx = gx[:idx_start_gx] + new_gx_block + gx[idx_end_gx:]
    with open(gx_path, 'w', encoding='utf-8') as f:
        f.write(gx)
    print("Updated gXbnnzqqN.js successfully.")
else:
    print("Checked gXbnnzqqN.js (already updated or not found).")
