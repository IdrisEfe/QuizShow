import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import time
from tkPDFViewer import tkPDFViewer as pdf
import fitz

class ChronometerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("QuizShow")
        self.master.configure(bg='#2E2E2E')

        self.master.geometry("800x600")

        # Görseli yükle
        image = Image.open("logo.png")  
        image = image.resize((150, 150))  
        self.photo = ImageTk.PhotoImage(image)

        # Görsel
        self.image_label = tk.Label(master, image=self.photo, bg='#2E2E2E')
        self.image_label.place(x=40, y=40) 
        
        self.amal_label = tk.Label(master, text="AMAL Yazılım Geliştirme Ekibi", font=("Arial", 12), bg='#2E2E2E', fg='#30D5C8')
        self.amal_label.place(x=20, y=50)  # Konum

        self.amal_label = tk.Label(master, text="QUIZ SHOW", font=("Impact", 25), bg='#2E2E2E', fg='white')
        self.amal_label.place(x=20, y=100)

        self.label_time = tk.Label(master, text="Süre girin:", bg='#2E2E2E', fg='white')
        self.label_time.pack()

        # Timer girişi
        self.entry_time = tk.Entry(master, bg='#2E2E2E', fg='white')
        self.entry_time.pack()

        # Geri sayım
        self.countdown_frame = tk.Frame(master, bg='#404040')
        self.countdown_frame.pack(side=tk.TOP, pady=(10, 0))
        self.countdown_var = tk.StringVar()
        self.countdown_label = tk.Label(self.countdown_frame, textvariable=self.countdown_var, font=("Arial", 24), bg='#2E2E2E', fg='white')
        self.countdown_label.pack()

        # Başlat
        self.start_button = tk.Button(master, text="Kronometreyi Başlat", command=self.start_chronometer, bg='#404040', fg='white', height=3, width=30)
        self.start_button.place(x=20, y=150)

        # Sıfırla
        self.reset_button = tk.Button(master, text="Sıfırla", command=self.reset_chronometer, bg='red', fg='white', height=3, width=15)
        self.reset_button.place(x=20, y=220)
        self.reset_button.config(state=tk.DISABLED)

        self.label_teams = tk.Label(master, text="Puanlar", bg='#2E2E2E', fg='white')
        self.label_teams.place(x=585, y=50)
        
        self.label_point_change = tk.Label(master, text="Puan Değişim Miktarı:", bg='#2E2E2E', fg='white')
        self.label_point_change.place(x=550, y=75)

        self.entry_point_change = tk.Entry(master, bg='#2E2E2E', fg='white')
        self.entry_point_change.place(x=550, y=100)

        self.pdf_path = 'Quiz Show Questions.pdf'
        self.scale_factor = 0.4
        self.document = fitz.open(self.pdf_path)
        self.total_pages = len(self.document)
        self.current_page = 0

        self.label = tk.Label(master)
        self.label.place(x=20, y=280)

        self.prev_button = tk.Button(self.master, text='Önceki', width=5, command=self.show_prev_page, bg='#404040', fg='white')
        self.prev_button.place(x=20, y=520)

        self.next_button = tk.Button(self.master, text="Sonraki", width=5, command=self.show_next_page, bg='#404040', fg='white')
        self.next_button.place(x=365, y=520)

        #self.enlarge_button = tk.Button(self.master, text='Büyüt', width=5, bg='#404040', fg='white', command=self.enlarge)
        #self.enlarge_button.place(x=190, y=520)

        self.show_page(self.current_page)

        self.team_scores = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.team_labels = []
        self.team_names = ['Hazırlık/A', 'Hazırlık/B', 'Hazırlık/C', 'Hazırlık/D','Hazırlık/E',
                           '9/A', '9/B', '9/C', '9/D', '10/A', '10/B', '10/C', '10/D']
        self.team_buttons_plus = []
        self.team_buttons_minus = []

        self.scores_frame = tk.Frame(master, bg='#2E2E2E')
        self.scores_frame.place(x=450, y=120)

        for i in range(9):
            if i < 5:
                frame = tk.Frame(self.scores_frame, bg='#2E2E2E')
                frame.grid(row=i, column=0, padx=(0, 10), pady=5)

                label = tk.Label(frame, text=f"{self.team_names[i]}", bg='#2E2E2E', fg='white')
                label.pack(side=tk.LEFT)

                button_minus = tk.Button(frame, text="-", command=lambda idx=i: self.update_score(idx, -self.get_point_change()), bg='#404040', fg='white', height=2, width=5)
                button_minus.pack(side=tk.LEFT)
        
                score_label = tk.Label(frame, text=str(self.team_scores[i]), bg='#2E2E2E', fg='white')
                score_label.pack(side=tk.LEFT)

                button_plus = tk.Button(frame, text="+", command=lambda idx=i: self.update_score(idx, self.get_point_change()), bg='#404040', fg='white', height=2, width=5)
                button_plus.pack(side=tk.LEFT)

            else:
                frame2 = tk.Frame(self.scores_frame, bg='#2E2E2E')
                frame2.grid(row=i-5, column=1, padx=(10, 0), pady=5)

                label = tk.Label(frame2, text=f"{self.team_names[i]}", bg='#2E2E2E', fg='white')
                label.pack(side=tk.LEFT)

                button_minus = tk.Button(frame2, text="-", command=lambda idx=i: self.update_score(idx, -self.get_point_change()), bg='#404040', fg='white', height=2, width=5)
                button_minus.pack(side=tk.LEFT)
        
                score_label = tk.Label(frame2, text=str(self.team_scores[i]), bg='#2E2E2E', fg='white')
                score_label.pack(side=tk.LEFT)

                button_plus = tk.Button(frame2, text="+", command=lambda idx=i: self.update_score(idx, self.get_point_change()), bg='#404040', fg='white', height=2, width=5)
                button_plus.pack(side=tk.LEFT)

            self.team_labels.append(score_label)
            self.team_buttons_plus.append(button_plus)
            self.team_buttons_minus.append(button_minus)

        self.running = False
    
    def render_page(self, page_num):
        # Render the page to an image
        page = self.document.load_page(page_num)
        pix = page.get_pixmap()
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        new_size = (int(pix.width * self.scale_factor), int(pix.height * self.scale_factor))
        image = image.resize(new_size, Image.LANCZOS)
        return image
    
    def show_page(self, page_num):
        image = self.render_page(page_num)
        self.photo = ImageTk.PhotoImage(image)
        self.label.config(image=self.photo)
    
    def show_prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_page(self.current_page)

    def show_next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.show_page(self.current_page)

    #def enlarge(self):
        #self.master2 = tk.Toplevel(self.master)
        #self.master2.title("QuizShow")
        #self.master2.configure(bg='#2E2E2E')
        #self.master2.geometry('800x600')

        #self.enlarged_label = tk.Label(self.master2, image=self.photo)
        #self.enlarged_label.place(x=20, y=280)

        #self.enlarged_prev_button = tk.Button(self.master2, text='Önceki', width=5, command=self.show_prev_page, bg='#404040', fg='white')
        #self.enlarged_prev_button.place(x=20, y=520)

        #self.master2.mainloop()

    def start_chronometer(self):
        if not self.running:
            try:
                target_time = float(self.entry_time.get())
            except ValueError:
                messagebox.showerror("Hata", "Lütfen geçerli bir süre girin.")
                return

            self.label_time.config(text="Kronometre çalışıyor...")
            self.start_button.config(state=tk.DISABLED)
            self.reset_button.config(state=tk.NORMAL)

            start_time = time.time()
            self.running = True  

            while self.running:
                elapsed_time = time.time() - start_time
                remaining_time = max(0, target_time - elapsed_time)

                if remaining_time == 0:
                    messagebox.showinfo("Süre doldu", "Süre doldu.")
                    self.running = False  
                    break

                self.countdown_var.set(f"Kalan süre: {remaining_time:.2f} saniye")
                self.master.update()

                time.sleep(0.01)

            self.label_time.config(text="Süre girin:")
            self.start_button.config(state=tk.NORMAL)
            self.reset_button.config(state=tk.DISABLED)
            self.countdown_var.set("")  

    def reset_chronometer(self):
        self.entry_time.delete(0, tk.END)
        self.label_time.config(text="Süre girin:")
        self.start_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.DISABLED)
        self.running = False  
        self.countdown_var.set("") 

    def update_score(self, team_index, delta):
        self.team_scores[team_index] += delta
        self.team_labels[team_index].config(text=str(self.team_scores[team_index]))

    def get_point_change(self):
        try:
            return int(self.entry_point_change.get())
        except ValueError:
            return 10



if __name__ == "__main__":
    root = tk.Tk(screenName=None,baseName=None, className="QuizShow", useTk=1)
    app = ChronometerApp(root)
    root.mainloop()