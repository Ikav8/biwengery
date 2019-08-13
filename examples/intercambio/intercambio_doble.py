import bs4

intercambio = open('intercambio_doble.html', 'r', encoding='UTF8')
intercambio_txt = intercambio.read()
bs = bs4.BeautifulSoup(intercambio_txt, 'html.parser')

offer_exchange_card = bs.find('offer-exchange-card')

es_fichaje = '€' in offer_exchange_card.text # Forma de coger solo los fichajes #
n_user = len(offer_exchange_card.find_all('user-link')) # Check si hay 1 o 2 jugadores implicados #

jugador_1 = offer_exchange_card.find_all('user-link')[0].text.strip()
jugador_2 = offer_exchange_card.find_all('user-link')[1].text.strip()

tds = offer_exchange_card.find_all(style="width: 40%")
divs_jugador_1 = tds[0].find_all('div')
aportacion_jugador_1 = 0
for gasto in divs_jugador_1:
    aportacion_jugador_1 += int(gasto.text.replace(u'\xa0', u' ').split(' ')[0].replace('.', ''))

divs_jugador_2 = tds[1].find_all('div')
aportacion_jugador_2 = 0
for gasto in divs_jugador_2:
    aportacion_jugador_2 += int(gasto.text.replace(u'\xa0', u' ').split(' ')[0].replace('.', ''))

balance_jugador_1 = aportacion_jugador_2 - aportacion_jugador_1
balance_jugador_2 = aportacion_jugador_1 - aportacion_jugador_2

print(es_fichaje, n_user, jugador_1, balance_jugador_1, jugador_2, balance_jugador_2, sep=' - ')