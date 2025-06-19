import tkinter as tk
import asyncio

class NayraaGUI:
    def __init__(self, engine, root=None, async_loop=None):
        self.engine = engine
        self.loop = async_loop
        self.window = root or tk.Tk()
        self.window.title("Nayraa Assistant")
        self.window.geometry("500x500")
        self.build_ui()

    def build_ui(self):
        self.text_area = tk.Text(self.window, wrap=tk.WORD, height=25, width=60)
        self.text_area.pack(padx=10, pady=10)

        self.entry = tk.Entry(self.window, width=40)
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", self.on_enter)

        self.send_button = tk.Button(self.window, text="Ask", command=self.on_click)
        self.send_button.pack()

    def show(self):
        try:
            self.window.deiconify()
        except:
            pass
        self.window.mainloop()

    def display_message(self, sender, message):
        self.text_area.insert(tk.END, f"{sender}: {message}\n")
        self.text_area.see(tk.END)

    def on_click(self):
        user_input = self.entry.get().strip()
        self.entry.delete(0, tk.END)
        if user_input:
            self.display_message("You", user_input)
            print("🟢 Button Clicked — handling input")
            self.handle_input(user_input)

    def on_enter(self, event):
        self.on_click()

    def handle_input(self, user_input):
        async def run():
            try:
                print("📥 User input received:", user_input)
                response = await self.engine.generate_response(user_input)
                print("🤖 Response generated:", response)
                self.display_message("Nayraa", response)
                await self.engine.speak_response(response)
            except Exception as e:
                print("❌ Error in run():", e)
                self.display_message("Nayraa", f"(Error: {e})")

        if self.loop:
            asyncio.run_coroutine_threadsafe(run(), self.loop)
        else:
            print("❌ Async loop not set!")
