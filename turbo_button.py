import customtkinter as ctk
import threading
import time
from pynput import keyboard, mouse

# Configurazione di CustomTkinter
ctk.set_appearance_mode("dark")  # Modalità: "light", "dark", "system"
ctk.set_default_color_theme("blue")  # Temi disponibili: "blue", "green", "dark-blue"

class ClickerApp:
    def __init__(self):
        # Inizializzazione delle variabili
        self.clicking_active = False
        self.frequency = 100  # Frequenza iniziale dei click al secondo
        self.frequency_lock = threading.Lock()
        self.state_lock = threading.Lock()
        self.click_count = 0
        self.click_count_lock = threading.Lock()
        self.running = True
        self.animation_thread = None  # Per gestire l'animazione
        self.mode = "Toggle"  # Modalità predefinita
        self.ctrl_pressed = False  # Flag per monitorare lo stato del tasto CTRL

        # Setup dell'interfaccia CustomTkinter
        self.root = ctk.CTk()
        self.root.title("Clicker Bot")
        self.root.geometry("600x450")  # Dimensione della finestra
        self.root.attributes('-topmost', True)  # Finestra sempre in primo piano
        self.root.resizable(False, False)

        # Frame per il selettore di modalità
        self.mode_frame = ctk.CTkFrame(self.root)
        self.mode_frame.pack(pady=10)

        self.mode_label = ctk.CTkLabel(
            self.mode_frame,
            text="Select Mode:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white"
        )
        self.mode_label.pack(side="left", padx=(10, 5))

        self.mode_var = ctk.StringVar(value="Toggle")
        self.mode_optionmenu = ctk.CTkOptionMenu(
            self.mode_frame,
            values=["Toggle", "Push to Activate"],
            variable=self.mode_var,
            command=self.on_mode_change
        )
        self.mode_optionmenu.pack(side="left", padx=5)

        # Frame per il controllo della frequenza
        self.freq_frame = ctk.CTkFrame(self.root)
        self.freq_frame.pack(pady=10)

        self.freq_label = ctk.CTkLabel(
            self.freq_frame,
            text="Frequency (Clicks/Second):",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white"
        )
        self.freq_label.pack(side="left", padx=(10, 5))

        self.freq_var = ctk.StringVar(value=str(self.frequency))
        self.freq_entry = ctk.CTkEntry(
            self.freq_frame,
            width=100,
            textvariable=self.freq_var,
            validate="focusout",
            validatecommand=self.validate_freq
        )
        self.freq_entry.pack(side="left", padx=5)
        self.freq_entry.bind("<Return>", self.update_frequency)

        # Label per mostrare lo stato (ARMED/DISARMED)
        self.status_label = ctk.CTkLabel(
            self.root,
            text="DISARMED",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white",
            fg_color="#00FF00",  # Verde per DISARMED
            corner_radius=10,
            width=200,
            height=50
        )
        self.status_label.pack(pady=10)

        # Label per mostrare le istruzioni e il conteggio dei click
        self.instructions_label = ctk.CTkLabel(
            self.root,
            text=self.build_instructions(cps=0),
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white",
            fg_color='transparent',
            justify="left",
            anchor="w"
        )
        self.instructions_label.pack(expand=True, fill="both", padx=20, pady=20)

        # Listener per la tastiera
        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_key_press,
            on_release=self.on_key_release
        )
        self.keyboard_listener.start()

        # Listener per il mouse (rotellina)
        self.mouse_listener = mouse.Listener(
            on_scroll=self.on_scroll
        )
        self.mouse_listener.start()

        # Controller del mouse per eseguire i click
        self.mouse_controller = mouse.Controller()

        # Avvio del thread di aggiornamento dell'interfaccia
        self.update_label()

    def build_instructions(self, cps):
        """Costruisce il testo delle istruzioni."""
        if self.mode == "Toggle":
            instructions = (
                "Instructions:\n\n"
                "CTRL Toggle = Spam/Stop Clicks\n"
                "Mouse Wheel ↑ = Clicks ++\n"
                "Mouse Wheel ↓ = Clicks --\n"
                f"# of Clicks/Second = {self.frequency}\n\n"
                "Credits: Salvatore Gambino"
            )
        elif self.mode == "Push to Activate":
            instructions = (
                "Instructions:\n\n"
                "CTRL Push = Spam Clicks\n"
                "CTRL Release = Stop Clicks\n"
                "Mouse Wheel ↑ = Clicks ++\n"
                "Mouse Wheel ↓ = Clicks --\n"
                f"# of Clicks/Second = {self.frequency}\n\n"
                "Credits: Salvatore Gambino"
            )
        else:
            instructions = "No instructions available."
        return instructions

    def validate_freq(self):
        """Valida e aggiorna la frequenza dal campo di input."""
        freq_str = self.freq_var.get()
        try:
            freq = int(freq_str)
            if freq < 1:
                raise ValueError
            with self.frequency_lock:
                self.frequency = freq
            return True
        except ValueError:
            # Ripristina il valore precedente in caso di input non valido
            self.freq_var.set(str(self.frequency))
            return False

    def update_frequency(self, event=None):
        """Aggiorna la frequenza"""
        if self.validate_freq():
            # Aggiorna la label delle istruzioni nel thread principale
            self.root.after(0, self.update_instructions_label)

    def on_mode_change(self, new_mode):
        """Gestisce il cambiamento di modalità."""
        with self.state_lock:
            if self.clicking_active:
                self.stop_clicking()
            self.mode = new_mode
            # Aggiorna la label delle istruzioni nel thread principale
            self.root.after(0, self.update_instructions_label)
            self.animate_inactive()

    def on_key_press(self, key):
        """Gestisce l'evento di pressione del tasto CTRL in base alla modalità."""
        try:
            if key in [keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]:
                if self.mode == "Toggle":
                    if not self.ctrl_pressed:
                        self.ctrl_pressed = True  # Imposta il flag per evitare toggling multiplo
                elif self.mode == "Push to Activate":
                    self.start_clicking()
                    self.update_status_label()
        except AttributeError:
            pass  # Gestisce altri tasti senza fare nulla

    def on_key_release(self, key):
        """Gestisce l'evento di rilascio del tasto CTRL in base alla modalità."""
        try:
            if key in [keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]:
                if self.mode == "Toggle":
                    if self.ctrl_pressed:
                        # Esegui il toggle nel thread principale
                        self.root.after(0, self.toggle_clicking)
                        self.ctrl_pressed = False  # Resetta il flag
                elif self.mode == "Push to Activate":
                    self.stop_clicking()
                    self.update_status_label()
        except AttributeError:
            pass  # Gestisce altri tasti senza fare nulla

    def toggle_clicking(self):
        """Esegue il toggle del processo di click."""
        if not self.clicking_active:
            self.start_clicking()
        else:
            self.stop_clicking()
        # Aggiorna lo stato nel thread principale
        self.root.after(0, self.update_status_label)

    def on_scroll(self, x, y, dx, dy):
        """Gestisce lo scroll della rotellina del mouse per modificare la frequenza dei click."""
        try:
            if self.clicking_active:
                with self.frequency_lock:
                    self.frequency += dy * 150  # Incremento di 10 cps per scroll
                    if self.frequency < 1:
                        self.frequency = 1  # Impedisce frequenze inferiori a 1 cps
                # Aggiorna la frequenza nel campo di input e le istruzioni
                self.root.after(0, lambda: self.freq_var.set(str(self.frequency)))
                self.root.after(0, self.update_instructions_label)
        except Exception as e:
            print(f"Errore in on_scroll: {e}")

    def update_status_label(self):
        """Aggiorna la label dello stato (ARMED/DISARMED) con il colore appropriato."""
        if self.clicking_active:
            status = "ARMED"
            bg_color = "#FF0000"  # Rosso per ARMED
        else:
            status = "DISARMED"
            bg_color = "#00FF00"  # Verde per DISARMED
        self.status_label.configure(text=status, fg_color=bg_color)

    def update_instructions_label(self):
        """Aggiorna la label delle istruzioni."""
        instructions = self.build_instructions(cps=self.frequency)
        self.instructions_label.configure(text=instructions)

    def start_clicking(self):
        """Avvia il processo di click."""
        with self.state_lock:
            if not self.clicking_active:
                self.clicking_active = True
                self.click_count = 0
                print("Clicking started.")
                # Aggiorna le istruzioni e lo stato nel thread principale
                self.root.after(0, self.update_instructions_label)
                self.root.after(0, self.update_status_label)
                self.animate_active()
                self.click_thread = threading.Thread(target=self.clicking_loop, daemon=True)
                self.click_thread.start()

    def stop_clicking(self):
        """Ferma il processo di click."""
        with self.state_lock:
            if self.clicking_active:
                self.clicking_active = False
                print("Clicking stopped.")
                # Aggiorna le istruzioni e lo stato nel thread principale
                self.root.after(0, self.update_instructions_label)
                self.root.after(0, self.update_status_label)
                self.animate_inactive()

    def clicking_loop(self):
        """Loop che esegue i click a una frequenza regolabile."""
        try:
            while self.clicking_active:
                with self.frequency_lock:
                    freq = self.frequency
                # Esegue un click sinistro del mouse
                self.mouse_controller.click(mouse.Button.left, 1)
                with self.click_count_lock:
                    self.click_count += 1
                # Calcola il tempo di attesa basato sulla frequenza
                time.sleep(1.0 / freq)
        except Exception as e:
            print(f"Errore nel clicking_loop: {e}")

    def update_label(self):
        """Aggiorna la label delle istruzioni periodicamente."""
        try:
            if self.clicking_active:
                # Aggiorna le istruzioni nel thread principale
                self.root.after(0, self.update_instructions_label)
            # Aggiorna la label ogni 500 ms
            self.root.after(500, self.update_label)
        except Exception as e:
            print(f"Errore in update_label: {e}")

    def animate_active(self):
        """Inizia l'animazione quando il clicker è attivo."""
        if self.animation_thread and self.animation_thread.is_alive():
            return  # Previene la creazione di più thread di animazione

        def animate():
            try:
                while self.clicking_active:
                    for color in ["#FF5733", "#33FF57", "#3357FF", "#F333FF"]:
                        if not self.clicking_active:
                            break
                        # Aggiorna il colore della label di stato
                        self.root.after(0, self.status_label.configure, {'fg_color': color})
                        time.sleep(0.3)
            except Exception as e:
                print(f"Errore in animate_active: {e}")

        self.animation_thread = threading.Thread(target=animate, daemon=True)
        self.animation_thread.start()

    def animate_inactive(self):
        """Ferma l'animazione quando il clicker è inattivo."""
        try:
            # Aggiorna lo stato della label
            self.update_status_label()
        except Exception as e:
            print(f"Errore in animate_inactive: {e}")

    def run(self):
        """Avvia l'interfaccia grafica."""
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def on_close(self):
        """Gestisce la chiusura dell'applicazione."""
        self.running = False
        self.clicking_active = False
        self.keyboard_listener.stop()
        self.mouse_listener.stop()
        self.root.destroy()

if __name__ == "__main__":
    app = ClickerApp()
    app.run()
