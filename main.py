import json
import time
import random
from web3 import Web3
from eth_account import Account


with open('abi.json') as file:
    abi = json.load(file)
with open('abi_mint.json') as file:
    abi_mint = json.load(file)


contract_address = '0x51aad5867d73c479ce8c59ae9c9e4bf59d74c4c1'
checksum_contract_address = Web3.to_checksum_address(contract_address)

# Адрес коллекции туда где будете бустить
collection_address = '0x88f9cabee97F2AF81b2cE0C968579cd73CD92D07'
checksum_collection_address = Web3.to_checksum_address(collection_address)


w3 = Web3(Web3.HTTPProvider('https://rpc.blast.io'))


def read_private_keys(filename):
    with open(filename, 'r') as file:
        private_keys = file.readlines()
    return [key.strip() for key in private_keys]


def read_mint_addresses(filename):
    with open(filename, 'r') as file:
        return [address.strip() for address in file.readlines()]



def get_random_gas_limit(min_gas, max_gas):
    return random.randint(min_gas, max_gas)

# Адреса для минта ищите на самом бластре фриминты

mint_addresses = read_mint_addresses('mints.txt')


random.shuffle(mint_addresses)


private_keys = read_private_keys('private_keys.txt')


random.shuffle(private_keys)


contract = w3.eth.contract(address=checksum_contract_address, abi=abi)


method_id = '0x0e3b0141'


successful_accounts = []  # Список для успешно выполненных кошельков


value_in_wei = w3.to_wei(0.01, 'ether')

contract = w3.eth.contract(address=checksum_contract_address, abi=abi)
mint_contract_address = random.choice(mint_addresses)
mint_contract = w3.eth.contract(address=mint_contract_address, abi=abi_mint)


