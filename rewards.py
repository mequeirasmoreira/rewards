import pyautogui
import webbrowser
import time
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading

def perform_searches(search_list_file, delay_between_searches, root, progress_var, total_searches_label, completed_searches_label, progress_bar, start_button):
    try:
        start_button.config(state=tk.DISABLED) # Desabilita o botão para evitar cliques múltiplos

        with open(search_list_file, 'r', encoding='utf-8') as f:
            search_terms = [line.strip() for line in f if line.strip()]

        total_searches = len(search_terms)
        total_searches_label.config(text=f"Total de pesquisas: {total_searches}")
        progress_bar['maximum'] = total_searches

        for i, term in enumerate(search_terms):
            completed_searches_label.config(text=f"Pesquisas realizadas: {i}")
            progress_var.set(i)
            root.update_idletasks() # Atualiza a interface gráfica

            # Abre o Bing
            webbrowser.open("https://www.bing.com/")
            time.sleep(delay_between_searches + 2) # Dá mais tempo para o Bing carregar e focar

            # Digita o termo de pesquisa (a barra de pesquisa do Bing geralmente tem foco automático)
            pyautogui.write(term)
            pyautogui.press('enter')

            # Dá tempo para a pesquisa ser realizada e a página carregar
            time.sleep(delay_between_searches)

            # Fecha a aba atual (depende do navegador e OS)
            pyautogui.hotkey('ctrl', 'w') # Para Windows/Linux, pode ser 'command', 'w' para macOS

            time.sleep(1) # Pequena pausa antes da próxima pesquisa

        completed_searches_label.config(text=f"Pesquisas realizadas: {total_searches}")
        progress_var.set(total_searches)
        root.update_idletasks()
        messagebox.showinfo("Pesquisas Concluídas", "Todas as pesquisas foram realizadas com sucesso!")

    except FileNotFoundError:
        messagebox.showerror("Erro", f"O arquivo '{search_list_file}' não foi encontrado.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
    finally:
        start_button.config(state=tk.NORMAL) # Reabilita o botão ao finalizar

def start_search_thread(search_list_file, delay_between_searches, root, progress_var, total_searches_label, completed_searches_label, progress_bar, start_button):
    """Inicia a função de pesquisa em uma thread separada para não travar a GUI."""
    thread = threading.Thread(target=perform_searches, args=(search_list_file, delay_between_searches, root, progress_var, total_searches_label, completed_searches_label, progress_bar, start_button))
    thread.daemon = True # Permite que o programa seja fechado mesmo se a thread estiver rodando
    thread.start()

def create_gui(search_list_file="pesquisas.txt"):
    root = tk.Tk()
    root.title("Automatizador de Pesquisas")
    root.geometry("400x300") # Aumenta um pouco a janela para o novo input

    # Variáveis de controle
    progress_var = tk.DoubleVar()
    delay_var = tk.DoubleVar(value=3.0) # Valor inicial para o delay

    # Labels
    title_label = tk.Label(root, text="Automação de Pesquisas no Bing", font=("Arial", 14, "bold"))
    title_label.pack(pady=10)

    total_searches_label = tk.Label(root, text="Total de pesquisas: 0", font=("Arial", 10))
    total_searches_label.pack(pady=5)

    completed_searches_label = tk.Label(root, text="Pesquisas realizadas: 0", font=("Arial", 10))
    completed_searches_label.pack(pady=5)

    # Input para o delay
    delay_frame = tk.Frame(root)
    delay_frame.pack(pady=5)
    tk.Label(delay_frame, text="Intervalo (segundos):").pack(side=tk.LEFT)
    delay_entry = tk.Entry(delay_frame, textvariable=delay_var, width=10)
    delay_entry.pack(side=tk.LEFT, padx=5)

    # Barra de progresso
    progress_bar = ttk.Progressbar(root, variable=progress_var, length=300, mode='determinate')
    progress_bar.pack(pady=10)

    # Botão Iniciar
    start_button = tk.Button(root, text="Iniciar Pesquisas", command=lambda: start_search_thread(search_list_file, delay_var.get(), root, progress_var, total_searches_label, completed_searches_label, progress_bar, start_button), font=("Arial", 12), bg="#4CAF50", fg="white")
    start_button.pack(pady=15)

    root.mainloop()

if __name__ == "__main__":
    
    create_gui(search_list_file="pesquisas.txt")