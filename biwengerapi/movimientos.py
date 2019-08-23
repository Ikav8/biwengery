import bs4

class movimiento:
    def __init__(self, jugador, balance, detalles):
        self.jugador = jugador
        self.balance = int(balance)
        self.detalles = detalles

    def __str__(self):
        signo = '+' if int(self.balance) > 0 else '-'
        return("[" + signo + "] " + self.jugador + " [ " + str(self.balance) + " ] (" + self.detalles + ").")

    def __repr__(self):
        signo = '+' if self.balance > 0 else '-'
        return ("[" + signo + "] " + self.jugador + " [ " + str(self.balance) + " ] (" + self.detalles + ").")

    def to_dict(self):
        return {
            'jugador' : self.jugador,
            'balance' : self.balance
        }

def procesar_html_con_movimientos(html_txt):
    bs = bs4.BeautifulSoup(html_txt, 'html.parser')
    movimientos = []
    fichajes_y_ventas = bs.find_all('player-card')
    for player_card in fichajes_y_ventas:
        movs_temp = procesar_fichaje_o_venta(player_card=player_card)
        if movs_temp != False:
            movimientos = movimientos + movs_temp

    intercambios = bs.find_all('offer-exchange-card')
    for offer_exchange_card in intercambios:
        movimientos = movimientos + intercambio(offer_exchange_card=offer_exchange_card)

    jornadas = bs.find_all(class_="roundFinished")
    for jornada in jornadas:
        movimientos = movimientos + procesar_resultados_jornada(roundFinished=jornada)
    return movimientos

def procesar_resultados_jornada(roundFinished):
    roundFinished_txt = roundFinished.text
    lis = roundFinished.find_all('li')
    jornada = 'Jornada ' + roundFinished.find('h3').text.split(' ')[-1]
    movimientos = []
    for li in lis:
        jugador = li.find('user-link').text
        balance = li.find('increment').text.strip().replace(u'\xa0', u' ').split(' ')[0].replace('.', '')
        detalles = jornada + ' - ' + li.text
        movimientos.append(movimiento(jugador=jugador, balance=balance, detalles=detalles))
    return movimientos

def procesar_fichaje_o_venta(player_card):
    player_card_txt = player_card.text
    movimientos = []
    if '€' not in player_card_txt:
        return False
    elif 'ha pagado la' in player_card_txt: # jugador a jugador (clausula)
        movimientos = movimientos + jugador_a_jugador_clausula(player_card)
    elif 'Cedido de' in player_card_txt: # jugador a jugador (cesion)
        movimientos = movimientos + jugador_a_jugador_cesion(player_card)
    elif len(player_card.find_all('user-link')) == 2:  # jugador a jugador
        movimientos = movimientos + jugador_a_jugador(player_card)
    elif 'Vendido por' in player_card_txt:  # jugador a mercado
        movimientos = movimientos + jugador_a_mercado(player_card)
    elif 'Cambia por' in player_card_txt:  # mercado a jugador
        movimientos = movimientos + mercado_a_jugador(player_card)
    else:
        return False
    return movimientos

def jugador_a_jugador(player_tag):
    dynamic_expression_container = player_tag.find('dynamic-expression-container')
    posicion = player_tag.find('player-position').text.strip()
    jugador = player_tag.find('span').text.strip()
    precio_txt = player_tag.find('strong').text.replace(u'\xa0', u' ')
    precio = int(precio_txt.split(' ')[0].replace('.', ''))
    equipo = player_tag.find('a').get('title', '?').strip()
    de = dynamic_expression_container.find_all('user-link')[0].text.strip()
    para = dynamic_expression_container.find_all('user-link')[1].text.strip()
    detalles = equipo + " - " + jugador + "(" + posicion + "): " + de + " -> " + para + " (" + precio_txt + ")"
    movimiento_jugador_1 = movimiento(jugador=de, balance=precio, detalles=detalles)
    movimiento_jugador_2 = movimiento(jugador=para, balance=-precio, detalles=detalles)
    return ([movimiento_jugador_1, movimiento_jugador_2])

def jugador_a_jugador_clausula(player_tag):
    dynamic_expression_container = player_tag.find('dynamic-expression-container')
    posicion = player_tag.find('player-position').text.strip()
    jugador = player_tag.find('span').text.strip()
    precio_txt = player_tag.find('strong').text.replace(u'\xa0', u' ')
    precio = int(precio_txt.split(' ')[0].replace('.', ''))
    equipo = player_tag.find('a')['title'].strip()
    de = dynamic_expression_container.find_all('user-link')[1].text.strip()
    para = dynamic_expression_container.find_all('user-link')[0].text.strip()
    detalles = equipo + " - " + jugador + "(" + posicion + "): " + de + " -> " + para + " (" + precio_txt + ")"
    movimiento_jugador_1 = movimiento(jugador=de, balance=precio, detalles=detalles)
    movimiento_jugador_2 = movimiento(jugador=para, balance=-precio, detalles=detalles)
    return ([movimiento_jugador_1, movimiento_jugador_2])

def jugador_a_jugador_cesion(player_tag):
    dynamic_expression_container = player_tag.find('dynamic-expression-container')
    posicion = player_tag.find('player-position').text.strip()
    jugador = player_tag.find('span').text.strip()
    precio_txt = player_tag.find_all('strong')[1].text.replace(u'\xa0', u' ')
    precio = int(precio_txt.split(' ')[0].replace('.', ''))
    equipo = player_tag.find('a')['title'].strip()
    de = dynamic_expression_container.find_all('user-link')[0].text.strip()
    para = dynamic_expression_container.find_all('user-link')[1].text.strip()
    detalles = equipo + " - " + jugador + "(" + posicion + "): " + de + " ~> " + para + " (" + precio_txt + ") - CESION"
    movimiento_jugador_1 = movimiento(jugador=de, balance=precio, detalles=detalles)
    movimiento_jugador_2 = movimiento(jugador=para, balance=-precio, detalles=detalles)
    return ([movimiento_jugador_1, movimiento_jugador_2])

def jugador_a_mercado(player_tag):
    dynamic_expression_container = player_tag.find('dynamic-expression-container')
    posicion = player_tag.find('player-position').text.strip()
    jugador = player_tag.find('span').text.strip()
    precio_txt = player_tag.find('strong').text.replace(u'\xa0', u' ')
    precio = int(precio_txt.split(' ')[0].replace('.', ''))
    equipo = player_tag.find('a').get('title', '¿?').strip()
    de = dynamic_expression_container.find_all('user-link')[0].text.strip()
    para = 'Mercado'
    detalles = equipo + " - " + jugador + "(" + posicion + "): " + de + " -> " + para + " (" + precio_txt + ")"
    movimiento_jugador_1 = movimiento(jugador=de, balance=precio, detalles=detalles)
    return ([movimiento_jugador_1])

def mercado_a_jugador(player_tag):
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
    return ([movimiento_jugador_1])

def intercambio(offer_exchange_card):
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
    return([movimiento_jugador_1, movimiento_jugador_2])