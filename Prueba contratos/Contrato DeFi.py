import json
from web3 import Web3
from web3.exceptions import TransactionNotFound

# Conexión a Ganache
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Conecta a ganache
if not web3.is_connected():
    print("Error: No se pudo conectar a la red Ethereum.")
    exit()
else:
    print("Conexion realizada")


# La dirección del contrato desplegado y su ABI
contract_address = '0xTuContratoDireccion'
contract_abi = []  # Reemplaza esto con el ABI de tu contrato

# Crea una instancia del contrato
contract = w3.eth.contract(address=contract_address, abi=contract_abi)
# La función para agregar un nuevo prestamista
def alta_prestamista(nuevo_prestamista_address):
    # La dirección del socio principal que invoca la función (debe ser remplazado por tu dirección)
    socio_principal_address = '0xTuDireccion'

    try:
        # Prepara la transacción
        tx = contract.functions.altaPrestamista(nuevo_prestamista_address).buildTransaction({
            'from': socio_principal_address,
            'nonce': w3.eth.getTransactionCount(socio_principal_address),
            'gas': 2000000,  # Ajusta el gas según sea necesario
            'gasPrice': w3.toWei('50', 'gwei')
        })

        # Firmar la transacción
        signed_tx = w3.eth.account.signTransaction(tx, private_key='0xTuClavePrivada')

        # Enviar la transacción
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

        # Esperar la confirmación de la transacción
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

        if tx_receipt.status == 1:
            return "El prestamista fue agregado exitosamente."
        else:
            return "Hubo un problema al agregar el prestamista."

    except ValueError as e:
        return f"Error: {e}"
    except TransactionNotFound:
        return "Error: No se encontró la transacción."
    except Exception as e:
        return f"Error desconocido: {e}"

# Ejemplo de cómo llamar a la función
print(alta_prestamista('0xDirecciónNuevoPrestamista'))
# La función para registrar un nuevo cliente
def alta_cliente(nuevo_cliente_address, prestamista_address, prestamista_private_key):
    try:
        # Verificar si el cliente ya está registrado
        if contract.functions.clientes(nuevo_cliente_address).call():
            return "Error: El cliente ya está registrado."

        # Preparar la transacción
        tx = contract.functions.altaCliente(nuevo_cliente_address).buildTransaction({
            'from': prestamista_address,
            'nonce': w3.eth.getTransactionCount(prestamista_address),
            'gas': 2000000,  # Ajusta el gas según sea necesario
            'gasPrice': w3.toWei('50', 'gwei')
        })

        # Firmar la transacción
        signed_tx = w3.eth.account.signTransaction(tx, private_key=prestamista_private_key)

        # Enviar la transacción
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

        # Esperar la confirmación de la transacción
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

        if tx_receipt.status == 1:
            return "El cliente ha sido registrado con éxito."
        else:
            return "Error: La transacción falló."

    except ValueError as e:
        return f"Error: {e}"
    except TransactionNotFound:
        return "Error: No se encontró la transacción."
    except Exception as e:
        return f"Error desconocido: {e}"

# Ejemplo de cómo llamar a la función
print(alta_cliente('0xDirecciónNuevoCliente', '0xDirecciónPrestamista', '0xClavePrivadaPrestamista'))

def depositar_garantia(direccion_cliente, valor, clave_privada_cliente):
    try:
        # Preparar la transacción para depositar garantía
        tx = contract.functions.depositarGarantia().buildTransaction({
            'from': direccion_cliente,
            'value': valor,
            'nonce': w3.eth.getTransactionCount(direccion_cliente),
            'gas': 2000000,  # Ajustar según sea necesario
            'gasPrice': w3.toWei('50', 'gwei')  # Ajustar según sea necesario
        })

        # Firmar la transacción con la clave privada del cliente
        signed_tx = w3.eth.account.signTransaction(tx, private_key=clave_privada_cliente)

        # Enviar la transacción a la blockchain
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

        # Esperar la confirmación de la transacción
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

        # Verificar el estado de la transacción
        if tx_receipt.status == 1:
            return "La garantía ha sido depositada exitosamente."
        else:
            return "Error: La transacción falló."

    except ValueError as e:
        return f"Error: {e}"
    except TransactionNotFound:
        return "Error: No se encontró la transacción."
    except Exception as e:
        return f"Error desconocido: {e}"

