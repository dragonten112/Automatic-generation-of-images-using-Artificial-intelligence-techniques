import customtkinter
from PIL import Image, ImageTk
import tkinter
import torch
import os
import threading

from diffusers import DiffusionPipeline
from googletrans import Translator
import subprocess
import re
import random


curiozitati=["""
                Inteligența artificială care creează fețe de oameni care nu există : 
                Există un program de inteligență artificială, proiectat de inginerii de la Nvidia,
                care poate crea fotografii realiste ale unor oameni care nu există în realitate. 
                De la fețele încețoșate, vagi, în alb și negru, create în 2014, programul de inteligență artificială cunoscut ca 
                „rețea generativă adversarială” (RGA) a străbătut o cale lungă în numai în cinci ani.
                rogramul folosește o metodă numită „transfer de stil”, care ia caracteristicile unei imagini și
                le amestecă cu alte caracteristici pentru a obține imagini noi.
                Această metodă este folosită pentru multe aplicații, cum ar fi Prisma și Facebook, pentru a converti o
                fotografie într-un tablou impresionist sau cubist.
             """,
             """
                 În 2017, Facebook a creat doi „chatboți” (programe de mesagerie text automată) care funcționau pe bază de
                inteligență artificială și vorbeau unul cu celălalt. A fost nevoie să fie opriți, fiindcă începuseră să
                dezvolte propria lor limbă pentru a comunica, după ce au calculat că limba engleză este ineficientă.
                Inteligența artificială operează cu un sistem de bonusuri, programul fiind răsplătit pentru o acțiune
                corespunzătoare și pedepsit pentru o acțiune eronată, reușind astfel să învețe.
                Cei doi roboți care funcționau pe bază de inteligență artificială, Bob și Alice, erau capabili să negocieze
                pentru a trage concluzii. Se pare că și-au dat seama că engleza nu era chiar ușor de folosit, așa că au început
                să folosească fraze care păreau fără sens, însă care, pentru ei, erau mai eficiente.
                În conversație, Bob spunea „Eu pot eu eu eu totul”, iar Alice răspundea
                „Bilele au zero pentru mine pentru mine pentru mine.” Potrivit cercetătorilor, repetiția cuvintelor „eu” și
                „pentru mine” indică felul în care operează inteligența artificială.
             """,
             """
                Uneori, NASA folosește algoritmi evoluționari care imită evoluția, așa cum a fost explicată de Charles Darwin,
                pentru a proiecta antene pentru comunicații radio, mai ales când acestea trebuie să aibă un design neobișnuit.
                Rezultatul constă în niște antene foarte eficiente, cu forme ciudate. 
                Detectarea tiparelor de radiație neobișnuită necesită antene cu design neobișnuit, care sunt fabricate cu ajutorul
                unui algoritm care imită evoluția.
                Programul pornește de la niște antene cu forme simple și adaugă sau modifică elemente într-un mod semi-aleatoriu
                pentru a proiecta noi forme de antene. După ce noile antene sunt evaluate, cele cu scoruri bune sunt alese, iar
                cele cu scoruri rele sunt lăsate deoparte, la fel ca în cazul selecției naturale.
             """
             
             ]









customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')

principal = customtkinter.CTk()
principal.geometry('1280x720')
principal.grid_columnconfigure(0, weight=1)
principal.grid_rowconfigure(0, weight=1)

grup1 = customtkinter.CTkFrame(master=principal, height=640, width=350)
grup1.grid(row=0, column=0, pady=20, padx=20, sticky="nsew")
grup1.grid_columnconfigure(0, weight=1)

grup2 = customtkinter.CTkFrame(master=principal, height=640, width=350)
grup2.grid(row=0, column=1, pady=20, padx=10, sticky="nsew")

imagineGrup = customtkinter.CTkFrame(master=grup2, height=512, width=512)
imagineGrup.grid(row=2, column=0, pady=20, padx=20)

grupSlidere = customtkinter.CTkFrame(master=grup1)
grupSlidere.grid(row=2, column=0, pady=10, padx=10)

lblSlider=customtkinter.CTkLabel(master=grup1,text="Selectează numărul de imagini:")
lblSlider.grid(row=1,column=0)

baradeprogres = customtkinter.CTkProgressBar(master=imagineGrup, mode="indeterminate",border_width=200)
baradeprogres.grid(row=1, column=1, pady=10, padx=10)
baradeprogres.set(0)





def galerie():
    CALE_SALVARE_IMG2 = 'D:/Licenta Aplicatie/ImaginiRezultate'
    cmdSalvare_IMG=os.startfile(CALE_SALVARE_IMG2)
    
buton_folder=customtkinter.CTkButton(master=imagineGrup, text="Galerie",command=galerie)
buton_folder.grid(row=2,column=1,pady=10,padx=10)





spatiu_canvas=tkinter.Canvas(grup2,width=512,height=512)
spatiu_canvas.grid(row=0,column=0)


def slider_evenimentPoze(nrPoze):
    nrPoze = int(slider1.get())
    lblnrPoze = customtkinter.CTkLabel(master=grupSlidere, text=nrPoze)
    lblnrPoze.grid(row=0, column=1)

