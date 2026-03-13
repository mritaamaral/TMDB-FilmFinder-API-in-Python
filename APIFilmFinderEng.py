import requests
import sys
import os
from dotenv import load_dotenv
import ctypes
import webbrowser
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, 
                             QScrollArea, QVBoxLayout, QFrame, QPushButton)
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath, QIcon
from PyQt5.QtCore import Qt, QRectF

#pip installs used: pip install requests, pip install PyQt5
#API Requests in JSON: https://api.themoviedb.org/3/search/movie?api_key=your_api&query=Avatar%202
#API Database: TMDB

#This first part of the code is for 'set' an icon on taskbar
try:
    myappid = 'meu.python.filmes.1.0' #With this line, I make Python recognize my application as something separate instead of just being Python code
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except:
    pass

class FilmFinderAPI(QWidget): #the .self is the object's memory
    def __init__(self): #.self is for connecting different parts, making the functions see each other throughout the project when it is defined as a parameter in them
        super().__init__()
        self.API_KEY = os.getenv("API_KEY")
        self.BASE_URL = "https://api.themoviedb.org/3"
        self.session = requests.Session() #The .Session() stores the search data and keeps the connection open instead of making a request on every call with get(), optimizing the code
        self.initUI()

    def initUI(self): #Creation of the main window
        self.setWindowTitle('FilmFinder API')
        self.setFixedSize(1150, 750)

        #Icon 'movie.png' implementation
        icon_path = os.path.join(os.getcwd(), 'movie.png')
        self.setWindowIcon(QIcon(icon_path))

        self.centerScreen()
        self.setStyleSheet("background-color: #470d00;")

        self.create_static_widgets()
        self.config_scroll_area()

    def centerScreen(self):
        fg = self.frameGeometry()
        screen = QApplication.primaryScreen().geometry().center()
        fg.moveCenter(screen)
        self.move(fg.topLeft())

    def showMessage(self, message, color="#ff4d4d"): #Function to display feedback on a red-patterned label
        self.labelFeedback.setStyleSheet(f"color: {color}; font-size: 15px; font-weight: bold; font-family: 'Segoe UI';")
        self.labelFeedback.setText(message)

    def create_static_widgets(self): #Function that will create widgets that will not change according to API actions, that is, static widgets
        self.labelTitleFilmAPI = QLabel('FilmFinder API', self)
        self.labelTitleFilmAPI.setGeometry(0, 40, 1150, 60)  
        self.labelTitleFilmAPI.setAlignment(Qt.AlignCenter) 
        self.labelTitleFilmAPI.setStyleSheet("color: white; font-size: 40px; font-weight: bold; font-family: 'Segoe UI';")

        self.lineEditSearchMovie = QLineEdit(self)
        self.lineEditSearchMovie.setPlaceholderText(" Search the name of the movie here...")
        self.lineEditSearchMovie.setGeometry(50, 120, 1050, 55)
        self.lineEditSearchMovie.returnPressed.connect(self.validateSearch)
        self.lineEditSearchMovie.setStyleSheet("""
            QLineEdit { background-color: black; color: white; border: 2px solid #1a1a1a; 
            border-radius: 27px; padding-left: 55px; font-size: 17px; font-family: 'Segoe UI'; }
            QLineEdit:focus { border: 2px solid #737373; }
        """)

        self.labelMagnifier = QLabel('🔍', self)
        self.labelMagnifier.setGeometry(75, 135, 25, 25)
        self.labelMagnifier.setStyleSheet("background: transparent; color: #666; font-size: 20px;")

        self.labelFeedback = QLabel("", self) #labelFeedback starts empty and is later changed according to the user's action
        self.labelFeedback.setGeometry(50, 178, 1050, 30)
        self.labelFeedback.setAlignment(Qt.AlignCenter)

    def config_scroll_area(self): #Define a scoll area
        self.scroll = QScrollArea(self)
        self.scroll.setGeometry(50, 210, 1070, 520)
        self.scroll.setWidgetResizable(True) #Ensures an automatic adjustment/resizing of the 'movie container' according to the scroll area set
        self.scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        
        self.container_results = QWidget() #A kind of empty, giant sheet of paper that will be filled with the movies
        self.layout_v = QVBoxLayout(self.container_results) #Organize the movie cards one below the other, like an infinite mural
        self.layout_v.setContentsMargins(0, 0, 20, 0) 
        self.layout_v.setSpacing(25)
        self.scroll.setWidget(self.container_results)

    def validateSearch(self):
        searchedmovie = self.lineEditSearchMovie.text().strip()
        if not searchedmovie:
            self.showMessage("⚠ Please, set a movie name.")
            return
        
        self.showMessage("Searching for the movie on the servers... Wait a second!🍿", "#888888")
        QApplication.processEvents() #Brings the feedback to the user while do the search
        
        self.searchMovies(searchedmovie)

    def searchMovies(self, query): #Funcion that calls the search/query on API
        while self.layout_v.count(): #A loop that will count if there is any item in the layout
            item = self.layout_v.takeAt(0) #Taking the first item(0), he removes from layout
            if item.widget(): item.widget().deleteLater() # .deleteLater() is for delete the informations with safe

        try:
            url_search = f"{self.BASE_URL}/search/movie?api_key={self.API_KEY}&query={query}"
            res_busca = self.session.get(url_search).json()
            results = res_busca.get('results', [])

            validate_movies = []
            for f in results: #Loop structure that will check the list to see if ALL movies (without exception) will have SYNOPSIS and POSTER
                if f.get('overview') and f.get('poster_path'):
                    validate_movies.append(f) #add movie items up to 10, when will the structure stop
                    if len(validate_movies) == 10:
                        break

            if not validate_movies:
                self.showMessage("No movie found.")
                return

            for filme in validate_movies:
                movie_id = filme['id']
                #Detailed search including credits, streaming providers, and videos (Trailer)
                url_details = f"{self.BASE_URL}/movie/{movie_id}?api_key={self.API_KEY}&append_to_response=credits,watch/providers,videos" #Will search for all the details that I assigned
                complete_data = self.session.get(url_details).json()

                #Casting
                cast_list = complete_data.get('credits', {}).get('cast', [])
                nomes_atores = ", ".join([ator['name'] for ator in cast_list[:6]])

                #Streaming Extraction (in Brazil - country I live)
                providers = complete_data.get('watch/providers', {}).get('results', {}).get('BR', {})
                streaming_lista = providers.get('flatrate', []) #Signature (ex: Netflix)

                #Trailer Key Extraction
                videos = complete_data.get('videos', {}).get('results', [])
                t_key = next((v['key'] for v in videos if v['type'] == 'Trailer' and v['site'] == 'YouTube'), None)
                
                self.create_movie_card(complete_data, nomes_atores, streaming_lista, t_key)
            
            self.showMessage(f"Results for: {query}", "#bbbbbb")

        except Exception as e:
            self.showMessage(f"Erro de conexão: {str(e)}")

    def create_movie_card(self, data, cast_text, streaming_list, t_key):
        card = QFrame() #Empty frame, usually to group with other elements into a single object
        card.setMinimumHeight(450)
        card.setStyleSheet("background-color: #2b0800; border-radius: 30px;")
        
        label_poster = QLabel(card) #Creates the label where the poster image will be inserted
        label_poster.setGeometry(40, 35, 280, 380)
        if data.get('poster_path'):
            try:
                img_url = f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
                img_data = self.session.get(img_url).content
                pix = QPixmap() #Image object within Qt
                pix.loadFromData(img_data) #Transform the downloaded data into a real image
                label_poster.setPixmap(self.to_round_pixmap(pix)) #Calls the function that will round the poster image
            except:
                label_poster.setText("🖼 Imagem indisponível")
                label_poster.setStyleSheet("color: white; font-family: 'Segoe UI';")
                label_poster.setAlignment(Qt.AlignCenter)

        #Title
        titulo = QLabel(data.get('title', 'Unavailable Title'), card)
        titulo.setGeometry(350, 35, 650, 50)
        titulo.setStyleSheet("color: white; font-size: 32px; font-weight: bold; font-family: 'Segoe UI';")

        #Date formatting logic
        raw_data = data.get('release_date', 'Unknown Date')
        if "-" in raw_data:
            y, m, d = raw_data.split("-")
            formatted_date = f"{d}/{m}/{y}"
        else:
            formatted_date = raw_data

        #Release Info and Note
        info_extra = QLabel(f"📅 <b>Release:</b> {formatted_date}    |    ⭐ <b>Review:</b> {data.get('vote_average', 0)}", card)
        info_extra.setGeometry(350, 90, 650, 30)
        info_extra.setStyleSheet("color: #cccccc; font-size: 16px; font-family: 'Segoe UI';")

        #If there are streamings, he participates in the condition
        if streaming_list:
            stream_names = ", ".join([p['provider_name'] for p in streaming_list])
            stream_text = f"📺 <b>Available at:</b> <span style='color: #00ff88;'>{stream_names}</span>"
        else:
            stream_text = "📺 <b>Streaming:</b> <span style='color: #f1c40f;'>Only Rent/Buy or Movie Theater</span>" #Span is to prevent the label from breaking into a new line
        
        lbl_streaming = QLabel(stream_text, card)
        lbl_streaming.setGeometry(350, 120, 650, 25)
        lbl_streaming.setStyleSheet("color: #cccccc; font-size: 16px; font-family: 'Segoe UI';")

        #Scroll for invisible Synopsis, in case the synopsis is large and exceeds the layout sizes
        scroll_synopsis = QScrollArea(card)
        scroll_synopsis.setGeometry(350, 150, 650, 130)
        scroll_synopsis.setWidgetResizable(True)
        scroll_synopsis.setStyleSheet("background: transparent; border: none;")
        scroll_synopsis.verticalScrollBar().setStyleSheet("width: 0px; background: transparent;")
        
        #Shows the movie synopsis
        synopsis_content = QLabel(f"<b>Synopsis:</b> {data.get('overview', 'No synopsis available.')}")
        synopsis_content.setWordWrap(True)
        synopsis_content.setStyleSheet("color: white; font-size: 16px; font-family: 'Segoe UI'; background: transparent;")
        scroll_synopsis.setWidget(synopsis_content)

        #Informações de elenco
        cast = QLabel(f"<b>Main cast:</b> {cast_text if cast_text else 'Information not available.'}", card)
        cast.setGeometry(350, 290, 650, 60)
        cast.setWordWrap(True)
        cast.setStyleSheet("color: white; font-size: 15px; font-family: 'Segoe UI';")

        if t_key: #If you have the key for the trailer on Youtube (e.g., K3efer43), it executes the condition
            btn_trailer = QPushButton("▶ WATCH TRAILER", card)
            btn_trailer.setGeometry(350, 360, 220, 45)
            btn_trailer.setCursor(Qt.PointingHandCursor)
            btn_trailer.setStyleSheet("""
                QPushButton { background-color: #661503; color: white; border-radius: 15px; font-weight: bold; font-size: 14px; }
                QPushButton:hover { background-color: #000000; }
            """)
            btn_trailer.clicked.connect(lambda ch, key=t_key: webbrowser.open(f"https://www.youtube.com/watch?v={key}")) #Link to open the trailer in the browser

        self.layout_v.addWidget(card)

    def to_round_pixmap(self, pixmap): #Specific function to round the edges of the poster image
        #Scale the pixmap to the desired dimensions while maintaining aspect ratio
        pixmap = pixmap.scaled(280, 380, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        
        out_img = QPixmap(280, 380) #New empty pixmap for the poster
        out_img.fill(Qt.transparent) #Ensure background is transparent to avoid artifacts in the corners
        
        painter = QPainter(out_img) #Initialize the painter for the output image
        painter.setRenderHint(QPainter.Antialiasing) #Enable antialiasing for smooth edge rendering
        
        path = QPainterPath() #Define the clipping path
        path.addRoundedRect(QRectF(0, 0, 280, 380), 20, 20) #Define the rounded rectangle template
        
        painter.setClipPath(path) #Set the clipping path so drawing only occurs within the rounded boundaries
        painter.drawPixmap(0, 0, pixmap) #Draw the movie poster onto the clipped area
        painter.end()
        
        return out_img

if __name__ == '__main__':
    load_dotenv()
    app = QApplication(sys.argv)
    janela = FilmFinderAPI()
    janela.show()
    sys.exit(app.exec_())

