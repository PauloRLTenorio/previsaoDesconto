def previsao():
    import tkinter as tk
    from tkinter import ttk
    from tktooltip import ToolTip # pip install tkinter-tooltip
    import joblib
    # import sklearn
    # from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
    import pandas as pd
    import json

    # Função para mostrar a dica
    def show_tooltip_valor_avaliacao(event1):
        stooltip_valor_avaliacao = ToolTip(val_avaliacao_entry, \
            'Digite o valor usando "." para separar milhar e "," para separar decimal com duas casas')
    # def show_tooltip_dias_ate_ser_vendido(event2):
    #     tooltip_dias_ate_ser_vendido = ToolTip(val_avaliacao_entry, 'Digite um número inteiro sem zeros a esquerda')

    def prever_desconto():
        # Obter os valores dos campos de entrada
        valor_digitado = val_avaliacao_entry.get()
        
        # Normalizar o valor
        valor_normalizado = float(valor_digitado.replace(".", "").replace(",", "").strip())
        
        x_numericos = {
            'val_avaliacao': valor_normalizado,
            'dias_ate_ser_vendido': dias_ate_ser_vendido.get()
        }

        x_listas = {
            'situacao_na_venda': situacao_na_venda_var.get(),
            'segmento': segmento_var.get(),
            'UF': UF_var.get(),
            'Tipo_de_imovel': Tipo_de_imovel_var.get()
        }

        for item in x_listas:
            x_listas[item] = var_cat_encoded[item][x_listas[item]]

        dicio = x_listas
        dicio.update(x_numericos)

        valores_x = pd.DataFrame(dicio, index=[0])
        colunas = list(dados.columns)
        valores_x = valores_x[colunas]

        desconto = modelo.predict(valores_x)
        desconto = round(desconto[0], 2)
        desconto = f'{desconto:.2f}'.replace('.',',')
        desconto_label.config(text=f"Desconto: {desconto}%")

    # Carregar o modelo e os dados
    modelo = joblib.load('modelo.joblib')
    with open('var_cat_encoded.json', 'r') as openfile:
        var_cat_encoded = json.load(openfile)
    dados = pd.read_csv("dados.csv")

    # Criar a janela principal
    root = tk.Tk()
    root.title("Previsão de Desconto")

    # Criar o rótulo do título do aplicativo com formatação de fonte
    titulo_aplicativo_label = tk.Label(root, text="Previsão de Desconto", font=("Helvetica", 16, "bold"))
    titulo_aplicativo_label.pack(pady=(12, 0))  # Espaçamento vertical

    # Definir as dimensões da janela e centralizá-la
    largura_janela = 300
    altura_janela = 520
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    posicao_x = (largura_tela - largura_janela) // 2
    posicao_y = (altura_tela - altura_janela) // 2
    root.geometry(f"{largura_janela}x{altura_janela}+{posicao_x}+{posicao_y}")

    # Criar variáveis para os campos de entrada
    # val_avaliacao = tk.DoubleVar()
    val_avaliacao = tk.StringVar()
    val_avaliacao.set("0,00")
    dias_ate_ser_vendido = tk.IntVar()

    # Criar variáveis para os dropdowns
    situacao_na_venda_var = tk.StringVar()
    segmento_var = tk.StringVar()
    UF_var = tk.StringVar()
    Tipo_de_imovel_var = tk.StringVar()

    # Criar campos de entrada
    val_avaliacao_label = tk.Label(root, text="Valor de Avaliação")
    val_avaliacao_label.pack(pady=(12, 0))
    # val_avaliacao_entry = tk.Entry(root, textvariable=val_avaliacao, width=28)
    val_avaliacao_entry = tk.Entry(root, textvariable=val_avaliacao, width=28)
    val_avaliacao_entry.pack()
    # Associa o evento de passar o mouse sobre o campo de entrada com a função de mostrar a dica
    val_avaliacao_entry.bind("<Enter>", show_tooltip_valor_avaliacao)

    dias_ate_ser_vendido_label = tk.Label(root, text="Dias até ser Vendido")
    dias_ate_ser_vendido_label.pack(pady=(12, 0))
    dias_ate_ser_vendido_entry = tk.Entry(root, textvariable=dias_ate_ser_vendido, width=28)
    dias_ate_ser_vendido_entry.pack()
    # # Associa o evento de passar o mouse sobre o campo de entrada com a função de mostrar a dica
    # dias_ate_ser_vendido_entry.bind("<Enter>", show_tooltip_dias_ate_ser_vendido)

    # Criar dropdowns
    situacao_na_venda_label = tk.Label(root, text="Situação na Venda")
    situacao_na_venda_label.pack(pady=(12, 0))
    situacao_na_venda_var = tk.StringVar()
    situacao_na_venda_dropdown = ttk.Combobox(root, textvariable=situacao_na_venda_var, width=25)
    situacao_na_venda_dropdown['values'] = ['Desocupado', 'Ocupado']
    situacao_na_venda_dropdown.pack()

    segmento_label = tk.Label(root, text="Segmento")
    segmento_label.pack(pady=(12, 0))
    segmento_var = tk.StringVar()
    segmento_dropdown = ttk.Combobox(root, textvariable=segmento_var, width=25)
    segmento_dropdown['values'] = ['A', 'B', 'C']
    segmento_dropdown.pack()

    UF_label = tk.Label(root, text="UF")
    UF_label.pack(pady=(12, 0))
    UF_var = tk.StringVar()
    UF_dropdown = ttk.Combobox(root, textvariable=UF_var, width=25)
    UF_dropdown['values'] = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', \
        'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO']
    UF_dropdown.pack()

    Tipo_de_imovel_label = tk.Label(root, text="Tipo de Imóvel")
    Tipo_de_imovel_label.pack(pady=(12, 0))
    Tipo_de_imovel_var = tk.StringVar()
    Tipo_de_imovel_dropdown = ttk.Combobox(root, textvariable=Tipo_de_imovel_var, width=25)
    Tipo_de_imovel_dropdown['values'] = ['Casa', 'Gleba', 'Comercial', 'Terreno', 'Loja', \
        'Apartamento', 'Galpão', 'Sobrado', 'Outros', 'Prédio', 'Sala', 'Gleba Urbana']
    Tipo_de_imovel_dropdown.pack()

    # Criar um botão para prever o desconto
    botao_prever = tk.Button(root, text="Prever Desconto", command=prever_desconto,\
                            font=("Helvetica", 14), height=2, width=16)
    botao_prever.pack(pady=(18, 0))

    # Exibir o desconto previsto
    desconto_label = tk.Label(root, text="",\
                            font=("Helvetica", 12, "bold"))
    desconto_label.pack(pady=(6, 0))

    # Defina o nome do criador
    nome_do_criador = "Paulo Tenório\nMatrícula: 113882-9"
    # Adicione um rótulo para indicar o criador
    criador_label = tk.Label(root, text=f"Desenvolvido por {nome_do_criador}", font=("Helvetica", 8))
    criador_label.pack(side="bottom", pady=(0,10))

    # # Transformar PNG em ICO
    # # Carregue a imagem em formato PNG
    # icone_png = Image.open("icone.png")
    # # Converta a imagem para o formato de ícone .ico
    # icone_ico = icone_png.save("icone.ico", format="ICO")

    # Configure o ícone da janela
    root.iconbitmap("icone.ico")

    root.mainloop()

previsao()
