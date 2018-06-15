from seeker import Seeker
from mail_module import send_mail

s = Seeker()
file_name = s.seek()
mail_text = 'DevExpress dependency report.'
mail_title = 'DevExpress dependency report'
send_to = ['pawelle@softsystem.pl']
send_from = 'etools@softsystem.pl'

#send_mail(send_from, send_to, mail_title, mail_text, [str(file_name)])
