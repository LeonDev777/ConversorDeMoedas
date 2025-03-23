import tkinter as tk
from tkinter import ttk
import requests
from tkinter import messagebox

class ConversorMoedasApp:
    moedas = ["USD", "EUR", "BRL", "GBP", "JPY", "CAD", "AUD"]  

    def __init__(self, root):
        self.root = root
        root.title("Conversor de Moedas Simples")

        style = ttk.Style()
        style.theme_use("clam")

      
        self.valor_label = ttk.Label(root, text="Valor:")
        self.valor_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.valor_entry = ttk.Entry(root)
        self.valor_entry.grid(row=0, column=1, padx=10, pady=10)

        self.moeda_origem_label = ttk.Label(root, text="Moeda de Origem:")
        self.moeda_origem_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.moeda_destino_label = ttk.Label(root, text="Moeda de Destino:")
        self.moeda_destino_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.moeda_origem_combo = ttk.Combobox(root, values=self.moedas)
        self.moeda_origem_combo.grid(row=1, column=1, padx=10, pady=10)
        self.moeda_origem_combo.set("USD")

        self.moeda_destino_combo = ttk.Combobox(root, values=self.moedas)
        self.moeda_destino_combo.grid(row=2, column=1, padx=10, pady=10)
        self.moeda_destino_combo.set("BRL")

        converter_button = ttk.Button(root, text="Converter", command=self.converter_moeda)
        converter_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

     
        self.resultado_label = ttk.Label(root, text="")
        self.resultado_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def converter_moeda(self):
        valor = self.valor_entry.get()
        moeda_origem = self.moeda_origem_combo.get()
        moeda_destino = self.moeda_destino_combo.get()

        print(f"converter_moeda: valor={valor}, moeda_origem={moeda_origem}, moeda_destino={moeda_destino}") 

        if not valor or not moeda_origem or not moeda_destino:
            print("converter_moeda: Preencha todos os campos!")
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return

        try:
            valor = float(valor)
            print(f"converter_moeda: valor convertido para float: {valor}") 

            access_key = "SUA_CHAVE_DE_ACESSO"

            url = f"https://api.exchangerate.host/convert?access_key={access_key}&from={moeda_origem}&to={moeda_destino}&amount={valor}"

            response = requests.get(url)
            print(f"converter_moeda: response.status_code = {response.status_code}") 

            if response.status_code == 200:
                data = response.json()
                print(f"converter_moeda: data = {data}") 

                if data.get("success"):
                    valor_convertido = data.get("result")

                    if valor_convertido is not None:
                         self.resultado_label.config(text=f"{valor:.2f} {moeda_origem} = {valor_convertido:.2f} {moeda_destino}")
                    else:
                        print("converter_moeda: Valor convertido não encontrado") 
                        messagebox.showerror("Erro", "Valor convertido não encontrado")

                else:
                    erro_info = data.get("error", "Erro desconhecido")
                    print(f"converter_moeda: Conversão falhou! Erro da API: {erro_info}") 
                    messagebox.showerror("Erro", f"Conversão falhou!")
            else:
                print(f"converter_moeda: Erro na requisição: {response.status_code}") 
                messagebox.showerror("Erro", f"Erro na requisição")

        except ValueError:
            print("converter_moeda: Digite um valor numérico válido!") 
            messagebox.showerror("Erro", "Digite um valor numérico válido!")
        except requests.exceptions.RequestException as e:
            print(f"converter_moeda: Erro na requisição: {e}") 
            messagebox.showerror("Erro", f"Erro na requisição: {e}")
        except Exception as e:
            print(f"converter_moeda: Ocorreu um erro inesperado: {e}") 
            messagebox.showerror("Erro", f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConversorMoedasApp(root)
    root.mainloop()