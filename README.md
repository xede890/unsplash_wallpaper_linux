# Unsplash Wallpaper for Linux (COSMIC Desktop)

A system tray wallpaper manager for the COSMIC desktop environment. Downloads random wallpapers from [Lorem Picsum](https://picsum.photos/) and sets them as your desktop background with a single click.

## Features

- System tray icon using the StatusNotifierItem (SNI) D-Bus protocol
- GTK3 popup panel with live wallpaper preview
- Category-based wallpaper selection: Rastgele (Random), Doga (Nature), Sehir (City), Deniz (Sea), Dag (Mountain), Minimal, Renkli (Colorful)
- Thumbnail grid of previously downloaded wallpapers for quick switching
- Directly configures COSMIC desktop background (`cosmic-bg`)
- Dark themed UI with rounded corners (Catppuccin Mocha style)

## Dependencies

- Python 3
- GTK 3 (`gi` - PyGObject)
- GtkLayerShell (`gi` - `GtkLayerShell`)
- COSMIC desktop environment (`cosmic-bg`)

### Install on Pop!_OS / Ubuntu

```bash
sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-gtklayershell-0.1
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/xede890/unsplash_wallpaper_linux.git
```

2. Copy files to the local data directory:

```bash
mkdir -p ~/.local/share/unsplash-wallpaper
cp unsplash-wallpaper.py icon.svg ~/.local/share/unsplash-wallpaper/
chmod +x ~/.local/share/unsplash-wallpaper/unsplash-wallpaper.py
```

3. Run:

```bash
python3 ~/.local/share/unsplash-wallpaper/unsplash-wallpaper.py
```

## Autostart

To start automatically on login, create a desktop entry:

```bash
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/unsplash-wallpaper.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=Unsplash Wallpaper
Exec=python3 /home/$USER/.local/share/unsplash-wallpaper/unsplash-wallpaper.py
Icon=/home/$USER/.local/share/unsplash-wallpaper/icon.svg
X-GNOME-Autostart-enabled=true
EOF
```

## Usage

1. Click the tray icon to open the wallpaper panel
2. Select a category (Rastgele, Doga, Sehir, Deniz, Dag, Minimal, Renkli)
3. Click **Rastgele Wallpaper** to download and apply a new wallpaper
4. Click any thumbnail in the grid to switch to a previously downloaded wallpaper

Wallpapers are saved to `~/Pictures/Wallpapers/`.

## File Structure

```
~/.local/share/unsplash-wallpaper/
  unsplash-wallpaper.py   # Main application
  icon.svg                # Tray icon
  state.json              # Persisted category selection (auto-generated)
```

---

# Unsplash Wallpaper - Linux (COSMIC Masaüstü)

COSMIC masaüstü ortamı için sistem tepsisi duvar kağıdı yöneticisi. [Lorem Picsum](https://picsum.photos/) adresinden rastgele duvar kağıtları indirir ve tek tıkla masaüstü arka planı olarak ayarlar.

## Özellikler

- StatusNotifierItem (SNI) D-Bus protokolü ile sistem tepsisi ikonu
- GTK3 açılır panel ile canlı duvar kağıdı önizlemesi
- Kategori bazlı duvar kağıdı seçimi: Rastgele, Doğa, Şehir, Deniz, Dağ, Minimal, Renkli
- Daha önce indirilen duvar kağıtlarının küçük resim ızgarası ile hızlı geçiş
- COSMIC masaüstü arka planını (`cosmic-bg`) doğrudan yapılandırır
- Karanlık temalı, yuvarlak köşeli arayüz (Catppuccin Mocha tarzı)

## Bağımlılıklar

- Python 3
- GTK 3 (`gi` - PyGObject)
- GtkLayerShell (`gi` - `GtkLayerShell`)
- COSMIC masaüstü ortamı (`cosmic-bg`)

### Pop!_OS / Ubuntu Üzerinde Kurulum

```bash
sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-gtklayershell-0.1
```

## Kurulum

1. Depoyu klonlayın:

```bash
git clone https://github.com/xede890/unsplash_wallpaper_linux.git
```

2. Dosyaları yerel veri dizinine kopyalayın:

```bash
mkdir -p ~/.local/share/unsplash-wallpaper
cp unsplash-wallpaper.py icon.svg ~/.local/share/unsplash-wallpaper/
chmod +x ~/.local/share/unsplash-wallpaper/unsplash-wallpaper.py
```

3. Çalıştırın:

```bash
python3 ~/.local/share/unsplash-wallpaper/unsplash-wallpaper.py
```

## Otomatik Başlatma

Giriş yapıldığında otomatik başlatmak için bir masaüstü girişi oluşturun:

```bash
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/unsplash-wallpaper.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=Unsplash Wallpaper
Exec=python3 /home/$USER/.local/share/unsplash-wallpaper/unsplash-wallpaper.py
Icon=/home/$USER/.local/share/unsplash-wallpaper/icon.svg
X-GNOME-Autostart-enabled=true
EOF
```

## Kullanım

1. Duvar kağıdı panelini açmak için tepsi ikonuna tıklayın
2. Bir kategori seçin (Rastgele, Doğa, Şehir, Deniz, Dağ, Minimal, Renkli)
3. Yeni bir duvar kağıdı indirip uygulamak için **Rastgele Wallpaper** butonuna tıklayın
4. Daha önce indirilen bir duvar kağıdına geçmek için ızgaradaki küçük resimlerden birine tıklayın

Duvar kağıtları `~/Pictures/Wallpapers/` dizinine kaydedilir.

## Dosya Yapısı

```
~/.local/share/unsplash-wallpaper/
  unsplash-wallpaper.py   # Ana uygulama
  icon.svg                # Tepsi ikonu
  state.json              # Kaydedilen kategori seçimi (otomatik oluşturulur)
```