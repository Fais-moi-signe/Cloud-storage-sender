import tkinter as tk
from tkinter import filedialog
from tkinter import *
import os
from google.oauth2 import service_account
from google.cloud import storage
import ntpath

credentials = service_account.Credentials.from_service_account_file(os.getcwd() + "/credentials/fais-moi-signe-334414-b826e16e8f52.json")
cloud_client = storage.Client(project="fais-moi-signe-334414", credentials=credentials)
bucket = cloud_client.get_bucket("fms_animations_bucket")
file_path = None
name_id = None

def select_file():
    global file_path
    global name_id
    if 'name_id' in globals():
        canvas.delete(name_id)
    file_path = filedialog.askopenfilename()
    print(f"Le chemin du fichier sélectionné est: {file_path}")
    name_id = canvas.create_text(150, 20, text=ntpath.basename(file_path))

def send_file():
    global file_path
    global image_id
    global name_id
    if 'name_id' in globals():
        canvas.delete(name_id)
    if 'image_id' in globals():
        canvas.delete(image_id)
    try:
        if file_path is None:
            raise Exception("Please select a file first")
        if os.path.getsize(file_path) > 2 * 1024 * 1024:  # 2 Mo en octets
            raise Exception("Maximum  file size is 2 Mo")
        if not file_path.endswith(".glb"):
            raise Exception("Not a .glb file")
        bucket = cloud_client.get_bucket('fms_animations_bucket')
        blob = bucket.blob(ntpath.basename(file_path))
        blob.upload_from_filename(file_path)
        image_id = canvas.create_image(100, 20, image=valid)
        name_id = canvas.create_text(150, 20, text=ntpath.basename(file_path))
        file_path = None
        return True
    except Exception as e:
        image_id = canvas.create_image(30, 20, image=error)
        name_id = canvas.create_text(160, 20, text=e)
        print(e)
        return False

root = tk.Tk()
root.title("Envoyer un fichier")

canvas = Canvas(root, width=300, height=30)
canvas.pack()

valid = PhotoImage(file="valid.png")
error = PhotoImage(file="error.png")

select_file_button = tk.Button(root, text="Sélectionner le fichier", command=select_file)
select_file_button.pack()

send_file_button = tk.Button(root, text="Envoyer", command=send_file)
send_file_button.pack()

checkmark_label = tk.Label()

root.mainloop()
