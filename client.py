import threading
import tkinter as tk
import websocket
import serial
from config import websocket_server_url
from pydub import AudioSegment
from pydub.playback import play
from gtts import gTTS
import time
import tkinter.messagebox as messagebox
import pyautogui
import requests
from selenium import webdriver

arduino_port = 'COM3'
arduino = serial.Serial(arduino_port, baudrate=9600)


morse_code_dict = {
    'A': '01', 'B': '1000', 'C': '1010', 'D': '100', 'E': '0',
    'F': '0010', 'G': '110', 'H': '0000', 'I': '00', 'J': '0111',
    'K': '101', 'L': '0100', 'M': '11', 'N': '10', 'O': '111',
    'P': '0110', 'Q': '1101', 'R': '010', 'S': '000', 'T': '1',
    'U': '001', 'V': '0001', 'W': '011', 'X': '1001', 'Y': '1011',
    'Z': '1100',
    '0': '11111', '1': '01111', '2': '00111', '3': '00011', '4': '00001',
    '5': '00000', '6': '10000', '7': '11000', '8': '11100', '9': '11110'
}


def playSound(message):
    if(play_sounds.get() == 1):
        sound_test = gTTS(text=message, lang='en', slow=False)
        
        sound_test.save("sounds/test.mp3")
        test_sound = AudioSegment.from_mp3("sounds/test.mp3")
        play(test_sound)


def create_message():
    message_window = tk.Toplevel(root)
    message_window.title("Create Message")
    
    # Entry for the message
    message_label = tk.Label(message_window, text="Message:")
    message_label.grid(row=0, column=0, padx=10, pady=10)
    message_entry = tk.Entry(message_window)
    message_entry.grid(row=0, column=1, padx=10, pady=10)

    # Checkbox for Morse code
    morse_var = tk.BooleanVar()
    morse_checkbutton = tk.Checkbutton(message_window, text="Morse Code", variable=morse_var)
    morse_checkbutton.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    # OK and Cancel buttons
    def send_message():
        message = message_entry.get()
        is_morse = morse_var.get()
        if(is_morse == 1):
            is_morse = "Yes"
        else:
            is_morse = "No"
        if message:
            morse = text_to_morse(message)
            if(is_morse == "Yes"):
                ard_message = f"SAY_MESSAGE_Yes_{morse}_{message}"
            else:
                ard_message = f"SAY_MESSAGE_{morse}_{message}"

            log_message(f"Sending Message: {ard_message} (Ard)")

            arduino.write(ard_message.encode())
            message_window.destroy()
        else:
            message_window.destroy()
            messagebox.showerror('Error', 'Error: Message cannot be empty.')
            

    ok_button = tk.Button(message_window, text="OK", command=send_message)
    ok_button.grid(row=2, column=0, padx=10, pady=10)

    cancel_button = tk.Button(message_window, text="Cancel", command=message_window.destroy)
    cancel_button.grid(row=2, column=1, padx=10, pady=10)


def send_manual():
    message_window = tk.Toplevel(root)
    message_window.title("Send Manual Command")
    
    # Entry for the message
    message_label = tk.Label(message_window, text="Command:")
    message_label.grid(row=0, column=0, padx=10, pady=10)
    message_entry = tk.Entry(message_window)
    message_entry.grid(row=0, column=1, padx=10, pady=10)

    # OK and Cancel buttons
    def send_message():
        message = message_entry.get()
        if(message):
            ard_message = message

            log_message(f"Sending command: {ard_message} (Ard)")

            arduino.write(ard_message.encode())
            message_window.destroy()
        else:
            message_window.destroy()
            messagebox.showerror('Error', 'Error: Message cannot be empty.')

    ok_button = tk.Button(message_window, text="OK", command=send_message)
    ok_button.grid(row=2, column=0, padx=10, pady=10)

    cancel_button = tk.Button(message_window, text="Cancel", command=message_window.destroy)
    cancel_button.grid(row=2, column=1, padx=10, pady=10)


