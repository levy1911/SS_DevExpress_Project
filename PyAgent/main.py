from seeker import Seeker
from mail_module import send_mail

s = Seeker()
file_name = s.seek()

send_mail('test@localhost', ['lewpaw@gmail.com'], 'TESTOWY', 'Tasdasdasdasdasdasd', [str(file_name)])
