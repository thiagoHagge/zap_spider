import requests
import shutil
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# User input for phone number and range
prompt = input('Digite o número inicial (somente número incluindo ddi):\n')
n = input('Insira a quantidade de números da busca:\n')

# Set up Chrome WebDriver options
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

# Open WhatsApp Web and wait for authentication
driver.get("https://web.whatsapp.com")
input("Autentique o whatsapp e na sequência aperte Enter")

# Ensure the directory exists
os.makedirs('./zap_users', exist_ok=True)

# Loop through the phone numbers
for x in range(int(n)):
    phone = str(int(prompt) + x)
    driver.get("https://web.whatsapp.com/send/?phone=" + phone)

    # Use explicit wait to ensure page load or check for invalid number indication
    try:
        # Wait until either the profile data or the "phone number is invalid" message is loaded
        WebDriverWait(driver, 15).until(
            lambda d: d.find_element(By.CSS_SELECTOR, '[title="Dados de perfil"]') or
                      d.find_element(By.XPATH, '//div[contains(text(),"não é um número de telefone válido")]')
        )

        # Check for invalid number message
        try:
            invalid_number = driver.find_element(By.XPATH,
                                                 '//div[contains(text(),"não é um número de telefone válido")]')
            print(f"Invalid number: {phone}. Skipping to next number.")
            continue  # Skip to the next number
        except NoSuchElementException:
            pass  # No invalid number message found, continue with processing

        # If valid, proceed with extracting profile information
        driver.find_element(By.CSS_SELECTOR, '[title="Dados de perfil"]').click()

        # Wait for profile details to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.copyable-text[dir="auto"]'))
        )
        name = driver.find_element(By.CSS_SELECTOR, '.copyable-text[dir="auto"]').text

        # Fetch all image elements
        imgs = driver.find_elements(By.TAG_NAME, 'img')
        for img in imgs:
            src = img.get_attribute('src')
            if src and 'stp=dst-jpg_s96x96' not in src and src.startswith('https://') and 'maps' not in src:
                print(f'Salvando imagem do número: {phone}. Nome: {name}')

                # Download the image
                try:
                    with requests.get(src, stream=True) as response:
                        response.raise_for_status()
                        with open(f'./zap_users/{phone}-{name}.png', 'wb') as out_file:
                            shutil.copyfileobj(response.raw, out_file)
                except requests.exceptions.RequestException as e:
                    print(f"Erro ao baixar a imagem: {e}")

    except (NoSuchElementException, TimeoutException) as e:
        print(f"Element not found or timeout occurred for phone number: {phone}. Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Clean up
driver.quit()