slider1 = customtkinter.CTkSlider(master=grupSlidere, from_=1, to=4, number_of_steps=3, command=slider_evenimentPoze)
slider1.grid(row=0, column=0)
setarei = slider1.set(1)

lblAfisareNrPoze = customtkinter.CTkLabel(master=grupSlidere, text='1')
lblAfisareNrPoze.grid(row=0, column=1, pady=5, padx=5)







caseta = customtkinter.CTkEntry(master=grup1, placeholder_text="La ce te gandesti acum?")
caseta.grid(row=0, column=0, pady=40, padx=20, sticky='ew')




def switch_event():
    print("switch toggled, current value:", switch_var.get())
    
switch_var = customtkinter.StringVar(value="on")
switch = customtkinter.CTkSwitch(master=grup1, text="CPU  (Atentie! bifeaza cu riscul tau! Bifeaza numai daca ai racire si un procesor foarte bun!)", command=switch_event,
                                     variable=switch_var, onvalue="on", offvalue="off")
    
switch.grid(row=5,column=0,pady=10,padx=10)
switch.toggle()

translator=Translator()

def neacceptat_text(text):
    
    text = re.sub(r'[^\w\s]', '', text)
    
    text = text.replace('ă', 'a').replace('î', 'i').replace('â', 'a').replace('ș', 's').replace('ț', 't')
    return text


def traducere(text):
    text = neacceptat_text(text)
    deTradus=translator.translate(text,src="ro",dest="en")
    return deTradus.text
    

def generare():
    
    prompt = caseta.get()
    prompt_trad=prompt
    detectare=translator.detect(prompt)
    if detectare.lang == 'ro' :
        prompt_trad=traducere(prompt)
    
    t = threading.Thread(target=proces, args=(prompt_trad,))
    t.start()
    
    

    
def proces(prompt):
    SD_MV_CALE = os.getenv('SD_MV_CALE')
    CALE_SALVARE_IMG = 'D:/Licenta Aplicatie/ImaginiRezultate'
    

    def numeImagini(path):
        filename, extension = os.path.splitext(path)
        counter = 1
        while os.path.exists(path):
            path = filename + ' (' + str(counter) + ' )' + extension
            counter += 1
        return path

    def numeScurt():
        limita_nume = (prompt[:25] + '...') if len(prompt) > 25 else prompt
        limita_nume = limita_nume.replace(' ', '_')
        rez_nume = os.path.join(CALE_SALVARE_IMG, limita_nume.removesuffix('...'))
        if not os.path.exists(rez_nume):
            os.makedirs(rez_nume)
        if not os.path.exists(CALE_SALVARE_IMG):
            os.makedirs(CALE_SALVARE_IMG)
        

    #device_type='cuda'
    if switch_var.get()=='on':
        device_type='cpu'
        pipe=DiffusionPipeline.from_pretrained(SD_MV_CALE,torch_dtype=torch.float32)
        pipe=pipe.to(device_type)
    else:
        device_type='cuda'
        pipe=DiffusionPipeline.from_pretrained(SD_MV_CALE,revision='fp16',torch_dtype=torch.float16)
        pipe=pipe.to(device_type)
        
    

    print(f"Characters in prompt : {len(prompt)} , limit : 200")
    #pipe = DiffusionPipeline.from_pretrained(SD_MV_CALE, revision="fp16", torch_dtype=torch.float16)
    #pipe = pipe.to(device_type)
    
    
    
    
        
       

    
    low_vram = True
    
    
    nr_imagini=int(slider1.get())
    
    lblAsteptare=customtkinter.CTkLabel(master=grup1, text="Poate dura un moment , pană atunci știai că : ")
    lblAsteptare.grid(row=6,column=0)
    
    curiozitate_random=random.choice(curiozitati)
    lblcuriozitate=customtkinter.CTkLabel(master=grup1,text=curiozitate_random,justify='left')
    lblcuriozitate.grid(row=7,column=0,pady=10,padx=10)    
    
    
    baradeprogres.start()
    
    for i in range(nr_imagini):
        pipe.enable_attention_slicing()
        image = pipe(prompt,height=512,width=512,guidance_scale=7.5,num_inference_steps=50).images[0]
        image_path = numeImagini(os.path.join(CALE_SALVARE_IMG, (prompt[:25] + '...') if len(prompt) > 25 else prompt) + '.png')
        print(image_path)
        image.save(image_path)
        display_imagine(image_path)
            

    baradeprogres.stop()    

    


def display_imagine(image_path):

    
    imagine_rez = Image.open(image_path)
    imagine_tk = ImageTk.PhotoImage(imagine_rez)
    #lblrandom = customtkinter.CTkLabel(master=imagineGrup, text="", image=imagine_tk)
    #lblrandom.image = imagine_tk  # Keep a reference to avoid garbage collection
    #lblrandom.grid(row=0, column=0)
    
    
    spatiu_canvas.image=imagine_tk
    spatiu_canvas.create_image(0,0 ,anchor='nw',image=imagine_tk)
    
    
buton = customtkinter.CTkButton(master=grup1, text="Genereaza", command=generare)
buton.grid(row=4, column=0, pady=10, padx=55, sticky='ew')









    



principal.mainloop()