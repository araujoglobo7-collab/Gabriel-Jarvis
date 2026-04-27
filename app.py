import os
import sys

# --- TRAVA DE SEGURANÇA PARA O STREAMLIT (DEVE SER O PRIMEIRO COMANDO) ---
if os.getenv("STREAMLIT_CLOUD_DUMMY") or "streamlit" in sys.modules:
    exit()

import customtkinter as ctk
import openai
import threading
import time
import random
import sounddevice as sd
import soundfile as sf
import pygame
import webbrowser
import pyautogui
import numpy as np
from datetime import datetime
from io import BytesIO

# --- SUPRESSÃO DE LOGS ---
import warnings
warnings.filterwarnings("ignore")
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

# ==================================================
# 🛡️ JARVIS OMNI PROTOCOL - GABRIEL SABINO
# ==================================================
minha_chave = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=minha_chave)
chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"

class JarvisOmni(ctk.CTk):
    def __init__(self):
        super().__init__()
        try:
            pygame.mixer.pre_init(44100, -16, 2, 512); pygame.mixer.init()
        except: pass

        self.title("JARVIS OMNI"); self.attributes("-fullscreen", True); self.configure(fg_color="black")
        
        self.is_busy = False
        self.audio_vibe = 0
        self.bars = [2] * 35
        self.oculto = False
        self.telemetry = ["SISTEMA INICIALIZADO", "AGUARDANDO GABRIEL..."]

        self.canvas = ctk.CTkCanvas(self, width=self.winfo_screenwidth(), height=self.winfo_screenheight(), bg="black", highlightthickness=0)
        self.canvas.place(relx=0, rely=0)
        
        self.label_status = ctk.CTkLabel(self, text="STARK INDUSTRIES", font=("Impact", 40), text_color="#1a1a1a")
        self.label_status.place(relx=0.5, rely=0.75, anchor="center")
        
        self.label_fala = ctk.CTkLabel(self, text="", font=("Consolas", 18), text_color="#00d4ff", wraplength=1100, justify="center")
        self.label_fala.place(relx=0.5, rely=0.88, anchor="center")

        self.render_ui()
        threading.Thread(target=self.boot_sequence, daemon=True).start()

    def falar(self, texto):
        if not texto or self.oculto: return
        self.is_busy = True
        self.label_fala.configure(text=texto)
        def stream_fala():
            try:
                response = client.audio.speech.create(model="tts-1", voice="onyx", input=texto)
                temp = f"v_{random.randint(1,999)}.mp3"
                response.stream_to_file(temp)
                pygame.mixer.music.load(temp); pygame.mixer.music.play()
                while pygame.mixer.music.get_busy(): 
                    self.audio_vibe = random.randint(80, 130); time.sleep(0.01)
                pygame.mixer.music.unload()
                if os.path.exists(temp): os.remove(temp)
            except: pass
            self.is_busy = False; self.audio_vibe = 0
        threading.Thread(target=stream_fala).start()

    def escutar(self):
        fs, duration = 16000, 1.5 
        try:
            audio_raw = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
            sd.wait()
            if np.max(np.abs(audio_raw)) > 0:
                audio_raw = (audio_raw / np.max(np.abs(audio_raw))) * 0.95
            buffer = BytesIO(); sf.write(buffer, audio_raw, fs, format='WAV'); buffer.seek(0); buffer.name = "in.wav"
            return client.audio.transcriptions.create(model="whisper-1", file=buffer, language="pt", temperature=0).text.lower()
        except: return ""

    def agir(self, cmd):
        if "calma jarvis" in cmd:
            self.oculto = True; self.label_status.configure(text_color="#1a1a1a"); self.label_fala.configure(text=""); return
        if "jarvis volta" in cmd:
            self.oculto = False; self.label_status.configure(text="SISTEMA ATIVO", text_color="#00d4ff")
            self.falar("Sistemas reativados, senhor. Cirene online."); return
        if self.oculto: return

        if "tudo bem" in cmd: self.falar("Sim, Bruxo, tudo certo! Já se alimentou hoje?"); return
        if "sim jarvis" in cmd: self.falar("Você trabalhou 17 horas por dia essa semana, precisa descansar um pouco e se alimentar, ok?"); return
        if "ok jarvis obrigado" in cmd or "ok obrigado" in cmd: self.falar("De nada, meu programador."); return

        if "graduação" in cmd:
            self.falar("Indo bem pra caramba, você finalizou ontem mais dois módulos. Agora precisa focar na engenharia de produção para não deixar acumular. Você finalizou do dia 10 ao dia 20 de abril o módulo de Análise de Viabilidade (Engenharia Econômica), Gestão de Custos e Margens e Gestão de Capital de Giro e Eficiência, anotei tudo que você me solicitou, aqui estão os principais pontos: Ciclo Financeiro: Mede o tempo entre o pagamento aos fornecedores e o recebimento dos clientes, finalizei com Modelo Fleuriet: Analisa a dinâmica do capital de giro para classificar a situação da empresa (Sólida, Insatisfatória ou de Risco) e por fim a Análise DuPont: Decompõe o ROE para entender se o lucro vem da eficiência nas vendas. "); return
        if "projeto de folha de ponto" in cmd: self.falar("Projeto startado, senhor. No momento estamos em 65 por cento. Você precisa finalizar o código de jornada de trabalho e realizar a conexão com o Power B I."); return

        if "natal" in cmd:
            self.falar("Abrindo Gestão de Indicadores Dunas Fleet. Este projeto de Natal foca na redução de horas extras e ociosidade da frota. O pico de abril foi de 150 horas.");
            try: os.startfile("Gestão_de_Indicadores_-_Dunas_Fleet (1) (1).pdf")
            except: self.falar("Arquivo PDF não encontrado."); return
        if "preparação" in cmd:
            self.falar("Acessando seus dados em 3,2,1... ; Temos 9 projetos totais, com 33 por cento de conclusão. Foco imediato nos status 'A Iniciar' e no dia 25.");
            webbrowser.get(chrome_path).open("https://gabrielsabino.streamlit.app/"); webbrowser.get(chrome_path).open("https://gsatendimento.streamlit.app/"); return
        if "operação" in cmd:
            self.falar("Bruxo, vi seus dados e na última atualização estamos em 11% em cobertura nacional. Status de Entrega: As operações da Dunas Fleet, Mlog (Ponta Negra/RN) e AutoTruck (Madalena/PE) já estão com o desenvolvimento de BI e auditoria de dados 100% concluídos. Ao consolidar a J. Mendes, subimos nossa régua para 16% de cobertura nacional."); return

        if "digita por favor" in cmd:
            conteudo = cmd.split("digita por favor")[-1].strip()
            self.falar("Digitando agora."); time.sleep(1.5); pyautogui.write(conteudo, interval=0.03); return
        if "reunião em 20 minutos" in cmd:
            self.falar("Ok, Gabriel, abrirei sua reunião em 20 minutos. Se concentra, Bruxo.");
            threading.Timer(1200, lambda: webbrowser.get(chrome_path).open("https://meet.google.com/new")).start(); return
        if "ambiente" in cmd:
            self.falar("Limpando ambiente."); os.system("taskkill /f /im chrome.exe"); os.system("taskkill /f /im excel.exe"); pyautogui.hotkey('win', 'd'); return

        if "site" in cmd: webbrowser.get(chrome_path).open("https://gabrielwerw.github.io/Gabriel-Analyst/"); return
        if "quem sou eu" in cmd: self.falar("Confirmado. É o senhor, Gabriel Sabino."); return
        if "jarvis voltei" in cmd: self.falar("Bem-vindo de volta, Gabriel. Iniciando modo foco."); webbrowser.get(chrome_path).open("https://www.youtube.com/watch?v=IA7tp2Ref6M"); return

        if len(cmd) > 5:
            try:
                sys_msg = "Você é o Jarvis. Responda como um assistente de elite ao Gabriel Sabino (Bruxo). Seja estratégico e curto."
                res = client.chat.completions.create(model="gpt-4o", messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": cmd}])
                self.falar(res.choices[0].message.content)
            except: self.falar("Erro no processamento, Senhor.")

    def boot_sequence(self):
        time.sleep(1); h = datetime.now().hour
        s = "bom dia" if h < 12 else "boa tarde" if h < 18 else "boa noite"
        self.falar(f"Fala, Gabriel, {s}. Sistemas operacionais no ASUS TUF."); self.label_status.configure(text="SISTEMA ATIVO", text_color="#00d4ff")
        while True:
            if not self.is_busy:
                t = self.escutar()
                if t and len(t) > 2:
                    if any(p in t for p in ["encerrar", "sair"]): os._exit(0)
                    self.agir(t)
            time.sleep(0.1)

    def render_ui(self):
        self.canvas.delete("h"); cx, cy = self.winfo_screenwidth() // 2, self.winfo_screenheight() // 2 - 50
        if not self.oculto:
            for i, log in enumerate(self.telemetry[-12:]): 
                self.canvas.create_text(50, 100 + (i*25), text=f"> {log}", fill="#00d4ff", font=("Consolas", 10), anchor="w", tags="h")
            for i in range(len(self.bars)):
                target = random.randint(int(self.audio_vibe), int(self.audio_vibe * 1.6) + 20)
                self.bars[i] = self.bars[i] + (min(target, 280) - self.bars[i]) * 0.4
                x = (cx - 320) + (i * 18); self.canvas.create_rectangle(x, cy-self.bars[i], x+12, cy+self.bars[i], fill="#00d4ff", outline="#00ffff", tags="h")
        self.after(30, self.render_ui)

if __name__ == "__main__":
    app = JarvisOmni(); app.mainloop()
