#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Juego Bíblico tipo Quiz (Tkinter, solo Python estándar)

Cómo ejecutar en Mac:
  python3 biblia_quiz_tk.py

Nota: Tkinter debe estar disponible (el instalador de Python.org suele incluirlo).
"""

import json
import os
import random
import tkinter as tk
from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class Question:
    text: str
    options: List[str]
    correct: int
    explanation: str
    difficulty: str  # "easy" or "hard"


class QuestionBank:
    def __init__(self) -> None:
        self.questions: List[Question] = []
        self._load_questions()

    def _load_questions(self) -> None:
        # 20 faciles + 21 dificiles, AT y NT, sin ambiguedad
        easy = [
            Question("¿Quién construyó el arca?", ["Noé", "Moisés", "Abraham", "David"], 0,
                     "Noé construyó el arca por mandato de Dios.", "easy"),
            Question("¿Cuál fue el primer libro de la Biblia?", ["Génesis", "Éxodo", "Levítico", "Salmos"], 0,
                     "Génesis es el primer libro.", "easy"),
            Question("¿Quién fue tragado por un gran pez?", ["Jonás", "Elías", "Pablo", "José"], 0,
                     "Jonás estuvo en el pez tres días.", "easy"),
            Question("¿En qué ciudad nació Jesús?", ["Belén", "Nazaret", "Jerusalén", "Capernaúm"], 0,
                     "Jesús nació en Belén.", "easy"),
            Question("¿Cuántos mandamientos recibió Moisés?", ["10", "12", "7", "5"], 0,
                     "Moisés recibió diez mandamientos.", "easy"),
            Question("¿Quién derrotó a Goliat?", ["David", "Saúl", "Sansón", "Josué"], 0,
                     "David venció a Goliat con una honda.", "easy"),
            Question("¿Cuál es la oración que Jesús enseñó?", ["Padre Nuestro", "Salmo 23", "Shema", "Magnificat"], 0,
                     "Jesús enseñó el Padre Nuestro.", "easy"),
            Question("¿Qué mar se abrió para Israel?", ["Mar Rojo", "Mar de Galilea", "Mediterráneo", "Mar Muerto"], 0,
                     "El Mar Rojo se abrió.", "easy"),
            Question("¿Cuál fue el primer milagro de Jesús?", ["Agua en vino", "Multiplicar panes", "Sanar ciego", "Caminar en agua"], 0,
                     "Convirtió agua en vino en Caná.", "easy"),
            Question("¿Quién escribió muchos Salmos?", ["David", "Salomón", "Isaías", "Pedro"], 0,
                     "David escribió muchos salmos.", "easy"),
            Question("¿Qué árbol prohibido estaba en el Edén?", ["Árbol del conocimiento", "Higuera", "Cedro", "Olivo"], 0,
                     "El árbol del conocimiento del bien y del mal.", "easy"),
            Question("¿Quién traicionó a Jesús?", ["Judas", "Pedro", "Juan", "Tomás"], 0,
                     "Judas Iscariote lo traicionó.", "easy"),
            Question("¿Quién lideró a Israel a la Tierra Prometida?", ["Josué", "Caleb", "Gedeón", "Samuel"], 0,
                     "Josué entró con el pueblo.", "easy"),
            Question("¿Cuántos evangelios hay?", ["4", "3", "5", "2"], 0,
                     "Hay cuatro evangelios.", "easy"),
            Question("¿Quién fue conocido por su fuerza y cabello?", ["Sansón", "Saúl", "Elías", "Job"], 0,
                     "Sansón tenía fuerza especial.", "easy"),
            Question("¿Cuál es el último libro de la Biblia?", ["Apocalipsis", "Judas", "Hebreos", "Hechos"], 0,
                     "Apocalipsis es el último.", "easy"),
            Question("¿Quién fue la madre de Jesús?", ["María", "Marta", "Ana", "Elisabet"], 0,
                     "María fue la madre de Jesús.", "easy"),
            Question("¿Qué rey pidió sabiduría a Dios?", ["Salomón", "David", "Acab", "Herodes"], 0,
                     "Salomón pidió sabiduría.", "easy"),
            Question("¿Quién construyó el templo en Jerusalén?", ["Salomón", "David", "Nehemías", "Zorobabel"], 0,
                     "Salomón construyó el templo.", "easy"),
            Question("¿Cuántos discípulos tuvo Jesús?", ["12", "10", "70", "7"], 0,
                     "Jesús tuvo doce discípulos.", "easy"),
        ]
        hard = [
            Question("¿Cuál profeta tuvo una visión de un valle de huesos secos?", ["Ezequiel", "Jeremías", "Isaías", "Oseas"], 0,
                     "Ezequiel vio los huesos secos.", "hard"),
            Question("¿Quién era el padre de Juan el Bautista?", ["Zacarías", "Elí", "José", "Simeón"], 0,
                     "Zacarías era sacerdote.", "hard"),
            Question("¿Qué juez de Israel derrotó a los madianitas con 300 hombres?", ["Gedeón", "Jefté", "Sansón", "Otoniel"], 0,
                     "Gedeón lideró a los 300.", "hard"),
            Question("¿En qué monte recibió Moisés la Ley?", ["Sinaí", "Carmelo", "Gerizim", "Hermón"], 0,
                     "La Ley se dio en el Sinaí.", "hard"),
            Question("¿Qué discípulo caminó sobre el agua con Jesús?", ["Pedro", "Juan", "Santiago", "Andrés"], 0,
                     "Pedro caminó sobre el agua.", "hard"),
            Question("¿Quién interpretó el sueño de Nabucodonosor sobre la estatua?", ["Daniel", "Jeremías", "Ezequiel", "Esdras"], 0,
                     "Daniel interpretó el sueño.", "hard"),
            Question("¿Cuál era el nombre hebreo de la reina Ester?", ["Hadassa", "Mical", "Rut", "Noemí"], 0,
                     "Ester se llamaba Hadassa.", "hard"),
            Question("¿Qué apóstol escribió la mayoría de las epístolas del NT?", ["Pablo", "Pedro", "Juan", "Santiago"], 0,
                     "Pablo escribió la mayoría.", "hard"),
            Question("¿En qué ciudad fue llamado Pablo después de su conversión?", ["Damasco", "Antioquía", "Jerusalén", "Éfeso"], 0,
                     "La conversión ocurrió camino a Damasco.", "hard"),
            Question("¿Quién dijo: 'No he visto fe tan grande en Israel'?", ["Jesús", "Pedro", "Pablo", "Juan"], 0,
                     "Jesús lo dijo del centurión.", "hard"),
            Question("¿Qué rey fue alcanzado por la lepra por usurpar el sacerdocio?", ["Uzías", "Saúl", "Ezequías", "Joás"], 0,
                     "Uzías fue herido con lepra.", "hard"),
            Question("¿Quién escribió el libro de Lamentaciones?", ["Jeremías", "Isaías", "Ezequiel", "Habacuc"], 0,
                     "Tradicionalmente se atribuye a Jeremías.", "hard"),
            Question("¿Qué profeta desafió a los profetas de Baal en el Carmelo?", ["Elías", "Eliseo", "Jonás", "Amós"], 0,
                     "Elías desafió a Baal.", "hard"),
            Question("¿Cuál era el nombre del sumo sacerdote que juzgó a Jesús?", ["Caifás", "Anás", "Eleazar", "Sadoc"], 0,
                     "Caifás presidió el juicio.", "hard"),
            Question("¿Qué libro contiene el 'Sermón del Monte'?", ["Mateo", "Marcos", "Lucas", "Juan"], 0,
                     "El Sermón del Monte está en Mateo.", "hard"),
            Question("¿Quién fue el primer mártir cristiano?", ["Esteban", "Santiago", "Pedro", "Pablo"], 0,
                     "Esteban fue apedreado.", "hard"),
            Question("¿Qué ciudad destruyó Dios junto con Gomorra?", ["Sodoma", "Nínive", "Jericó", "Tiro"], 0,
                     "Sodoma y Gomorra fueron destruidas.", "hard"),
            Question("¿En qué río fue bautizado Jesús?", ["Jordán", "Éufrates", "Tigris", "Nilo"], 0,
                     "Jesús fue bautizado en el Jordán.", "hard"),
            Question("¿Qué carta fue escrita a una iglesia conocida por su tibieza?", ["Apocalipsis a Laodicea", "Gálatas", "Filipenses", "Colosenses"], 0,
                     "Laodicea es reprendida por tibia.", "hard"),
            Question("¿Cuántos años estuvo Israel en el desierto?", ["40", "70", "12", "30"], 0,
                     "Fueron 40 años en el desierto.", "hard"),
            Question("Como se llamo el papa de sanson?", ["manoa", "saul", "micaia", "malquesua"], 0,
                     " el papa de sanson se llamaba , manoa", "hard"),
        ]
        self.questions = easy + hard

    def get_questions(self, mode: str, count: int) -> List[Question]:
        if mode == "easy":
            pool = [q for q in self.questions if q.difficulty == "easy"]
        elif mode == "hard":
            pool = [q for q in self.questions if q.difficulty == "hard"]
        else:
            pool = self.questions[:]
        random.shuffle(pool)
        return pool[:count]


class ScoreStore:
    def __init__(self, path: str) -> None:
        self.path = path
        self.data: Dict[str, int] = {"easy": 0, "hard": 0, "mixed": 0}
        self._load()

    def _load(self) -> None:
        if not os.path.exists(self.path):
            self._save()
            return
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                raw = json.load(f)
            if not isinstance(raw, dict):
                raise ValueError("bad json")
            for key in self.data:
                if isinstance(raw.get(key), int):
                    self.data[key] = raw[key]
        except Exception:
            # Reset if corrupt
            self.data = {"easy": 0, "hard": 0, "mixed": 0}
            self._save()

    def _save(self) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def get(self, mode: str) -> int:
        return self.data.get(mode, 0)

    def update_if_high(self, mode: str, score: int) -> bool:
        if score > self.data.get(mode, 0):
            self.data[mode] = score
            self._save()
            return True
        return False


class SoundEngine:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.enabled = True

    def set_enabled(self, enabled: bool) -> None:
        self.enabled = enabled

    def _bell(self) -> None:
        if self.enabled:
            self.root.bell()

    def click(self) -> None:
        self._bell()

    def correct(self) -> None:
        if not self.enabled:
            return
        # Ritmo alegre: 3 bells
        self.root.bell()
        self.root.after(120, self.root.bell)
        self.root.after(240, self.root.bell)

    def incorrect(self) -> None:
        if not self.enabled:
            return
        self.root.bell()
        self.root.after(220, self.root.bell)


class QuizApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Isaac Ruiz - Python Developer")
        self.root.geometry("900x620")
        self.root.minsize(760, 540)
        self.root.configure(bg="#12151b")

        self.bank = QuestionBank()
        self.scores = ScoreStore("highscore.json")
        self.sound = SoundEngine(root)

        # State
        self.mode_var = tk.StringVar(value="mixed")
        self.count_var = tk.IntVar(value=20)
        self.sound_var = tk.BooleanVar(value=True)
        self.lives_var = tk.BooleanVar(value=False)

        self.current_questions: List[Question] = []
        self.current_index = 0
        self.score = 0
        self.correct_count = 0
        self.wrong_count = 0
        self.streak = 0
        self.max_streak = 0
        self.lives = 3
        self.answered = False
        self.current_mode_key = "mixed"

        self._build_ui()
        self.show_start()

    def _build_ui(self) -> None:
        self.container = tk.Frame(self.root, bg="#12151b")
        self.container.pack(fill="both", expand=True)

        self.frames: Dict[str, tk.Frame] = {
            "start": tk.Frame(self.container, bg="#12151b"),
            "game": tk.Frame(self.container, bg="#12151b"),
            "end": tk.Frame(self.container, bg="#12151b"),
        }
        for f in self.frames.values():
            f.place(relx=0, rely=0, relwidth=1, relheight=1)

        self._build_start(self.frames["start"])
        self._build_game(self.frames["game"])
        self._build_end(self.frames["end"])

    def _title_label(self, parent: tk.Widget, text: str) -> tk.Label:
        return tk.Label(parent, text=text, bg="#12151b", fg="#f5f7ff",
                        font=("Helvetica Neue", 28, "bold"))

    def _subtitle_label(self, parent: tk.Widget, text: str) -> tk.Label:
        return tk.Label(parent, text=text, bg="#12151b", fg="#b8c1d9",
                        font=("Helvetica Neue", 13))

    def _build_start(self, frame: tk.Frame) -> None:
        top = tk.Frame(frame, bg="#12151b")
        top.pack(pady=30)
        self._title_label(top, "Juego Bíblico Kingston").pack()
        self._subtitle_label(top, "Antiguo y Nuevo Testamento").pack(pady=6)

        card = tk.Frame(frame, bg="#1b2029", bd=0, highlightthickness=1,
                        highlightbackground="#2c3443")
        card.pack(padx=60, pady=20, fill="x")

        row1 = tk.Frame(card, bg="#1b2029")
        row1.pack(fill="x", pady=14, padx=16)
        tk.Label(row1, text="Modo", bg="#1b2029", fg="#dbe2f4",
                 font=("Helvetica Neue", 12, "bold")).pack(anchor="w")
        modes = tk.Frame(row1, bg="#1b2029")
        modes.pack(anchor="w", pady=6)
        for text, val in [("Solo Fácil", "easy"), ("Solo Difícil", "hard"), ("Mixto", "mixed")]:
            tk.Radiobutton(modes, text=text, value=val, variable=self.mode_var,
                           bg="#1b2029", fg="#e6ecff", selectcolor="#2b3342",
                           activebackground="#1b2029", activeforeground="#ffffff").pack(side="left", padx=8)

        row2 = tk.Frame(card, bg="#1b2029")
        row2.pack(fill="x", pady=14, padx=16)
        tk.Label(row2, text="Número de preguntas", bg="#1b2029", fg="#dbe2f4",
                 font=("Helvetica Neue", 12, "bold")).pack(anchor="w")
        counts = tk.Frame(row2, bg="#1b2029")
        counts.pack(anchor="w", pady=6)
        for c in [10, 20, 30, 40]:
            tk.Radiobutton(counts, text=str(c), value=c, variable=self.count_var,
                           bg="#1b2029", fg="#e6ecff", selectcolor="#2b3342",
                           activebackground="#1b2029", activeforeground="#ffffff").pack(side="left", padx=8)

        row3 = tk.Frame(card, bg="#1b2029")
        row3.pack(fill="x", pady=14, padx=16)
        tk.Label(row3, text="Ajustes", bg="#1b2029", fg="#dbe2f4",
                 font=("Helvetica Neue", 12, "bold")).pack(anchor="w")
        toggles = tk.Frame(row3, bg="#1b2029")
        toggles.pack(anchor="w", pady=6)
        tk.Checkbutton(toggles, text="Activar vidas (3)", variable=self.lives_var,
                       bg="#1b2029", fg="#e6ecff", selectcolor="#2b3342",
                       activebackground="#1b2029", activeforeground="#ffffff").pack(side="left", padx=8)
        tk.Checkbutton(toggles, text="Sonido", variable=self.sound_var,
                       bg="#1b2029", fg="#e6ecff", selectcolor="#2b3342",
                       activebackground="#1b2029", activeforeground="#ffffff").pack(side="left", padx=8)

        self.start_btn = tk.Button(frame, text="Iniciar", command=self.start_game,
                                   bg="#ff8f1f", fg="#12151b", activebackground="#ffb15a",
                                   font=("Helvetica Neue", 14, "bold"), padx=20, pady=8, bd=0)
        self.start_btn.pack(pady=16)

    def _build_game(self, frame: tk.Frame) -> None:
        header = tk.Frame(frame, bg="#12151b")
        header.pack(fill="x", pady=10, padx=16)

        self.score_lbl = tk.Label(header, text="Puntos: 0", bg="#12151b", fg="#14f0a0",
                                  font=("Helvetica Neue", 13, "bold"))
        self.score_lbl.pack(side="left")

        self.progress_lbl = tk.Label(header, text="Pregunta 1/10", bg="#12151b", fg="#e309c9",
                                     font=("Helvetica Neue", 12))
        self.progress_lbl.pack(side="left", padx=16)

        self.streak_lbl = tk.Label(header, text="Racha: 0", bg="#12151b", fg="#cffa0b",
                                   font=("Helvetica Neue", 12))
        self.streak_lbl.pack(side="left", padx=16)

        self.lives_lbl = tk.Label(header, text="Vidas: 3", bg="#12151b", fg="#b8c1d9",
                                  font=("Helvetica Neue", 12))
        self.lives_lbl.pack(side="left", padx=16)

        self.high_lbl = tk.Label(header, text="High Score: 0", bg="#12151b", fg="#06c8f4",
                                 font=("Helvetica Neue", 12, "bold"))
        self.high_lbl.pack(side="right")

        self.card = tk.Frame(frame, bg="#1b2029", bd=0, highlightthickness=1,
                             highlightbackground="#2c3443")
        self.card.pack(fill="both", expand=True, padx=40, pady=20)

        self.question_lbl = tk.Label(self.card, text="Pregunta", bg="#1b2029", fg="#f5f7ff",
                                     wraplength=760, justify="center",
                                     font=("Helvetica Neue", 20, "bold"))
        self.question_lbl.pack(pady=24, padx=20)

        self.answers_frame = tk.Frame(self.card, bg="#1b2029")
        self.answers_frame.pack(pady=10)

        self.answer_buttons: List[tk.Button] = []
        for i in range(4):
            btn = tk.Button(self.answers_frame, text="Opción", width=30, pady=10,
                            bg="#2b3342", fg="#ed04d9", bd=0,
                            activebackground="#3a465b", activeforeground="#ffffff",
                            font=("Helvetica Neue", 13, "bold"),
                            command=lambda idx=i: self.on_answer(idx))
            btn.grid(row=i // 2, column=i % 2, padx=12, pady=10, sticky="nsew")
            self.answer_buttons.append(btn)

        self.expl_frame = tk.Frame(self.card, bg="#1b2029")
        self.expl_frame.pack(fill="x", pady=10)
        self.delta_lbl = tk.Label(self.expl_frame, text="", bg="#1b2029", fg="#9cd67a",
                                  font=("Helvetica Neue", 12, "bold"))
        self.delta_lbl.pack(pady=2)
        self.expl_lbl = tk.Label(self.expl_frame, text="", bg="#1b2029", fg="#cbd5ef",
                                 font=("Helvetica Neue", 12), wraplength=760, justify="center")
        self.expl_lbl.pack(pady=4)

        self.next_btn = tk.Button(self.card, text="Siguiente", command=self.next_question,
                                  bg="#7ee081", fg="#12151b", activebackground="#a0f5a3",
                                  font=("Helvetica Neue", 12, "bold"), padx=16, pady=6, bd=0)
        self.next_btn.pack(pady=10)
        self.next_btn.configure(state="disabled")

        # keyboard bindings
        self.root.bind("1", lambda e: self.on_answer(0))
        self.root.bind("2", lambda e: self.on_answer(1))
        self.root.bind("3", lambda e: self.on_answer(2))
        self.root.bind("4", lambda e: self.on_answer(3))
        self.root.bind("<Return>", lambda e: self.next_question())

    def _build_end(self, frame: tk.Frame) -> None:
        top = tk.Frame(frame, bg="#12151b")
        top.pack(pady=26)
        self._title_label(top, "Resultado Final").pack()
        self.end_summary = tk.Label(frame, text="", bg="#12151b", fg="#e6ecff",
                                    font=("Helvetica Neue", 14), justify="center")
        self.end_summary.pack(pady=12)

        self.end_btns = tk.Frame(frame, bg="#12151b")
        self.end_btns.pack(pady=10)
        tk.Button(self.end_btns, text="Reiniciar", command=self.start_game,
                  bg="#ff8f1f", fg="#12151b", activebackground="#ffb15a",
                  font=("Helvetica Neue", 12, "bold"), padx=14, pady=6, bd=0).pack(side="left", padx=8)
        tk.Button(self.end_btns, text="Volver al inicio", command=self.show_start,
                  bg="#2b3342", fg="#e6ecff", activebackground="#3a465b",
                  font=("Helvetica Neue", 12, "bold"), padx=14, pady=6, bd=0).pack(side="left", padx=8)

    def show_frame(self, name: str) -> None:
        frame = self.frames[name]
        frame.lift()

    def show_start(self) -> None:
        self.show_frame("start")

    def start_game(self) -> None:
        mode = self.mode_var.get()
        count = self.count_var.get()
        self.sound.set_enabled(self.sound_var.get())
        self.current_mode_key = mode
        self.current_questions = self.bank.get_questions(mode, count)
        self.current_index = 0
        self.score = 0
        self.correct_count = 0
        self.wrong_count = 0
        self.streak = 0
        self.max_streak = 0
        self.lives = 3
        self.answered = False

        self.update_status()
        self.show_frame("game")
        self.load_question()

    def update_status(self) -> None:
        self.score_lbl.configure(text=f"Puntos: {self.score}")
        total = len(self.current_questions) or self.count_var.get()
        self.progress_lbl.configure(
            text=f"Pregunta {self.current_index + 1}/{total}")
        self.streak_lbl.configure(text=f"Racha: {self.streak}")
        if self.lives_var.get():
            self.lives_lbl.configure(text=f"Vidas: {self.lives}")
            self.lives_lbl.pack(side="left", padx=16)
        else:
            self.lives_lbl.pack_forget()
        self.high_lbl.configure(
            text=f"High Score: {self.scores.get(self.current_mode_key)}")

    def load_question(self) -> None:
        if self.current_index >= len(self.current_questions):
            self.end_game()
            return
        self.answered = False
        q = self.current_questions[self.current_index]
        self.question_lbl.configure(text=q.text)
        for i, opt in enumerate(q.options):
            self.answer_buttons[i].configure(
                text=f"{chr(65+i)}. {opt}", state="normal", bg="#2b3342")
        self.expl_lbl.configure(text="")
        self.delta_lbl.configure(text="")
        self.next_btn.configure(state="disabled")
        self.update_status()

    def on_answer(self, idx: int) -> None:
        if self.answered:
            return
        self.answered = True
        self.sound.click()
        q = self.current_questions[self.current_index]
        correct = (idx == q.correct)

        delta = 0
        if q.difficulty == "easy":
            delta = 10 if correct else -5
        else:
            delta = 20 if correct else -10

        if correct:
            self.sound.correct()
            self.score += delta
            self.correct_count += 1
            self.streak += 1
            self.max_streak = max(self.max_streak, self.streak)
            self._flash_card("#1f3b2d", "#1b2029")
            self.delta_lbl.configure(
                text=f"+{delta} puntos | Total: {self.score}", fg="#8df09b")
        else:
            self.sound.incorrect()
            self.score += delta
            self.wrong_count += 1
            self.streak = 0
            if self.lives_var.get():
                self.lives -= 1
            self._shake_card()
            sign = "" if delta < 0 else "+"
            self.delta_lbl.configure(
                text=f"{sign}{delta} puntos | Total: {self.score}", fg="#ff9aa2")

        self.expl_lbl.configure(text=f"Explicación: {q.explanation}")

        for btn in self.answer_buttons:
            btn.configure(state="disabled")
        # highlight correct/incorrect selection
        for i, btn in enumerate(self.answer_buttons):
            if i == q.correct:
                btn.configure(bg="#2f6b3c")
            elif i == idx:
                btn.configure(bg="#7a2b2b")

        self.next_btn.configure(state="normal")
        self.update_status()

        if self.lives_var.get() and self.lives <= 0:
            self.end_game()

    def _flash_card(self, color: str, back: str) -> None:
        self.card.configure(bg=color)
        self.answers_frame.configure(bg=color)
        self.expl_frame.configure(bg=color)
        self.question_lbl.configure(bg=color)
        for btn in self.answer_buttons:
            btn.configure(activebackground=color)
        self.root.after(140, lambda: self._restore_card(back))

    def _restore_card(self, back: str) -> None:
        self.card.configure(bg=back)
        self.answers_frame.configure(bg=back)
        self.expl_frame.configure(bg=back)
        self.question_lbl.configure(bg=back)
        for btn in self.answer_buttons:
            btn.configure(activebackground="#3a465b")

    def _shake_card(self) -> None:
        # Simple shake animation by moving card frame
        start_x = self.card.winfo_x()
        start_y = self.card.winfo_y()
        offsets = [(-8, 0), (8, 0), (-6, 0), (6, 0), (0, 0)]

        def step(i: int) -> None:
            if i >= len(offsets):
                return
            dx, dy = offsets[i]
            self.card.place_configure(x=start_x + dx, y=start_y + dy)
            self.root.after(40, lambda: step(i + 1))

        self.card.place_configure(x=start_x, y=start_y)
        step(0)

    def next_question(self) -> None:
        if not self.answered:
            return
        self.current_index += 1
        self.load_question()

    def end_game(self) -> None:
        updated = self.scores.update_if_high(self.current_mode_key, self.score)
        status = "¡Nuevo récord!" if updated else ""
        summary = (
            f"Puntos: {self.score}\n"
            f"Aciertos: {self.correct_count} | Errores: {self.wrong_count}\n"
            f"Racha máxima: {self.max_streak}\n"
            f"High Score ({self.current_mode_key}): {self.scores.get(self.current_mode_key)}\n"
            f"{status}"
        )
        self.end_summary.configure(text=summary)
        self.show_frame("end")


def main() -> None:
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