def solicitar_prestamo(direccion_cliente, monto, plazo, clave_privada_cliente):
    try:
        # Verificar si el cliente tiene suficiente garantía
        if not tiene_suficiente_garantia(direccion_cliente, monto):
            return "Error: No hay suficiente garantía para solicitar el préstamo."

        # Preparar la transacción para solicitar préstamo
        tx = contract.functions.solicitarPrestamo(monto, plazo).buildTransaction({
            'from': direccion_cliente,
            'nonce': w3.eth.getTransactionCount(direccion_cliente),
            'gas': 2000000,  # Ajustar según sea necesario
            'gasPrice': w3.toWei('50', 'gwei')  # Ajustar según sea necesario
        })

        # Firmar la transacción con la clave privada del cliente
        signed_tx = w3.eth.account.signTransaction(tx, private_key=clave_privada_cliente)

        # Enviar la transacción a la blockchain
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

        # Esperar la confirmación de la transacción
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

        # Verificar el estado de la transacción
        if tx_receipt.status == 1:
            return f"La solicitud de préstamo fue exitosa. ID del préstamo: {tx_receipt.transactionHash.hex()}"
        else:
            return "Error: La transacción falló."

    except ValueError as e:
        return f"Error: {e}"
    except TransactionNotFound:
        return "Error: No se encontró la transacción."
    except Exception as e:
        return f"Error desconocido: {e}"

# Función auxiliar para verificar si el cliente tiene suficiente garantía
def tiene_suficiente_garantia(direccion_cliente, monto):
    # Implementa la lógica para verificar si el cliente tiene suficiente garantía
    return True  # Por ahora, retornamos True como ejemplo


def solicitar_prestamo(direccion_cliente, monto, plazo, clave_privada_cliente):
    try:
        # Verificar si el cliente tiene suficiente garantía
        if not tiene_suficiente_garantia(direccion_cliente, monto):
            return "Error: No hay suficiente garantía para solicitar el préstamo."

        # Preparar la transacción para solicitar préstamo
        tx = contract.functions.solicitarPrestamo(monto, plazo).buildTransaction({
            'from': direccion_cliente,
            'nonce': w3.eth.getTransactionCount(direccion_cliente),
            'gas': 2000000,  # Ajustar según sea necesario
            'gasPrice': w3.toWei('50', 'gwei')  # Ajustar según sea necesario
        })

        # Firmar la transacción con la clave privada del cliente
        signed_tx = w3.eth.account.signTransaction(tx, private_key=clave_privada_cliente)

        # Enviar la transacción a la blockchain
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

        # Esperar la confirmación de la transacción
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

        # Verificar el estado de la transacción
        if tx_receipt.status == 1:
            return f"La solicitud de préstamo fue exitosa. ID del préstamo: {tx_receipt.transactionHash.hex()}"
        else:
            return "Error: La transacción falló."

    except ValueError as e:
        return f"Error: {e}"
    except TransactionNotFound:
        return "Error: No se encontró la transacción."
    except Exception as e:
        return f"Error desconocido: {e}"

# Función auxiliar para verificar si el cliente tiene suficiente garantía
def tiene_suficiente_garantia(direccion_cliente, monto):
    # Implementa la lógica para verificar si el cliente tiene suficiente garantía
    return True  # Por ahora, retornamos True como ejemplo

def aprobar_prestamo(prestatario_address, prestamo_id, prestamista_address, prestamista_private_key):
    try:
        # Comprobar la validez del préstamo y del prestatario
        if not es_valido_prestamo(prestatario_address, prestamo_id):
            return "Error: El préstamo no es válido o el prestatario no existe."

        # Preparar la transacción para aprobar el préstamo
        tx = contract.functions.aprobarPrestamo(prestatario_address, prestamo_id).buildTransaction({
            'from': prestamista_address,
            'nonce': w3.eth.getTransactionCount(prestamista_address),
            'gas': 2000000,  # Ajustar según sea necesario
            'gasPrice': w3.toWei('50', 'gwei')  # Ajustar según sea necesario
        })

        # Firmar la transacción con la clave privada del prestamista
        signed_tx = w3.eth.account.signTransaction(tx, private_key=prestamista_private_key)

        # Enviar la transacción a la blockchain
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

        # Esperar la confirmación de la transacción
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

        # Verificar el estado de la transacción
        if tx_receipt.status == 1:
            return "El préstamo ha sido aprobado exitosamente."
        else:
            return "Error: La transacción falló."

    except ValueError as e:
        return f"Error: {e}"
    except TransactionNotFound:
        return "Error: No se encontró la transacción."
    except Exception as e:
        return f"Error desconocido: {e}"

# Función auxiliar para verificar la validez del préstamo y del prestatario
def es_valido_prestamo(prestatario_address, prestamo_id):
    # Implementa la lógica para verificar la validez del préstamo y del prestatario
    return True  # Por ahora, retornamos True como ejemplo
