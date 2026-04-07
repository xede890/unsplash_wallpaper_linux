#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkLayerShell', '0.1')
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib, Gio, GtkLayerShell
try:
    gi.require_foreign('cairo')
    HAS_CAIRO = True
except ImportError:
    HAS_CAIRO = False
import json
import os
import random
import subprocess
import threading
import urllib.request
import time
from pathlib import Path

WALLPAPER_DIR = Path.home() / "Pictures" / "Wallpapers"
COSMIC_CONFIG = Path.home() / ".config" / "cosmic" / "com.system76.CosmicBackground" / "v1" / "all"
STATE_FILE = Path.home() / ".local" / "share" / "unsplash-wallpaper" / "state.json"
ICON_PATH = "/home/mehmet/.local/share/unsplash-wallpaper/icon.svg"
THUMB_SIZE = 260
GRID_THUMB = 100

CATEGORIES = {
    "Rastgele": None,
    "Doga": [10, 11, 15, 16, 17, 18, 19, 27, 28, 29, 36, 37, 39, 41, 42, 43, 47, 49, 50, 54, 56, 57, 58, 59, 73, 76, 82, 84, 89, 91, 94, 95, 96, 100, 104, 106, 107, 110, 111, 114, 116, 118, 119, 120, 122, 129, 131, 133, 134, 135, 136, 137, 139, 140, 141, 142, 143, 146, 147, 152, 153, 155, 156, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 190, 191, 192, 193],
    "Sehir": [1, 3, 4, 26, 48, 60, 65, 77, 78, 83, 85, 88, 101, 102, 103, 105, 113, 121, 126, 127, 154, 194, 198, 200, 202, 203, 204, 209, 210, 211, 212, 214, 217, 218, 219, 220, 224, 225, 228, 229, 231, 236, 238, 242, 244, 246, 248, 250, 252, 256, 258, 259, 260, 261, 263, 269, 271, 274, 277, 279, 282, 284, 286, 290, 291, 299],
    "Deniz": [14, 33, 45, 53, 54, 59, 82, 84, 119, 122, 129, 141, 148, 152, 155, 165, 179, 188, 189, 190, 195, 216, 234, 235, 239, 240, 243, 247, 253, 257, 264, 266, 268, 270, 273, 278, 281, 283, 292, 297],
    "Dag": [10, 15, 16, 17, 29, 41, 91, 95, 100, 104, 110, 114, 116, 120, 131, 133, 135, 139, 142, 143, 146, 156, 158, 160, 163, 167, 172, 173, 174, 176, 178, 181, 184, 185, 191, 193, 296, 298],
    "Minimal": [2, 6, 9, 12, 20, 21, 22, 23, 24, 25, 30, 31, 32, 34, 35, 38, 40, 44, 46, 51, 52, 55, 61, 62, 63, 64, 66, 67, 68, 69, 70, 71, 72, 74, 75, 79, 80, 81, 86, 87, 90, 92, 93, 97, 98, 99],
    "Renkli": [5, 7, 8, 13, 37, 42, 43, 47, 49, 50, 56, 57, 58, 73, 76, 89, 94, 96, 106, 107, 111, 118, 134, 136, 137, 140, 147, 153, 159, 161, 162, 164, 166, 168, 169, 170, 175, 177, 180, 182, 183, 186, 192],
}

WALLPAPER_DIR.mkdir(parents=True, exist_ok=True)


def get_current_wallpaper():
    try:
        text = COSMIC_CONFIG.read_text()
        for line in text.splitlines():
            if "Path(" in line:
                return line.split('Path("')[1].split('")')[0]
    except Exception:
        pass
    return None


def set_cosmic_wallpaper(filepath):
    COSMIC_CONFIG.parent.mkdir(parents=True, exist_ok=True)
    COSMIC_CONFIG.write_text(f'''(
    output: "all",
    source: Path("{filepath}"),
    filter_by_theme: true,
    rotation_frequency: 300,
    filter_method: Lanczos,
    scaling_mode: Zoom,
    sampling_method: Alphanumeric,
)
''')
    subprocess.Popen(["pkill", "cosmic-bg"], stderr=subprocess.DEVNULL)
    time.sleep(0.5)
    subprocess.Popen(["cosmic-bg"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def load_state():
    try:
        return json.loads(STATE_FILE.read_text())
    except Exception:
        return {"category": "Rastgele"}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state))


