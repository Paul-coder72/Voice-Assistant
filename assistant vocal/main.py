from imports import *


###     only for french users    ###
###             sorry            ###

# init la reconnaissance/synthèse vocale
recognizer = sr.Recognizer()
engine = pyttsx3.init()


# fonction pour parler
def speak(text):
    engine.say(text)
    engine.runAndWait()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id) 



def recognize_speech():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("écoute...") 

        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio, language='fr-FR')
            print("Vous avez dit :", command)
            return command.lower()
        
        except sr.UnknownValueError:
            speak("Je n'ai pas compris votre commande. Veuiller répéter.")
            return ""
        except sr.RequestError:
            speak("Erreur de connexion")
            return ""


# fonction pour executer des commandes vocales
def execute_command():
    command = recognize_speech()
    if "mets" and "sur youtube" in command:
        song_name = command.replace("mets ", "").replace("youtube", "")
        
        # recherche sur Youtube
        speak(f"Recherche de {song_name} sur Youtube")
            
        results = yts.YoutubeSearch(song_name, max_results=1).to_dict()
        if results:
            video_url = f"https://www.youtube.com/watch?v={results[0]['id']}"
            speak(f"Lecture de {results[0]['title']} sur YouTube.")
            webbrowser.open(video_url)
        else:
            speak("La musique que vous demandez n'existe pas ou ne peut pas être lue pour le moment.")

    elif "ouvre google" or "ouvre l'application google" or "google" in command:
        webbrowser.open("http://www.google.com")

    elif "ouvre youtube" in command:
        speak("Ouverture de YouTube...")
        webbrowser.open("https://www.youtube.com")

    elif "ferme l'application" in command:
        speak("Fermeture de l'application...")
        app.quit()
    
    elif "calculatrice" in command:
        speak("Ouvre l'application de calculatrice...")
        subprocess.Popen(["calc.exe"])

    elif "météo" in command:
        speak("D'accord. Voici le météo actuelle à votre position...")
        webbrowser.open("https://meteofrance.com")
    
    elif "quelle" and "heure" in command:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Il est actuellement {current_time}.")

    elif "actualités du jour" in command:
        speak("Récupération des actualités...")
        news_url = "https://www.francetvinfo.fr/"
        webbrowser.open(news_url)
        news_data = requests.get(news_url)
        soup = BeautifulSoup(news_data.content, "html.parser")
        news_titles = soup.find_all("h2", class_="title")
        for title in news_titles[:5]:
            speak(title.text.strip())        
        speak("Les dernières nouvelles ont été récupérées.")

    elif "recherche" in command:
        recherche = command.replace("recherche ", "")

    elif "mail" or "mails" in command:
        speak("Ouverture des mails...")
        subprocess.Popen(["outlook.exe"])

    else:
        speak("Je n'ai pas compris votre commande. Veuillez répéter.")



# init l'application
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue')

app = ctk.CTk()
app.title("Assistant Vocal")
app.geometry("500x400")


# label d'instructions
label = ctk.CTkLabel(app, text="Cliquez sur le bouton pour écouter une commande", font=("Helvetica", 16))
label.pack(pady=30)


# bouton d'écoute
e_button = ctk.CTkButton(app, text="Parler", font=("Helvetica", 14), height=50, width=200, command=execute_command)
e_button.pack(pady=20)


# bouton d'arrêt
q_button = ctk.CTkButton(app, text="Quitter", font=("Helvetica", 14), height=50, width=200, fg_color='red', command=app.quit)
q_button.pack(pady=20)


app.mainloop()