for private_key in private_keys:
    account = Account.from_key(private_key)
    balance = w3.eth.get_balance(account.address)
    if balance < 0.01 * 10**18:  
        print(f"Баланс аккаунта {account.address} меньше 0.01 ETH, выполняем REFUND")
        nonce = w3.eth.get_transaction_count(account.address)
        collection_address = checksum_collection_address  

        # Создание транзакции REFUND
        tx_refund = contract.functions.refund(checksum_collection_address).build_transaction({
            'chainId': 81457,  
            'gas': get_random_gas_limit(150000, 200000), 
            'gasPrice': w3.eth.gas_price,  
            'nonce': nonce,  
        })

        
        signed_tx_refund = w3.eth.account.sign_transaction(tx_refund, private_key)
        tx_hash_refund = w3.eth.send_raw_transaction(signed_tx_refund.rawTransaction)
        
       
        receipt_refund = w3.eth.wait_for_transaction_receipt(tx_hash_refund)
        if receipt_refund.status:
            print(f"Транзакция REFUND от аккаунта {account.address} успешно отправлена и подтверждена. Hash: {tx_hash_refund.hex()}")
            random_delay = random.uniform(25, 37)
            rounded_delay = round(random_delay)
            print(f"Ожидаю {rounded_delay} сек. перед следующей транзакцией")
            time.sleep(rounded_delay)

    # Внутренний цикл для выполнения BOOST и REFUND
    for _ in range(1):
        account = Account.from_key(private_key)
        nonce = w3.eth.get_transaction_count(account.address)
        quantity = 1  
        collection_address = checksum_collection_address  
        
        # Создание транзакции BOOST
        tx_boost = contract.functions.boost(quantity, collection_address).build_transaction({
            'chainId': 81457,  
            'gas': get_random_gas_limit(150000, 200000),  
            'gasPrice': w3.eth.gas_price,  
            'nonce': nonce,  
            'value': value_in_wei  
        })

       
        signed_tx_boost = w3.eth.account.sign_transaction(tx_boost, private_key)
        tx_hash_boost = w3.eth.send_raw_transaction(signed_tx_boost.rawTransaction)
        
        
        receipt_boost = w3.eth.wait_for_transaction_receipt(tx_hash_boost)
        if receipt_boost.status:
            print(f"Транзакция BOOST от аккаунта {account.address} успешно отправлена и подтверждена. Hash: {tx_hash_boost.hex()}")
            random_delay = random.uniform(25, 27)
            rounded_delay = round(random_delay)
            print(f"Ожидаю {rounded_delay} сек. перед следующей транзакцией")
            time.sleep(rounded_delay)
            
            tx_refund = contract.functions.refund(checksum_collection_address).build_transaction({
                'chainId': 81457,  
                'gas': get_random_gas_limit(150000, 200000), 
                'gasPrice': w3.eth.gas_price, 
                'nonce': nonce + 1, 
            })

            
            signed_tx_refund = w3.eth.account.sign_transaction(tx_refund, private_key)
            tx_hash_refund = w3.eth.send_raw_transaction(signed_tx_refund.rawTransaction)
            
            
            receipt_refund = w3.eth.wait_for_transaction_receipt(tx_hash_refund)
            if receipt_refund.status:
                print(f"Транзакция REFUND от аккаунта {account.address} успешно отправлена и подтверждена. Hash: {tx_hash_refund.hex()}")
                random_delay = random.uniform(15, 37)
                rounded_delay = round(random_delay)
                print(f"Ожидаю {rounded_delay} сек. перед следующей транзакцией")
                time.sleep(rounded_delay)
            else:
                print(f"Транзакция REFUND от аккаунта {account.address} завершилась с ошибкой. Hash: {tx_hash_refund.hex()}")
        else:
            print(f"Транзакция BOOST от аккаунта {account.address} завершилась с ошибкой. Hash: {tx_hash_boost.hex()}")




    # Отправить транзакцию BOOST снова
    account = Account.from_key(private_key)
    nonce = w3.eth.get_transaction_count(account.address)
    quantity = 1  
    collection_address = checksum_collection_address  
    
    
    tx_boost = contract.functions.boost(quantity, collection_address).build_transaction({
        'chainId': 81457,  
        'gas': get_random_gas_limit(150000, 200000), 
        'gasPrice': w3.eth.gas_price, 
        'nonce': nonce,  
        'value': value_in_wei  
    })

   
    signed_tx_boost = w3.eth.account.sign_transaction(tx_boost, private_key)
    tx_hash_boost = w3.eth.send_raw_transaction(signed_tx_boost.rawTransaction)
    
   
    receipt_boost = w3.eth.wait_for_transaction_receipt(tx_hash_boost)
    if receipt_boost.status:
        print(f"Транзакция BOOST от аккаунта {account.address} успешно отправлена и подтверждена. Hash: {tx_hash_boost.hex()}")
        random_delay = random.uniform(15, 17)
        rounded_delay = round(random_delay)
        print(f"Ожидаю {rounded_delay} сек. перед следующей транзакцией")
        time.sleep(rounded_delay)
    else:
        print(f"Транзакция BOOST от аккаунта {account.address} завершилась с ошибкой. Hash: {tx_hash_boost.hex()}")


    # Минт  НФТ
    account = Account.from_key(private_key)
    nonce = w3.eth.get_transaction_count(account.address)
    
    # Выбор случайного адреса контракта из списка
    mint_addresses = random.choice(mint_addresses)
    
   

    quantity_to_mint = random.randint(1, 3)  # Замените это на нужное количество НФТ для минта
    tx = mint_contract.functions.publicMint(quantity_to_mint).build_transaction({
        'chainId': 81457,  
        'gas': get_random_gas_limit(2000000, 3000000), 
        'gasPrice': w3.eth.gas_price, 
        'nonce': nonce, 
    })
    
   
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    
    
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Аккаунт {account.address} успешно сминтил. Hash: {tx_hash.hex()}")
    
    successful_accounts.append(account.address)

    # Пауза на случайное количество секунд
    random_delay = random.uniform(1250, 2500)
    rounded_delay = round(random_delay)
    print(f"Ожидаю {rounded_delay} сек. перед следующей транзакцией")
    time.sleep(rounded_delay)


# Запись успешно выполненных кошельков в файл
with open('successful.txt', 'w') as file:
    for account_address in successful_accounts:
        file.write(f"{account_address}\n")