def download_wallpaper(category=None):
    id_list = CATEGORIES.get(category) if category else None
    if id_list:
        img_id = random.choice(id_list)
    else:
        img_id = random.randint(1, 1084)

    info_url = f"https://picsum.photos/id/{img_id}/info"
    req = urllib.request.Request(info_url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        author = data.get("author", "Unknown")
    except Exception:
        author = "Unknown"

    img_url = f"https://picsum.photos/id/{img_id}/1920/1200"
    filename = f"wallpaper_{img_id}_{int(time.time())}.jpg"
    filepath = WALLPAPER_DIR / filename

    req = urllib.request.Request(img_url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read()
        if len(data) < 5000:
            raise Exception("Image too small")
        filepath.write_bytes(data)

    return str(filepath), author


def get_saved_wallpapers():
    files = sorted(WALLPAPER_DIR.glob("wallpaper_*.jpg"), key=os.path.getmtime, reverse=True)
    result = [str(f) for f in files if f.stat().st_size > 5000]
    old_files = sorted(WALLPAPER_DIR.glob("unsplash_*.jpg"), key=os.path.getmtime, reverse=True)
    result += [str(f) for f in old_files if f.stat().st_size > 5000]
    return result


def make_pixbuf(filepath, size):
    try:
        return GdkPixbuf.Pixbuf.new_from_file_at_scale(filepath, size, -1, True)
    except Exception:
        return None


class PopupPanel(Gtk.Window):
    def __init__(self):
        super().__init__(type=Gtk.WindowType.TOPLEVEL)

        # Layer shell: overlay layer, anchored top-right under the panel bar
        GtkLayerShell.init_for_window(self)
        GtkLayerShell.set_layer(self, GtkLayerShell.Layer.OVERLAY)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.TOP, True)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.RIGHT, True)
        GtkLayerShell.set_margin(self, GtkLayerShell.Edge.TOP, 2)
        GtkLayerShell.set_margin(self, GtkLayerShell.Edge.RIGHT, 8)
        GtkLayerShell.set_keyboard_mode(self, GtkLayerShell.KeyboardMode.ON_DEMAND)

        self.set_resizable(False)
        self.set_default_size(300, -1)

        # Close on focus loss
        self.connect("focus-out-event", lambda w, e: self.dismiss())

        # Rounded corners and dark background
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual and HAS_CAIRO:
            self.set_visual(visual)
            self.set_app_paintable(True)
            self.connect("draw", self.on_draw)

        # Main layout
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        vbox.set_margin_top(10)
        vbox.set_margin_bottom(10)
        vbox.set_margin_start(10)
        vbox.set_margin_end(10)
        self.add(vbox)

        # Current wallpaper preview
        self.preview_image = Gtk.Image()
        vbox.pack_start(self.preview_image, False, False, 0)

        # Author/info
        self.info_label = Gtk.Label()
        self.info_label.set_markup("<small>Aktif wallpaper</small>")
        vbox.pack_start(self.info_label, False, False, 0)

        # Category selector (chip buttons)
        state = load_state()
        self.active_category = state.get("category", "Rastgele")
        self.cat_buttons = {}
        cat_flow = Gtk.FlowBox()
        cat_flow.set_max_children_per_line(4)
        cat_flow.set_min_children_per_line(3)
        cat_flow.set_selection_mode(Gtk.SelectionMode.NONE)
        cat_flow.set_row_spacing(4)
        cat_flow.set_column_spacing(4)
        for name in CATEGORIES.keys():
            btn = Gtk.Button(label=name)
            ctx = btn.get_style_context()
            if name == self.active_category:
                ctx.add_class("cat-btn-active")
            else:
                ctx.add_class("cat-btn")
            btn.connect("clicked", self.on_category_clicked, name)
            self.cat_buttons[name] = btn
            cat_flow.add(btn)
        vbox.pack_start(cat_flow, False, False, 0)

        # Refresh button
        self.refresh_btn = Gtk.Button(label="Rastgele Wallpaper")
        self.refresh_btn.connect("clicked", self.on_refresh)
        vbox.pack_start(self.refresh_btn, False, False, 0)

        # Status
        self.status_label = Gtk.Label()
        vbox.pack_start(self.status_label, False, False, 0)

        # Separator
        vbox.pack_start(Gtk.Separator(), False, False, 2)

        # Saved wallpapers
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_max_content_height(250)
        scroll.set_propagate_natural_height(True)
        self.grid = Gtk.FlowBox()
        self.grid.set_max_children_per_line(3)
        self.grid.set_min_children_per_line(3)
        self.grid.set_selection_mode(Gtk.SelectionMode.NONE)
        self.grid.set_homogeneous(True)
        self.grid.set_row_spacing(4)
        self.grid.set_column_spacing(4)
        scroll.add(self.grid)
        vbox.pack_start(scroll, True, True, 0)

        self.load_current_preview()
        self.load_saved_wallpapers()
        self.apply_css()

    def dismiss(self):
        self.destroy()

    def on_draw(self, widget, cr):
        cr.set_source_rgba(0.12, 0.12, 0.18, 0.95)
        w, h = self.get_size()
        radius = 12
        cr.new_sub_path()
        cr.arc(w - radius, radius, radius, -1.5708, 0)
        cr.arc(w - radius, h - radius, radius, 0, 1.5708)
        cr.arc(radius, h - radius, radius, 1.5708, 3.1416)
        cr.arc(radius, radius, radius, 3.1416, 4.7124)
        cr.close_path()
        cr.fill()
        return False

    def apply_css(self):
        css = Gtk.CssProvider()
        css.load_from_data(b"""
            * { background-color: transparent; color: #cdd6f4; }
            button { background: #585b70; color: #cdd6f4; border-radius: 8px; padding: 8px 16px; border: none; font-weight: bold; }
            button:hover { background: #6c7086; }
            button:active { background: #585b70; }
            .cat-btn { background: #313244; color: #7f849c; border-radius: 6px; padding: 4px 8px; border: none; font-size: 11px; }
            .cat-btn-active { background: #45475a; color: #cdd6f4; border-radius: 6px; padding: 4px 8px; border: 1px solid #89b4fa; font-size: 11px; font-weight: bold; }
            .cat-btn:hover { background: #45475a; }
            separator { background: #45475a; min-height: 1px; }
            scrolledwindow { background: transparent; }
        """)
        Gtk.StyleContext.add_provider_for_screen(
            self.get_screen(), css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def load_current_preview(self):
        current = get_current_wallpaper()
        if current and os.path.exists(current):
            pb = make_pixbuf(current, THUMB_SIZE)
            if pb:
                self.preview_image.set_from_pixbuf(pb)
                name = Path(current).stem.replace("wallpaper_", "").replace("unsplash_", "").replace("-", " ").replace("_", " ")
                self.info_label.set_markup(f"<small>{name[:40]}</small>")

    def load_saved_wallpapers(self):
        for child in self.grid.get_children():
            self.grid.remove(child)

        current = get_current_wallpaper()
        for filepath in get_saved_wallpapers()[:12]:
            pb = make_pixbuf(filepath, GRID_THUMB)
            if not pb:
                continue

            overlay = Gtk.Overlay()
            img = Gtk.Image.new_from_pixbuf(pb)
            event_box = Gtk.EventBox()
            event_box.add(img)
            event_box.connect("button-press-event", self.on_wallpaper_click, filepath)
            event_box.set_tooltip_text("Wallpaper olarak ayarla")
            overlay.add(event_box)

            if filepath == current:
                badge = Gtk.Label()
                badge.set_markup("<span background='#89b4fa' foreground='#1e1e2e'> aktif </span>")
                badge.set_halign(Gtk.Align.END)
                badge.set_valign(Gtk.Align.START)
                overlay.add_overlay(badge)

            self.grid.add(overlay)
        self.grid.show_all()

    def on_wallpaper_click(self, widget, event, filepath):
        self.status_label.set_markup("<small>Ayarlaniyor...</small>")
        set_cosmic_wallpaper(filepath)
        self.load_current_preview()
        self.load_saved_wallpapers()
        self.status_label.set_markup("<small>Degistirildi!</small>")

    def on_category_clicked(self, btn, name):
        self.active_category = name
        save_state({"category": name})
        for bname, b in self.cat_buttons.items():
            ctx = b.get_style_context()
            ctx.remove_class("cat-btn")
            ctx.remove_class("cat-btn-active")
            ctx.add_class("cat-btn-active" if bname == name else "cat-btn")

    def on_refresh(self, widget):
        self.refresh_btn.set_sensitive(False)
        category = self.active_category
        self.status_label.set_markup("<small>Indiriliyor...</small>")

        def do_download():
            try:
                filepath, author = download_wallpaper(category)
                GLib.idle_add(self._on_done, filepath, author)
            except Exception as e:
                GLib.idle_add(self._on_error, str(e))

        threading.Thread(target=do_download, daemon=True).start()

    def _on_done(self, filepath, author):
        self.refresh_btn.set_sensitive(True)
        set_cosmic_wallpaper(filepath)
        self.load_current_preview()
        self.load_saved_wallpapers()
        self.status_label.set_markup(f"<small>{author}</small>")

    def _on_error(self, msg):
        self.refresh_btn.set_sensitive(True)
        self.status_label.set_markup(f"<small>Hata: {msg[:40]}</small>")


SNI_XML = """
<node>
  <interface name="org.kde.StatusNotifierItem">
    <method name="Activate">
      <arg direction="in" name="x" type="i"/>
      <arg direction="in" name="y" type="i"/>
    </method>
    <method name="ContextMenu">
      <arg direction="in" name="x" type="i"/>
      <arg direction="in" name="y" type="i"/>
    </method>
    <method name="SecondaryActivate">
      <arg direction="in" name="x" type="i"/>
      <arg direction="in" name="y" type="i"/>
    </method>
    <method name="Scroll">
      <arg direction="in" name="delta" type="i"/>
      <arg direction="in" name="orientation" type="s"/>
    </method>
    <property name="Category" type="s" access="read"/>
    <property name="Id" type="s" access="read"/>
    <property name="Title" type="s" access="read"/>
    <property name="Status" type="s" access="read"/>
    <property name="IconName" type="s" access="read"/>
    <property name="IconThemePath" type="s" access="read"/>
    <property name="Menu" type="o" access="read"/>
    <property name="ItemIsMenu" type="b" access="read"/>
  </interface>
</node>
"""


class WallpaperTray:
    BUS_NAME = "org.kde.StatusNotifierItem-{}-1"
    OBJ_PATH = "/StatusNotifierItem"

    def __init__(self):
        self.panel = None
        self.bus_name = self.BUS_NAME.format(os.getpid())
        self.node_info = Gio.DBusNodeInfo.new_for_xml(SNI_XML)

        self.conn = Gio.bus_get_sync(Gio.BusType.SESSION)
        Gio.bus_own_name(
            Gio.BusType.SESSION,
            self.bus_name,
            Gio.BusNameOwnerFlags.NONE,
            self._on_bus_acquired,
            None, None
        )

    def _on_bus_acquired(self, conn, name):
        conn.register_object(
            self.OBJ_PATH,
            self.node_info.interfaces[0],
            self._on_method_call,
            self._on_get_property,
            None
        )
        # Register with the StatusNotifierWatcher
        try:
            conn.call_sync(
                "org.kde.StatusNotifierWatcher",
                "/StatusNotifierWatcher",
                "org.kde.StatusNotifierWatcher",
                "RegisterStatusNotifierItem",
                GLib.Variant("(s)", (self.bus_name,)),
                None,
                Gio.DBusCallFlags.NONE,
                -1, None
            )
        except Exception as e:
            print(f"Warning: Could not register with StatusNotifierWatcher: {e}")

    def _on_method_call(self, conn, sender, path, iface, method, params, invocation):
        if method == "Activate":
            x, y = params.unpack()
            GLib.idle_add(self.toggle_panel)
        invocation.return_value(None)

    def _on_get_property(self, conn, sender, path, iface, prop_name):
        props = {
            "Category": GLib.Variant("s", "ApplicationStatus"),
            "Id": GLib.Variant("s", "wallpaper-manager"),
            "Title": GLib.Variant("s", "Wallpaper"),
            "Status": GLib.Variant("s", "Active"),
            "IconName": GLib.Variant("s", ICON_PATH),
            "IconThemePath": GLib.Variant("s", ""),
            "Menu": GLib.Variant("o", "/NO_MENU"),
            "ItemIsMenu": GLib.Variant("b", False),
        }
        return props.get(prop_name)

    def toggle_panel(self, _icon_x=0):
        if self.panel:
            self.panel.dismiss()
            self.panel = None
            return

        self.panel = PopupPanel()
        self.panel.connect("destroy", lambda w: setattr(self, 'panel', None))
        self.panel.show_all()


if __name__ == "__main__":
    app = WallpaperTray()
    Gtk.main()
