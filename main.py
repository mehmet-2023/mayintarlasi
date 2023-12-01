import tkinter as tk
from random import randint

def mayinlari_yerlestir(satir, sutun, mayin_sayisi):
    mayinlar = set()

    while len(mayinlar) < mayin_sayisi:
        mayinlar.add((randint(0, satir - 1), randint(0, sutun - 1)))

    return mayinlar

def mayinlari_cevir(mayinlar, i, j, satir, sutun):
    sayac = 0
    for x in range(max(0, i - 1), min(satir - 1, i + 1) + 1):
        for y in range(max(0, j - 1), min(sutun - 1, j + 1) + 1):
            if (x, y) in mayinlar:
                sayac += 1
    return sayac

def boslari_ac(mayinlar, buttons, i, j, satir, sutun):
    for x in range(max(0, i - 1), min(satir - 1, i + 1) + 1):
        for y in range(max(0, j - 1), min(sutun - 1, j + 1) + 1):
            if buttons[x][y]["state"] == tk.NORMAL:
                mayin_sayisi = mayinlari_cevir(mayinlar, x, y, satir, sutun)
                buttons[x][y].config(text=str(mayin_sayisi), state=tk.DISABLED, disabledforeground=uzaklik_rengi(mayin_sayisi))

                if mayin_sayisi == 0:
                    boslari_ac(mayinlar, buttons, x, y, satir, sutun)

def tikla(mayinlar, buttons, i, j, satir, sutun, sayac_label, oyunu_yeniden_baslat):
    if (i, j) in mayinlar:
        buttons[i][j].config(text="*", state=tk.DISABLED, disabledforeground="red")
        oyunu_bitir(buttons, mayinlar, False, oyunu_yeniden_baslat)
    else:
        mayin_sayisi = mayinlari_cevir(mayinlar, i, j, satir, sutun)
        buttons[i][j].config(text=str(mayin_sayisi), state=tk.DISABLED, disabledforeground=uzaklik_rengi(mayin_sayisi))
        if mayin_sayisi == 0:
            boslari_ac(mayinlar, buttons, i, j, satir, sutun)
        kazandigini_kontrol_et(buttons, mayinlar, satir, sutun, sayac_label, oyunu_yeniden_baslat)


def bayrak_koy(mayinlar, buttons, i, j):
    if buttons[i][j]["state"] == tk.NORMAL:
        buttons[i][j].config(text="🚩",fg="gray", state=tk.DISABLED)
    elif buttons[i][j]["text"] == "🚩":
        buttons[i][j].config(text="", state=tk.NORMAL,
        fg="grey")


def uzaklik_rengi(uzaklik):
    renkler = ["black", "blue", "green", "purple", "red", "brown", "cyan", "orange"]
    return renkler[uzaklik]

def oyunu_bitir(buttons, mayinlar, kazandi_mi, oyunu_yeniden_baslat):
    for i in range(len(buttons)):
        for j in range(len(buttons[0])):
            if (i, j) in mayinlar:
                buttons[i][j].config(text="*", state=tk.DISABLED, disabledforeground="red")
            else:
                buttons[i][j].config(state=tk.DISABLED)

    if kazandi_mi:
        sayac_label.config(text="Oyunu Kazandınız!")
    else:
        sayac_label.config(text="Oyunu Kaybettiniz!")

    oyunu_yeniden_baslat.config(state=tk.NORMAL)

def kazandigini_kontrol_et(buttons, mayinlar, satir, sutun, sayac_label, oyunu_yeniden_baslat):
    acilan_kutucuk_sayisi = sum(row.count(tk.DISABLED) for row in buttons)
    toplam_kutucuk_sayisi = satir * sutun
    mayin_sayisi = len(mayinlar)

    if acilan_kutucuk_sayisi == toplam_kutucuk_sayisi - mayin_sayisi:
        oyunu_bitir(buttons, mayinlar, True, oyunu_yeniden_baslat)

def oyunu_yeniden_baslat():
    for i in range(len(buttons)):
        for j in range(len(buttons[0])):
            buttons[i][j].config(text=" ", state=tk.NORMAL, bg="SystemButtonFace")

    global sayac_label
    sayac_label.config(text="Mayın Sayısı: {}".format(mayin_sayisi))
    oyunu_yeniden_baslat.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Mayın Tarlası")

    satir, sutun, mayin_sayisi = 8, 8, 10
    mayinlar = mayinlari_yerlestir(satir, sutun, mayin_sayisi)

    global sayac_label
    sayac_label = tk.Label(root, text="Mayın Sayısı: {}".format(mayin_sayisi))
    sayac_label.grid(row=0, column=0, columnspan=sutun)

    global buttons
    buttons = [[None for _ in range(sutun)] for _ in range(satir)]
    for i in range(satir):
        for j in range(sutun):
            buttons[i][j] = tk.Button(root, text=" ", width=3, height=1,
                                      command=lambda i=i, j=j: tikla(mayinlar, buttons, i, j, satir, sutun, sayac_label, oyunu_yeniden_baslat),
                                      bd=1)
            buttons[i][j].bind("<Button-3>", lambda event, i=i, j=j: bayrak_koy(mayinlar, buttons, i, j))
            buttons[i][j].grid(row=i + 1, column=j)


    oyunu_yeniden_baslat = tk.Button(root, text="Yeniden Oyna", command=oyunu_yeniden_baslat, state=tk.DISABLED)
    oyunu_yeniden_baslat.grid(row=satir + 1, column=0, columnspan=sutun)

    root.mainloop()
