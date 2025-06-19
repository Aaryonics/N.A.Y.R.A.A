import asyncio
import tkinter as tk
from core.engine import NayraaEngine
from gui.main_window import NayraaGUI
from gui.system_tray import SystemTrayManager
from config.settings import Settings
import threading


# ✅ Global event loop setup
global_async_loop = asyncio.new_event_loop()

def start_loop():
    asyncio.set_event_loop(global_async_loop)
    global_async_loop.run_forever()

threading.Thread(target=start_loop, daemon=True).start()

class NayraaApp:
    def __init__(self):
        self.settings = Settings()
        self.root = tk.Tk()
        self.root.withdraw()  # Start hidden
        self.engine = NayraaEngine(self.settings)
        self.gui = NayraaGUI(self.engine, self.root, global_async_loop)
        self.tray_manager = SystemTrayManager(self.gui, self.engine, self.root)

    async def start_engine(self):
        await self.engine.initialize()
        await self.engine.run()

if __name__ == "__main__":
    app = NayraaApp()

    if app.settings.start_minimized:
        # Start tray
        threading.Thread(target=app.tray_manager.start, daemon=True).start()
        app.root.mainloop()  # Runs forever until tray opens GUI
    else:
        app.gui.show()  # ✅ THIS is what was missing
