from tkinter import *
import random
from PIL import Image, ImageTk
from tkinter import messagebox
import queue  
import os
import threading
from tkinter.font import Font

class MainApp(object):
    def __init__(self):
        self.root=Tk()
        self.initialize_gui()
        self.button_pressed = None
        #Create instances for images
        self.briscola_image= None
        self.player_image1= None
        self.player_image2= None
        self.player_image3= None
        self.table_image= None
        self.opponent_image1= None
        self.opponent_image2= None
        self.opponent_image3= None
        self.table_image2= None

    def initialize_gui(self):
        self.action_queue = queue.Queue()
        #self.root.title('Codemy.com - Card Deck')
        #root.iconbitmap('c:/gui/codemy.ico')
        self.root.geometry("1920x1080")
        self.root.configure(background="green")
        
        
        self.my_frame = Frame(self.root, bg="green")
        self.my_frame.pack(pady=20)

        # Create Frames For Cards
        self.briscola_frame = LabelFrame(self.my_frame, text="Briscola", bd=0)
        self.briscola_frame.pack(padx=20, ipadx=20)

        self.opponent_frame = LabelFrame(self.my_frame, text="Opponent", bd=0)
        self.opponent_frame.pack(padx=20, ipadx=20, pady=10)

        self.table_frame = LabelFrame(self.my_frame, text="Table", bd=0)
        self.table_frame.pack(padx=20, ipadx=20, pady=10)

        self.player_frame = LabelFrame(self.my_frame, text="Player", bd=0)
        self.player_frame.pack(padx=20, ipadx=20, pady=10)

        #Put briscola card in frame
        self.briscola_frame.columnconfigure(0, weight=1)
        self.briscola_frame.columnconfigure(2, weight=1)
        
        self.briscola_label = Label(self.briscola_frame, text='')
        self.briscola_label.grid(row=0, column=1, pady=20, padx=10, sticky="nsew")

        # Put table cards in frames
        self.table_frame.columnconfigure(0, weight=1)
        self.table_frame.columnconfigure(3, weight=1)
        
        self.table_label = Label(self.table_frame, text='')
        self.table_label.grid(row=1, column=1, pady=20, padx=10, sticky="nsew")

        self.table_label2 = Label(self.table_frame, text='')
        self.table_label2.grid(row=1, column=2, pady=20, padx=10, sticky="nsew")


        # Put Player cards in frames
        self.player_frame.columnconfigure(0, weight=1)
        self.player_frame.columnconfigure(4, weight=1)

        self.player_label_1 = Label(self.player_frame, text='')
        self.player_label_1.grid(row=2, column=1, pady=10, padx=10, sticky="nsew")
#(row=2, column=1, pady=20, padx=20)

        self.player_label_2 = Label(self.player_frame, text='')
        self.player_label_2.grid(row=2, column=2, pady=10, padx=10, sticky="nsew")
#(row=2, column=2, pady=20, padx=20)
 
        self.player_label_3 = Label(self.player_frame, text='')
        self.player_label_3.grid(row=2, column=3, pady=10, padx=10, sticky="nsew")
#(row=2, column=3, pady=20)


        
        # Put Opponent cards in frames
        self.opponent_frame.columnconfigure(0, weight=1)
        self.opponent_frame.columnconfigure(4, weight=1)

        self.opponent_label_1 = Label(self.opponent_frame, text='')
        self.opponent_label_1.grid(row=3, column=1, pady=10, padx=10, sticky="nsew")

        self.opponent_label_2 = Label(self.opponent_frame, text='')
        self.opponent_label_2.grid(row=3, column=2, pady=10, padx=10, sticky="nsew")
 
        self.opponent_label_3 = Label(self.opponent_frame, text='')
        self.opponent_label_3.grid(row=3, column=3, pady=10, padx=10, sticky="nsew")


       
        # Create Button Frame
        self.button_frame = Frame(self.root, bg="green")
        self.button_frame.pack(pady=20)

        # Create a couple buttons

        self.card0_button = Button(self.button_frame, text="Card 0", font=("Helvetica", 14), command=self.play_card0)
        self.card0_button.grid(row=0, column=1, padx=10)

        self.card1_button = Button(self.button_frame, text="Card 1", font=("Helvetica", 14), command=self.play_card1)
        self.card1_button.grid(row=0, column=2, padx=10)

        self.card2_button = Button(self.button_frame, text="Card 2", font=("Helvetica", 14), command=self.play_card2)
        self.card2_button.grid(row=0, column=3, padx=10)


    def run(self):
        # Start the Tkinter main event loop
        self.root.mainloop()
     
    '''   
    # Define your button click functions
    def play_card(self,action):
        #player_cards=[self.player_label_1, self.player_label_2, self.player_label_3]
        #image_path = player_cards[action].cget("image")
        #image_name = os.path.basename(image_path)

        #card_name = image_name.split('.png')[0]
        self.action_queue.put(action) # Put the action into the queue when a button is clicked
        self.button_pressed.set()  # Signal that the button has been pressed
    '''
    
    def start_waiting_thread(self):
        # Start a separate thread to wait for button presses
        waiting_thread = threading.Thread(target=self.play_card())
        waiting_thread.start()

    def play_card(self):
        self.action_queue.put(self.button_pressed)

    def play_card0(self):
        self.button_pressed=0
        #self.play_card()
        #self.button_pressed=None
    
    def play_card1(self):
        self.button_pressed=1
        #self.play_card()
        #self.button_pressed=None

    def play_card2(self):
        self.button_pressed=2
        #self.play_card()
        #self.button_pressed=None

    # Resize Cards
    def resize_cards(self,card):
        # Open the image
        our_card_img = Image.open(card)

        # Resize The Image
        our_card_resize_image = our_card_img.resize((134, 192))
	
        # output the card
        global our_card_image
        our_card_image = ImageTk.PhotoImage(our_card_resize_image)

        # Return that card
        return our_card_image

   
    def custom_message_box(self,title, message, font_size=12):
        custom_dialog = Toplevel(self.root)
        custom_dialog.title(title)

        custom_font = Font(family="Helvetica", size=font_size)

        label = Label(custom_dialog, text=message, font=custom_font, padx=20, pady=10)
        label.pack()

        ok_button = Button(custom_dialog, text="OK", command=custom_dialog.destroy)
        ok_button.pack()

        custom_dialog.geometry("300x150")
        custom_dialog.transient(self.root)
        custom_dialog.grab_set()
        self.root.wait_window(custom_dialog)
  

main_app= MainApp()