def simulate_manual():
    message_window = tk.Toplevel(root)
    message_window.title("Simulate Manual Command From WS")
    
    # Entry for the message
    message_label = tk.Label(message_window, text="Command:")
    message_label.grid(row=0, column=0, padx=10, pady=10)
    message_entry = tk.Entry(message_window)
    message_entry.grid(row=0, column=1, padx=10, pady=10)

    # OK and Cancel buttons
    def send_message():
        message = message_entry.get()
        if(message):
            ard_message = message

            log_message(f"Simulating from WS: {ard_message}")

            ws.send(f"SIMULATE_{ard_message}")
            message_window.destroy()
        else:
            message_window.destroy()
            messagebox.showerror('Error', 'Error: Message cannot be empty.')

    ok_button = tk.Button(message_window, text="OK", command=send_message)
    ok_button.grid(row=2, column=0, padx=10, pady=10)

    cancel_button = tk.Button(message_window, text="Cancel", command=message_window.destroy)
    cancel_button.grid(row=2, column=1, padx=10, pady=10)


def ping_web():
    message_window = tk.Toplevel(root)
    message_window.title("Ping Website")


    # /runmainstuff?username=ySqw3h7I301m1xltehL4wIJsMTl2VAg1gV&password=5Y4on24TdJMabwGv8eyQRRIpp6uK7YbxB3&api_call=change_track&change=skiptrack
    
    # Entry for the message
    message_label0 = tk.Label(message_window, text="Website:")
    message_label0.grid(row=0, column=0, padx=10, pady=10)
    message_entry0 = tk.Entry(message_window)
    message_entry0.insert(0, "https://webapimain.saturnwillow.repl.co/runmainstuff") 
    message_entry0.grid(row=0, column=1, padx=10, pady=10)

    message_label1 = tk.Label(message_window, text="Username:")
    message_label1.grid(row=1, column=0, padx=10, pady=10)
    message_entry1 = tk.Entry(message_window)
    message_entry1.insert(0, "ySqw3h7I301m1xltehL4wIJsMTl2VAg1gV") 
    message_entry1.grid(row=1, column=1, padx=10, pady=10)

    message_label2 = tk.Label(message_window, text="Password:")
    message_label2.grid(row=2, column=0, padx=10, pady=10)
    message_entry2 = tk.Entry(message_window)
    message_entry2.insert(0, "5Y4on24TdJMabwGv8eyQRRIpp6uK7YbxB3") 
    message_entry2.grid(row=2, column=1, padx=10, pady=10)

    message_label3 = tk.Label(message_window, text="Api Call:")
    message_label3.grid(row=3, column=0, padx=10, pady=10)
    message_entry3 = tk.Entry(message_window)
    message_entry3.grid(row=3, column=1, padx=10, pady=10)


    message_label4 = tk.Label(message_window, text="Other Args (Seperated by commas, define with =):")
    message_label4.grid(row=4, column=0, padx=10, pady=10)
    message_entry4 = tk.Entry(message_window)
    message_entry4.insert(0, "") 
    message_entry4.grid(row=4, column=1, padx=10, pady=10)


    # OK and Cancel buttons
    def send_message():
        message = [
            message_entry0.get(), 
            message_entry1.get(),
            message_entry2.get(),
            message_entry3.get(),
            message_entry4.get()
        ]
        if(message):
            website = str(message[0])
            website += f"?username={message[1]}"
            website += f"&password={message[2]}"
            website += f"&api_call={message[3]}"

            other_args = message[4]
            other_args = other_args.split(", ")
            for arg in other_args:
                website += f"&{arg}"


            log_message(f"Pinging Website: {website}")

            requests.get(website)
            message_window.destroy()
        else:
            message_window.destroy()
            messagebox.showerror('Error', 'Error: Website cannot be empty.')

    ok_button = tk.Button(message_window, text="OK", command=send_message)
    ok_button.grid(row=5, column=0, padx=10, pady=10)

    cancel_button = tk.Button(message_window, text="Cancel", command=message_window.destroy)
    cancel_button.grid(row=5, column=1, padx=10, pady=10)


def send_ws_message():
    message_window = tk.Toplevel(root)
    message_window.title("Manual Command To WS")
    
    # Entry for the message
    message_label = tk.Label(message_window, text="Command:")
    message_label.grid(row=0, column=0, padx=10, pady=10)
    message_entry = tk.Entry(message_window)
    message_entry.grid(row=0, column=1, padx=10, pady=10)

    # OK and Cancel buttons
    def send_message():
        message = message_entry.get()
        if(message):
            ard_message = message

            log_message(f"Sending: {ard_message} (WS)")

            ws.send(f"{ard_message}")
            message_window.destroy()
        else:
            message_window.destroy()
            messagebox.showerror('Error', 'Error: Message cannot be empty.')

    ok_button = tk.Button(message_window, text="OK", command=send_message)
    ok_button.grid(row=2, column=0, padx=10, pady=10)

    cancel_button = tk.Button(message_window, text="Cancel", command=message_window.destroy)
    cancel_button.grid(row=2, column=1, padx=10, pady=10)


