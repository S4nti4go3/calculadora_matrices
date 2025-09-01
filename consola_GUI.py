import random
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog

class MatrixCalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🕹️ Calculadora de Matrices - Modo Gamer 🕹️")
        self.root.state('zoomed')  # Maximizada
        self.matrices = {}
        self.historial = []
        self.current_matrix_name = None

        # ================= FRAMES =================
        self.frame_lateral = tk.Frame(root, width=250, bg="#1b1b2f")
        self.frame_lateral.pack(side="left", fill="y")

        self.frame_principal = tk.Frame(root, bg="#0f3460")
        self.frame_principal.pack(side="right", fill="both", expand=True)

        tk.Label(self.frame_principal, text="🕹️ Calculadora de Matrices 🕹️",
                 font=("Arial", 24, "bold"), fg="#e94560", bg="#0f3460").pack(pady=20)

        # Canvas y scroll
        self.canvas = tk.Canvas(self.frame_principal, bg="#0f3460")
        self.scroll_y = tk.Scrollbar(self.frame_principal, orient="vertical", command=self.canvas.yview)
        self.scroll_x = tk.Scrollbar(self.frame_principal, orient="horizontal", command=self.canvas.xview)
        self.content_frame = tk.Frame(self.canvas, bg="#0f3460")

        self.content_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0,0), window=self.content_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)

        self.canvas.pack(side="top", fill="both", expand=True)
        self.scroll_y.pack(side="right", fill="y")
        self.scroll_x.pack(side="bottom", fill="x")

        self.create_buttons()
        self.actualizar_lista_matrices()

    # ================= BOTONES =================
    def create_buttons(self):
        botones = [
            ("Crear matriz", self.crear_matriz),
            ("Listar matrices", self.actualizar_lista_matrices),
            ("Modificar matriz seleccionada", self.modificar_matriz_desde_pantalla),
            ("Eliminar matriz", self.eliminar_matriz),  # ← BOTÓN NUEVO
            ("Guardar matriz", self.guardar_matriz),
            ("Cargar matriz", self.cargar_matriz),
            ("Historial", self.mostrar_historial),
            ("Exportar historial", self.exportar_historial),
            ("Suma", lambda: self.op_binaria("suma")),
            ("Resta", lambda: self.op_binaria("resta")),
            ("Multiplicación", lambda: self.op_binaria("producto_matriz")),
            ("Hadamard", lambda: self.op_binaria("producto_hadamard")),
            ("División", lambda: self.op_binaria("division_elemento")),
            ("Transpuesta", self.op_transpuesta),
            ("Determinante", self.op_determinante),
            ("Adjunta", self.op_adjunta),
            ("Inversa", self.op_inversa),
            ("Escalar", self.op_escalar),
            ("Salir", self.root.quit)
        ]
        for text, cmd in botones:
            b = tk.Button(self.frame_lateral, text=text, width=25, height=2, bg="#162447", fg="#e94560",
                          font=("Arial", 10, "bold"), command=cmd)
            b.pack(pady=4)

    # ================= LISTA DE MATRICES =================
    def actualizar_lista_matrices(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        tk.Label(self.content_frame, text="Matrices Disponibles:",
                 font=("Arial", 16, "bold"), fg="#ffd369", bg="#0f3460").pack(pady=10)

        for nombre, matriz in self.matrices.items():
            frame = tk.Frame(self.content_frame, bg="#1b1b2f", bd=2, relief="ridge")
            frame.pack(pady=5, padx=10, fill="x")

            tk.Label(frame, text=nombre, font=("Arial", 14, "bold"), fg="#ffd369", bg="#1b1b2f").pack(side="top", anchor="w")

            table_frame = tk.Frame(frame, bg="#0f3460")
            table_frame.pack(pady=5)
            rows, cols = len(matriz), len(matriz[0])
            for i in range(rows):
                for j in range(cols):
                    val = tk.Text(table_frame, width=6, height=1, bg="#0f3460", fg="#ffd369")
                    val.insert("1.0", f"{matriz[i][j]:.2f}")
                    val.configure(state="normal")
                    val.grid(row=i, column=j, padx=1, pady=1)

            tk.Button(frame, text="Seleccionar", bg="#e94560", fg="white",
                      command=lambda n=nombre: self.seleccionar_matriz_actual(n)).pack(pady=5)

    def seleccionar_matriz_actual(self, nombre):
        self.current_matrix_name = nombre
        messagebox.showinfo("✅ Seleccionada", f"Matriz '{nombre}' seleccionada.", parent=self.root)

    # ================= CREAR MATRIZ =================
    def crear_matriz(self):
        nombre = simpledialog.askstring("Nombre", "Ingrese el nombre de la matriz:", parent=self.root)
        if not nombre:
            return
        while nombre in self.matrices:
            nombre = simpledialog.askstring("Nombre", f"'{nombre}' ya existe. Ingrese otro nombre:", parent=self.root)
            if not nombre:
                return
        try:
            filas = simpledialog.askinteger("Filas", "Número de filas:", parent=self.root)
            columnas = simpledialog.askinteger("Columnas", "Número de columnas:", parent=self.root)
            if filas <=0 or columnas <=0:
                messagebox.showerror("⚠️ Error", "Filas y columnas deben ser mayores que 0.", parent=self.root)
                return
            if filas>50 or columnas>50:
                messagebox.showwarning("⚠️ Atención", "Matriz muy grande. Máximo recomendado: 50x50", parent=self.root)
        except:
            messagebox.showerror("⚠️ Error", "Valores inválidos.", parent=self.root)
            return

        tipo = simpledialog.askstring("Tipo", "Manual (M) o Aleatoria (A)?", parent=self.root)
        if not tipo:
            return
        tipo = tipo.strip().upper()
        matriz = []

        if tipo == "M":
            for i in range(filas):
                fila = []
                for j in range(columnas):
                    while True:
                        try:
                            val = simpledialog.askfloat("Elemento", f"Elemento ({i},{j}):", parent=self.root)
                            if val != val or val in (float("inf"), float("-inf")):
                                messagebox.showerror("⚠️ Error", "Valor inválido (NaN o Inf)", parent=self.root)
                                continue
                            fila.append(val)
                            break
                        except:
                            continue
                matriz.append(fila)
        elif tipo == "A":
            while True:
                try:
                    minimo = simpledialog.askinteger("Mínimo", "Valor mínimo:", parent=self.root)
                    maximo = simpledialog.askinteger("Máximo", "Valor máximo:", parent=self.root)
                    if minimo>maximo:
                        messagebox.showerror("⚠️ Error", "Mínimo no puede ser mayor que máximo.", parent=self.root)
                        continue
                    break
                except:
                    continue
            matriz = [[random.randint(minimo, maximo) for _ in range(columnas)] for _ in range(filas)]
        else:
            messagebox.showerror("⚠️ Error", "Opción inválida", parent=self.root)
            return

        self.matrices[nombre] = matriz
        self.historial.append(f"Matriz '{nombre}' creada")
        self.current_matrix_name = nombre
        messagebox.showinfo("✅ Éxito", f"Matriz '{nombre}' creada.", parent=self.root)
        self.actualizar_lista_matrices()

    # ================= ELIMINAR MATRIZ =================
    def eliminar_matriz(self):
        if not self.matrices:
            messagebox.showwarning("⚠️ Atención", "No hay matrices para eliminar.", parent=self.root)
            return
        nombre = simpledialog.askstring("Eliminar", "Nombre de la matriz a eliminar:", parent=self.root)
        if not nombre or nombre not in self.matrices:
            messagebox.showerror("⚠️ Error", "Matriz no encontrada.", parent=self.root)
            return
        del self.matrices[nombre]
        if self.current_matrix_name == nombre:
            self.current_matrix_name = None
        self.historial.append(f"Matriz '{nombre}' eliminada")
        messagebox.showinfo("✅ Eliminada", f"Matriz '{nombre}' eliminada.", parent=self.root)
        self.actualizar_lista_matrices()

    # ================= MODIFICAR MATRIZ DESDE PANTALLA =================
    def modificar_matriz_desde_pantalla(self):
        if not self.current_matrix_name:
            messagebox.showwarning("⚠️ Atención", "Primero selecciona una matriz.", parent=self.root)
            return
        matriz = self.matrices[self.current_matrix_name]
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        tk.Label(self.content_frame, text=f"Modificando '{self.current_matrix_name}'",
                 font=("Arial", 16, "bold"), fg="#ffd369", bg="#0f3460").pack(pady=10)
        table_frame = tk.Frame(self.content_frame, bg="#0f3460")
        table_frame.pack(pady=10)

        rows, cols = len(matriz), len(matriz[0])
        entries = []
        for i in range(rows):
            fila_entries = []
            for j in range(cols):
                e = tk.Entry(table_frame, width=6, justify="center", bg="#0f3460", fg="#ffd369")
                e.insert(0, f"{matriz[i][j]:.2f}")
                e.grid(row=i, column=j, padx=1, pady=1)
                fila_entries.append(e)
            entries.append(fila_entries)

        def guardar_cambios():
            try:
                for i in range(rows):
                    for j in range(cols):
                        val = float(entries[i][j].get())
                        matriz[i][j] = val
                self.matrices[self.current_matrix_name] = matriz
                self.historial.append(f"Matriz '{self.current_matrix_name}' modificada desde pantalla")
                messagebox.showinfo("✅ Éxito", f"Matriz '{self.current_matrix_name}' actualizada.", parent=self.root)
                self.actualizar_lista_matrices()
            except:
                messagebox.showerror("⚠️ Error", "Entrada inválida.", parent=self.root)

        tk.Button(self.content_frame, text="Guardar Cambios", bg="#e94560", fg="white",
                  font=("Arial", 12, "bold"), command=guardar_cambios).pack(pady=10)

    # ================= FUNCIONES AUXILIARES =================
    def seleccionar_matriz(self, prompt="Nombre de la matriz"):
        if not self.matrices:
            messagebox.showwarning("⚠️ Atención", "No hay matrices disponibles.", parent=self.root)
            return None
        nombre = simpledialog.askstring("Seleccionar matriz", prompt, parent=self.root)
        if not nombre or nombre not in self.matrices:
            messagebox.showerror("⚠️ Error", "No existe esa matriz.", parent=self.root)
            return None
        return self.matrices[nombre], nombre

    # ================= OPERACIONES =================
    def op_binaria(self, tipo):
        if len(self.matrices) < 2:
            messagebox.showwarning("⚠️ Atención","Se necesitan al menos 2 matrices.", parent=self.root)
            return
        selA = self.seleccionar_matriz("Primera matriz")
        selB = self.seleccionar_matriz("Segunda matriz")
        if not selA or not selB:
            return
        A,_ = selA
        B,_ = selB
        try:
            if tipo=="suma":
                if len(A)!=len(B) or len(A[0])!=len(B[0]):
                    messagebox.showerror("⚠️ Error","Dimensiones no coinciden para suma", parent=self.root)
                    return
                R=[[A[i][j]+B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
            elif tipo=="resta":
                if len(A)!=len(B) or len(A[0])!=len(B[0]):
                    messagebox.showerror("⚠️ Error","Dimensiones no coinciden para resta", parent=self.root)
                    return
                R=[[A[i][j]-B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
            elif tipo=="producto_matriz":
                if len(A[0])!=len(B):
                    messagebox.showerror("⚠️ Error","Columnas A != Filas B", parent=self.root)
                    return
                R=[[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
            elif tipo=="producto_hadamard":
                if len(A)!=len(B) or len(A[0])!=len(B[0]):
                    messagebox.showerror("⚠️ Error","Dimensiones no coinciden para Hadamard", parent=self.root)
                    return
                R=[[A[i][j]*B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
            elif tipo=="division_elemento":
                if len(A)!=len(B) or len(A[0])!=len(B[0]):
                    messagebox.showerror("⚠️ Error","Dimensiones no coinciden para división", parent=self.root)
                    return
                R=[[A[i][j]/B[i][j] if B[i][j]!=0 else float("inf") for j in range(len(A[0]))] for i in range(len(A))]
            else:
                messagebox.showerror("⚠️ Error","Operación desconocida", parent=self.root)
                return
            nombre = simpledialog.askstring("Nombre", "Nombre de la matriz resultado", parent=self.root)
            if not nombre:
                return
            self.matrices[nombre]=R
            self.historial.append(f"Resultado de {tipo.upper()} → {nombre}")
            messagebox.showinfo("✅ Éxito", f"Operación {tipo} guardada como '{nombre}'", parent=self.root)
            self.actualizar_lista_matrices()
        except Exception as e:
            messagebox.showerror("⚠️ Error", f"Ocurrió un error: {e}", parent=self.root)

    # ================= FUNCIONES DE MATRICES =================
    def op_transpuesta(self):
        sel = self.seleccionar_matriz()
        if not sel: return
        A, _ = sel
        R = [list(f) for f in zip(*A)]
        nombre = simpledialog.askstring("Nombre", "Nombre de la transpuesta", parent=self.root)
        if not nombre: return
        self.matrices[nombre]=R
        self.historial.append(f"Transpuesta → {nombre}")
        messagebox.showinfo("✅ Éxito", f"Transpuesta guardada como '{nombre}'", parent=self.root)
        self.actualizar_lista_matrices()

    def op_determinante(self):
        sel = self.seleccionar_matriz()
        if not sel: return
        A, nombre_matriz = sel
        if len(A)!=len(A[0]):
            messagebox.showerror("⚠️ Error", "Solo se permite determinante en matrices cuadradas.", parent=self.root)
            return
        det = self.determinante(A)
        self.historial.append(f"Determinante de '{nombre_matriz}' calculado")
        messagebox.showinfo("📌 Determinante", f"Determinante de '{nombre_matriz}' = {det}", parent=self.root)

    def determinante(self, M):
        if len(M) == 1: return M[0][0]
        if len(M) == 2: return M[0][0]*M[1][1]-M[0][1]*M[1][0]
        det=0
        for c in range(len(M[0])):
            minor=[fila[:c]+fila[c+1:] for fila in M[1:]]
            det+=((-1)**c)*M[0][c]*self.determinante(minor)
        return det

    def op_adjunta(self):
        sel = self.seleccionar_matriz()
        if not sel: return
        A,_=sel
        if len(A)!=len(A[0]):
            messagebox.showerror("⚠️ Error","Solo cuadradas", parent=self.root)
            return
        adj=[]
        n=len(A)
        for i in range(n):
            fila=[]
            for j in range(n):
                minor=[row[:j]+row[j+1:] for k,row in enumerate(A) if k!=i]
                fila.append(((-1)**(i+j))*self.determinante(minor))
            adj.append(fila)
        adj_T=[list(f) for f in zip(*adj)]
        nombre=simpledialog.askstring("Nombre","Nombre adjunta", parent=self.root)
        if not nombre: return
        self.matrices[nombre]=adj_T
        self.historial.append(f"Adjunta → {nombre}")
        messagebox.showinfo("✅ Éxito", f"Adjunta guardada como '{nombre}'", parent=self.root)
        self.actualizar_lista_matrices()

    def op_inversa(self):
        sel=self.seleccionar_matriz()
        if not sel: return
        A,_=sel
        if len(A)!=len(A[0]):
            messagebox.showerror("⚠️ Error","Solo cuadradas", parent=self.root)
            return
        det=self.determinante(A)
        if det==0:
            messagebox.showerror("⚠️ Error","Matriz no tiene inversa", parent=self.root)
            return
        n=len(A)
        adj=[]
        for i in range(n):
            fila=[]
            for j in range(n):
                minor=[row[:j]+row[j+1:] for k,row in enumerate(A) if k!=i]
                fila.append(((-1)**(i+j))*self.determinante(minor))
            adj.append(fila)
        adj_T=[list(f) for f in zip(*adj)]
        R=[[adj_T[i][j]/det for j in range(n)] for i in range(n)]
        nombre=simpledialog.askstring("Nombre","Nombre inversa", parent=self.root)
        if not nombre: return
        self.matrices[nombre]=R
        self.historial.append(f"Inversa → {nombre}")
        messagebox.showinfo("✅ Éxito", f"Inversa guardada como '{nombre}'", parent=self.root)
        self.actualizar_lista_matrices()

    def op_escalar(self):
        sel=self.seleccionar_matriz()
        if not sel: return
        A,_=sel
        try:
            esc=float(simpledialog.askstring("Escalar","Valor escalar", parent=self.root))
        except:
            messagebox.showerror("⚠️ Error","Valor inválido", parent=self.root)
            return
        R=[[A[i][j]*esc for j in range(len(A[0]))] for i in range(len(A))]
        nombre=simpledialog.askstring("Nombre","Nombre resultado", parent=self.root)
        if not nombre: return
        self.matrices[nombre]=R
        self.historial.append(f"Escalar({esc}) → {nombre}")
        messagebox.showinfo("✅ Éxito", f"Resultado guardado como '{nombre}'", parent=self.root)
        self.actualizar_lista_matrices()

    # ================= GUARDAR / CARGAR =================
    def guardar_matriz(self):
        sel=self.seleccionar_matriz()
        if not sel: return
        A,nombre=sel
        ruta=filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files","*.txt")])
        if not ruta: return
        with open(ruta,"w") as f:
            for fila in A:
                f.write(",".join(str(x) for x in fila)+"\n")
        messagebox.showinfo("✅ Guardada", f"Matriz '{nombre}' guardada en {ruta}", parent=self.root)

    def cargar_matriz(self):
        ruta=filedialog.askopenfilename(filetypes=[("Text files","*.txt")])
        if not ruta: return
        with open(ruta,"r") as f:
            lineas=f.readlines()
        matriz=[list(map(float,l.strip().split(","))) for l in lineas]
        nombre=simpledialog.askstring("Nombre","Nombre matriz cargada", parent=self.root)
        if not nombre: return
        self.matrices[nombre]=matriz
        self.historial.append(f"Matriz '{nombre}' cargada desde archivo")
        self.actualizar_lista_matrices()

    # ================= HISTORIAL =================
    def mostrar_historial(self):
        if not self.historial:
            messagebox.showinfo("Historial","No hay operaciones aún.", parent=self.root)
            return
        ventana=tk.Toplevel(self.root)
        ventana.title("Historial")
        texto=tk.Text(ventana,width=50,height=20)
        texto.pack()
        texto.insert("1.0","\n".join(self.historial))

    def exportar_historial(self):
        if not self.historial:
            messagebox.showwarning("⚠️ Atención","No hay historial", parent=self.root)
            return
        ruta=filedialog.asksaveasfilename(defaultextension=".txt")
        if not ruta: return
        with open(ruta,"w") as f:
            for h in self.historial:
                f.write(h+"\n")
        messagebox.showinfo("✅ Exportado", f"Historial exportado a {ruta}", parent=self.root)


if __name__=="__main__":
    root=tk.Tk()
    app=MatrixCalculatorGUI(root)
    root.mainloop()
