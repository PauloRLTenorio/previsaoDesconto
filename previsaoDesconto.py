from gerarModeloEstatistico3_3 import gerarModelo
from previsao_desconto1_4 import previsao
from print_in_rectangle import print_in_rectangle

# Apresentação
apresentacao = 'Aguarde enquanto carrega os dados'
print_in_rectangle(apresentacao, 1, 0)

gerarModelo()
previsao()
