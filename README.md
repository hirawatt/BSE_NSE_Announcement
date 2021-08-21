# :coffee: BSE_Announcements
[BSE Announcements](https://www.bseindia.com/corporates/ann.html) page simplified and for better and easier access to Company Announcements. It is being tested only on Linux so far, but aims for full Winows and Mac support. Contributions Welcome!

![7e44b8f4b21c673029d1d0a407e4eaa0.png](:/294c410d76444a70b902fe1f551c5256)

## Table of contents
- [Installation](#installation)
- [Roadmap](#roadmap)
- [Development](#development)

## Installation
- Install [Python](https://www.python.org/downloads/) for your Operating System from the required link.
- Download [this file](https://github.com/hirawatt/BSE_NSE_Announcement/archive/refs/heads/master.zip) and extract files.
- Open Terminal/Command Prompt from the Extracted Folder.
- Run the commands below
```bash
pip install -r requirements.txt
streamlit run st_app.py
```
## Roadmap
-  Support for
	-  Browsers
		- [x] Firefox
		- [ ] Chrome
		- [ ] Safari
	-  Operating System
		- [x] Linux
		- [ ] Mac
		- [ ] Windows
- [ ] Auto Reload after a specific time
- [ ] Show unread/new links seperately
- [ ] Create a Watchlist of Companies
- [ ] Desktop Notification for Watchlist Company Results
## Development
Contributions are very welcome! Project structure:
- `st_app.py` - Streamlit App File
- `/data` - Data Files to be stored
- `/drivers` - Browser Drivers to be installed
