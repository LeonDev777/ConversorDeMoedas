import tkinter as tk
from tkinter import ttk
import requests
from tkinter import messagebox

def converter_moeda():
    valor = valor_entry.get()
    moeda_origem = moeda_origem_combo.get()
    moeda_destino = moeda_destino_combo.get()

    if not valor or not moeda_origem or not moeda_destino:
        messagebox.showerror("Erro", "Preencha todos os campos!")
        return

    try:
        valor = float(valor)

      
        access_key = "9cb4fc944a10dd762c9274985f94a104"  

        url = f"https://api.exchangerate.host/convert?access_key={access_key}&from={moeda_origem}&to={moeda_destino}&amount={valor}"

        response = requests.get(url)

       
        if response.status_code == 200:
            data = response.json()

       
            if data.get("success"):
                #extrai o valor convertido
                valor_convertido = data.get("result")

                if valor_convertido is not None:
                     resultado_label.config(text=f"{valor:.2f} {moeda_origem} = {valor_convertido:.2f} {moeda_destino}")
                else:
                    messagebox.showerror("Erro", "Valor convertido não encontrado")

            else:
                erro_info = data.get("error", "Erro desconhecido")
                messagebox.showerror("Erro", f"Conversão falhou!")
        else:
            messagebox.showerror("Erro", f"Erro na requisição")


    except ValueError:
        messagebox.showerror("Erro", "Digite um valor numérico válido!")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"Erro na requisição: {e}")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro inesperado: {e}")


root = tk.Tk()
root.title("Conversor de Moedas Simples")

style = ttk.Style()
style.theme_use("clam")

#rótulos e campos de entrada
valor_label = ttk.Label(root, text="Valor:")
valor_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

valor_entry = ttk.Entry(root)
valor_entry.grid(row=0, column=1, padx=10, pady=10)

moeda_origem_label = ttk.Label(root, text="Moeda de Origem:")
moeda_origem_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

moeda_destino_label = ttk.Label(root, text="Moeda de Destino:")
moeda_destino_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

#comboboxes para escolher as moedas
moedas = ["USD", "EUR", "BRL", "GBP", "JPY", "CAD", "AUD"]

moeda_origem_combo = ttk.Combobox(root, values=moedas)
moeda_origem_combo.grid(row=1, column=1, padx=10, pady=10)
moeda_origem_combo.set("USD")

moeda_destino_combo = ttk.Combobox(root, values=moedas)
moeda_destino_combo.grid(row=2, column=1, padx=10, pady=10)
moeda_destino_combo.set("BRL")

#botão de Converter
converter_button = ttk.Button(root, text="Converter", command=converter_moeda)
converter_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

#label para mostrar o resultado
resultado_label = ttk.Label(root, text="")
resultado_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

#inicia o loop principal da interface
root.mainloop()