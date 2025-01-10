from core.engine import Engine
from stages.menu import menu
from stages.play import play
from stages.db_menu import db_menu
from stages.login import login
from stages.register import register


e = Engine('Strategy')
e.register('Menu', menu)
e.register('Play', play)
e.register('DB', db_menu)
e.register('Login', login)
e.register('Register', register)
e.switch_to('Menu')
e.run()