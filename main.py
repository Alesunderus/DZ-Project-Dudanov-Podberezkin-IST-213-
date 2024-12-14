from core.engine import Engine
from stages.menu import menu
from stages.play import play
from stages.db_menu import db_menu

e = Engine('Strategy')
e.register('Menu', menu)
e.register('Play', play)
e.register('DB', db_menu)
e.switch_to('Menu')
e.run()