def text_to_morse(text):
    morse_code = ""
    for char in text:
        if(char == " "):
            morse_code += " "
        if char.upper() in morse_code_dict:
            morse_code += morse_code_dict[char.upper()] + " "

    morse_code = morse_code[:-1]
    return morse_code

def send_to_arduino(message):
    arduino.write(message.encode('utf-8'))
    log_message(f"Sent to Arduino: {message}")

def on_message(ws, message):
    global ping_recived
    # Handle incoming messages here
    if(message != "PONG"):
        log_message(f"Received: {message}")

    if(message == "Start"):
        time.sleep(1.5)
        connection_icon.configure(file="images/connection.png")
        ping_recived = True
        arduino.write("CONNECTED".encode())

    if message == "say_hello":
        # play(hello_sound)
        ard_message = f"SAY_MESSAGE_000065_Hello!"

        arduino.write(ard_message.encode())

        playSound('Hello!')
        log_message("Hello!")

    if message.startswith("say_message"):
        # play(hello_sound)
        message_split = message.split("&")
        currMsg = message_split[1]

        
        ard_message = text_to_morse(currMsg)

        # Add {message_split[2]}_ to the message and pass in if you want morse or not
        # do this everywhere

        if(message_split[2] == "Yes"):
            ard_message = f"SAY_MESSAGE_{message_split[2]}_{ard_message}_{currMsg}"
        else:
            ard_message = f"SAY_MESSAGE_{ard_message}_{currMsg}"
        
        arduino.write(ard_message.encode())
        log_message(f"Sending command: {ard_message} (Ard)")
        playSound(currMsg)


    if message == "PONG":
        connection_icon.configure(file="images/connection.png")
        ping_recived = True

        

    if message.startswith("flash_light"):
        # play(hello_sound)
        currMsg = message.split("&")
        currMsg = currMsg[1]
        sound_msg = f"Flashing light {currMsg} times."

        msg = f'FLASH_LIGHT_{currMsg}'

        arduino.write(msg.encode())


        playSound(sound_msg)


    if message.startswith("copy_desmos"):
        # play(hello_sound)
        currMsg = message.split("&")
        currMsg = currMsg[1]
        sound_msg = f"Copying Desmos from website: {currMsg}."


        playSound(sound_msg)


        # Copy the desmos.
        driver = webdriver.Firefox()

        log_message(currMsg)

        driver.get(currMsg)

        time.sleep(3)

        pyautogui.click(200, 100)
        time.sleep(0.3)


        pyautogui.click(700, 450)
        time.sleep(0.3)

        pyautogui.write("SaturnWillow@gmail.com")
        time.sleep(0.3)

        pyautogui.click(700, 530)
        time.sleep(0.3)

        pyautogui.write("DESMOSpass2023!")
        time.sleep(0.3)

        pyautogui.click(850, 580)
        time.sleep(0.3)
        
        '''
        username = driver.find_element_by_name("username")
        password = driver.find_element_by_name("password")

        username.send_keys("YourUsername")
        password.send_keys("YourPassword")

        login_button = driver.find_element_by_name("loginButton")
        login_button.click()
        '''

        '''
        button_element = driver.find_element_by_id("buttonId")  # Replace with the actual element identifier
        button_element.click()
        '''


        time.sleep(1)

        driver.quit()


        
    
    
    if message == "toggle_light":
        arduino.write(b'TOGGLE_LIGHT\n')
        playSound('Toggled Light.')


    if message.startswith("change_track"):
        message = message.split("&")
        if(message[1] == "playpause"):
            playpausetrack()
            playSound("Played or Paused the Track.")
            log_message("Played or Paused the Track.")
        if(message[1] == "skiptrack"):
            skiptrack()
            playSound("Skipped the Track.")
            log_message("Skipped the Track.")
        if(message[1] == "prevtrack"):
            prevtrack()
            playSound("Went back a Track.")
            log_message("Went back a Track.")

    if message.startswith("run_command"):
        message = message.split("&")
        arduino.write(message[1].encode())
        log_message(f"Sending command: {message[1]} (Ard)")
        playSound(f"Running Command: {message[1]}")
        

def send_message(ws, message):
    # Send a message to the WebSocket server
    ws.send(message)
    log_message(f"Sent: {message}")
    
