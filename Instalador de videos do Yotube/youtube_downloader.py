import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pytube import YouTube
import os
import threading

class VideoDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Baixador de Videos - Youtube")
        self.root.geometry("500x300")

        #variaveis
        self.url_var = tk.StringVar()
        self.save_path = os.path.expanduser("~/Downloads") #pasta padrao para salvar os videos

        #widgets
        self.create_widgets()

    def create_widgets(self):
        #janela principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(main_frame, text="URL do video").pack(anchor="w")
        url_entry = ttk.Entry(main_frame, textvariable=self.url_var, width=50)
        url_entry.pack(pady=5)
        url_entry.focus()

        #botão pra selecionar pasta
        ttk.Button(
            main_frame,
            text="Selecionar pasta",
            command=self.choose_directory
        ).pack(pady=5)

        #label para mostrar a pasta selecionada
        self.path_label = ttk.Label(main_frame, text=f"Salvar em:{self.save_path}")
        self.path_label.pack(anchor="w")

        #botão de download

        ttk.Button(
            main_frame,
            text="baixar video",
            style="Accent.TButton",
            command=self.start_download_thread
        ).pack(pady=20)

        #barra de progresso
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')

        #estilo do botão destacado
        style = ttk.Style()
        style.configure("Accent.TButton", foreground="white", background="#0078d4")
    
    def choose_directory(self):
        '''abre dialogo para escolher pasta de destino'''
        folder = filedialog.askdirectory(initialdir=self.save_path)
        if folder:
            self.save_path = folder
            self.path_label.config(text=f"Salvar em: {self.save_path}")

    def start_download_thread(self):
        '''inicia o dpwnload em uma thread separada para não travar a GUI'''
        threading.Thread(target=self.download_video, daemon=True).start()

    def download_video(self):
        '''faz o download do video'''
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("erro", "por favor insira uma URL valida")
            return
        try:
            #mostra barra de progresso
            self.progress.pack(fill=tk.X)
            self.progress.start()

            #baixa o video
            yt = YouTube(url, on_progress_callback=self.progress_function)

            video = yt.streams.get_highest_resolution()

            #atualiza a interface
            self.root.title(f"baixando: {yt.title}")

            #faz o download
            video.download(output_path=self.save_path)

            #concluido
            messagebox.showinfo("Sucesso em baixar o video, divirta-se!\n Salvo em: {self.save.path}")


        except Exception as e:
            messagebox.showerror("erro", f"falha no download:\n{str(e)}")

        finally:
            self.progress.stop()
            self.progress.pack_forget()
            self.root.title("Baixador de Videos do YouTube")


    def progress_function(self, stream, chunk, bytes_remaining):
                '''atualiza a barra de progresso'''
                total_size = stream.filesize
                bytes_downloaded = total_size - bytes_remaining
                percentage = (bytes_downloaded / total_size) * 100
                self.progress['value'] = percentage
                self.root.update_idletasks()
    
    
if __name__ == "__main__":
    root = tk.Tk()
    app = VideoDownloaderApp(root)
    root.mainloop()
                
#programa finalizado