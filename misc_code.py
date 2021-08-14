# Generate HTML file
f = open('bse.html', 'w')
html_template = """
<html>
<head>BSE Announcements</head>
<body>
<p>BSE Announcements</p>
<table>
    <tr>
        <th>{}</th>
    </tr>
    <tr>
        <td>{}</td>
    </tr>
</table>
</body>
</html>
"""
col = "Hello"
f.write(html_template.format(col, col))
f.close()
webbrowser.open('bse.html')



# Selecting the Web Browser for Automation
web = webbrowser.get(using=None) # web is a webbrowser object
defaultweb = vars(web)['name']
print(defaultweb)
if defaultweb == 'firefox':
    driver = firefoxdriver
elif defaultweb == 'chrome':
    driver = chromedriver
elif driver == 'safari':
    driver = safari
#web.open("screener.in")

# Exchange Time DATA
exc_time = ["Exchange Received Time", "Ex Disseminated Time", "Time Taken"]

for c in range(1, 2):
    try:
        columns = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div[3]/div/div/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[4]/td/table[{}]/tbody/tr[2]/td/b[{}]'.format(str(r), str(c))).text
        column_info.append(columns)
    except Exception as e:
        print(e)
