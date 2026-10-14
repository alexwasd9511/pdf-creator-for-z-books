import time
import os
import tkinter as tk
from tkinter import messagebox
import pyautogui
from PIL import ImageTk
from PIL import Image
def Do_Pdf():
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

def Select_Cut_Area():
    app.iconify()
    app.after(500)#bu olmadan çalışmıyor buna dön!
    screenshot =  pyautogui.screenshot()
    screen_weight, screen_height = screenshot.size
    select_win = tk.Toplevel(app)
    select_win.attribtes("-fullscreen", True)
    select_win.attribtes("-topmost", True)
    select_win.config(cursor = "cross") #imleç

    background_image = ImageTk.PhotoImage(screenshot)

    canvas = tk.Canvas(select_win,width = screen_weight,height= screen_height,highlightthickness=0)
    canvas.pack(fill = "both" , expand=True)
    canvas.create_image(0,0, image=background_image, anchor="nw")
    start_x = 0
    start_y = 0
    rect_id = None
    def first_press(event):
        nonlocal start_x, start_y, rect_id
        start_x = event.x
        start_y = event.y
        rect_id = canvas.create_rectangle(start_x,start_y,start_x,start_y, outline="red", width=2)
    def press_and_move(event):
        nonlocal rect_id
        currently_x, currently_y = event.x,event.y
        canvas.coords(rect_id,start_x,start_y,currently_x, currently_y)
    def release(event):
        end_x, end_y = event.x,event.y

        x1, x2 = min(start_x,end_x), max(start_x,end_x)
        y1, y2 = min(start_y,end_y), max(start_y,end_y)
        calc_left = x1
        calc_top = y1
        calc_right = screen_weight - x2
        calc_bottom = screen_height - y2
        crop_l.delete(0, tk.END)#önceki değerleri çıkarıp yenisini koyuyorum
        crop_l.insert(0, str(calc_left))
        crop_t.delete(0, tk.END)
        crop_t.insert(0, str(calc_top))
        crop_r.delete(0, tk.END)
        crop_r.insert(0, str(calc_right))
        crop_b.delete(0, tk.END)
        crop_b.insert(0, str(calc_bottom))
        select_win.destroy()
        app.deiconify()
    canvas.bind("<ButtonPress-1>", first_press)
    canvas.bind("<B1-Motion>", press_and_move)
    canvas.bind("<ButtonRelease-1>", release)
    canvas.image = background_image
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
btn_select = tk.Button(app,text= "kesilcek yeri seçin", command=Select_Cut_Area, bg="#d9edf7",fg="#31708f",)
btn_select.pack(fill="x",padx=15, pady=(5, 10))
btn = tk.Button(app, text="START", command=Do_Pdf, bg="#e1e1e1", height=2)
btn.pack(fill="x", padx=15, pady=20)
app.mainloop()
