import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO

def calcular_aditivo():
    try:
        cnpjs_atual = int(entry_cnpjs_atual.get())  # Quantidade atual de CNPJs
        mensalidade_cliente = float(entry_mensalidade.get().replace(',', '.'))
        valor_aditivo = float(entry_aditivo.get().replace(',', '.'))

        # Verificar se o cliente terá desconto
        desconto_aplicado = var_desconto.get() == 1  # 1 é "Sim", 0 é "Não"

        # Pacote de 50 CNPJs adicionais
        total_cnpjs_50 = cnpjs_atual + 50
        custo_adicional_50 = 50 * valor_aditivo
        nova_mensalidade_50 = mensalidade_cliente + custo_adicional_50

        # Pacote de 100 CNPJs adicionais
        valor_aditivo_100 = valor_aditivo - 0.10 if desconto_aplicado else valor_aditivo
        total_cnpjs_100 = cnpjs_atual + 100
        custo_adicional_100 = 100 * valor_aditivo_100
        nova_mensalidade_100 = mensalidade_cliente + custo_adicional_100

        # Pacote de 150 CNPJs adicionais
        valor_aditivo_150 = valor_aditivo - 0.20 if desconto_aplicado else valor_aditivo
        total_cnpjs_150 = cnpjs_atual + 150
        custo_adicional_150 = 150 * valor_aditivo_150
        nova_mensalidade_150 = mensalidade_cliente + custo_adicional_150

        resultado = f"""
        Pacote de 50 CNPJs adicionais:
        Total de CNPJs: {cnpjs_atual} + 50 = {total_cnpjs_50}
        Custo Adicional: 50 CNPJs = R${custo_adicional_50:.2f}
        Nova Mensalidade: R${mensalidade_cliente:.2f} + R${custo_adicional_50:.2f} = R${nova_mensalidade_50:.2f}

        Pacote de 100 CNPJs adicionais:
        Total de CNPJs: {cnpjs_atual} + 100 = {total_cnpjs_100}
        Custo Adicional: 100 CNPJs = R${custo_adicional_100:.2f}
        Nova Mensalidade: R${mensalidade_cliente:.2f} + R${custo_adicional_100:.2f} = R${nova_mensalidade_100:.2f}

        Pacote de 150 CNPJs adicionais:
        Total de CNPJs: {cnpjs_atual} + 150 = {total_cnpjs_150}
        Custo Adicional: 150 CNPJs = R${custo_adicional_150:.2f}
        Nova Mensalidade: R${mensalidade_cliente:.2f} + R${custo_adicional_150:.2f} = R${nova_mensalidade_150:.2f}
        """
        messagebox.showinfo("Resultado", resultado)

    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")

# Criação da interface gráfica
root = tk.Tk()
root.title("Cálculo de Aditivo")
root.geometry("490x240")  # Tamanho da janela
root.configure(bg="#2c3e50")  # Cor de fundo azul escuro

# Carregar a nova imagem do bitmap
url = "https://i.postimg.cc/fL1xFRZp/108cce18-b6ba-4263-88c5-cb093c39afd6.jpg"
response = requests.get(url)
img_data = response.content
img = Image.open(BytesIO(img_data)).resize((75, 75))  # Aumente o tamanho da imagem
img = ImageTk.PhotoImage(img)
root.iconphoto(False, img)  # Defina o novo ícone para a janela

# Adicionar imagem ao topo
img_label = tk.Label(root, image=img, bg="#2c3e50")  # Cor de fundo da imagem
img_label.image = img  # Manter uma referência da imagem
img_label.grid(row=0, column=0, columnspan=2)

# Título
titulo_label = tk.Label(root, text="Cálculo de Aditivo", font=("Arial", 16), fg="white", bg="#2c3e50")  # Letras brancas
titulo_label.grid(row=1, column=0, columnspan=2)

# Labels e inputs
tk.Label(root, text="Quantidade atual de CNPJs:", fg="white", bg="#2c3e50").grid(row=2, column=0)
entry_cnpjs_atual = tk.Entry(root)
entry_cnpjs_atual.grid(row=2, column=1)

tk.Label(root, text="Mensalidade do Cliente:", fg="white", bg="#2c3e50").grid(row=3, column=0)
entry_mensalidade = tk.Entry(root)
entry_mensalidade.grid(row=3, column=1)

tk.Label(root, text="Valor do Aditivo por CNPJ:", fg="white", bg="#2c3e50").grid(row=4, column=0)
entry_aditivo = tk.Entry(root)
entry_aditivo.grid(row=4, column=1)

# Pergunta sobre desconto
var_desconto = tk.IntVar()
tk.Label(root, text="Cliente terá desconto em 100/150 CNPJs?", fg="white", bg="#2c3e50").grid(row=5, column=0, columnspan=2)
tk.Radiobutton(root, text="Sim", variable=var_desconto, value=1, bg="#2c3e50").grid(row=6, column=0)
tk.Radiobutton(root, text="Não", variable=var_desconto, value=0, bg="#2c3e50").grid(row=6, column=1)

# Botão para calcular, centralizado
button_calcular = tk.Button(root, text="Calcular Aditivo", command=calcular_aditivo)
button_calcular.grid(row=7, column=0, columnspan=2)

# Iniciar a interface gráfica
root.mainloop()
