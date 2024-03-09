// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ContratoPrestamoDefi {
    address public socioPrincipal;
    mapping(uint256 => Prestamo) public prestamos;
    mapping(address => cliente) public clientes;
    mapping(address => bool) public empleadosPrestamistas;

    struct Prestamo {
        uint256 IdPrestamo;
        address prestatario;
        uint256 CantidadPrestamo;
        uint256 PlazoReembolso;
        uint256 MarcaTiempoinSolisitud;
        uint256 TiempoLimiteReembolso;
        bool PrestamoAprobado;
        bool PrestamoReembolsado;
        bool GarantiaLiquidada;      
    }
      
    struct cliente {
        bool activado;
        uint256 saldoGarantia;
    }

    // Eventos
    event SolicitudPrestamo(address indexed prestatario, uint256 monto);
    event PrestamoAprobado(address indexed prestatario, uint256 monto);
    event PrestamoReembolsado(address indexed prestatario, uint256 monto);
    event GarantiaLiquidada(address indexed prestatario, uint256 monto);
     
    // Modificadores 
    modifier soloSocioPrincipal() {
        require(msg.sender == socioPrincipal, "ERROR: No tienes permisos para operar");
        _;
    }
        
    modifier soloEmpleadoPrestamista() {
        require(empleadosPrestamistas[msg.sender], "ERROR: No tienes permisos para operar");
        _;
    }

    modifier soloClienteRegistrado() {
        require(clientes[msg.sender].activado, "ERROR: No eres cliente");
        _;
    }

    constructor() {
        socioPrincipal = msg.sender;
        empleadosPrestamistas[socioPrincipal] = true; // Asumiendo que el socio principal también es un empleado prestamista
    }

    // Ejemplo de función corregida
    function altaPrestamista(address _Prestamista) public soloSocioPrincipal {
        // Implementación de la lógica para agregar un prestamista
        empleadosPrestamistas[_Prestamista] = true;
    }

    // Otros métodos necesitarán ser definidos correctamente siguiendo el patrón del ejemplo

}
