import tkinter as tk
from tkinter import ttk, messagebox
import pyttsx3
import pyjokes
import webbrowser
import subprocess
import datetime
import speech_recognition as sr
import pywhatkit as kit
import geocoder
import pyaudio
from con import username, password, first_name, last_name, gender, email, phone, conversation, added_conversation

# Now you can use these variables/functions directly



# Initialize the engine object
engine = pyttsx3.init()

# Function to validate login credentials
def validate_login():
    entered_username = username_entry.get()
    entered_password = password_entry.get()

    if entered_username == username and entered_password == password:
        login_window.destroy()
        open_main_chat_window()
    else:
        messagebox.showerror("Invalid Credentials", "Username or password is incorrect. Please try again.")

# Function to open the main chat window
def open_main_chat_window():
    def on_plus_click():
        # Placeholder function for the '+' button
        messagebox.showinfo("Info", "Plus button clicked")

    def on_camera_click():
        # Placeholder function for the camera button
        messagebox.showinfo("Info", "Camera button clicked")

    def on_mic_click():
        # Placeholder function for the microphone button
        messagebox.showinfo("Info", "Microphone button clicked")

    def jokes():
        joke = pyjokes.get_joke()

    def speak(response):
        # Set the voice for the engine
        engine.say(response)
        engine.runAndWait()

    def set_voice_male():
        # Set the voice to male
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)

    def set_voice_female():
        # Set the voice to female
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)

    def get_location_details():
        # Get location details using geocoder
        location = geocoder.ip('me')
        latitude = location.latlng[0]
        longitude = location.latlng[1]
        country = location.country
        state = location.state
        google_maps_link = f"https://www.google.com/maps/place/{latitude},{longitude}"

        return f"Latitude: {latitude}\nLongitude: {longitude}\nCountry: {country}\nState: {state}\nGoogle Maps Link: {google_maps_link}"

    def listen_to_speech():
        r = sr.Recognizer()
        with sr.Microphone() as source:
            mic_button.config(text="Listening...")
            root.update()
            audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            return text
        except Exception as e:
            print("Sorry, I could not recognize your voice.")
            return None
        finally:
            mic_button.config(text="🎤")
            root.update()

    def handle_user_input(event=None):
        if event is None:
            user_input = listen_to_speech()
        else:
            user_input = input_box.get()

        input_box.delete(0, tk.END)
        chat_history.config(state=tk.NORMAL)
        tag = f"user-{len(chat_history.tag_names())}"
        chat_history.insert(tk.END, f"user: {user_input}\n", tag)
        chat_history.tag_configure(tag, justify="right", lmargin2=50)

        # Check for added conversations first
        added_response = added_conversation.get(user_input.lower())
        if added_response:
            response = added_response
        else:
            # Save response to the specified file if > syntax is used
            if ' > ' in user_input:
                command, filename = user_input.split(' > ')
                response = conversation.get(command.lower(),
                                            "I'm sorry, I didn't understand your question. Can you please rephrase it?")
                with open(filename.strip(), 'w') as file:
                    file.write(f"user: {command}\nbot: {response}")
            else:
                # Continue with existing conversation logic
                if user_input.lower() == "hello":
                    current_time = datetime.datetime.now().time()
                    current_hour = current_time.hour

                    if 6 <= current_hour < 12:
                        response = f"Good morning sir, it's {current_time}, how can I assist you today?"
                    elif 12 <= current_hour < 17:
                        response = f"Good afternoon sir, it's {current_time}, how can I assist you today?"
                    elif 17 <= current_hour < 20:
                        response = f"Good evening sir, it's {current_time}, how can I assist you today?"
                    else:
                        # Check if it's nighttime (between 20:00 and 23:59)
                        if 20 <= current_hour <= 23:
                            response = f"Hello sir, it's {current_time}, you should sleep."
                        else:
                            response = f"Good night sir, it's {current_time}, how can I assist you today?"

                elif user_input.lower().startswith("open "):
                    app_or_site_name = user_input[5:]
                    try:
                        if "website" in app_or_site_name.lower():
                            site_name, domain = app_or_site_name.replace(" website", "").split()
                            webbrowser.open(f'http://{site_name}{domain}')
                        else:
                            subprocess.Popen(app_or_site_name)
                        response = f"Opening {app_or_site_name}"
                    except Exception as e:
                        response = f"Sorry, I couldn't open {app_or_site_name}. Please make sure the application or website exists and the name is correct."
                elif user_input.lower().startswith("/voice male"):
                    set_voice_male()
                    response = "CHANGING TO MALE VOICE SIR!"
                elif user_input.lower().startswith("/voice female"):
                    set_voice_female()
                    response = "CHANGING TO FEMALE VOICE SIR!"
                elif user_input.lower().startswith("/clear"):
                    chat_history.delete(1.0, tk.END)
                    response = "Clearing all chats in the window"
                elif user_input.lower().startswith("/locate"):
                    location_details = get_location_details()
                    response = f"Location Details:\n{location_details}"
                elif user_input.lower().startswith("/add"):
                    add_conversation_entry_gui()
                    response = ""  # Empty response for /add to avoid speaking
                elif user_input.lower().startswith("/show_added_conversations"):
                    show_added_conversations()
                    response = "Displaying added conversations"
                elif user_input.lower().startswith("play "):
                    song_name = user_input[5:]
                    try:
                        kit.playonyt(song_name)
                        response = f"Playing {song_name} on YouTube"
                    except Exception as e:
                        response = f"Sorry, I couldn't play {song_name}. Please make sure the song exists and the name is correct."
                else:
                    response = conversation.get(user_input.lower(),
                                                "I'm sorry, I didn't understand your question. Can you please rephrase it?")

        if response:  # Speak only if there is a response
            tag = f"bot-{len(chat_history.tag_names())}"
            chat_history.insert(tk.END, f"bot: {response}\n", tag)
            chat_history.tag_configure(tag, lmargin1=50)
            chat_history.config(state=tk.DISABLED)
            chat_history.yview(tk.END)
            speak(response)

    def add_conversation_entry_gui():
        add_window = tk.Toplevel(root)
        add_window.title("Add Conversation Entry")
        input_frame = tk.Frame(add_window, bg="#ECE5DD")
        input_frame.pack(padx=10, pady=10)
        entry_label = tk.Label(input_frame, text="Enter a new conversation entry:")
        entry_label.grid(row=0, column=0, padx=5, pady=5)
        entry_var = tk.StringVar()
        entry_entry = tk.Entry(input_frame, textvariable=entry_var, width=30)
        entry_entry.grid(row=0, column=1, padx=5, pady=5)
        response_label = tk.Label(input_frame, text="Enter the response for the new entry:")
        response_label.grid(row=1, column=0, padx=5, pady=5)
        response_var = tk.StringVar()
        response_entry = tk.Entry(input_frame, textvariable=response_var, width=30)
        response_entry.grid(row=1, column=1, padx=5, pady=5)
        create_button = ttk.Button(input_frame, text="Create", command=lambda: save_conversation_entry(entry_var.get(), response_var.get(), add_window))
        create_button.grid(row=2, column=1, pady=10)

    def save_conversation_entry(new_entry, new_response, window):
        added_conversation[new_entry.lower()] = new_response
        with open("con.py", "r") as file:
            content = file.read()
        added_conversation_str = f'    "{new_entry.lower()}": "{new_response}",'
        content = content.replace("added_conversation = {", f'added_conversation = {{\n{added_conversation_str}\n')
        with open("con.py", "w") as file:
            file.write(content)
        window.destroy()

    def show_added_conversations():
        for entry, response in added_conversation.items():
            print(f"{entry}: {response}")

    def open_settings_window():
        def save_changes():
            # Update the global variables with new values
            global first_name, last_name, gender, email, phone
            first_name = first_name_var.get()
            last_name = last_name_var.get()
            gender = gender_var.get()
            email = email_var.get()
            phone = phone_var.get()

            # Write the changes to con.py
            with open("con.py", "r") as file:
                content = file.readlines()

            # Update the lines corresponding to user details
            content[3] = f'first_name = "{first_name}"\n'
            content[4] = f'last_name = "{last_name}"\n'
            content[5] = f'gender = "{gender}"\n'
            content[6] = f'email = "{email}"\n'
            content[7] = f'phone = "{phone}"\n'

            # Write the updated content back to con.py
            with open("con.py", "w") as file:
                file.writelines(content)

            # Close the settings window
            settings_window.destroy()

        # Create settings window
        settings_window = tk.Toplevel(root)
        settings_window.title("Settings")

        # Create input fields for user details
        first_name_label = ttk.Label(settings_window, text="First Name:")
        first_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        first_name_var = tk.StringVar(value=first_name)
        first_name_entry = ttk.Entry(settings_window, textvariable=first_name_var)
        first_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        last_name_label = ttk.Label(settings_window, text="Last Name:")
        last_name_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        last_name_var = tk.StringVar(value=last_name)
        last_name_entry = ttk.Entry(settings_window, textvariable=last_name_var)
        last_name_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        gender_label = ttk.Label(settings_window, text="Gender:")
        gender_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        gender_var = tk.StringVar(value=gender)
        gender_entry = ttk.Entry(settings_window, textvariable=gender_var)
        gender_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        email_label = ttk.Label(settings_window, text="Email:")
        email_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        email_var = tk.StringVar(value=email)
        email_entry = ttk.Entry(settings_window, textvariable=email_var)
        email_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        phone_label = ttk.Label(settings_window, text="Phone:")
        phone_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        phone_var = tk.StringVar(value=phone)
        phone_entry = ttk.Entry(settings_window, textvariable=phone_var)
        phone_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        
        restart_text = ttk.Label(settings_window, text="YOU SHOULD RESTART THE SOFTWARE FOR CHANGES TO OCCUR")
        restart_text.grid(row=5, column=0, columnspan=2, pady=10)
        # Save Button
        save_button = ttk.Button(settings_window, text="Save Changes", command=save_changes)
        save_button.grid(row=6, column=0, columnspan=2, pady=10)

    root = tk.Tk()
    root.title("A V S")
    root.configure(bg="#ECE5DD")
    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 16))
    style.configure("TLabel", font=("Helvetica", 16))
    chat_history = tk.Text(root, state=tk.DISABLED, height=20, width=50, wrap=tk.WORD, bg="#ECE5DD", bd=0)
    chat_history.pack(padx=10, pady=10)
    input_frame = tk.Frame(root, bg="#ECE5DD")
    input_frame.pack(fill="x", padx=10, pady=10)
    input_box = tk.Entry(input_frame, width=50)
    input_box.pack(side="left", fill="x", expand=True)
    input_box.bind("<Return>", handle_user_input)
    input_box.focus()
    send_button = ttk.Button(input_frame, text="Send", command=handle_user_input)
    send_button.pack(side="right")
    mic_button = ttk.Button(input_frame, text="🎙️", command=handle_user_input)
    mic_button.pack(side="right")

    settings_button = ttk.Button(root, text="⚙️", command=open_settings_window)
    settings_button.place(relx=1.0, x=-10, y=10, anchor="ne")

    root.mainloop()

# Create the login window
login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("500x200")

username_label = ttk.Label(login_window, text="Username:")
username_label.pack(pady=5)

username_entry = ttk.Entry(login_window)
username_entry.pack(pady=5)

password_label = ttk.Label(login_window, text="Password:")
password_label.pack(pady=5)

password_entry = ttk.Entry(login_window, show="*")  # Show asterisks for password
password_entry.pack(pady=5)

login_button = ttk.Button(login_window, text="Login", command=validate_login)
login_button.pack(pady=10)

login_window.mainloop()