def log_message(message):
    text_widget.insert(tk.END, message + "\n")
    text_widget.see(tk.END)  # Auto-scroll to the end


def prevtrack():
    pyautogui.press("prevtrack")

def playpausetrack():
    pyautogui.press("playpause")

def skiptrack():
    pyautogui.press("nexttrack")

root = tk.Tk()
root.title("WebSocket Control")

connection_icon = tk.PhotoImage(file="images/noconnection.png")

# Create a label with the connection image
connection_label = tk.Label(root, image=connection_icon)
connection_label.pack(anchor="nw", padx=10, pady=10)


# Create a frame to contain the buttons
button_frame = tk.Frame(root)
button_frame.pack()

# Define icon images
back_icon = tk.PhotoImage(file="images/prev.png")  # Replace "back_icon.png" with the actual image file
play_icon = tk.PhotoImage(file="images/playpause.png")  # Replace "play_icon.png" with the actual image file
skip_icon = tk.PhotoImage(file="images/skip.png")  # Replace "skip_icon.png" with the actual image file


# Create the buttons with icons
back_button = tk.Button(button_frame, image=back_icon, command=prevtrack)
play_button = tk.Button(button_frame, image=play_icon, command=playpausetrack)
skip_button = tk.Button(button_frame, image=skip_icon, command=skiptrack)

# Pack the buttons in the frame side by side
back_button.pack(side=tk.LEFT, padx=3)
play_button.pack(side=tk.LEFT, padx=3)
skip_button.pack(side=tk.LEFT, padx=3)


send_button = tk.Button(root, text="Manual Command (Ard)", command=send_manual)
send_button.pack()
create_message_button = tk.Button(root, text="Create Message (Ard)", command=create_message)
create_message_button.pack()
simulate_manual_button = tk.Button(root, text="Simulate Message (WS)", command=simulate_manual)
simulate_manual_button.pack()
send_ws_message_button = tk.Button(root, text="Send Message (WS)", command=send_ws_message)
send_ws_message_button.pack()
ping_website_button = tk.Button(root, text="Ping Website", command=ping_web)
ping_website_button.pack()
play_sounds = tk.IntVar()
play_sounds_checkbox = tk.Checkbutton(root, text = "Play Sounds", variable = play_sounds, onvalue = 1, offvalue = 0, height = 2, width = 10) 
play_sounds_checkbox.pack()

text_widget = tk.Text(root, wrap=tk.WORD)
text_widget.pack(fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(root, command=text_widget.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_widget.config(yscrollcommand=scrollbar.set)


# Connect to the WebSocket server
log_message("Starting connection.")
ws = websocket.WebSocketApp(websocket_server_url, on_message=on_message)
ws_thread = threading.Thread(target=ws.run_forever)
ws_thread.daemon = True
ws_thread.start()

ping_recived = True


def send_ping():
    global ping_recived, ws  # Add the 'ws' variable to the global scope
    # log_message(f"Ping Recived: {ping_recived}")
    try:
        if ping_recived == True:
            ws.send("PING")
            # log_message("Sent: PING")
            ping_recived = False
            connection_icon.configure(file="images/searching.png")
        else:
            arduino.write("DISCONNECTED".encode())
            connection_icon.configure(file="images/noconnection.png")
            log_message("Server Down. [1]")
            # Close the WebSocket connection if it's open
            if ws and ws.sock:
                ws.close()
                log_message("Closed WebSocket connection")
            # Reconnect to the WebSocket server
            ws = websocket.WebSocketApp(websocket_server_url, on_message=on_message)
            ws_thread = threading.Thread(target=ws.run_forever)
            ws_thread.daemon = True
            ws_thread.start()
            log_message("Reopened Connection.")
            
    except:
        arduino.write("DISCONNECTED".encode())
        connection_icon.configure(file="images/noconnection.png")
        log_message("Server Down. [2]")
        # Close the WebSocket connection if it's open
        if ws and ws.sock:
            ws.close()
            log_message("Closed WebSocket connection")
        # Reconnect to the WebSocket server
        ws = websocket.WebSocketApp(websocket_server_url, on_message=on_message)
        ws_thread = threading.Thread(target=ws.run_forever)
        ws_thread.daemon = True
        ws_thread.start()
        log_message("Reopened Connection.")


    root.after(3000, send_ping)



root.after(3000, send_ping)

root.mainloop()

arduino.write("DISCONNECTED".encode())