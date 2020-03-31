""" This program has been developed by Stenli Todorov S5114948 """
from tkinter import *
from Logic import *
import webbrowser
from PIL import Image, ImageTk

text_font = ('Times New Roman', 15)
label_font = ('Arial', 25)


class TripAdviser:

    def __init__(self, parent):
        self.parent = parent
        parent.title('Trip Adviser')

        self.canvas = Canvas(parent)

        self.canvas.place(height=768, width=1366)
        self.photo_raw = Image.open('snow.jpg')
        # Thanks to http://7-themes.com/7040652-train-smoke-railway-minimalism.html
        self.photo = ImageTk.PhotoImage(self.photo_raw)
        self.background = Label(parent, image=self.photo)
        self.background.place(relwidth=1, relheight=1)

        self.city = 'Bournemouth'
        self.enter_frame = Frame(parent, bd=5, bg='Grey')
        self.enter_box = Message(self.enter_frame)
        self.enter_city_label = Label(self.enter_box, text='Enter city (Default is Bournemouth)')
        self.enter_city = Entry(self.enter_box, width=35)
        self.enter_city_button = Button(self.enter_box, text='Submit', font=text_font,
                                        command=lambda: self.update_city(self.enter_city.get()))
        self.enter_frame.place(relx=0.01, rely=0.5, relwidth=0.25, relheight=0.11)
        self.enter_box.place(relwidth=1, relheight=1)
        self.enter_city_label.grid(row=0, column=0)
        self.enter_city.grid(row=1, column=0)
        self.enter_city_button.grid(row=1, column=1)

        self.weather_frame = Frame(parent, bg='Grey', bd=5)
        self.weather_messagebox = Message(self.weather_frame)
        self.weather_frame.place(relx=0.01, rely=0.62, relwidth=0.32, relheight=0.10)
        self.weather_messagebox.place(relheight=1, relwidth=1)

        self.location = get_weather(self.city)
        self.desc = self.location['weather'][0]['description']
        weather_degrees = self.location['main']['temp']
        self.weather = "%.2f" % (weather_degrees - 273.15)

        self.weather_label = Label(self.weather_messagebox,
                                   text='The temperature in {} is {} Degrees.'.format(self.city, self.weather),
                                   font=text_font)
        self.weather_condition_label = Label(self.weather_messagebox, text='Conditions are: {}'.format(self.desc),
                                             font=text_font)
        self.weather_condition_label.grid(row=3, column=0)

        self.weather_label.grid(row=1, column=0)
        location_temp = float(self.weather)
        if location_temp > 15.0:
            temperature = 'Orange'
        elif location_temp < 8.0:
            temperature = 'Blue'
        else:
            temperature = 'Light green'
        self.main_frame = Frame(self.weather_messagebox, height=4, width=370, bd=1, relief=SUNKEN,
                                bg='{}'.format(temperature))
        self.main_frame.grid(row=2, column=0)

        self.article = '-'
        self.news = get_news(self.city)
        self.headlines = get_headlines(self.news)
        self.news_frame = Frame(bd=5, bg='Grey')
        self.news_box = Message(self.news_frame)
        self.news_label1 = Label(self.news_box, text=self.headlines[0], font=text_font)
        self.news_label2 = Label(self.news_box, text=self.headlines[1], font=text_font)
        self.news_label3 = Label(self.news_box, text=self.headlines[2], font=text_font)
        self.news_main = Label(self.news_box, text='Most recent news: ', font=text_font)
        self.news_main.place(relx=0.2, rely=0.01)
        self.news_frame.place(relx=0.01, rely=0.73, relwidth=0.73, relheight=0.25)
        self.news_box.place(relwidth=1, relheight=1)
        self.news_label1.place(relx=0.01, rely=0.2, relwidth=0.7)
        self.news_label2.place(relx=0.01, rely=0.4, relwidth=0.7)
        self.news_label3.place(relx=0.01, rely=0.6, relwidth=0.7)

        self.read_button1 = Button(self.news_box, text='Read more', font=text_font,
                                   command=lambda: self.open_url(self.headlines[0]))
        self.read_button2 = Button(self.news_box, text='Read more', font=text_font,
                                   command=lambda: self.open_url(self.headlines[1]))
        self.read_button3 = Button(self.news_box, text='Read more', font=text_font,
                                   command=lambda: self.open_url(self.headlines[2]))
        self.read_button1.place(relx=0.8, rely=0.2, relwidth=0.1)
        self.read_button2.place(relx=0.8, rely=0.4, relwidth=0.1)
        self.read_button3.place(relx=0.8, rely=0.6, relwidth=0.1)

        self.travel_enter_frame = Frame(parent, bd=5, bg='Grey')
        self.travel_enter_box = Message(self.travel_enter_frame)
        self.travel_enter_frame.place(relx=0.74, rely=0.01, relwidth=0.25, relheight=0.199)
        self.travel_enter_box.place(relwidth=1, relheight=1)

        self.travel_enter_departure_label = Label(self.travel_enter_box, text='Departure:', font=text_font)
        self.travel_enter_arrival_label = Label(self.travel_enter_box, text='Arrival:', font=text_font)
        self.travel_enter_departure = Entry(self.travel_enter_box)
        self.travel_enter_arrival = Entry(self.travel_enter_box)
        self.travel_enter_date_label = Label(self.travel_enter_box, text='Date (YYYY.MM.DD):', font=text_font)
        self.travel_enter_date = Entry(self.travel_enter_box)
        self.travel_enter_button = Button(self.travel_enter_box, text='Submit', height=1, font=text_font,
                                          command=lambda: self.update_travel_info())
        self.travel_enter_departure_label.grid(row=0, column=0)
        self.travel_enter_arrival_label.grid(row=1, column=0)
        self.travel_enter_date_label.grid(row=2, column=0)
        self.travel_enter_departure.grid(row=0, column=1)
        self.travel_enter_arrival.grid(row=1, column=1)
        self.travel_enter_date.grid(row=2, column=1)
        self.travel_enter_button.grid(row=3, column=1)

        self.travel_departure_location = []
        self.travel_departure_time = []
        self.travel_destination_location = []
        self.travel_destination_time = []
        self.travel_duration = []

        self.travel_info_frame = Frame(parent, bd=5, bg='Grey')
        self.travel_info_box = Message(self.travel_info_frame)
        self.travel_info_from_label = Label(self.travel_info_box, text='From: ', font=text_font)
        self.travel_info_to_label = Label(self.travel_info_box, text='To: ', font=text_font)
        self.travel_info_time_label = Label(self.travel_info_box, text='Duration: ', font=text_font)
        self.travel_info_departure_time_label = Label(self.travel_info_box, text='At: -', font=text_font)
        self.travel_info_arrival_time_label = Label(self.travel_info_box, text='At: -', font=text_font)
        self.travel_info_departure_label = Label(self.travel_info_box, text='You have not entered a location yet.',
                                                 font=text_font)
        self.travel_info_arrival_label = Label(self.travel_info_box, text='You have not entered a location yet.',
                                               font=text_font)
        self.travel_info_date_label = Label(self.travel_info_box, text='You have not entered a date yet.',
                                            font=text_font)
        self.travel_info_status_label = Label(self.travel_info_box, text='Waiting for input!', font=text_font)
        self.travel_info_page_number_label = Label(self.travel_info_box, text='Page 0 of 0.', font=text_font)

        self.travel_info_frame.place(relx=0.01, rely=0.01, relheight=0.25, relwidth=0.57)
        self.travel_info_box.place(relheight=1, relwidth=1)
        self.travel_info_from_label.grid(row=0, column=0)
        self.travel_info_to_label.grid(row=1, column=0)
        self.travel_info_time_label.grid(row=2, column=0)
        self.travel_info_departure_label.grid(row=0, column=1)
        self.travel_info_departure_time_label.grid(row=0, column=2)
        self.travel_info_arrival_label.grid(row=1, column=1)
        self.travel_info_arrival_time_label.grid(row=1, column=2)
        self.travel_info_date_label.grid(row=2, column=1)
        self.travel_info_status_label.grid(row=3, column=0)
        self.travel_info_page_number_label.grid(row=2, column=2)
        self.travel_inner_frame = Frame(self.travel_info_box)
        self.travel_inner_button_next = Button(self.travel_inner_frame, text='Next.', font=text_font,
                                               command=lambda: self.page_mover(1))
        self.travel_inner_button_back = Button(self.travel_inner_frame, text='Back.', font=text_font,
                                               command=lambda: self.page_mover(0))
        self.travel_inner_frame.grid(row=3, column=1)
        self.travel_inner_button_next.grid(row=0, column=1)
        self.travel_inner_button_back.grid(row=0, column=0)
        self.page_position = 0

    def open_url(self, title):
        url = get_article_link(self.news, title)
        webbrowser.open_new(url=url)

    def update_travel_info(self):
        date_raw = str(self.travel_enter_date.get())
        date = date_raw.replace('.', '')
        all_data = get_transport_info(self.travel_enter_departure.get(), self.travel_enter_arrival.get(), date)

        for departures in all_data['departurePoint']:
            self.travel_departure_location.append(departures)

        for departure_times in all_data['departureTime']:
            departure_time_formatted = departure_times.replace('T', ' ')
            self.travel_departure_time.append(departure_time_formatted)

        for arrivals in all_data['arrivalPoint']:
            self.travel_destination_location.append(arrivals)

        for arrival_time in all_data['arrivalTime']:
            arrival_time_formatted = arrival_time.replace('T', ' ')
            self.travel_destination_time.append(arrival_time_formatted)

        self.travel_duration = all_data['duration']

        self.page_location(0)
        self.travel_info_status_label.config(text='Trip found!', font=text_font)
        self.travel_info_page_number_label.config(text='Page 1 of {}'.format(len(self.travel_departure_location)),
                                                  font=text_font)

    def page_mover(self, position):
        num_pages = len(self.travel_departure_location)

        if self.page_position + 1 < num_pages and position == 1:
            self.page_position = self.page_position + position
            self.page_location(self.page_position)
            self.travel_info_page_number_label.config(text='Page {} of {}'.format(self.page_position + 1, num_pages),
                                                      font=text_font)
            self.travel_info_status_label.config(text='Status OK!!', font=text_font)

        elif self.page_position > 0 and position == 0:
            self.page_position = self.page_position - 1
            self.page_location(self.page_position)
            self.travel_info_page_number_label.config(text='Page {} of {}'.format(self.page_position + 1, num_pages),
                                                      font=text_font)
            self.travel_info_status_label.config(text='Status OK!!', font=text_font)

        else:
            self.travel_info_status_label.config(text='No more data that direction!', font=text_font)

    def page_location(self, place):
        self.travel_info_departure_label.config(text=self.travel_departure_location[place])
        self.travel_info_departure_time_label.config(text='At: {}'.format(self.travel_departure_time[place]))
        self.travel_info_arrival_label.config(text=self.travel_destination_location[place])
        self.travel_info_arrival_time_label.config(text='At: {}'.format(self.travel_destination_time[place]))
        self.travel_info_date_label.config(text=self.travel_duration)

    def update_city(self, city):
        if city != '':
            self.city = city
            try:
                self.location = get_weather(city)
                self.desc = self.location['weather'][0]['description']
                weather_degrees = self.location['main']['temp']
                self.weather = "%.2f" % (weather_degrees - 273.15)
                self.weather_label.config(text='The temperature in {} is {} Degrees.'.format(city, self.weather),
                                          font=text_font)
                self.weather_condition_label.config(text='Conditions are: {}'.format(self.desc), font=text_font)
            except KeyError:
                self.enter_city_label.config(text='Could not find city, try again?', font=text_font)
            self.enter_city_label.config(text='City found!', font=text_font)
            self.news = get_news(city)
            self.headlines = get_headlines(self.news)
            self.news_label1.config(text=self.headlines[0], font=text_font)
            self.news_label2.config(text=self.headlines[1], font=text_font)
            self.news_label3.config(text=self.headlines[2], font=text_font)

        else:
            self.enter_city_label.config(text='Could not find city, try again?', font=text_font)


root = Tk()
root.minsize(1366, 768)
TripAdviser(root)
root.iconbitmap('Map.ico')  # Thanks to http://www.iconarchive.com/tag/train
root.mainloop()
