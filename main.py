import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from Bemutatando_Modul import PB_MetroMusic
from Sajat_Modul_PB import pb_resize_image


ASSETS = os.path.join(os.path.dirname(__file__), "assets")
BG_PATH = os.path.join(ASSETS, "background.jpg")
MUSIC_PATH = os.path.join(ASSETS, "music.mp3")
GALLERY_FOLDER = os.path.join(ASSETS, "gallery")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Metro 2033")
        self.geometry("1024x768")
        self.minsize(800, 600)
        self.protocol("WM_DELETE_WINDOW", self.on_quit)
        self.music = PB_MetroMusic(MUSIC_PATH)
        self.music.play_music()
        self.container = tk.Frame(self)
        self.container.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.bg_label = tk.Label(self.container)
        self.bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.bg_original = None
        self.bg_photo = None
        self.load_background()
        self.frames = {}
        for F in (MainMenu, WorldPage, QuizPage, GalleryPage):
            page = F(parent=self.container, controller=self)
            self.frames[F.__name__] = page
            page.place(relwidth=1, relheight=1)
        self.after(100, lambda: self.show_frame("MainMenu"))
        self.bind("<Configure>", self.on_resize)
        self.after_idle(self._initial_paint)

    def load_background(self):
        if os.path.exists(BG_PATH):
            self.bg_original = Image.open(BG_PATH)
        else:
            self.container.configure(bg="black")

    def _initial_paint(self, retries=10):
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        if (w < 50 or h < 50) and retries > 0:
            self.after(100, lambda: self._initial_paint(retries - 1))
            return
        self.update_background()

    def update_background(self):
        if not self.bg_original:
            return
        w = self.winfo_width()
        h = self.winfo_height()
        if w < 10 or h < 10:
            return
        img = self.bg_original.resize((w, h), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(img)
        self.bg_label.config(image=self.bg_photo)
        self.bg_label.lower()

    def set_transparent_label_bg(self, label):
        if not self.bg_original:
            return
        self.after(150, lambda: self._apply_label_bg(label))

    def _apply_label_bg(self, label):
        try:
            x, y = label.winfo_x(), label.winfo_y()
            w, h = label.winfo_width(), label.winfo_height()
            if w < 5 or h < 5:
                self.after(100, lambda: self._apply_label_bg(label))
                return
            resized = self.bg_original.resize((self.winfo_width(), self.winfo_height()), Image.LANCZOS)
            cropped = resized.crop((x + 1, y + 1.5, x + w, y + h))
            photo = ImageTk.PhotoImage(cropped)
            label.config(image=photo, compound="center", bd=0, highlightthickness=0, relief="flat", bg=self["bg"])
            label.image = photo
        except Exception:
            pass

    def on_resize(self, event):
        self.update_background()

    def show_frame(self, name):
        for frame in self.frames.values():
            frame.place_forget()
        self.frames[name].place(relwidth=1, relheight=1)
        self.bg_label.lower()
        self.frames[name].lift()

    def toggle_music(self):
        self.music.toggle_music()

    def on_quit(self):
        self.music.stop_music()
        self.destroy()


class BasePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="")
        self.controller = controller


