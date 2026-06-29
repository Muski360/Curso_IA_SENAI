import pyautogui as pt
from faker import Faker
faker = Faker()


pt.press('win')
pt.write("word")
pt.press('enter')
pt.sleep(4)
pt.leftClick(226,211)
pt.sleep(2)
texto = "Não obstante, o desenvolvimento continuo de distintas formas de atuacao promove a alavancagem das diversas correntes de pensamento."
pt.write(texto)
pt.sleep(1)
pt.hotkey('ctrl','b')
pt.sleep(1)
pt.leftClick(253,329)
nome = faker.name()
pt.write(nome)
pt.sleep(1)
pt.press('enter')
pt.sleep(1)
pt.hotkey('alt','F4')
