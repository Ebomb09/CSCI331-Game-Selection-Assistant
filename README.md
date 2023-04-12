# Game Selection Assistant

An online library of games, representing a user’s collection, that they can use to determine what they wish to play next.

## Installation
1. Clone the repository
2. Create and activate a python virtual environment
```bash
python3 -m venv .
source bin/activate
```
3. Install the project requirements
```bash
pip install -r requirements.txt
```
4. Initialize gsa
```
flask --app gsa init-db
```

## Usage
Activate the virtual environment and run the flask command.
```bash
flask --app gsa run
```

## Technologies
Game Selection Assistant makes use of some python libraries to implement functionality.
* [howlongtobeatpy](https://pypi.org/project/howlongtobeatpy)
	* Retrieve game info and search for game function
* [flask](https://pypi.org/project/Flask)
	* Host web interface
* [requests](https://pypi.org/project/requests)
	* Make requests to HowLongToBeat and retrieve game's page listing
* [beautifulsoup4](https://pypi.org/project/beautifulsoup4)
	* Parse requests data from HowLongToBeat into game tags and description
* [sqlite3](https://docs.python.org/3/library/sqlite3.html)
	* Cache game data and user account / game storage
