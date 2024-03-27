import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.ttk import Combobox
import pandas as pd
import numpy as np

def encontrar_mejor_precio_y_origen(fila):

    precios = fila[['PreciosProveedor', 'DDS', 'MASA', 'SUIZO', 'COFARSUR']]
    # Convertir todas las entradas a valores numéricos
    precios_numericos = pd.to_numeric(precios, errors='coerce')
    # Filtrar los valores que son 0 o NaN
    precios_filtrados = precios_numericos.replace({0: np.nan})
    # Encontrar el mínimo precio
    mejor_precio = precios_filtrados.min()
    # Encontrar el nombre de la columna con el mínimo precio
    origen_mejor_precio = precios_filtrados.idxmin()
    if pd.isna(origen_mejor_precio):  # Manejar el caso donde no se encuentra ningún precio válido
        mejor_origen = 'Ninguno'
    else:
        mejor_origen = origen_mejor_precio.split('_')[0]
    return pd.Series({'Mejor_Precio': mejor_precio, 'Mejor_Origen': mejor_origen})


def encontrar_mejor_precio_y_origen_sinProveedor(fila):

    precios = fila[['DDS', 'MASA', 'SUIZO', 'COFARSUR']]
    # Convertir todas las entradas a valores numéricos
    precios_numericos = pd.to_numeric(precios, errors='coerce')
    # Filtrar los valores que son 0 o NaN
    precios_filtrados = precios_numericos.replace({0: np.nan})
    # Encontrar el mínimo precio
    mejor_precio = precios_filtrados.min()
    # Encontrar el nombre de la columna con el mínimo precio
    origen_mejor_precio = precios_filtrados.idxmin()
    if pd.isna(origen_mejor_precio):  # Manejar el caso donde no se encuentra ningún precio válido
        mejor_origen = 'Ninguno'
    else:
        mejor_origen = origen_mejor_precio.split('_')[0]
    return pd.Series({'Mejor_Precio': mejor_precio, 'Mejor_Origen': mejor_origen})

