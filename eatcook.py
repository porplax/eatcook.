# Import required modules.
import socket
import typer
import os
import json
import subprocess

# Import functions, classes from required modules.
from colorama import Fore, Back, Style
from email.parser import BytesParser

# Stores routes and what to do with client urls.
routebook = {}

# Adds to routebook. Although, Ugly way of doing so. And just a stupid function. But hey, the option's there.
def add_route(request, dest):
    routebook[request] = dest
    return routebook

def run(host,port,folder):
    main(host,port,folder)


# Where the main action happens. (😎)
def main(host:str=None,port:int=None,folder:str=None):
    # Instead of printing to terminal on the go, append to list then omit each element of the list.
    global data, routebook
    out = []



    # Create the socket object.
    s = socket.socket()
    # If folder is not specified, use user script's directory.
    if folder is None: out.append(Fore.LIGHTYELLOW_EX + "[NOTE]: Using script directory (Folder argument is empty)."); folder = "./" # Opinion: One-liners rocks.
    # Clear the terminal. If the operating system is Windows: Use 'clear', else use 'cls'.
    if os.name == "posix": os.system("clear")
    else: os.system("cls")
    # If host passes, check if the port is valid.
    if host == None: out.append(Fore.YELLOW + "[WARNING]: Host was not specified. Using 127.0.0.1 instead."); host = "127.0.0.1"
    else: pass
    # If port passes, check if the port is valid.
    if port == None: out.append(Fore.YELLOW + "[WARNING]: Port number was not specified. Using :8000 instead."); port = 8000
    else: pass

    # Define routebook.
    try:
        with open(f'{folder}routebook.json', 'r') as f:
            routebook = json.load(f)
    except:
        print(Fore.RED + "[ERROR]: Could not find routes file. ")
        print(Fore.RESET)

    address = (host,port)
    out.append(Fore.GREEN + f"[SERVER]: Using {host} as host.")
    out.append(Fore.GREEN + f"[SERVER]: Listening on :{port}")

    # Bind the server.
    s.bind(address)
    out.append(Fore.GREEN + f"[SERVER]: Successfully binded the socket.")

    # Put the server into listening mode.
    s.listen(5)
    for i in out:
        print(i)
    print(Fore.RESET)
    err = 0
    s.setblocking(True)
    # Start the loop. This responds to client requests.
    while True:
        client, address = s.accept()
        print(f"[INFO]: Got request from {address}.")

        # Receive request. Extremely inefficient parser to get client's url. (🧍‍)
        headers = BytesParser().parsebytes(client.recv(4096))
        headers = str(headers)
        indexed = headers.find('/')
        to_remove = headers[:indexed]
        headers = headers.replace(to_remove, '')
        indexed = headers.find(' ')
        url = headers[:indexed] # This 7 lines of code right here took me over an hour to figure out. I just want to die.

        err = 0
        c = 0
        request = ""
        data = None
        for i in routebook:
            if url == "/favicon.ico": break # This is an odd, common request ;-;
            if url == i:
                file = f'{folder}{routebook[i]}'
                if routebook[i].endswith('.py'):
                    try: data = subprocess.run(['python', f'{folder}{routebook[i]}'], check=True, capture_output=True, text=True).stdout
                    except: print(Fore.RED + f"[ERROR] Couldn't run {routebook[i]}")
                    request = i # Self-note: VERY IMPORTANT!!!
                    continue
                try:
                    with open(file, 'r') as f:
                        data = f.read()
                except:
                    print(Fore.RED + f"[ERROR]: Got request from {address} but couldn't find the appropriate file to respond with.")
                    print(Fore.RESET)
                    err = 500
                    data = """
                    <body style="background-color: black;">
                    <h1 align='center' style='font-family: Arial; color: white;'>eatcook.</h1>
                    <p align='center' style='font-family: Arial; color: white;'>Error: Server misconfiguration.</p>
                    </body>
                    """
                request = i


        # 404 response.
        if request != url and err != 500 and url != "/favicon.ico":

            file = f'{folder}404.html'
            try:
                with open(file, 'r') as f:
                    data = f.read()
            except:
                print(Fore.YELLOW + f"[WARNING]: No 404 file found for {address}'s incorrect request ({url}).")
                print(Fore.RESET)
                data = f"""
                <body style="background-color: black;">
                    <h1 align='center' style='font-family: Arial; color: white;'>eatcook.</h1>
                    <p align='center' style='font-family: Arial; color: white;'>Error: 404. Couldn't find {url}</p>
                    </body>
                                    """




        # Sends response.
        client.send('HTTP/1.1 200 OK\r\n'.encode())
        client.send('Content-type: text/html\n'.encode())
        # Send the html page.
        client.send(f"""
    {data}
\n""".encode())

        # Close the client.
        client.close()


if __name__ == '__main__':
    typer.run(main)