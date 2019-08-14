import bs4

class movimiento:
    def __init__(self, jugador, balance, detalles):
        self.jugador = jugador
        self.balance = balance
        self.detalles = detalles

    def __str__(self):
        signo = '+' if self.balance > 0 else '-'
        return("[" + signo + "] " + self.jugador + " [ " + str(self.balance) + " ] (" + self.detalles + ").")


def jugador_a_jugador(texto):
    bs = bs4.BeautifulSoup(texto, 'html.parser')
    player_tag = bs.find('player-card')
    dynamic_expression_container = player_tag.find('dynamic-expression-container')
    posicion = player_tag.find('player-position').text.strip()
    jugador = player_tag.find('span').text.strip()
    precio_txt = player_tag.find('strong').text.replace(u'\xa0', u' ')
    precio = int(precio_txt.split(' ')[0].replace('.', ''))
    equipo = player_tag.find('a')['title'].strip()
    de = dynamic_expression_container.find_all('user-link')[0].text.strip()
    para = dynamic_expression_container.find_all('user-link')[1].text.strip()
    detalles = equipo + " - " + jugador + "(" + posicion + "): " + de + " -> " + para + " (" + precio_txt + ")"
    movimiento_jugador_1 = movimiento(jugador=de, balance=precio, detalles=detalles)
    movimiento_jugador_2 = movimiento(jugador=para, balance=-precio, detalles=detalles)
    return (movimiento_jugador_1, movimiento_jugador_2)

def jugador_a_mercado(texto):
    bs = bs4.BeautifulSoup(texto, 'html.parser')
    player_tag = bs.find('player-card')
    dynamic_expression_container = player_tag.find('dynamic-expression-container')
    posicion = player_tag.find('player-position').text.strip()
    jugador = player_tag.find('span').text.strip()
    precio_txt = player_tag.find('strong').text.replace(u'\xa0', u' ')
    precio = int(precio_txt.split(' ')[0].replace('.', ''))
    equipo = player_tag.find('a')['title'].strip()
    de = dynamic_expression_container.find_all('user-link')[0].text.strip()
    para = 'Mercado'
    detalles = equipo + " - " + jugador + "(" + posicion + "): " + de + " -> " + para + " (" + precio_txt + ")"
    movimiento_jugador_1 = movimiento(jugador=de, balance=precio, detalles=detalles)
    return (movimiento_jugador_1)

def mercado_a_jugador(texto):
    bs = bs4.BeautifulSoup(texto, 'html.parser')
    player_tag = bs.find('player-card')
    dynamic_expression_container = player_tag.find('dynamic-expression-container')
    posicion = player_tag.find('player-position').text.strip()
    jugador = player_tag.find('span').text.strip()
    precio_txt = player_tag.find('strong').text.replace(u'\xa0', u' ')
    precio = int(precio_txt.split(' ')[0].replace('.', ''))
    equipo = player_tag.find('a')['title'].strip()
    para = dynamic_expression_container.find_all('user-link')[0].text.strip()
    de = 'Mercado'
    detalles = equipo + " - " + jugador + "(" + posicion + "): " + de + " -> " + para + " (" + precio_txt + ")"
    movimiento_jugador_1 = movimiento(jugador=para, balance=-precio, detalles=detalles)
    return (movimiento_jugador_1)

def intercambio(texto):
    bs = bs4.BeautifulSoup(texto, 'html.parser')
    offer_exchange_card = bs.find('offer-exchange-card')
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

    texto_intercambio_1 = ' + '.join(list(filter(None, tds[0].text.replace(u'\xa0', u' ').strip().split('\n'))))
    texto_intercambio_2 = ' + '.join(list(filter(None, tds[1].text.replace(u'\xa0', u' ').strip().split('\n'))))

    detalles = "Intercambio: [" + jugador_1 + " <> " + jugador_2 + "] - (" + texto_intercambio_1 + " <> " + texto_intercambio_2 + ")"

    movimiento_jugador_1 = movimiento(jugador=jugador_1, balance=balance_jugador_1, detalles=detalles)
    movimiento_jugador_2 = movimiento(jugador=jugador_2, balance=balance_jugador_2, detalles=detalles)
    return(movimiento_jugador_1, movimiento_jugador_2)