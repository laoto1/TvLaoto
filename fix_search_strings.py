import re

def update_strings(filepath, new_strings):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # insert before </resources>
    content = content.replace("</resources>", new_strings + "\n</resources>")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

vi_strings = """    <string name="search_title">TÌM KIẾM KÊNH</string>
    <string name="search_placeholder">Nhập tên kênh (ví dụ: VTV1, HTV, Thể thao)...</string>
    <string name="search_submit">XEM KẾT QUẢ</string>"""

en_strings = """    <string name="search_title">SEARCH CHANNELS</string>
    <string name="search_placeholder">Enter channel name (e.g., HBO, ESPN, News)...</string>
    <string name="search_submit">VIEW RESULTS</string>"""

update_strings('app/src/main/res/values-vi/strings.xml', vi_strings)
update_strings('app/src/main/res/values/strings.xml', en_strings)
print("Updated strings.xml with search strings")
