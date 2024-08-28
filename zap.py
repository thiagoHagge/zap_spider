import requests
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException  
prompt = input('Digite o número inicial (somente número incluindo ddi):\n')
n = input('Insira a quantidade de números da busca:\n')
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
driver.get("https://web.whatsapp.com")
input("Autentique o whatsapp e na sequêcia aperte Enter")
#testar caso de numero não existente
for x in range(int(n)):
 phone = str(int(prompt)+x)
 driver.get("https://web.whatsapp.com/send/?phone="+phone)
 driver.implicitly_wait(90)
 try:
  driver.find_element(By.CSS_SELECTOR, '[title="Dados de perfil"]').click()
  driver.implicitly_wait(10)
  name = driver.find_element(By.CSS_SELECTOR,'.copyable-text[dir="auto"]').text
  imgs = driver.find_elements(By.TAG_NAME, 'img')
  for img in imgs:
   src = img.get_attribute('src')
   if src is not None:
    if src.find('stp=dst-jpg_s96x96') == -1 and src.find('https://') == 0 and src.find('maps') == -1:
     print('salvando imagem do número:'+phone+'. Nome: '+name)
     response = requests.get(src, stream=True)
     with open('./zap_users/'+phone+'-'+name+'.png', 'wb') as out_file:
      shutil.copyfileobj(response.raw, out_file)
     del response
 except NoSuchElementException:
    c=0 
