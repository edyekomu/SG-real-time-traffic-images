import requests
from io import BytesIO
import tkinter
from PIL import Image, ImageTk

url = "https://api.data.gov.sg/v1/transport/traffic-images"

def query_api(image_no):
    # fetch image URL by sending GET request to API
    response = requests.get(url)
    data = response.json()

    image_url = data["items"][0]["cameras"][image_no]["image"]
    return image_url

def update_image(window, image_label, image_no):
    # fetch URL and extract image data in byte format
    image_url = query_api(image_no)
    response = requests.get(image_url)
    image_data = Image.open(BytesIO(response.content)).resize((400, 300), Image.Resampling.LANCZOS)
    
    # update image on window
    image_tk = ImageTk.PhotoImage(image_data)
    image_label.config(image=image_tk)
    image_label.image = image_tk

    # recommended to call API endpoint every minute
    # update image after time
    window.after(60000, update_image, window, image_label)

def update_timer():
    global timer
    time_text['text'] = 'Next Update: ' + str(timer)
    if timer == 0:
        timer = 60
    timer -= 1
    window.after(1000, update_timer)

def button_clicked():
    global image_no
    global timer
    timer = 60
    image_no += 1

    update_image(window, image_label, image_no)
    

# setting up window
window = tkinter.Tk()
window.title("Live Traffic Image")
window.geometry('500x400')

# create label to display image
image_label = tkinter.Label(window)
image_label.pack()

# create countdown text to indicate next update
time_text = tkinter.Label(window, font=("Arial", 14))
time_text.pack()

# create button
button = tkinter.Button(window, text='Next', command=button_clicked)
button.pack()

# start update cycle
image_no = 0
timer = 60
update_image(window, image_label, image_no)
update_timer()

# run main loop
window.mainloop()




