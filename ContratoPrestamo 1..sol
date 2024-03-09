// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;


//Paso 1 - Base. Crear contract PrestamoDeFi 
contract ContratoPrestamoDefi {
    address public SosioPrinsipal;

//Paso 2 - Variables de Estado/Globales 
    struct Prestamo {
        uint256 IdPrestamo;
        address prestatatario;
        uint256 CantidadPrestamo;
        uint256 PlazoReembolso;
        uint256 MarcaTiempoinSolisitud;
        uint256 TiempoLimiteReembolso;
        bool PrestamoAprobado;
        bool PrestamoReembolsado;
        bool GarantiaLiquidada;      
    }

    Cliente
 activado: Indica si el cliente está registrado y activo en el sistema.
 saldoGarantia: Saldo total de garantías depositadas por el cliente.
 prestamos: Mapeo de ID de préstamo a la estructura Prestamo.
 prestamoIds: Lista de ID de préstamos asociados al cliente.
    struct cliente {
    bool activado = folse;
    uint256 saldoGarantia;

    }
    
    mapping (uint256 => Prestamo) public prestamos;


}


//Paso 3 - Eventos 

//Paso 4 - Modificadores 

//Paso 5 - Constructor 

//Paso 6 - Función: altaPrestamista 
function altaPrestamista(
        uint256 _idEmpleado,
        string memory _nombre,
        address _Prestamista,
    ) public SosioPrinsipal {
        require(prestamista,[_idPrestamista].idprestamista == 0, "Error: el Prestamista ya existe");
        prestamista[_idPrestamistas] = Prestamista(
            _idEmpleado,
            _nombre,
            address prestamista,
        );
    }
//Paso 7 - Función: altaCliente 

//Paso 8 - Función: depositarGarantía

//Paso 9 - Función: solicitarPréstamos 

//Paso 10 - Función: aprobarPrestamo 
function aprobarPrestamo () public soloAdministrador {
        // Comprobamos si el tiempo límite de la subasta se ha sobrepasado o es igual
        if(block.timestamp < finSubasta) {
            // error
            revert SubastaNoFinalizadaTodavia();
        }
//Paso 11 - Función: reembolsarPrestamo 
function reembolsarPrestamo()
        public payable 
        soloPrestatario
//Paso 12 - Función: liquidarGarantia 

//Paso 13 - Función: obtenerPrestamosPorPrestatario 

//Paso 14 - Función: obtenerDetalleDePrestamo