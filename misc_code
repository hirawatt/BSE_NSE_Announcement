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


# Form Buttons for BSE Announcements Input
segment = st.selectbox("Segment", segments, index=2)
from_date = st.date_input('From Date', max_value=date.today())
to_date = st.date_input('To Date', max_value=date.today())
button = st.form_submit_button("Submit")

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


df1['PDF'] = df1['PDF'].apply(lambda pdf_links: '<a href="https://bseindia.com{}">pdf link</a>'.format(pdf_links))
def create_clickable_id(id):
    url_template= '''<a href="../../link/to/{id}" target="_blank">{id}</a>'''.format(id=id)
    return url_template
