import biwengerapi.movimientos as movs

html = open('ejemplo_basico.html', 'r', encoding='UTF8')
html_txt = html.read()

movis = movs.procesar_html_con_movimientos(html_txt=html_txt)
print('\nEjemplo basico:\n')
for mov in movis:
    print(mov)

html = open('linea_temporal_1_semana.html', 'r', encoding='UTF8')
html_txt = html.read()

movis = movs.procesar_html_con_movimientos(html_txt=html_txt)
print('\nEjemplo 1 semana:\n')
for mov in movis:
    print(mov)