class Aplicacion:
    def __init__(self, root):
        # Variables para almacenar los DataFrames
        self.base_de_datos_df = None
        self.base_de_datos_TXT = None
        self.proveedor_df = None
        self.masivas_df = None
        self.exportacion_df = None
        self.cofar_df = None
        
        self.root = root
        self.root.geometry("750x450")  # Anchura x Altura
        self.root.title("COMPARADOR")
        self.root.config(bg="black")

        # Título
        self.titulo_label = tk.Label(root, text="COMPARADOR", bg="black", fg="white", font=("Arial", 20, "bold"))
        self.titulo_label.pack(pady=10)

        # Frame para los botones de carga de archivos
        frame_carga = tk.Frame(root, bg="black")
        frame_carga.pack(pady=10)

        # Botón para cargar CSV
        self.btn_cargar_csv = tk.Button(frame_carga, text="Simulador De Compras", command=self.realizar_todas_acciones, bg="grey", fg="white", font=("Arial", 10, "bold"))
        self.btn_cargar_csv.pack(side="left", padx=10, pady=5)
        self.btn_cargar_csv.bind("<Enter>", lambda event: self.mostrar_descripcion("Cargar Simulador de Integra en formato .CSV\nObligatorio"))
        self.btn_cargar_csv.bind("<Leave>", lambda event: self.ocultar_descripcion())

        # Botón para exportar a TXT
        self.btn_exportar_txt = tk.Button(frame_carga, text="Exportar TXT", command=self.exportar_a_txt, bg="grey", fg="white", font=("Arial", 10, "bold"))
        self.btn_exportar_txt.pack(side="left", padx=10, pady=5)
        self.btn_exportar_txt.bind("<Enter>", lambda event: self.mostrar_descripcion("archivo para cargar en Quantio Cloud formato .Txt"))
        self.btn_exportar_txt.bind("<Leave>", lambda event: self.ocultar_descripcion())

        # Separador
        separator = ttk.Separator(root, orient='horizontal')
        separator.pack(fill='x', padx=10, pady=5)

        # Frame para los botones de carga de proveedor y Quantio Cloud
        frame_carga2 = tk.Frame(root, bg="black")
        frame_carga2.pack(pady=10)

        # Botón para cargar proveedor
        self.btn_cargar_proveedor = tk.Button(frame_carga2, text="Cargar Proveedor", command=self.cargar_proveedor, bg="grey", fg="white", font=("Arial", 10, "bold"))
        self.btn_cargar_proveedor.pack(side="left", padx=10, pady=5)
        self.btn_cargar_proveedor.bind("<Leave>", lambda event: self.ocultar_descripcion())

        self.btn_cargar_proveedor.bind("<Enter>", lambda event: self.mostrar_descripcion("Ingresar Archivo de proveedor sin titulos solo Codebar en las columnas 1 y Precio en la 2 formato .Txt\n Opcional"))
        # Botón para cargar Quantio Cloud
        self.btn_cargar_quantio = tk.Button(frame_carga2, text="Cargar Quantio Cloud", command=self.cargar_comparativa, bg="grey", fg="white", font=("Arial", 10, "bold"))
        self.btn_cargar_quantio.pack(side="left", padx=10, pady=5)
        self.btn_cargar_quantio.bind("<Leave>", lambda event: self.ocultar_descripcion())
        self.btn_cargar_quantio.bind("<Enter>", lambda event: self.mostrar_descripcion("Cargar Quantio Cloud en formato .Xlsx\n Obligatorio"))

        # Entrada para el descuento
        self.combo_descuento = Combobox(frame_carga2, values=["10%", "20%", "30%"])  # Puedes ajustar los valores según tus necesidades
        self.combo_descuento.pack(side="left", padx=5, pady=5)
        self.combo_descuento.current(0)  # Selecciona el primer valor por defecto



        # Botón para cargar Cofarsur
        self.btn_cargar_cofarsur = tk.Button(frame_carga2, text="Cofarsur", command=self.cargar_cofar, bg="grey", fg="white", font=("Arial", 10, "bold"))
        self.btn_cargar_cofarsur.pack(side="left", padx=10, pady=5)
        self.btn_cargar_cofarsur.bind("<Leave>", lambda event: self.ocultar_descripcion())
        self.btn_cargar_cofarsur.bind("<Enter>", lambda event: self.mostrar_descripcion("Ingresar Archivo Cofarsur en formato .CSV\n Opcional si no lo cargamos desde el cloud"))

        # Separador
        separator2 = ttk.Separator(root, orient='horizontal')
        separator2.pack(fill='x', padx=10, pady=5)

        # Frame para el botón de carga de Cofarsur
        frame_exportar_pedido = tk.Frame(root, bg="black")
        frame_exportar_pedido.pack(pady=10)

        # Botón para exportar el pedido
        self.btn_exportar_pedido = tk.Button(frame_exportar_pedido, text="Exportar Pedido", command=self.exportar_a_xlsx, bg="grey", fg="white", font=("Arial", 10, "bold"))
        self.btn_exportar_pedido.pack(pady=5)
        self.btn_exportar_pedido.bind("<Enter>", lambda event: self.mostrar_descripcion("Exportar Pedido"))
        self.btn_exportar_pedido.bind("<Leave>", lambda event: self.ocultar_descripcion())

        # Etiqueta para mostrar el muestreo
        self.lbl_muestreo = tk.Label(root, text="", bg="black", fg="white", font=("Arial", 10))
        self.lbl_muestreo.pack(pady=10)

        # Etiqueta para mostrar la descripción del botón al hacer hover
        self.lbl_descripcion = tk.Label(root, text="", bg="black", fg="white", font=("Arial", 10, "italic"))
        self.lbl_descripcion.pack(pady=5)



    def mostrar_descripcion(self, texto):
        self.lbl_descripcion.config(text=texto)

    def ocultar_descripcion(self):
        self.lbl_descripcion.config(text="")

    
    def cargar_archivo(self):
        # Abrir el diálogo para seleccionar el archivo CSV
        ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
        
        if ruta_archivo:
            # Cargar el archivo CSV en un DataFrame
            self.base_de_datos_df = pd.read_csv(ruta_archivo, delimiter=';')
            self.base_de_datos_TXT = pd.read_csv(ruta_archivo, delimiter=';')
            
            print(self.base_de_datos_df)  # Imprimir el DataFrame cargado
            

    def reordenar_y_renombrar(self):
        if self.masivas_df is not None:
            print("Cargado el df")
        if self.base_de_datos_df is not None:
            # Reordenar y renombrar las columnas del DataFrame
            self.base_de_datos_df = self.base_de_datos_df[['Codigo', 'C.Barra', 'Descripcion', 'Comprar', 'Máximo 3 meses', 
                                              'Vtas 01mes Atras Cerrado', 'Vtas 02mes Atras Cerrado', 
                                              'Vtas 03mes Atras Cerrado', 'Stock Actual C.D.', 'Stock Sucursales', 
                                              'Surtido Total','Precio']]
            
            filas_con_error = []
        
            for idx, valor in enumerate(self.base_de_datos_df['C.Barra']):
                try:
                    # Intentamos convertir el valor a tipo float
                    valor_convertido = float(str(valor).replace(',', ''))

                    # Si la conversión es exitosa, actualizamos el valor en el DataFrame
                    self.base_de_datos_df.at[idx, 'C.Barra'] = valor_convertido
                except ValueError:
                    # Si ocurre un error al convertir, agregamos el índice de la fila a la lista de errores
                    filas_con_error.append(idx)
                    continue
            
            # Ahora eliminamos las filas con errores del DataFrame
            self.base_de_datos_df = self.base_de_datos_df.drop(filas_con_error)
            
            # Convertimos la columna 'C.Barra' a tipo int64
            self.base_de_datos_df['C.Barra'] = self.base_de_datos_df['C.Barra'].astype('int64')
        
        
        # Ahora la columna 'C.Barra' debería estar del tipo int64
            print(self.base_de_datos_df.dtypes)
            self.base_de_datos_df.columns = ['IDQuantio', 'C.Barra', 'Descripcion', 'ComprarQ', 'Máximo 3 meses', 
                                      'Vtas 01mes Atras Cerrado', 'Vtas 02mes Atras Cerrado', 
                                      'Vtas 03mes Atras Cerrado', 'Stock Actual C.D.', 'Stock Sucursales', 
                                      'Surtido Total', 'PVP']
            tk.messagebox.showinfo("Operación Completada", "Reordenamiento y Renombramiento completados correctamente.")
        else:
            tk.messagebox.showerror("Error", "Primero carga un archivo CSV.")

    def realizar_muestreo(self):
        if self.base_de_datos_df is not None:
            # Realizar muestreo simple de las cabeceras y las primeras 3 filas
            muestreo = self.base_de_datos_df.head(3)
            self.lbl_muestreo.config(text=muestreo)
        else:
            tk.messagebox.showerror("Error", "Primero carga un archivo CSV.")

    def cargar_proveedor(self):
        # Abrir el diálogo para seleccionar el archivo XLSX
        ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos XLSX", "*.xlsx")])
        
        if ruta_archivo:
            # Cargar el archivo XLSX en un DataFrame
            self.proveedor_df = pd.read_excel(ruta_archivo, header=None)
            self.lbl_muestreo.config(text="Proveedor XLSX cargado:\n\n" + str(self.proveedor_df.head(3)))

    def cargar_comparativa(self):
        # Abrir el diálogo para seleccionar el archivo Excel para la comparativa
        ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos Excel", "*.xlsx")])
        
        if ruta_archivo:
            # Cargar el archivo Excel en un DataFrame
            self.masivas_df = pd.read_excel(ruta_archivo)
            # Mostrar un muestreo básico del DataFrame de comparativa
            self.lbl_muestreo.config(text="Quantio Cloud Cargado:\n\n" + str(self.masivas_df.head(3)))


    def cargar_cofar(self):
    # Abrir el diálogo0 para seleccionar el archivo CSV
        descuento_str = self.combo_descuento.get()
        
        # Eliminar el "%" y convertir a número
        descuento_num = float(descuento_str.rstrip("%")) / 100
        
        # Almacenar el descuento como una variable de instancia
        self.descuento = descuento_num
        ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
    
        if ruta_archivo:
            try:
                # Intentar leer el archivo CSV utilizando la codificación UTF-8
                self.cofar_df = pd.read_csv(ruta_archivo, delimiter=';',header=None, encoding='utf-8', usecols=[1, 9])
                self.cofar_df.rename(columns={self.cofar_df.columns[0]: 'Codigo'}, inplace=True)  # La última columna es la de precios
                self.cofar_df.rename(columns={self.cofar_df.columns[1]: 'Cofarsur'}, inplace=True)  # La última columna es la de precios
                
                self.cofar_df["Cofarsur"]= self.cofar_df["Cofarsur"]/100*(1-descuento_num)


                
                self.lbl_muestreo.config(text="Cofar Carga:\n\n" + str(self.cofar_df.head(3)))
            except UnicodeDecodeError:
                try:
                    # Intentar leer el archivo CSV utilizando la codificación latin1
                    self.cofar_df = pd.read_csv(ruta_archivo, delimiter=';', encoding='latin1',usecols=[1, 9])
                    
                    self.cofar_df["Cofarsur"]= self.cofar_df["Cofarsur"]/100*(1-descuento_num)
                    self.lbl_muestreo.config(text="Cofar Carga:\n\n" + str(self.cofar_df.head(3)))
                except UnicodeDecodeError:
                    # Si falla con ambas codificaciones, mostrar un mensaje de error
                    tk.messagebox.showerror("Error", "No se pudo leer el archivo CSV. Verifica la codificación del archivo.")
                    return
            
            # Imprimir el DataFrame cargado
            print(self.cofar_df)
        else:
            tk.messagebox.showerror("Error", "Selecciona un archivo CSV.")




            


    def exportar_a_xlsx(self):
        if self.cofar_df is not None:
        
            if self.base_de_datos_df is not None and self.proveedor_df is not None:
                # Fusionar los DataFrames en base a la columna "C.Barra"
                self.exportacion_df = pd.merge(self.base_de_datos_df, self.proveedor_df,left_on="C.Barra", right_on=self.proveedor_df.columns[0], how="left")
                self.exportacion_df.rename(columns={self.exportacion_df.columns[-1]: 'PreciosProveedor'}, inplace=True)  # La última columna es la de precios
                self.exportacion_df = pd.merge(self.exportacion_df, self.masivas_df,left_on="C.Barra", right_on=self.masivas_df.columns[1], how="left")
                self.exportacion_df = pd.merge(self.exportacion_df, self.cofar_df,left_on="C.Barra", right_on=self.cofar_df.columns[0], how="left")
                self.exportacion_df.rename(columns={self.exportacion_df.columns[-1]: 'COFARSUR'}, inplace=True)  # La última columna es la de precios

                # Renombrar columnas
                self.exportacion_df = self.exportacion_df.reindex(columns=['IDQuantio', 'C.Barra', 'Descripcion', 'ComprarQ', 'Máximo 3 meses', 
                                        'Vtas 01mes Atras Cerrado', 'Vtas 02mes Atras Cerrado', 
                                        'Vtas 03mes Atras Cerrado', 'Stock Actual C.D.', 'Stock Sucursales', 
                                        'Surtido Total',"PreciosProveedor","DDS","MASA","SUIZO",'COFARSUR', 'PVP'])
                
                
                mejor_precio_origen = self.exportacion_df.apply(encontrar_mejor_precio_y_origen, axis=1)
                self.exportacion_df = pd.concat([self.exportacion_df, mejor_precio_origen], axis=1)

            
                ruta_archivo = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Archivo de Excel", "*.xlsx")])
                self.exportacion_df.to_excel(ruta_archivo,index=False)
                messagebox.showinfo("Guardado Exitoso", "DataFrame guardado como archivo XLSX correctamente.")
                
            else:
                if self.base_de_datos_df is not None and self.proveedor_df is None:
                # Fusionar los DataFrames en base a la columna "C.Barra"

                    self.exportacion_df = pd.merge(self.base_de_datos_df, self.masivas_df,left_on="C.Barra", right_on=self.masivas_df.columns[1], how="left")
                    self.exportacion_df = pd.merge(self.exportacion_df, self.cofar_df,left_on="C.Barra", right_on=self.cofar_df.columns[0], how="left")
                    self.exportacion_df.rename(columns={self.exportacion_df.columns[-1]: 'COFARSUR'}, inplace=True)  # La última columna es la de precios

                    # Renombrar columnas
                    self.exportacion_df = self.exportacion_df.reindex(columns=['IDQuantio', 'C.Barra', 'Descripcion', 'ComprarQ', 'Máximo 3 meses', 
                                            'Vtas 01mes Atras Cerrado', 'Vtas 02mes Atras Cerrado', 
                                            'Vtas 03mes Atras Cerrado', 'Stock Actual C.D.', 'Stock Sucursales', 
                                            'Surtido Total',"DDS","MASA","SUIZO",'COFARSUR', 'PVP'])
                    
                    
                    mejor_precio_origen = self.exportacion_df.apply(encontrar_mejor_precio_y_origen_sinProveedor, axis=1)
                    self.exportacion_df = pd.concat([self.exportacion_df, mejor_precio_origen], axis=1)

                
                    ruta_archivo = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Archivo de Excel", "*.xlsx")])
                    self.exportacion_df.to_excel(ruta_archivo,index=False)
                    messagebox.showinfo("Guardado Exitoso", "DataFrame guardado como archivo XLSX correctamente.")
                else:    
                    tk.messagebox.showerror("Error", "Primero carga ambos DataFrames.")
        else:
            if self.base_de_datos_df is not None and self.proveedor_df is not None:
                # Fusionar los DataFrames en base a la columna "C.Barra"
                self.exportacion_df = pd.merge(self.base_de_datos_df, self.proveedor_df,left_on="C.Barra", right_on=self.proveedor_df.columns[0], how="left")
                self.exportacion_df.rename(columns={self.exportacion_df.columns[-1]: 'PreciosProveedor'}, inplace=True)  # La última columna es la de precios
                self.exportacion_df = pd.merge(self.exportacion_df, self.masivas_df,left_on="C.Barra", right_on=self.masivas_df.columns[1], how="left")
              
              

                # Renombrar columnas
                self.exportacion_df = self.exportacion_df.reindex(columns=['IDQuantio', 'C.Barra', 'Descripcion', 'ComprarQ', 'Máximo 3 meses', 
                                        'Vtas 01mes Atras Cerrado', 'Vtas 02mes Atras Cerrado', 
                                        'Vtas 03mes Atras Cerrado', 'Stock Actual C.D.', 'Stock Sucursales', 
                                        'Surtido Total',"PreciosProveedor","DDS","MASA","SUIZO",'COFARSUR', 'PVP'])
                
                
                mejor_precio_origen = self.exportacion_df.apply(encontrar_mejor_precio_y_origen, axis=1)
                self.exportacion_df = pd.concat([self.exportacion_df, mejor_precio_origen], axis=1)
            
                ruta_archivo = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Archivo de Excel", "*.xlsx")])
                self.exportacion_df.to_excel(ruta_archivo,index=False)
                messagebox.showinfo("Guardado Exitoso", "DataFrame guardado como archivo XLSX correctamente.")    
            else:
                if self.base_de_datos_df is not None:
                # Fusionar los DataFrames en base a la columna "C.Barra"

                    self.exportacion_df = pd.merge(self.base_de_datos_df, self.masivas_df,left_on="C.Barra", right_on=self.masivas_df.columns[1], how="left")
                

                    # Renombrar columnas
                    self.exportacion_df = self.exportacion_df.reindex(columns=['IDQuantio', 'C.Barra', 'Descripcion', 'ComprarQ', 'Máximo 3 meses', 
                                            'Vtas 01mes Atras Cerrado', 'Vtas 02mes Atras Cerrado', 
                                            'Vtas 03mes Atras Cerrado', 'Stock Actual C.D.', 'Stock Sucursales', 
                                            'Surtido Total',"DDS","MASA","SUIZO",'COFARSUR', 'PVP'])
                    
                    
                    mejor_precio_origen = self.exportacion_df.apply(encontrar_mejor_precio_y_origen_sinProveedor, axis=1)
                    self.exportacion_df = pd.concat([self.exportacion_df, mejor_precio_origen], axis=1)

                
                    ruta_archivo = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Archivo de Excel", "*.xlsx")])
                    self.exportacion_df.to_excel(ruta_archivo,index=False)
                    messagebox.showinfo("Guardado Exitoso", "DataFrame guardado como archivo XLSX correctamente.")
                else:    
                    tk.messagebox.showerror("Error", "Primero carga ambos DataFrames.")
                
            
                
          

    def exportar_a_txt(self):
        if self.base_de_datos_TXT is not None:
            # Convertir 'C.Barra' a tipo string (str)
            self.base_de_datos_TXT['C.Barra'] = self.base_de_datos_TXT['C.Barra'].astype(str)
            
            # Eliminar las filas donde 'C.Barra' es NaN o tiene menos de 13 caracteres
            self.base_de_datos_TXT = self.base_de_datos_TXT.dropna(subset=['C.Barra'])
            self.base_de_datos_TXT = self.base_de_datos_TXT[self.base_de_datos_TXT['C.Barra'].str.len() >= 13]
            
            # Eliminar ".0" al final de los valores en 'C.Barra'
            self.base_de_datos_TXT['C.Barra'] = self.base_de_datos_TXT['C.Barra'].str.replace(r'\.0$', '', regex=True)
            
            # Convertir 'C.Barra' a tipo entero (int64)
            self.base_de_datos_TXT['C.Barra'] = self.base_de_datos_TXT['C.Barra'].astype(np.int64)
            
            # Asignar un valor fijo de 10 a la columna "Comprar"
            self.base_de_datos_TXT['Comprar'] = 10
            
            # Abrir el diálogo para seleccionar la ubicación y el nombre del archivo TXT
            ruta_archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivo de texto", "*.txt")])
            if ruta_archivo:
                self.base_de_datos_TXT.to_csv(ruta_archivo, sep=';', index=False, header=False, columns=['C.Barra', 'Descripcion', 'Comprar'])
                messagebox.showinfo("Exportación a TXT", "Archivo TXT generado correctamente.")
                
                
        else:
            tk.messagebox.showerror("Error", "Primero carga un archivo CSV.")

    def realizar_todas_acciones(self):
        self.cargar_archivo()
        self.reordenar_y_renombrar()
        self.realizar_muestreo()

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()