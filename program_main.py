import time
import os
import tkinter as tk
from tkinter import messagebox
import pyautogui
from PIL import Image
def pdf_yap():
    try:
        page_count = int(p_sayisi.get())
        delay = float(p_delay.get())
        out_name = p_name.get().strip() or "output"
        c_left = int(crop_l.get())
        c_top = int(crop_t.get())
        c_right = int(crop_r.get())
        c_bottom = int(crop_b.get())
    except ValueError:
        messagebox.showerror("hata", "sayıları doğru girin")
        return
    app.iconify()
    for i in range(5, 0, -1):
        print(f"kaldi {i} sn...")
        time.sleep(1)
    images = []
    for page in range(1, page_count + 1):
        time.sleep(delay)
        shot = pyautogui.screenshot()
        w, h = shot.size
        l = max(0, c_left)
        t = max(0, c_top)
        r = min(w, w - c_right)
        b = min(h, h - c_bottom)   
        if r > l and b > t:
            img = shot.crop((l, t, r, b))
        else:
            img = shot
        if img.mode != 'RGB':
            img = img.convert('RGB')
        images.append(img)
        print(f"Sayfa {page} oldu.")
        if page < page_count:
            pyautogui.press('right')
    out_dir = os.path.dirname(os.path.abspath(__file__))
    target_path = os.path.join(out_dir, f"{out_name}.pdf")
    if images:
        images[0].save(target_path, "PDF", save_all=True, append_images=images[1:])
        messagebox.showinfo("Bitti", f"PDF dosya ile ayni klasörde oluşmuştur:\n{target_path}")
    app.deiconify()
app = tk.Tk()
app.title("PDF creator")
app.geometry("380x420")
tk.Label(app, text="kitabın sayfa sayısını girin.:").pack(anchor="w", padx=15, pady=(10,0))
p_sayisi = tk.Entry(app)
p_sayisi.insert(0, "50")
p_sayisi.pack(fill="x", padx=15)
tk.Label(app, text="(sayfalar arası kaç saniye default = 1):").pack(anchor="w", padx=15, pady=(5,0))
p_delay = tk.Entry(app)
p_delay.insert(0, "1.0")
p_delay.pack(fill="x", padx=15)
tk.Label(app, text="kitabın pdf'innin Adi:").pack(anchor="w", padx=15, pady=(5,0))
p_name = tk.Entry(app)
p_name.insert(0, "kitap")
p_name.pack(fill="x", padx=15)
tk.Label(app, text="Kirpma (sol yukari sağ aşaği):").pack(anchor="w", padx=15, pady=(15,0))
f_crop = tk.Frame(app)
f_crop.pack(padx=15, pady=5)
crop_l = tk.Entry(f_crop, width=5); crop_l.insert(0, "0"); crop_l.pack(side="left", padx=2)
crop_t = tk.Entry(f_crop, width=5); crop_t.insert(0, "0"); crop_t.pack(side="left", padx=2)
crop_r = tk.Entry(f_crop, width=5); crop_r.insert(0, "0"); crop_r.pack(side="left", padx=2)
crop_b = tk.Entry(f_crop, width=5); crop_b.insert(0, "0"); crop_b.pack(side="left", padx=2)
btn = tk.Button(app, text="START", command=pdf_yap, bg="#e1e1e1", height=2)
btn.pack(fill="x", padx=15, pady=20)
app.mainloop()
