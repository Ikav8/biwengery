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
    pass