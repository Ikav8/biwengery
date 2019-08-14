import biwengerapi.movimientos as movs

texto = open('../jugador_a_jugador/jugador_a_jugador.html', 'r', encoding='UTF8')
a, b = movs.jugador_a_jugador(texto)
print(a)
print(b)

print('-------------')

texto = open('../jugador_a_mercado/jugador_a_mercado.html', 'r', encoding='UTF8')
print(movs.jugador_a_mercado(texto))

print('-------------')

texto = open('../mercado_a_jugador/mercado_a_jugador.html', 'r', encoding='UTF8')
print(movs.mercado_a_jugador(texto))

print('-------------')

texto = open('../intercambio/intercambio_doble.html', 'r', encoding='UTF8')
a, b = movs.intercambio(texto)
print(a)
print(b)