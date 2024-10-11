import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
import openpyxl
from datetime import datetime

# Função para salvar os dados no Excel
def salvar_excel(nome_cliente, mensalidade_atual, nova_mensalidade_50, nova_mensalidade_100, nova_mensalidade_150, proposta_aprovada):
    try:
        # Abrir ou criar o arquivo Excel
        try:
            workbook = openpyxl.load_workbook("propostas_clientes.xlsx")
        except FileNotFoundError:
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            # Criar cabeçalhos
            sheet.append(["Data", "Nome do Cliente", "Mensalidade Atual", "Nova Mensalidade (50 CNPJs)", "Nova Mensalidade (100 CNPJs)", "Nova Mensalidade (150 CNPJs)", "Proposta Aprovada"])
        else:
            sheet = workbook.active
        
        # Inserir uma nova linha com os dados
        sheet.append([
            datetime.now().strftime("%d/%m/%Y"),
            nome_cliente,
            f"R$ {mensalidade_atual:.2f}",
            f"R$ {nova_mensalidade_50:.2f}",
            f"R$ {nova_mensalidade_100:.2f}",
            f"R$ {nova_mensalidade_150:.2f}",
            proposta_aprovada
        ])
        
        # Salvar o arquivo Excel
        workbook.save("propostas_clientes.xlsx")
        messagebox.showinfo("Sucesso", "Dados salvos no Excel com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar no Excel: {e}")

def calcular_aditivo():
    try:
        nome_cliente = entry_nome_cliente.get()  # Nome do cliente
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

        # Pergunta se o cliente aprovou a proposta
        aprovar = messagebox.askyesno("Aprovação", f"O cliente {nome_cliente} aprovou a proposta?")
        if aprovar:
            # Nova janela para escolher qual proposta o cliente aprovou
            def escolher_proposta():
                opcao_aprovada = var_proposta.get()
                if opcao_aprovada == "50":
                    salvar_excel(nome_cliente, mensalidade_cliente, nova_mensalidade_50, 0, 0, "50 CNPJs")
                elif opcao_aprovada == "100":
                    salvar_excel(nome_cliente, mensalidade_cliente, nova_mensalidade_50, nova_mensalidade_100, 0, "100 CNPJs")
                elif opcao_aprovada == "150":
                    salvar_excel(nome_cliente, mensalidade_cliente, nova_mensalidade_50, nova_mensalidade_100, nova_mensalidade_150, "150 CNPJs")
                janela_proposta.destroy()  # Fechar janela após salvar

            # Criar janela para seleção de proposta
            janela_proposta = tk.Toplevel(root)
            janela_proposta.title("Seleção de Proposta")
            janela_proposta.geometry("300x150")

            var_proposta = tk.StringVar(value="50")  # Valor padrão

            tk.Label(janela_proposta, text="Selecione a proposta aprovada:").pack(pady=10)
            tk.Radiobutton(janela_proposta, text="50 CNPJs", variable=var_proposta, value="50").pack()
            tk.Radiobutton(janela_proposta, text="100 CNPJs", variable=var_proposta, value="100").pack()
            tk.Radiobutton(janela_proposta, text="150 CNPJs", variable=var_proposta, value="150").pack()

            tk.Button(janela_proposta, text="Confirmar", command=escolher_proposta).pack(pady=10)

        else:
            messagebox.showinfo("Sem Aprovação", f"A proposta não foi aprovada pelo cliente {nome_cliente}.")

    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")

# Criação da interface gráfica
root = tk.Tk()
root.title("Cálculo de Aditivo")
root.geometry("490x320")  # Aumentar tamanho para acomodar o novo campo
root.configure(bg="#2c3e50")  # Cor de fundo azul escuro

# Carregar a imagem do bitmap
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

# Campo de nome do cliente
tk.Label(root, text="Nome do Cliente:", fg="white", bg="#2c3e50").grid(row=2, column=0)
entry_nome_cliente = tk.Entry(root)
entry_nome_cliente.grid(row=2, column=1)

# Labels e inputs
tk.Label(root, text="Quantidade atual de CNPJs:", fg="white", bg="#2c3e50").grid(row=3, column=0)
entry_cnpjs_atual = tk.Entry(root)
entry_cnpjs_atual.grid(row=3, column=1)

tk.Label(root, text="Mensalidade do Cliente:", fg="white", bg="#2c3e50").grid(row=4, column=0)
entry_mensalidade = tk.Entry(root)
entry_mensalidade.grid(row=4, column=1)

tk.Label(root, text="Valor do Aditivo por CNPJ:", fg="white", bg="#2c3e50").grid(row=5, column=0)
entry_aditivo = tk.Entry(root)
entry_aditivo.grid(row=5, column=1)

# Pergunta sobre desconto
var_desconto = tk.IntVar()
tk.Label(root, text="Cliente terá desconto em 100/150 CNPJs?", fg="white", bg="#2c3e50").grid(row=6, column=0, columnspan=2)
tk.Radiobutton(root, text="Sim", variable=var_desconto, value=1, bg="#2c3e50").grid(row=7, column=0)
tk.Radiobutton(root, text="Não", variable=var_desconto, value=0, bg="#2c3e50").grid(row=7, column=1)

# Botão para calcular, centralizado
button_calcular = tk.Button(root, text="Calcular Aditivo", command=calcular_aditivo)
button_calcular.grid(row=8, column=0, columnspan=2)

# Iniciar a interface gráfica
root.mainloop()
