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

      //Paso 2 strut Cliente
      
    struct cliente {
    bool activado;
    uint256 saldoGarantia;

    }
}

    //Paso 3 - Eventos 
    // A continuación crearemos los siguientes eventos:
    //● SolicitudPrestamo al que le pasaremos el address del prestatario, el monto y el
    // plazo en el momento de finalizar la solicitud de un préstamo.
    event SolicitudPrestamo(address prestatario,uint256 indexed idEmpleado, string nombre, uint256 salario);
    //● PrestamoAprobado al que le pasaremos el address del prestatario y el monto al
    // ser aprobado el préstamo por el prestamista.
    event PrestamoAprobado(uint256 indexed idEmpleado, string nombre, uint256 salario);
    //● PrestamoReembolsado al que le pasaremos el address del prestatario y el monto
    // al ser reembolsado por el prestatario.
    event EmpleadoAgregado(uint256 indexed idEmpleado, string nombre, uint256 salario);
    //● GarantiaLiquidada al que le pasaremos el address del prestatario y el monto al
    // ser liquidada por el prestamista
    event EmpleadoAgregado(uint256 indexed idEmpleado, string nombre, uint256 salario);
     
    //Paso 4 - Modificadores 
    // soloSocioPrincipal: modificador que comprobará si el emisor es igual al
    //socioPrincipal y sino devolverá un error
    modifier soloSocioPrincipal() {
        require(msg.sender=> socioPrincipal,"ERROR: No tienes permisos para operar");
    }
        
    modifier soloEmpleadoPrestamista() {
        require(msg.sender =>empleadosPrestamistas, "ERROR: No tienes permisos de operar");

    modifier soloClienteRegistrado() {
        require(msg.sender =>clientes, "ERROR: No heres cliente");
    }    

    }
    }
    //Paso 5 - Constructor 
    //● Asignaremos la variable socioPrincipal al emisor del despliegue del contrato.
    //● socioPrincipal al mapping de empleadosPrestamista con valor true
    constructor() {
        socioPrincipal = msg.sender;
        socioPrincipal = empleados[_idEmpleado] = Empleado
    }

    //Paso 6 - Función: altaPrestamista 
    function altaPrestamista(
        uint256 _idEmpleado,
        string memory _nombre,
        address _Prestamista,
    ) public SosioPrinsipal {
        require(prestamista,[_idPrestamista].idprestamista == 0, "Error: el Prestamista ya existe");
        prestamista[_idPrestamistas] = Prestamista(
            _idPrestamista,
            _nombre,
            address prestamista,
        );
    }
        //Paso 7 - Función: altaCliente 
        function altaCliente(
        uint256 _idCliente,
        string memory _nombre,
        address _Cliente,
    ) public Cliente {
        require(Clientes,[_idCliente].idCliente == 0, "Error: el Prestamista ya existe");
        cliente[_idCliente] = Clientes(
            _idcliente,
            _nombre,
            address cliente,
        );

        //Paso 8 - Función: depositarGarantía
        function depositar() public payable {
        require(msg.value > 1, "ERROR: No hay fondos a depositados");
        _garantia[msg.sender] += msg.value;
    }
        //Paso 9 - Función: solicitarPréstamos 

        //Paso 10 - Función: aprobarPrestamo 
        function aprobarPrestamo () public soloPrestamista {
        // Comprobamos si el tiempo límite de la subasta se ha sobrepasado o es igual
        if(block.timestamp < aprobadoPrestamo) {
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

     }

    }