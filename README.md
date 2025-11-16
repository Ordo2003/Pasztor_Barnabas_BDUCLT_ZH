Hallgató neve: Pásztor Barnabás

Hallgató NEPTUN kódja: BDUCLT

Feladat leírása: A beadandó egy grafikus felületű, multimédiás Python alkalmazás, amely a Metro 2033 világát mutatja be.

A program három fő, és egy kis funkciót tartalmaz:

Világleírás – Több oldalas szöveges ismertető a Metro 2033 univerzumáról.

Galéria – Képek megjelenítése saját leírásokkal, egy kattintásra nagyítható nézettel.

Kvíz – Három kérdésből álló interaktív feleletválasztós játék, a végén kiértékeléssel.

Zene – Egy háttérzene hangzik fel a program indulásával egyidejűleg, ami manuálisan megállítható, de a program bezárásával automatikusan is leáll.

Modulok, osztályok és függvények:

Modulok:

Tanult modul: tkinter

Bemutatandó modul: pygame

Saját modul: pb_resize_image (A PIL modul felhasználásával.)

Osztályok:

App – a teljes alkalmazás fő ablaka, háttérkezeléssel, zenevezérléssel, és a főmenüvel. (root = App())

BasePage – A különböző oldalak alapkerete.

MainMenu – A főmenü nézete. 

WorldPage – Többoldalas, lapozható világleíró oldal. 

GalleryPage – Galéria a Metro 2033 képeiről.

QuizPage – Kvíz oldal.

Függvények:

App: 

load_background()

_initial_paint()

update_background()

set_transparent_label_bg()

_apply_label_bg()

on_resize()

show_frame()

toggle_music()

on_quit()

WorldPage:

show_text()

next_page()

prev_page()

GalleryPage:

load_gallery()

toggle_image()

QuizPage

show_question()

next_question()

show_result()
