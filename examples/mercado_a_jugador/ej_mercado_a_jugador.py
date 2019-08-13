import bs4

m_to_j = open('mercado_a_jugador.html', 'r', encoding='UTF8')
m_to_j_txt = m_to_j.read()
bs = bs4.BeautifulSoup(m_to_j_txt, 'html.parser')

player_tag = bs.find('player-card')
dynamic_expression_container = player_tag.find('dynamic-expression-container')

es_fichaje = '€' in player_tag.text # Forma de coger solo los fichajes #
n_user = len(player_tag.find_all('user-link')) # Check si hay 1 o 2 jugadores implicados #


posicion = player_tag.find('player-position').text.strip()
jugador = player_tag.find('span').text.strip()
precio = int(player_tag.find('strong').text.split(' ')[0].replace(u'\xa0', u' ').split(' ')[0].replace('.', ''))
equipo = player_tag.find('a')['title'].strip()
de = 'Mercado'
para = dynamic_expression_container.find_all('user-link')[0].text.strip()
print(es_fichaje, n_user, jugador, posicion, precio, equipo, de, para, sep=' - ')