class MainMenu(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        frame = tk.Frame(self, bg="", bd=0)
        frame.place(relx=0.5, rely=0.45, anchor="center")
        ttk.Button(frame, text="Metro 2033 világa", command=lambda: controller.show_frame("WorldPage")).pack(fill="x", pady=8)
        ttk.Button(frame, text="Galéria", command=lambda: controller.show_frame("GalleryPage")).pack(fill="x", pady=8)
        ttk.Button(frame, text="Kvíz", command=lambda: controller.show_frame("QuizPage")).pack(fill="x", pady=8)
        ttk.Button(frame, text="Kilépés", command=controller.on_quit).pack(fill="x", pady=8)
        ttk.Button(self, text="Zene szüneteltetése", command=controller.toggle_music).place(relx=0.5, rely=0.65, anchor="center")


class WorldPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        ttk.Button(self, text="Vissza", command=lambda: controller.show_frame("MainMenu")).place(relx=0.02, rely=0.01)
        self.texts = ["Az egész világ romokban hever. Az emberiség csaknem teljesen kipusztult. "
            "A félig lerombolt városokat a sugárzás alkalmatlanná tette az életre. "
            "Moszkva szellemvárossá változott, megmérgezte a radioaktív sugárzás, és szörnyek népesítik be. "
            "Határain túl pedig a szóbeszéd szerint végtelen, felperzselt pusztaságok és mutáns fákkal-növényekkel teli erdőrengetegek kezdődnek. "
            "De hogy mi lehet ott pontosan, azt senki sem tudja...\n \n"
            "A civilizáció a végét járja. Az ember egykori nagyságának emlékét mesék és legendák növik be. "
            "Több mint húsz év telt el attól a naptól kerzdve, hogy az utolsó repülőgép felszállt a földről. A rozsdaette vasúti sínek nem vezetnek sehová. "
            "Az évszázad torzóiban maradt építkezései romhalmazokká lettek. Az éter üres, a rádiósok, akik milliomodszor is ráállnak azokra a hullámhosszokra, "
            "amelyeken valaha New Yorkot, Párizst, Tokiót és Buenos Airest fogták, most csüggesztő süvöltést hallanak.",
            "Mindössze huszonkét év telt el azóta, hogy az Utolsó Háború megtörtént, s a Földnek nem az ember az ura. "
            "A sugárzás szülte teremtmények nála sokkal jobban alkalmazkodtak az új világhoz. "
            "Az emberek kora végleg lejárt. Csak nagyon kevesen vannak azok, akik nem akarnak ebbe beletörődni – csupán 40.000 ember. "
            "Nem tudják, hogy megmenekültek-e mások is, vagy ők az utolsó emberek a bolygón. A moszkvai metróban élnek, - a valaha épített legnagyobb atombombabiztos óvóhelyen. "
            "Az emberiség utolsó menedékén.\n \n"
            "Valamennyien a metróban voltak a végórákban, és ez mentette meg az életüket. "
            "A hermetikus kapuk megvédik őket a sugárzástól és a felszín szörnyetegeitől, elhasználódott szűrők tisztítják a vizüket és a levegőjüket. "
            "Mesterembereik építette generátorok termelik az áramot, a föld alatti farmokon gombát termesztenek és disznókat nevelnek.",
            "A központi kormányzás rendszere már rég összeomlott, és az állomások törpeállamokként működnek. "
            "Az ott élő emberek eszmék, vallások vagy egyszerűen csak vízszűrők mentén szerveződnek közösségekbe. "
            "Fasiszták, Vörösök, Kultisták vagy éppen Banditák... Ebben a világban a holnap nem létezik. Nincs benne hely álmoknak, terveknek, reményeknek. "
            "Az érzések helyébe az ösztönök lépnek, amelyek közül a legfőbb a túlélés ösztöne. Túlélni bármi áron.\n \n"
            "Artyomnak ebben a szörnyű világban kell felnőnie ahhoz a feladathoz, hogy az állomását fenyegető szörnyű veszéllyel szembenézzen. "
            "Az egész metróhálózaton át kell jutnia, hogy nem csak az állomását, de talán az egész emberiséget megmentse a pusztulástól. "
            "De hogyan tudja majd eldönteni, hogy hőstettet követ-e el, vagy óriási hibát? \n \n"
            "Dmitry Glukhovsky története az atomháború utáni világot írja le, de valójában nagyon is a mostani világunkról szól: "
            "hidegháborúról, menekültválságról, új diktatúrákról..."
            "A Metró trilógiája a világ számos országában bestseller lett, és népszerű számítógépes játékok is készültek belőle. "
            "Ez a multimédiás alkalmazás azt a célt szolgálja, hogy az érdeklődők megismerkedhessenek a Metro 2033 világával, "
            "hátha kedvet kapnak ezután a könyvek elolvasásához vagy a játékok végigjátszásához."]
        self.index = 0
        self.text_label = tk.Label(self, text="", font=("Consolas", 14), fg="white", justify="left", anchor="nw", wraplength=900, bd=0, highlightthickness=0)
        self.text_label.place(relx=0.05, rely=0.34, relwidth=0.9, relheight=0.56)
        ttk.Button(self, text="Előző", command=self.prev_page).place(relx=0.3, rely=0.9)
        ttk.Button(self, text="Következő", command=self.next_page).place(relx=0.6, rely=0.9)
        controller.after(300, lambda: controller.set_transparent_label_bg(self.text_label))
        self.show_text()

    def show_text(self):
        self.text_label.config(text=self.texts[self.index])
        self.controller.set_transparent_label_bg(self.text_label)

    def next_page(self):
        if self.index < len(self.texts) - 1:
            self.index += 1
            self.show_text()

    def prev_page(self):
        if self.index > 0:
            self.index -= 1
            self.show_text()


class GalleryPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        ttk.Button(self, text="Vissza", command=lambda: controller.show_frame("MainMenu")).place(relx=0.02, rely=0.01)
        self.canvas = tk.Canvas(self, bg="#111", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#111")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.place(relx=0.05, rely=0.3, relwidth=0.9, relheight=0.68)
        self.scrollbar.place(relx=0.95, rely=0.3, relheight=0.68)
        self.thumbnails = []
        self.load_gallery()

    def load_gallery(self):
        if not os.path.exists(GALLERY_FOLDER):
            os.makedirs(GALLERY_FOLDER)
            return
        files = [f for f in os.listdir(GALLERY_FOLDER)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))]
        for i, file in enumerate(files):
            path = os.path.join(GALLERY_FOLDER, file)
            base_name, _ = os.path.splitext(file)
            txt_path = os.path.join(GALLERY_FOLDER, base_name + ".txt")
            img = pb_resize_image(path)
            photo = ImageTk.PhotoImage(img)
            frame = tk.Frame(self.scrollable_frame, bg="#111")
            lbl = tk.Label(frame, image=photo, bg="#222", bd=2, relief="ridge", cursor="hand2")
            lbl.image = photo
            lbl.pack(padx=5, pady=(5, 0))
            lbl.bind("<Button-1>", lambda e, p=path, t=txt_path: self.toggle_image(p, t))
            caption = ""
            if os.path.exists(txt_path):
                with open(txt_path, "r", encoding="utf-8") as f:
                    caption = f.read().strip()
            if caption:
                tk.Label(frame, text=caption, bg="#111", fg="#ccc", font=("Arial", 10), wraplength=250, justify="center").pack(pady=(3, 8))
            frame.grid(row=i // 3, column=i % 3, padx=10, pady=10)
            self.thumbnails.append(frame)

    def toggle_image(self, path, txt_path):
        if hasattr(self, "overlay_bg") and self.overlay_bg.winfo_exists():
            self.overlay_bg.destroy()
        if hasattr(self, "overlay_img") and self.overlay_img.winfo_exists():
            self.overlay_img.destroy()
            return
        self.overlay_bg = tk.Toplevel(self)
        self.overlay_bg.attributes("-fullscreen", False)
        self.overlay_bg.geometry(
            f"{self.winfo_width()}x{self.winfo_height()}+{self.winfo_rootx()}+{self.winfo_rooty()}")
        self.overlay_bg.overrideredirect(True)
        self.overlay_bg.configure(bg="black")
        self.overlay_bg.attributes("-alpha", 0.0)
        self.overlay_img = tk.Toplevel(self)
        self.overlay_img.attributes("-fullscreen", False)
        self.overlay_img.geometry(
            f"{self.winfo_width()}x{self.winfo_height()}+{self.winfo_rootx()}+{self.winfo_rooty()}")
        self.overlay_img.overrideredirect(True)
        self.overlay_img.configure(bg="")
        img = Image.open(path)
        w, h = self.winfo_width(), self.winfo_height()
        img.thumbnail((w - 150, h - 200))
        photo = ImageTk.PhotoImage(img)
        self.enlarged_photo = photo
        lbl = tk.Label(self.overlay_img, image=photo, bg="black", cursor="hand2")
        lbl.image = photo
        lbl.place(relx=0.5, rely=0.5, anchor="center")
        for win in (self.overlay_bg, self.overlay_img):
            win.bind("<Button-1>", lambda e: [self.overlay_bg.destroy(), self.overlay_img.destroy()])
        self.overlay_img.lift()


class QuizPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        ttk.Button(self, text="Vissza", command=lambda: controller.show_frame("MainMenu")).place(relx=0.02, rely=0.01)
        self.questions = [("Hol játszódik a Metro 2033?", ["Moszkva", "London", "New York", "Tokió"], 0),
            ("Ki írta a regényt?", ["Orwell", "Tolkien", "King", "Glukhovsky"], 3),
            ("Ki a főszereplője a könyveknek?", ["Melnyik","Artyom", "Anna", "Ulman"], 1)]
        self.index = 0
        self.score = 0
        self.q_label = tk.Label(self, text="", font=("Arial", 16), fg="white", bd=0, highlightthickness=0)
        self.q_label.place(relx=0.05, rely=0.30, relwidth=0.9)
        controller.after(300, lambda: controller.set_transparent_label_bg(self.q_label))
        self.var = tk.IntVar()
        self.options = [ttk.Radiobutton(self, text="", variable=self.var, value=i) for i in range(4)]
        for i, opt in enumerate(self.options):
            opt.place(relx=0.1, rely=0.47 + i * 0.08)
        ttk.Button(self, text="Következő", command=self.next_question).place(relx=0.8, rely=0.85)
        self.show_question()

    def show_question(self):
        q, answers, _ = self.questions[self.index]
        self.q_label.config(text=q)
        self.var.set(-1)
        for i, text in enumerate(answers):
            self.options[i].config(text=text)
        self.controller.set_transparent_label_bg(self.q_label)

    def next_question(self):
        _, _, correct = self.questions[self.index]
        if self.var.get() == correct:
            self.score += 1
        self.index += 1
        if self.index >= len(self.questions):
            self.show_result()
        else:
            self.show_question()

    def show_result(self):
        for widget in self.options:
            widget.place_forget()
        self.q_label.config(text=f"Eredményed: {self.score}/{len(self.questions)}")


if __name__ == "__main__":
    app = App()
    app.update_background()
    app.mainloop()