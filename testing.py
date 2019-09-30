import biwengerapi.movimientos as movs
import pandas as pd

pd.options.display.float_format = '{:, .2f}'.format

html = open('testing.html', 'r', encoding='UTF8')
html_txt = html.read()

movis_iniciales = [
    movs.movimiento(jugador='Alberteam', balance=19700000, detalles='INICIAL'),
    movs.movimiento(jugador='Dani8', balance=19690000, detalles='INICIAL'),
    movs.movimiento(jugador='IkaTęām', balance=19640000, detalles='INICIAL'),
    movs.movimiento(jugador='KBS', balance=19870000, detalles='INICIAL'),
    movs.movimiento(jugador='Manchica F.C', balance=19700000, detalles='INICIAL'),
    movs.movimiento(jugador='Persy', balance=19720000, detalles='INICIAL'),
    movs.movimiento(jugador='RNP_Team', balance=19750000, detalles='INICIAL'),
    movs.movimiento(jugador="Rubio's team", balance=19630000, detalles='INICIAL'),
    movs.movimiento(jugador='YoyoTeam', balance=19690000, detalles='INICIAL')
]

movis = movs.procesar_html_con_movimientos(html_txt=html_txt)
unique_detalles = []
for m in movis:
    if m.detalles not in unique_detalles:
        unique_detalles.append(m.detalles)


movis = movis_iniciales + movis

for mov in movis:
    if 'Persy' in mov.jugador:
        mov.jugador = 'PERSY  '
    if 'Manchica' in mov.jugador:
        mov.jugador = 'SERGIO '
    if 'IKA' in mov.jugador or 'Ika' in mov.jugador:
        mov.jugador = 'IKA    '
    if 'Raul' in mov.jugador or 'RNP' in mov.jugador:
        mov.jugador = 'RAUL   '
    if 'Alberteam' in mov.jugador:
        mov.jugador = 'ALBERTO'
    if 'KBS' in mov.jugador:
        mov.jugador = 'KAMA   '
    if 'YoyoTeam' in mov.jugador:
        mov.jugador = 'YOYO   '
    if 'Rubio' in mov.jugador:
        mov.jugador = 'RUBIO  '
    if 'Dani8' in mov.jugador:
        mov.jugador = 'DANI   '

df = pd.DataFrame.from_records([m.to_dict() for m in movis])

df['balance'] = df['balance'].astype('int64')

df = df.groupby('jugador').sum().sort_values('balance')

for i, row in df.iterrows():
    print(row.name, " \t==> \t", '{:,} €'.format(row["balance"]).replace(',', '.'))

#print(df)
