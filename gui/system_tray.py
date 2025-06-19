import pystray
from PIL import Image, ImageDraw
import threading

class SystemTrayManager:
    def __init__(self, gui, engine, root):
        self.gui = gui
        self.engine = engine
        self.root = root

    def create_icon(self):
        # Create a simple icon (circle)
        img = Image.new("RGB", (64, 64), color="white")
        draw = ImageDraw.Draw(img)
        draw.ellipse((16, 16, 48, 48), fill="blue")
        return img

    def on_show(self, icon, item):
        # Use .after to safely call from system tray (thread-safe)
        self.root.after(0, self.gui.show)


    def on_exit(self, icon, item):
        icon.stop()

    def start(self):
        image = self.create_icon()
        menu = pystray.Menu(
            pystray.MenuItem("Open Nayraa", self.on_show),
            pystray.MenuItem("Exit", self.on_exit)
        )
        self.icon = pystray.Icon("Nayraa", image, "Nayraa Assistant", menu)
        threading.Thread(target=self.icon.run).start()
