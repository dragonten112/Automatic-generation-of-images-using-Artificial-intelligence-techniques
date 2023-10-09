import os
import random
import re
import subprocess
import threading
import tkinter
from PIL import Image, ImageTk
from diffusers import DiffusionPipeline
from googletrans import Translator
import customtkinter
import torch

class Generare:
    def __init__(self, principal, caseta, switch_var, slider1, baradeprogres, grup1, grup2, imagineGrup, spatiu_canvas):
        
        self.principal = principal
        self.caseta = caseta
        self.switch_var = switch_var
        self.slider1 = slider1
        self.baradeprogres = baradeprogres
        self.grup1 = grup1
        self.grup2 = grup2
        self.imagineGrup = imagineGrup
        self.spatiu_canvas = spatiu_canvas

        self.translator = Translator()
        self.curiozitati = ["...", "...", "..."]  # Adăugați curiozitățile dorite în listă

    def generare(self):
        prompt = self.caseta.get()
        prompt_trad = prompt
        detectare = self.translator.detect(prompt)
        if detectare.lang == 'ro':
            prompt_trad = self.traducere(prompt)
            
        t = threading.Thread(target=self.generate_image, args=(prompt_trad,))
        t.start()

    def generate_image(self, prompt):
        
        SD_MV_CALE = os.getenv('SD_MV_CALE')
        CALE_SALVARE_IMG = 'D:/Licenta Aplicatie/ImaginiRezultate'
        # Restul codului pentru generarea imaginilor
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
        if  self.switch_var.get()=='on':
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
        
        
        nr_imagini=int(self.slider1.get())
        
        lblAsteptare=customtkinter.CTkLabel(master=self.grup1, text="Poate dura un moment , pană atunci știai că : ")
        lblAsteptare.grid(row=6,column=0)
        
        curiozitate_random=random.choice(self.curiozitati)
        lblcuriozitate=customtkinter.CTkLabel(master=self.grup1,text=curiozitate_random,justify='left')
        lblcuriozitate.grid(row=7,column=0,pady=10,padx=10)    
        
        
        self.baradeprogres.start()
        
        for i in range(nr_imagini):
            pipe.enable_attention_slicing()
            image = pipe(prompt,height=512,width=512,guidance_scale=7.5,num_inference_steps=50).images[0]
            image_path = numeImagini(os.path.join(CALE_SALVARE_IMG, (prompt[:25] + '...') if len(prompt) > 25 else prompt) + '.png')
            print(image_path)
            image.save(image_path)
            self.display_image(image_path)
                

        self.baradeprogres.stop()
    
class Traducere:
    def __init__(self):
        self.translator = Translator()

    def neacceptat_text(self, text):
        text = re.sub(r'[^\w\s]', '', text)
        text = text.replace('ă', 'a').replace('î', 'i').replace('â', 'a').replace('ș', 's').replace('ț', 't')
        return text

    def traducere(self, text):
        text = self.neacceptat_text(text)
        deTradus = self.translator.translate(text, src="ro", dest="en")
        return deTradus.text
    
class Interfata:
    def __init__(self):
        self.customtkinter = customtkinter
        self.principal = self.customtkinter.CTk()
        self.principal.geometry('1280x720')
        self.principal.grid_columnconfigure(0, weight=1)
        self.principal.grid_rowconfigure(0, weight=1)

        self.grup1 = self.customtkinter.CTkFrame(master=self.principal, height=640, width=350)
        self.grup1.grid(row=0, column=0, pady=20, padx=20, sticky="nsew")
        self.grup1.grid_columnconfigure(0, weight=1)

        self.grup2 = self.customtkinter.CTkFrame(master=self.principal, height=640, width=350)
        self.grup2.grid(row=0, column=1, pady=20, padx=10, sticky="nsew")

        self.imagineGrup = self.customtkinter.CTkFrame(master=self.grup2, height=512, width=512)
        self.imagineGrup.grid(row=2, column=0, pady=20, padx=20)

        self.grupSlidere = self.customtkinter.CTkFrame(master=self.grup1)
        self.grupSlidere.grid(row=2, column=0, pady=10, padx=10)

        self.lblSlider = self.customtkinter.CTkLabel(master=self.grup1, text="Selectează numărul de imagini:")
        self.lblSlider.grid(row=1, column=0)

        self.slider1 = self.customtkinter.CTkSlider(master=self.grupSlidere, from_=1, to=4, number_of_steps=3, command=self.slider_evenimentPoze)
        self.slider1.grid(row=0, column=0)
        self.setarei = self.slider1.set(1)

        self.lblAfisareNrPoze = self.customtkinter.CTkLabel(master=self.grupSlidere, text='1')
        self.lblAfisareNrPoze.grid(row=0, column=1, pady=5, padx=5)

        self.caseta = self.customtkinter.CTkEntry(master=self.grup1, placeholder_text="La ce te gandesti acum?")
        self.caseta.grid(row=0, column=0, pady=40, padx=20, sticky='ew')

        self.switch_var = self.customtkinter.StringVar(value="on")
        self.switch = self.customtkinter.CTkSwitch(master=self.grup1, text="CPU (Atentie! Bifeaza cu riscul tau! Bifeaza numai daca ai racire si un procesor foarte bun!)", command=self.switch_event, variable=self.switch_var, onvalue="on", offvalue="off")
        self.switch.grid(row=5, column=0, pady=10, padx=10)
        self.switch.toggle()
        
        self.baradeprogres = customtkinter.CTkProgressBar(master=self.imagineGrup, mode="indeterminate", border_width=200)
        self.baradeprogres.grid(row=1, column=1, pady=10, padx=10)
        self.baradeprogres.set(0)

        self.buton_folder = self.customtkinter.CTkButton(master=self.imagineGrup, text="Galerie", command=self.galerie)
        self.buton_folder.grid(row=2, column=1, pady=10, padx=10)
        
        
        
        self.spatiu_canvas = tkinter.Canvas(self.grup2, width=512, height=512)
        self.spatiu_canvas.grid(row=0, column=0)
        
        self.generare = Generare(self.principal, self.caseta, self.switch_var, self.slider1, self.baradeprogres, self.grup1, self.grup2, self.imagineGrup, self.spatiu_canvas)


        self.buton_generare = self.customtkinter.CTkButton(master=self.grup1, text="Generare", command=self.generare.generate_image)
        self.buton_generare.grid(row=4, column=0, pady=10, padx=55, sticky='ew')

        self.principal.mainloop()

    def galerie(self):
        CALE_SALVARE_IMG2 = 'D:/Licenta Aplicatie/ImaginiRezultate'
        cmdSalvare_IMG = os.startfile(CALE_SALVARE_IMG2)

    def slider_evenimentPoze(self, nrPoze):
        nrPoze = int(self.slider1.get())
        lblnrPoze = self.customtkinter.CTkLabel(master=self.grupSlidere, text=nrPoze)
        lblnrPoze.grid(row=0, column=1)

    def switch_event(self):
        print("switch toggled, current value:", self.switch_var.get())

    def display_image(self, image_path):
        imagine_rez = Image.open(image_path)
        imagine_tk = ImageTk.PhotoImage(imagine_rez)
        self.spatiu_canvas.image = imagine_tk
        self.spatiu_canvas.create_image(0, 0, anchor='nw', image=imagine_tk)


if __name__ == "__main__":
    interfata = Interfata()