# (0) Configuracion Corecta red de prueba local Ganache con el nodo Ethereum(simulado)
from web3 import Web3
from web3.exceptions import TransactionNotFound
from web3.middleware import geth_poa_middleware

# (A) Configura la conexión con el nodo Ethereum
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))  # Ajusta esto a tu proveedor de Web3

# (B) Asegúrate de que estás conectado a la blockchain
assert w3.isConnected()

# (C) La dirección del contrato desplegado y su ABI
contract_address = '0x735f1f6da2b18c62182cd2d73f641C8dEFA334B9'
contract_abi = []  # Reemplaza esto con el ABI de tu contrato

# (D) Crea una instancia del contrato
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# (1) Función alta_prestamista, agrega un nuevo prestamista
def alta_prestamista(nuevo_prestamista_address):
    # (A) La dirección del socio principal que invoca la función (debe ser remplazado por tu dirección)
    socio_principal_address = '0xTuDireccion'

    # (B) Asegúrate de desbloquear la cuenta si es necesario
    # (a) w3.geth.personal.unlockAccount(socio_principal_address, 'password', 1500)

    # (b) Prepara la transacción
    tx = contract.functions.altaPrestamista(nuevo_prestamista_address).buildTransaction({
        'from': socio_principal_address,
        'nonce': w3.eth.getTransactionCount(socio_principal_address),
        'gas': 2000000,  # Ajusta el gas según sea necesario
        'gasPrice': w3.toWei('50', 'gwei')
    })

    # (c) Firmar la transacción con private key
    signed_tx = w3.eth.account.signTransaction(tx, private_key='0xTuClavePrivada')

    # (d) Enviar la transacción
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

    # (e) Esperar la confirmación de la transacción
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    if tx_receipt.status == 1:
        return "El prestamista fue agregado exitosamente."
    else:
        return "Hubo un problema al agregar el prestamista."

# (f) Ejemplo de cómo llamar a la función
print(alta_prestamista('0xDirecciónNuevoPrestamista'))
   
   # (2) Funcion alta_cliente
def alta_cliente(nuevo_cliente_address, prestamista_address, prestamista_private_key):
    try:
        # (A) Verificar si el cliente ya está registrado
        if contract.functions.clientes(nuevo_cliente_address).call():
            return "Error: El cliente ya está registrado."

        # (a) Preparar la transacción
        tx = contract.functions.altaCliente(nuevo_cliente_address).buildTransaction({
            'from': prestamista_address,
            'nonce': w3.eth.getTransactionCount(prestamista_address),
            'gas': 2000000,  # (c) Ajusta el gas según sea necesario
            'gasPrice': w3.toWei('50', 'gwei')
        })

        # (B) Firmar la transacción con private key
        signed_tx = w3.eth.account.signTransaction(tx, private_key=prestamista_private_key)

        # (a) Enviar la transacción
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

        # (b) Esperar la confirmación de la transacción
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

    # (C) Ejemplo de cómo llamar a la función
print(alta_cliente('0xDirecciónNuevoCliente', '0xDirecciónPrestamista', '0xClavePrivadaPrestamista'))
 
    # (3) Funcion depositar_garantia
def depositar_garantia(direccion_cliente, valor_garantia, clave_privada_cliente, contrato, prestamo_solicitado):
    try:
       # (A) Funcion depositar_garantia 
        if valor_garantia < prestamo_solicitado:
            return "Error: La garantía depositada no es suficiente para el préstamo solicitado."

        # (B) Preparar la transacción para depositar garantía
        tx = contrato.functions.depositarGarantia().buildTransaction({
            'from': direccion_cliente,
            'value': valor_garantia,
            'nonce': w3.eth.getTransactionCount(direccion_cliente),
            'gas': 2000000,  # (a) Ajustar según sea necesario
            'gasPrice': w3.toWei('50', 'gwei')  #(b) Ajustar según sea necesario
        })

        # (C) Firmar la transacción con la clave privada del cliente
        signed_tx = w3.eth.account.signTransaction(tx, private_key=clave_privada_cliente)

        # (D) Enviar la transacción a la blockchain
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

        # (a) Esperar la confirmación de la transacción
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

        # (b) Verificar el estado de la transacción
        if tx_receipt.status == 1:
            # (c) Verificar si la garantía depositada es suficiente para el préstamo solicitado
            if tiene_suficiente_garantia(valor_garantia, prestamo_solicitado):
                return "La garantía ha sido depositada exitosamente."
            else:
                return "Error: La garantía depositada no es suficiente para el préstamo solicitado."
        else:
            return "Error: La transacción falló."

    except ValueError as e:
        return f"Error: {e}"
    except TransactionNotFound:
        return "Error: No se encontró la transacción."
    except Exception as e:
        return f"Error desconocido: {e}"
    
     # (3_1) Funcion axiliar
def tiene_suficiente_garantia(garantia_actual, prestamo_solicitado):
    # (A) Verificar si la garantía actual es suficiente para el préstamo solicitado
    return garantia_actual >= prestamo_solicitado

    # (4) Funcion solicitar_prestamo
def solicitar_prestamo(direccion_cliente, monto, plazo, clave_privada_cliente):
    try:
        # (A) Verificar si el cliente tiene suficiente garantía
        if not tiene_suficiente_garantia(direccion_cliente, monto):
            return "Error: No hay suficiente garantía para solicitar el préstamo."

        # (a) Preparar la transacción para solicitar préstamo
        tx = contract.functions.solicitarPrestamo(monto, plazo).buildTransaction({
            'from': direccion_cliente,
            'nonce': w3.eth.getTransactionCount(direccion_cliente),
            'gas': 2000000,  # (b) Ajustar según sea necesario
            'gasPrice': w3.toWei('50', 'gwei')  # Ajustar según sea necesario
        })

        # (B) Firmar la transacción con la clave privada del cliente
        signed_tx = w3.eth.account.signTransaction(tx, private_key=clave_privada_cliente)

        # (C) Enviar la transacción a la blockchain
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

        # (a) Esperar la confirmación de la transacción
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

        # (b) Verificar el estado de la transacción
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

    # (5) Funcion aprobar_prestamo
