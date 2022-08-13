<img src="https://u.cubeupload.com/ihavecandy/eatcook.png">

# eatcook.
```python
pip install eatcook
```

Eatcook is a simple socket HTTP server. With the ablity to run python files at interpret them as html. (Like CGI)
The server also provides a extremely easy way to create sub pages. Using `routebook.json` to redirect users to them

`routebook.json:`
```json
{
  "/", "index.html"  
}
```
OR 
```json
{
  "/", "index.py"
}
```

To get 404 page, place a file named `404.html` in the folder in which you're running in.
# Running at CLI
```
py -m eatcook --host 127.0.0.1 --port 8000 --folder (where http files are located)
```
Host & Port will run at 127.0.0.1:8000 by default if none are given.

Folder will also run in the directory of which you're working in if none are given: `./`

# Running in python
```py
import eatcook

eatcook.run(host, port, folder) # Runs eatcook.
eatcook.add_route("/", "index.html") # Adds to script's route dict if no routebook.json is found. Though, it's much recommended to just use routebook.json
```

To run python scripts as html:
```py
import random

generated = random.randint(1,100000)
print(f"<h1 align='center'>{generated}</h1>") # Sends a generated number to client's browser.
```
