  <h1>Comparador de Precios</h1>

    <p>Esta aplicación permite comparar precios de productos de diferentes proveedores y exportar los resultados en formatos Excel y TXT.</p>

    <h2>Instalación</h2>
    <p>Para ejecutar esta aplicación, es necesario instalar los siguientes paquetes de Python:</p>
    <pre>
        pip install tkinter pandas numpy
    </pre>

    <h2>Uso</h2>
    <h3>Paso 1: Cargar Simulador de Compras</h3>
    <p>Haga clic en el botón <strong>Simulador De Compras</strong> para cargar un archivo CSV que contenga los datos del simulador de compras.</p>

    <h3>Paso 2: Exportar TXT</h3>
    <p>Haga clic en el botón <strong>Exportar TXT</strong> para exportar los datos cargados en un archivo de texto.</p>

    <h3>Paso 3: Cargar Proveedor</h3>
    <p>Haga clic en el botón <strong>Cargar Proveedor</strong> para cargar un archivo XLSX con los precios de un proveedor específico.</p>

    <h3>Paso 4: Cargar Quantio Cloud</h3>
    <p>Haga clic en el botón <strong>Cargar Quantio Cloud</strong> para cargar un archivo Excel con los datos de Quantio Cloud.</p>

    <h3>Paso 5: Cargar Cofarsur</h3>
    <p>Haga clic en el botón <strong>Cargar Cofarsur</strong> para cargar un archivo CSV con los datos de Cofarsur. Puede seleccionar un descuento aplicable en el menú desplegable antes de cargar el archivo.</p>

    <h3>Paso 6: Exportar Pedido</h3>
    <p>Haga clic en el botón <strong>Exportar Pedido</strong> para exportar los resultados de la comparación a un archivo Excel.</p>

    <h2>Descripción del Código</h2>
    <h3>Funciones Principales</h3>
    <h4>encontrar_mejor_precio_y_origen(fila)</h4>
    <p>Esta función encuentra el mejor precio y el origen del mismo en una fila de datos que contiene precios de diferentes proveedores.</p>

    <h4>encontrar_mejor_precio_y_origen_sinProveedor(fila)</h4>
    <p>Similar a la función anterior, pero no considera los precios del proveedor principal.</p>

    <h3>Clase Aplicacion</h3>
    <p>La clase <code>Aplicacion</code> gestiona la interfaz gráfica y las operaciones principales de la aplicación.</p>

    <h4>__init__(self, root)</h4>
    <p>Inicializa la interfaz gráfica y las variables de la aplicación.</p>

    <h4>mostrar_descripcion(self, texto) y ocultar_descripcion(self)</h4>
    <p>Gestionan la visualización de descripciones en la interfaz al pasar el cursor sobre los botones.</p>

    <h4>cargar_archivo(self)</h4>
    <p>Carga el archivo CSV seleccionado por el usuario.</p>

    <h4>reordenar_y_renombrar(self)</h4>
    <p>Reordena y renombra las columnas del DataFrame cargado.</p>

    <h4>realizar_muestreo(self)</h4>
    <p>Muestra una vista previa de los datos cargados.</p>

    <h4>cargar_proveedor(self)</h4>
    <p>Carga un archivo XLSX con los datos del proveedor.</p>

    <h4>cargar_comparativa(self)</h4>
    <p>Carga un archivo Excel con los datos de Quantio Cloud.</p>

    <h4>cargar_cofar(self)</h4>
    <p>Carga un archivo CSV con los datos de Cofarsur y aplica el descuento seleccionado.</p>

    <h4>exportar_a_xlsx(self)</h4>
    <p>Exporta los datos combinados a un archivo Excel.</p>

    <h4>exportar_a_txt(self)</h4>
    <p>Exporta los datos a un archivo de texto con formato específico.</p>

    <h4>realizar_todas_acciones(self)</h4>
    <p>Realiza la carga, reordenamiento, renombramiento y muestra una vista previa de los datos.</p>

    <h2>Autores</h2>
    <p>Desarrollado por [Tu Nombre].</p>

    <h2>Licencia</h2>
    <p>Este proyecto está bajo la Licencia MIT. Consulte el archivo LICENSE para obtener más detalles.</p>
