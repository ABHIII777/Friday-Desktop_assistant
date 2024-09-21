import tkinter as tk
from tkinter import scrolledtext, ttk
import webbrowser as web
import subprocess, datetime
import pyttsx3
from AppOpener import *
import speech_recognition as sp

class ChatbotApp:
    def __init__(self, root):
        
        # initiating engine for text to speech
        
        self.engine = pyttsx3.init('sapi5')
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voices', voices[0].id)

        #  setting screen

        self.root = root
        self.root.title("FRIDAY...")
        self.root.geometry("650x550")
        
        #  styling screen and it's components
        
        style = ttk.Style()
        style.configure('TFrame', background='#ff3030')
        style.configure('TButton', background='#ffeb3b', foreground='black', font=('Arial', 10))
        style.configure('TEntry', font=('Arial', 12))

        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.chat_log = scrolledtext.ScrolledText(self.main_frame, state='disabled', wrap=tk.WORD, font=('Arial', 12))
        self.chat_log.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.user_input = ttk.Entry(self.main_frame, width=80)
        self.user_input.pack(pady=10, padx=10, side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.user_input.bind("<Return>", self.send_message)  # Bind Enter key to send message

        self.send_button = ttk.Button(self.main_frame, text="Send", command=self.send_message)
        self.send_button.pack(padx=10, side=tk.RIGHT)

        self.chat_log.config(bg='#ffeb3b', fg='#ff3030')
        self.user_input.config(background='#000', foreground='#000000')

    def say(self, audio):
        self.engine.say(audio)
        self.engine.runAndWait()

    def send_message(self, event=None):
        user_message = self.user_input.get()
        if user_message.strip() != "":
            self.update_chat_log(f"User: {user_message}")
            self.user_input.delete(0, tk.END)
            self.get_bot_response(user_message)

    def update_chat_log(self, message):
        self.chat_log.config(state='normal')
        self.chat_log.insert(tk.END, message + "\n")
        self.chat_log.config(state='disabled')
        self.chat_log.yview(tk.END)  # Scroll to the end

    def google_search(self, user_message):
        query = "" 
        for i in range(7, len(user_message)):
            query += user_message[i] 
        
        rawSearchURL = "https://www.google.com/search?q="
        splitSearchURL = "+".join(query.split())
        searchURL = rawSearchURL + splitSearchURL
        self.update_chat_log(f"Friday: Searching results for {query}.")
        self.say(f"Searching results for {query}")
        web.open_new_tab(searchURL)
    
    def youtube_search(self, user_message):
        query = ""
        for i in range(12, len(user_message)):
            query += user_message[i]
        
        rawYtURL = "https://www.youtube.com/results?search_query="
        splitYtURL = "+".join(query.split())
        YtURL = rawYtURL + splitYtURL
        self.update_chat_log(f"Friday: Searching results for {query}.")
        self.say(f"Searching results for {query}")
        web.open_new_tab(YtURL)
        
    def change_wallpaper(self):
        subprocess.run("iris", shell=True)
        self.say("Changing current wallpaper")
        self.update_chat_log("Friday: Wallpaper changed successfully")

    def openApps(self, user_message):
        try:
            self.say(f"Opening {user_message} application")
            self.update_chat_log(f"Friday: Opening {user_message} application.")
            open(user_message)
        
        except Exception as e:
            self.say(f"An error {e} occured during the process")
            self.update_chat_log(f"Friday: An error {e} occured during the process.")
    
    def getAppList(self):
        app_list = give_appnames()
        self.say("Getting names of all applications")
        self.update_chat_log(app_list)
  
    def get_time(self):
        hour = datetime.datetime.now().hour 

        if 0 <= hour <= 12:
            self.update_chat_log(f"Friday: It's {hour} in morning")
            self.say(f"It's {hour} in morning")

        elif 12 <= hour <= 18:
            self.update_chat_log(f"Friday: It's {hour} in noon")
            self.say(f"It's {hour} in noon")
        
        else:
            self.update_chat_log(f"Friday: It's {hour} in evening")
            self.say(f"It's {hour} in evening")
        
    def get_bot_response(self, user_message):

        responses = {
            "hello" : "hi there",
            "how are you" : "I am doing fine",
            "thanks" : "no worries",
            "nice": "i guess output was correct",
            "yo": "hey",
            "how you doing": "better than never",
            "you know any good jokes" : "none jokes are programmed"
        }
        
        if user_message not in responses:

            if "search " in user_message:
                self.google_search(user_message)
                
            elif "yt videos of " in user_message:
                self.youtube_search(user_message)
            
            elif "change wallpaper" in user_message:
                self.change_wallpaper()

            elif "open " in user_message:
                query = ""

                for i in range(5, len(user_message)):
                    query += user_message[i]

                try:
                    self.say(f"Opening {query} application.")
                    self.openApps(query)
                
                except Exception as e:
                    self.say(f"An error {e} occured during the process")
                    self.update_chat_log(f"Friday: Error {e} occured.")

            elif "get apps list" in user_message:
                self.getAppList()

            elif "time" in user_message:
                self.get_time()

            else:
                self.update_chat_log(f"Friday: Command {user_message} not found")
                self.say(f"Command {user_message} not found")

        else:
            responseQuery = responses.get(user_message.lower(), "Command not found")
            self.update_chat_log(f"Friday: {responseQuery}")
            self.say(responseQuery)
        
if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotApp(root)
    root.mainloop()
