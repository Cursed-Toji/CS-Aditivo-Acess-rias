import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
import openpyxl
from datetime import datetime

# Função para salvar os dados no Excel
def salvar_excel(nome_cliente, mensalidade_atual, nova_mensalidade, proposta_aprovada, lucro):
    try:
        # Abrir ou criar o arquivo Excel
        try:
            workbook = openpyxl.load_workbook("propostas_clientes.xlsx")
        except FileNotFoundError:
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            # Criar cabeçalhos
            sheet.append(["Data", "Nome do Cliente", "Mensalidade Atual", "Nova Mensalidade", "Proposta Aprovada", "Lucro"])
        else:
            sheet = workbook.active
        
        # Inserir uma nova linha com os dados
        sheet.append([
            datetime.now().strftime("%d/%m/%Y"),
            nome_cliente,
            f"R$ {mensalidade_atual:.2f}",
            f"R$ {nova_mensalidade:.2f}",
            proposta_aprovada,
            f"R$ {lucro:.2f}"
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

        # Pacotes de CNPJs adicionais
        pacotes = {
            "50": {"quantidade": 50, "desconto": 0},
            "100": {"quantidade": 100, "desconto": 0.10 if desconto_aplicado else 0},
            "150": {"quantidade": 150, "desconto": 0.20 if desconto_aplicado else 0},
        }

        # Calcular novas mensalidades
        for pacote, dados in pacotes.items():
            total_cnpjs = cnpjs_atual + dados["quantidade"]
            valor_aditivo_pacote = valor_aditivo - dados["desconto"]
            custo_adicional = dados["quantidade"] * valor_aditivo_pacote
            nova_mensalidade = mensalidade_cliente + custo_adicional
            dados.update({
                "total_cnpjs": total_cnpjs,
                "valor_aditivo": valor_aditivo_pacote,
                "custo_adicional": custo_adicional,
                "nova_mensalidade": nova_mensalidade
            })

        # Exibir resultados
        resultado = "\n\n".join([
            f"Pacote de {pacote} CNPJs adicionais:\n"
            f"Total de CNPJs: {cnpjs_atual} + {dados['quantidade']} = {dados['total_cnpjs']}\n"
            f"Custo Adicional: {dados['quantidade']} CNPJs = R${dados['custo_adicional']:.2f}\n"
            f"Nova Mensalidade: R${mensalidade_cliente:.2f} + R${dados['custo_adicional']:.2f} = R${dados['nova_mensalidade']:.2f}"
            for pacote, dados in pacotes.items()
        ])
        messagebox.showinfo("Resultado", resultado)

        # Pergunta se o cliente aprovou a proposta
        aprovar = messagebox.askyesno("Aprovação", f"O cliente {nome_cliente} aprovou a proposta?")
        if aprovar:
            # Nova janela para escolher qual proposta o cliente aprovou
            def escolher_proposta():
                opcao_aprovada = var_proposta.get()
                if opcao_aprovada in pacotes:
                    dados = pacotes[opcao_aprovada]
                    lucro = dados['nova_mensalidade'] - mensalidade_cliente
                    salvar_excel(nome_cliente, mensalidade_cliente, dados['nova_mensalidade'], f"{opcao_aprovada} CNPJs", lucro)
                janela_proposta.destroy()  # Fechar janela após salvar

            # Criar janela para seleção de proposta
            janela_proposta = tk.Toplevel(root)
            janela_proposta.title("Seleção de Proposta")
            janela_proposta.geometry("300x150")

            var_proposta = tk.StringVar(value="50")  # Valor padrão

            tk.Label(janela_proposta, text="Selecione a proposta aprovada:").pack(pady=10)
            for pacote in pacotes:
                tk.Radiobutton(janela_proposta, text=f"{pacote} CNPJs", variable=var_proposta, value=pacote).pack()

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

# Labels e inputs
tk.Label(root, text="Nome do Cliente:", fg="white", bg="#2c3e50").grid(row=2, column=0)
entry_nome_cliente = tk.Entry(root)
entry_nome_cliente.grid(row=2, column=1)

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
