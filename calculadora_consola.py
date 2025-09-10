import random

class MatrixCalculator:
    """
    Calculadora de matrices en consola.
    Permite:
    - Crear, modificar, guardar y cargar matrices.
    - Realizar operaciones entre matrices: suma, resta, multiplicación, Hadamard, división elemento a elemento.
    - Realizar operaciones sobre una matriz: transpuesta, determinante, adjunta, inversa, multiplicación por escalar.
    - Guardar un historial de operaciones realizadas.
    - Eliminar matrices existentes.
    """

    def __init__(self):
        """Inicializa la calculadora con un diccionario de matrices y un historial vacío."""
        self.matrices = {}
        self.historial = []

    # ======================= CREACIÓN Y LISTADO =======================
    def crear_matriz(self, nombre):
        try:
            filas = int(input("Número de filas: "))
            columnas = int(input("Número de columnas: "))

            if filas <= 0 or columnas <= 0:
                print("⚠️ Filas y columnas deben ser mayores que 0.")
                return
            if filas > 50 or columnas > 50:
                print(f"⚠️ La matriz es demasiado grande ({filas}x{columnas}). Máximo recomendado: 50x50")
                return

            tipo = input("¿Desea llenarla manual (M) o aleatoria (A)? ").strip().upper()
            matriz = []

            if tipo == "M":
                for i in range(filas):
                    fila = []
                    for j in range(columnas):
                        while True:
                            try:
                                val = float(input(f"Elemento ({i},{j}): "))
                                if val != val or val in (float("inf"), float("-inf")):
                                    print("⚠️ Valor inválido (NaN o Inf). Intente de nuevo.")
                                    continue
                                fila.append(val)
                                break
                            except ValueError:
                                print("⚠️ Entrada inválida. Ingrese un número.")
                    matriz.append(fila)

            elif tipo == "A":
                while True:
                    try:
                        minimo = int(input("Valor mínimo: "))
                        maximo = int(input("Valor máximo: "))
                        if minimo > maximo:
                            print("⚠️ El mínimo no puede ser mayor que el máximo.")
                            continue
                        break
                    except ValueError:
                        print("⚠️ Entrada inválida. Deben ser números enteros.")
                matriz = [[random.randint(minimo, maximo) for _ in range(columnas)] for _ in range(filas)]
            else:
                print("⚠️ Opción inválida.")
                return

            self.matrices[nombre] = matriz
            print(f"✅ Matriz '{nombre}' creada con éxito.")

        except ValueError:
            print("⚠️ Entrada inválida. Debe ser un número entero.")

    def listar_matrices(self):
        """Muestra todas las matrices almacenadas de forma compacta (columnas si hay 3 o más)."""
        if not self.matrices:
            print("⚠️ No hay matrices creadas.")
            return

        nombres = list(self.matrices.keys())
        num_matrices = len(nombres)

        if num_matrices < 3:
            for nombre in nombres:
                print(f"\n🔹 Matriz {nombre}:")
                for fila in self.matrices[nombre]:
                    print(" ".join(f"{x:8.2f}" for x in fila))
        else:
            # Mostrar matrices en columnas tipo 3 en paralelo
            col_count = 3
            rows = max(len(self.matrices[nombres[i]]) for i in range(num_matrices))
            for r in range(rows):
                line = ""
                for c in range(col_count):
                    idx = r + c*rows
                    if idx < num_matrices:
                        matriz = self.matrices[nombres[idx]]
                        if r < len(matriz):
                            line += " ".join(f"{x:6.2f}" for x in matriz[r]) + "    "
                        else:
                            line += " " * (6*len(matriz[0])+4)
                print(line)

    def modificar_elemento(self):
        if not self.matrices:
            print("⚠️ No hay matrices para modificar.")
            return

        nombre = input("Nombre de la matriz a modificar: ").strip()
        if nombre not in self.matrices:
            print("⚠️ No existe esa matriz.")
            return

        matriz = self.matrices[nombre]
        try:
            i = int(input("Fila: "))
            j = int(input("Columna: "))
            if i < 0 or j < 0 or i >= len(matriz) or j >= len(matriz[0]):
                print("⚠️ Posición fuera de rango.")
                return

            while True:
                try:
                    val = float(input("Nuevo valor: "))
                    if val != val or val in (float("inf"), float("-inf")):
                        print("⚠️ Valor inválido (NaN o Inf). Intente de nuevo.")
                        continue
                    break
                except ValueError:
                    print("⚠️ Entrada inválida. Ingrese un número.")

            matriz[i][j] = val
            print("✅ Valor actualizado.")

        except ValueError:
            print("⚠️ Entrada inválida. Debe ser un número entero.")

    # ======================= ELIMINAR =======================
    def eliminar_matriz(self):
        """Elimina una matriz existente por nombre."""
        if not self.matrices:
            print("⚠️ No hay matrices para eliminar.")
            return
        nombre = input("Nombre de la matriz a eliminar: ").strip()
        if nombre in self.matrices:
            del self.matrices[nombre]
            self.historial.append(f"Matriz eliminada → {nombre}")
            print(f"✅ Matriz '{nombre}' eliminada.")
        else:
            print("⚠️ No existe esa matriz.")

    # ======================= GUARDAR / CARGAR =======================
    def guardar_matriz(self):
        if not self.matrices:
            print("⚠️ No hay matrices para guardar.")
            return

        nombre = input("Nombre de la matriz a guardar: ").strip()
        if nombre not in self.matrices:
            print("⚠️ No existe esa matriz.")
            return

        archivo = input("Nombre del archivo (.txt o .csv): ").strip()
        try:
            with open(archivo, "w") as f:
                for fila in self.matrices[nombre]:
                    f.write(",".join(map(str, fila)) + "\n")
            print(f"✅ Matriz '{nombre}' guardada en {archivo}.")
        except Exception as e:
            print(f"⚠️ Error al guardar: {e}")

    def cargar_matriz(self):
        archivo = input("Nombre del archivo a cargar: ").strip()
        try:
            with open(archivo, "r") as f:
                lineas = f.readlines()

            matriz = []
            for linea in lineas:
                try:
                    matriz.append(list(map(float, linea.strip().split(","))))
                except ValueError:
                    print("⚠️ El archivo contiene datos inválidos.")
                    return

            if not matriz:
                print("⚠️ El archivo está vacío o mal formateado.")
                return

            nombre = input("Nombre para la matriz cargada: ").strip()
            self.matrices[nombre] = matriz
            print(f"✅ Matriz '{nombre}' cargada desde {archivo}.")

        except FileNotFoundError:
            print("⚠️ Archivo no encontrado.")
        except Exception as e:
            print(f"⚠️ Error al cargar: {e}")

    # ======================= OPERACIONES BINARIAS =======================
    def op_binaria(self, tipo):
        if len(self.matrices) < 2:
            print("⚠️ Se necesitan al menos 2 matrices.")
            return

        A = self.seleccionar_matriz("primera")
        B = self.seleccionar_matriz("segunda")
        if not A or not B:
            return

        try:
            if tipo == "suma":
                if len(A) != len(B) or len(A[0]) != len(B[0]):
                    print("⚠️ Las dimensiones no coinciden para la suma.")
                    return
                R = [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

            elif tipo == "resta":
                if len(A) != len(B) or len(A[0]) != len(B[0]):
                    print("⚠️ Las dimensiones no coinciden para la resta.")
                    return
                R = [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

            elif tipo == "producto_matriz":
                if len(A[0]) != len(B):
                    print("⚠️ Columnas de A ≠ Filas de B.")
                    return
                R = [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]

            elif tipo == "producto_hadamard":
                if len(A) != len(B) or len(A[0]) != len(B[0]):
                    print("⚠️ Las dimensiones no coinciden para Hadamard.")
                    return
                R = [[A[i][j] * B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

            elif tipo == "division_elemento":
                if len(A) != len(B) or len(A[0]) != len(B[0]):
                    print("⚠️ Las dimensiones no coinciden para división.")
                    return
                R = [[A[i][j] / B[i][j] if B[i][j] != 0 else float("inf") for j in range(len(A[0]))] for i in range(len(A))]

            else:
                print("⚠️ Operación desconocida.")
                return

            nombre = input("Nombre de la matriz resultado: ").strip()
            self.matrices[nombre] = R
            self.historial.append(f"Resultado de {tipo.upper()} → {nombre}")
            print(f"✅ Operación {tipo} guardada como '{nombre}'.")

        except Exception as e:
            print(f"⚠️ Error en operación: {e}")

    # ======================= OPERACIONES SOBRE UNA MATRIZ =======================
    def op_transpuesta(self):
        A = self.seleccionar_matriz()
        if not A:
            return
        R = [list(fila) for fila in zip(*A)]
        nombre = input("Nombre de la transpuesta: ").strip()
        self.matrices[nombre] = R
        self.historial.append(f"Transpuesta → {nombre}")
        print(f"✅ Transpuesta guardada como '{nombre}'.")

    def op_determinante(self):
        A = self.seleccionar_matriz()
        if not A:
            return
        if len(A) != len(A[0]):
            print("⚠️ Solo se permite determinante en matrices cuadradas.")
            return
        print("📌 Cálculo paso a paso del determinante:")
        det = self.determinante(A, paso=True)
        print(f"Determinante = {det}")

    def determinante(self, M, paso=False, nivel=0):
        if len(M) == 1:
            return M[0][0]
        if len(M) == 2:
            return M[0][0]*M[1][1] - M[0][1]*M[1][0]
        det = 0
        for c in range(len(M[0])):
            minor = [fila[:c]+fila[c+1:] for fila in M[1:]]
            cofactor = ((-1)**c) * M[0][c] * self.determinante(minor, paso, nivel+1)
            if paso:
                print(" "*nivel + f"Expandir con elemento {M[0][c]} en columna {c}: {cofactor}")
            det += cofactor
        return det

    def op_adjunta(self):
        A = self.seleccionar_matriz()
        if not A or len(A) != len(A[0]):
            print("⚠️ Solo se permite adjunta en matrices cuadradas.")
            return
        adj = []
        for i in range(len(A)):
            fila = []
            for j in range(len(A)):
                minor = [row[:j] + row[j+1:] for k, row in enumerate(A) if k != i]
                fila.append(((-1) ** (i+j)) * self.determinante(minor))
            adj.append(fila)
        R = [list(fila) for fila in zip(*adj)]
        nombre = input("Nombre de la adjunta: ").strip()
        self.matrices[nombre] = R
        self.historial.append(f"Adjunta → {nombre}")
        print(f"✅ Adjunta guardada como '{nombre}'.")

    def op_inversa(self):
        A = self.seleccionar_matriz()
        if not A or len(A) != len(A[0]):
            print("⚠️ Solo se permite inversa en matrices cuadradas.")
            return
        det = self.determinante(A)
        if det == 0:
            print("⚠️ La matriz no tiene inversa.")
            return
        adj = []
        for i in range(len(A)):
            fila = []
            for j in range(len(A)):
                minor = [row[:j] + row[j+1:] for k, row in enumerate(A) if k != i]
                fila.append(((-1) ** (i+j)) * self.determinante(minor))
            adj.append(fila)
        adj_T = [list(fila) for fila in zip(*adj)]
        try:
            R = [[adj_T[i][j]/det for j in range(len(A))] for i in range(len(A))]
        except ZeroDivisionError:
            print("⚠️ Error: división por cero en la inversa.")
            return
        nombre = input("Nombre de la inversa: ").strip()
        self.matrices[nombre] = R
        self.historial.append(f"Inversa → {nombre}")
        print(f"✅ Inversa guardada como '{nombre}'.")

    def op_escalar(self):
        A = self.seleccionar_matriz()
        if not A:
            return
        while True:
            try:
                esc = float(input("Ingrese el escalar: "))
                if esc != esc or esc in (float("inf"), float("-inf")):
                    print("⚠️ Escalar inválido.")
                    continue
                break
            except ValueError:
                print("⚠️ Entrada inválida. Ingrese un número.")
        R = [[A[i][j]*esc for j in range(len(A[0]))] for i in range(len(A))]
        nombre = input("Nombre de la matriz resultado: ").strip()
        self.matrices[nombre] = R
        self.historial.append(f"Escalar ({esc}) → {nombre}")
        print(f"✅ Escalar aplicado, guardado como '{nombre}'.")

    # ======================= AUXILIARES =======================
    def seleccionar_matriz(self, orden=""):
        if not self.matrices:
            print("⚠️ No hay matrices.")
            return None
        nombre = input(f"Nombre de la {orden} matriz: ").strip()
        if nombre not in self.matrices:
            print("⚠️ No existe esa matriz.")
            return None
        return self.matrices[nombre]

    def mostrar_historial(self):
        if not self.historial:
            print("⚠️ No hay operaciones registradas.")
            return
        print("\n📜 Historial de operaciones:")
        for op in self.historial:
            print(" -", op)

    def exportar_historial(self):
        if not self.historial:
            print("⚠️ No hay operaciones para exportar.")
            return
        archivo = input("Nombre del archivo para exportar historial: ").strip()
        try:
            with open(archivo, "w") as f:
                for op in self.historial:
                    f.write(op + "\n")
            print(f"✅ Historial exportado a {archivo}.")
        except Exception as e:
            print(f"⚠️ Error al exportar historial: {e}")

    # ======================= MENÚ =======================
    def menu(self):
        opciones = {
            "1": ("Crear matriz", lambda: self.crear_matriz(input("Nombre: ").strip())),
            "2": ("Listar matrices", self.listar_matrices),
            "3": ("Modificar elemento", self.modificar_elemento),
            "4": ("Guardar matriz", self.guardar_matriz),
            "5": ("Cargar matriz", self.cargar_matriz),
            "6": ("Eliminar matriz", self.eliminar_matriz),
            "7": ("Historial", self.mostrar_historial),
            "8": ("Exportar historial", self.exportar_historial),
            "9": ("Suma", lambda: self.op_binaria("suma")),
            "10": ("Resta", lambda: self.op_binaria("resta")),
            "11": ("Multiplicación", lambda: self.op_binaria("producto_matriz")),
            "12": ("Hadamard", lambda: self.op_binaria("producto_hadamard")),
            "13": ("División", lambda: self.op_binaria("division_elemento")),
            "14": ("Transpuesta", self.op_transpuesta),
            "15": ("Determinante", self.op_determinante),
            "16": ("Adjunta", self.op_adjunta),
            "17": ("Inversa", self.op_inversa),
            "18": ("Escalar", self.op_escalar),
            "0": ("Salir", None)
        }

        while True:
            print("\n===== CALCULADORA DE MATRICES =====")
            for k, (desc, _) in opciones.items():
                print(f"{k}. {desc}")
            op = input("Seleccione una opción: ").strip()
            if op == "0":
                print("👋 Adiós.")
                break
            elif op in opciones:
                try:
                    opciones[op][1]()
                except Exception as e:
                    print(f"⚠️ Error en la opción: {e}")
            else:
                print("⚠️ Opción inválida.")

# ======================= MAIN =======================
if __name__ == "__main__":
    calc = MatrixCalculator()
    calc.menu()


