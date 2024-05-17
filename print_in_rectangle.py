# Se informar o parametro notice então usará o conteudo abaixo do if, senão será sem ele. Usei isto para print de avisos quando usar notice.
# Noutro caso, notice2, apenas para usar a moldura formado por #.
# Informar notice e notice2 igual a algo diferente de zero para ativá-los

def print_in_rectangle(content, notice="", notice2=""):
    if notice == 1:
        content = "\n\n   " + 10*"*" + f"   {content}   " + 10*"*" + "   \n\n"
    if notice2 == 1:
        content = "\n\n   " + 10*" " + f"   {content}   " + 10*" " + "   \n\n"
    lines = content.split('\n')
    max_length = max(len(line) for line in lines)
    border = '#' * (max_length + 4)
    print('\n')
    print(border)
    for line in lines:
        spaces = max_length - len(line)
        print(f'# {line}{" " * spaces} #')
    print(border)
    print('\n')