def aprobar_prestamo(prestatario_address, prestamo_id, prestamista_address, prestamista_private_key):
    try:
        # (A) Comprobar la validez del préstamo y del prestatario
        if not es_valido_prestamo(prestatario_address, prestamo_id):
            return "Error: El préstamo no es válido o el prestatario no existe."

        # (B) Preparar la transacción para aprobar el préstamo
        tx = contract.functions.aprobarPrestamo(prestatario_address, prestamo_id).buildTransaction({
            'from': prestamista_address,
            'nonce': w3.eth.getTransactionCount(prestamista_address),
            'gas': 2000000,  # (a) Ajustar según sea necesario
            'gasPrice': w3.toWei('50', 'gwei')  # (b) Ajustar según sea necesario
        })

        # (C) Firmar la transacción con la clave privada del prestamista
        signed_tx = w3.eth.account.signTransaction(tx, private_key=prestamista_private_key)

        # (a) Enviar la transacción a la blockchain
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

        # (b) Esperar la confirmación de la transacción
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

        # (D) Verificar el estado de la transacción
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

# (5_1) Función auxiliar para verificar la validez del préstamo y del prestatario
def es_valido_prestamo(prestatario_address, prestamo_id):
    # (a) Implementa la lógica para verificar la validez del préstamo y del prestatario
    return True  # Por ahora, retornamos True como ejemplo

    # (6) Funcion reembolsar_prestamo
def reembolsar_prestamo(prestamo_id, cliente_address, cliente_private_key, contrato):
    try:
        #  (A) Verificar la validez del préstamo y si el cliente es el prestatario
        if not es_valido_prestamo(prestamo_id, cliente_address, contrato):

        # (B) Preparar la transacción para reembolsar el préstamo
         tx = contract.functions.reembolsarPrestamo(prestamo_id).buildTransaction({
            'from': cliente_address,
            'nonce': w3.eth.getTransactionCount(cliente_address),
            'gas': 2000000,  # Ajustar según sea necesario
            'gasPrice': w3.toWei('50', 'gwei')  # Ajustar según sea necesario
        })

        # (C) Firmar la transacción con la clave privada del cliente
        signed_tx = w3.eth.account.signTransaction(tx, private_key=cliente_private_key)

        # (a) Enviar la transacción a la blockchain
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

        # (b) Esperar la confirmación de la transacción
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

        # (c) Verificar el estado de la transacción
        if tx_receipt.status == 1:
            return "El préstamo ha sido reembolsado exitosamente."
        else:
            return "Error: La transacción falló al reembolsar el préstamo."

    except ValueError as e:
        return f"Error: {e}"
    except TransactionNotFound:
        return "Error: No se encontró la transacción."
    except Exception as e:
        return f"Error desconocido: {e}"


     # (7) Funcion liquidar_garantia
def liquidar_garantia(prestamo_id, prestamista_address, prestamista_private_key):
    try:
        # (A) Verificar si el préstamo está aprobado y no reembolsado y si ha vencido el plazo
        estado_prestamo = contrato.functions.obtenerEstadoPrestamo(prestamo_id).call()
        if estado_prestamo != 2:
            raise Exception("El préstamo no está aprobado y/o reembolsado.")
        if not contrato.functions.haVencidoPlazo(prestamo_id).call():
            raise Exception("El plazo del préstamo no ha vencido.")

        # (B) Verificar si el préstamo es válido
        if not es_valido_prestamo(prestamista_address, prestamo_id):
            raise Exception("El préstamo no es válido para el prestamista.")

    except Exception as e:
        return str(e)

    # (C) Construir transacción
    transaccion = contrato.functions.liquidarGarantia(prestamo_id).buildTransaction({
        'chainId': w3.eth.chain_id,
        'gas': 2000000,
        'gasPrice': w3.toWei('50', 'gwei'),
        'nonce': w3.eth.getTransactionCount(prestamista_address),
    })

    # (D) Preparar y firmar la transacción
    transaccion_firmada = w3.eth.account.signTransaction(transaccion, prestamista_private_key)

    try:
        # (E) Enviar la transacción a la blockchain
        tx_hash = w3.eth.sendRawTransaction(transaccion_firmada.rawTransaction)
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

        if tx_receipt.status == 1:
            return "La garantía ha sido liquidada exitosamente."
        else:
            return "La transacción ha fallado al liquidar la garantía."
    except Exception as e:
        return "Error al enviar la transacción: " + str(e)

        # (8) Funcion obtener_prestamos_por_prestatario
def obtener_prestamos_por_prestatario(prestatario_address):
     # (A) Preparar la transacion
    try:
        # (a) Realizar una llamada al contrato para obtener la lista de IDs de préstamos del prestatario
        prestamos = contract.functions.obtenerPrestamosPorPrestatario(prestatario_address).call()
        return prestamos
    except ValueError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Error desconocido: {e}"

    # (9) Funcion obtener_detalle_de_prestamo
def obtener_detalle_de_prestamo(prestatario_address, prestamo_id):
    try:
        # Realizar una llamada al contrato para obtener los detalles del préstamo
        detalle_prestamo = contract.functions.obtenerDetalleDePrestamo(prestatario_address, prestamo_id).call()
        return detalle_prestamo
    except ValueError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Error desconocido: {e}"
