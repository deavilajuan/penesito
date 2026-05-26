from datetime import date, timedelta
import re

# ============================================================
# VALIDACIONES
# ============================================================

TIPOS_VALIDOS = ["estudiante", "docente", "administrativo"]


def validar_texto(texto, campo):

    if not texto.strip():

        raise ValueError(f"{campo} no puede estar vacío.")

    return texto.strip()


def validar_anio(anio):

    if anio < 1000 or anio > 2026:

        raise ValueError("Año inválido.")

    return anio


def validar_email(email):

    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if not re.match(patron, email):

        raise ValueError("Correo electrónico inválido.")

    return email


def validar_tipo_usuario(tipo):

    if tipo.lower() not in TIPOS_VALIDOS:

        raise ValueError(
            "Tipo inválido. Use: estudiante, docente o administrativo."
        )

    return tipo.lower()


# ============================================================
# LIBRO
# ============================================================

class Libro:

    contador = 1

    def __init__(self, titulo, autor, categoria, anio, isbn=None):

        self.id = Libro.contador
        Libro.contador += 1

        self.titulo = validar_texto(titulo, "Título")
        self.autor = validar_texto(autor, "Autor")
        self.categoria = validar_texto(categoria, "Categoría")
        self.anio = validar_anio(anio)

        self.isbn = isbn if isbn else "N/A"

        self.disponible = True

    def mostrar_info(self):

        estado = "Disponible" if self.disponible else "Prestado"

        print(f"[{self.id}] {self.titulo}")
        print(f"Autor      : {self.autor}")
        print(f"Categoría  : {self.categoria}")
        print(f"Año        : {self.anio}")
        print(f"ISBN       : {self.isbn}")
        print(f"Estado     : {estado}")


# ============================================================
# PRESTAMO
# ============================================================

class Prestamo:

    contador = 1

    def __init__(self, libro, usuario, dias=14):

        self.id = Prestamo.contador
        Prestamo.contador += 1

        self.libro = libro
        self.usuario = usuario

        self.fecha_prestamo = date.today()
        self.fecha_devolucion = date.today() + timedelta(days=dias)

        self.estado = "activo"

    def devolver(self):

        self.estado = "completado"

        self.libro.disponible = True

    def mostrar_info(self):

        print(f"Préstamo #{self.id}")
        print(f"Libro      : {self.libro.titulo}")
        print(f"Usuario    : {self.usuario.nombre}")
        print(f"Estado     : {self.estado}")
        print(f"Vence      : {self.fecha_devolucion}")


# ============================================================
# USUARIO
# ============================================================

class Usuario:

    contador = 1

    def __init__(self, nombre, apellido, tipo, email):

        self.id = Usuario.contador
        Usuario.contador += 1

        self.nombre = validar_texto(nombre, "Nombre")
        self.apellido = validar_texto(apellido, "Apellido")
        self.tipo = validar_tipo_usuario(tipo)
        self.email = validar_email(email)

        self.prestamos = []

    def mostrar_info(self):

        print(f"[{self.id}] {self.nombre} {self.apellido}")
        print(f"Tipo   : {self.tipo}")
        print(f"Email  : {self.email}")


# ============================================================
# NODO ABB
# ============================================================

class NodoABB:

    def __init__(self, libro):

        self.libro = libro
        self.izq = None
        self.der = None


# ============================================================
# ABB
# ============================================================

class ABB:

    def __init__(self):

        self.raiz = None

    def insertar(self, libro):

        self.raiz = self._insertar(self.raiz, libro)

    def _insertar(self, nodo, libro):

        if nodo is None:

            return NodoABB(libro)

        if libro.titulo.lower() < nodo.libro.titulo.lower():

            nodo.izq = self._insertar(nodo.izq, libro)

        else:

            nodo.der = self._insertar(nodo.der, libro)

        return nodo

    def mostrar(self):

        libros = []

        self._inorden(self.raiz, libros)

        return libros

    def _inorden(self, nodo, libros):

        if nodo:

            self._inorden(nodo.izq, libros)

            libros.append(nodo.libro)

            self._inorden(nodo.der, libros)

    def buscar(self, texto):

        resultados = []

        self._buscar(self.raiz, texto.lower(), resultados)

        return resultados

    def _buscar(self, nodo, texto, resultados):

        if nodo:

            self._buscar(nodo.izq, texto, resultados)

            if texto in nodo.libro.titulo.lower():

                resultados.append(nodo.libro)

            self._buscar(nodo.der, texto, resultados)


# ============================================================
# BIBLIOTECA
# ============================================================

class Biblioteca:

    LIMITE_PRESTAMOS = 3

    def __init__(self):

        self.libros = ABB()
        self.usuarios = []
        self.prestamos = []

    # --------------------------------------------------------
    # LIBROS
    # --------------------------------------------------------

    def agregar_libro(self, titulo, autor, categoria, anio, isbn=None):

        libro = Libro(
            titulo,
            autor,
            categoria,
            anio,
            isbn
        )

        self.libros.insertar(libro)

        print(f"Libro agregado correctamente. ID libro: {libro.id}")

    def mostrar_catalogo(self):

        return self.libros.mostrar()

    def buscar_libro(self, texto):

        return self.libros.buscar(texto)

    def buscar_libro_id(self, id_libro):

        for libro in self.mostrar_catalogo():

            if libro.id == id_libro:

                return libro

        return None

    # --------------------------------------------------------
    # USUARIOS
    # --------------------------------------------------------

    def registrar_usuario(self, nombre, apellido, tipo, email):

        for u in self.usuarios:

            if u.email.lower() == email.lower():

                print("Ese correo ya existe.")
                return

        usuario = Usuario(
            nombre,
            apellido,
            tipo,
            email
        )

        self.usuarios.append(usuario)

        print(f"Usuario registrado correctamente. ID usuario: {usuario.id}")

    def buscar_usuario(self, id_usuario):

        for u in self.usuarios:

            if u.id == id_usuario:

                return u

        return None

    # --------------------------------------------------------
    # PRESTAMOS
    # --------------------------------------------------------

    def registrar_prestamo(self, id_libro, id_usuario, dias=14):

        libro = self.buscar_libro_id(id_libro)
        usuario = self.buscar_usuario(id_usuario)

        if libro is None:

            print("Libro no encontrado.")
            return

        if usuario is None:

            print("Usuario no encontrado.")
            return

        if not libro.disponible:

            print("Libro no disponible.")
            return

        prestamos_activos = 0

        for p in usuario.prestamos:

            if p.estado == "activo":

                prestamos_activos += 1

        if prestamos_activos >= Biblioteca.LIMITE_PRESTAMOS:

            print("El usuario alcanzó el límite de préstamos.")
            return

        prestamo = Prestamo(libro, usuario, dias)

        libro.disponible = False

        usuario.prestamos.append(prestamo)

        self.prestamos.append(prestamo)

        print(f"Préstamo registrado correctamente. ID préstamo: {prestamo.id}")

    def devolver_libro(self, id_prestamo):

        for p in self.prestamos:

            if p.id == id_prestamo:

                if p.estado != "activo":

                    print("El préstamo ya fue completado.")
                    return

                p.devolver()

                print("Devolución realizada.")
                return

        print("Préstamo no encontrado.")


# ============================================================
# FUNCIONES
# ============================================================

def mostrar_libros(libros):

    if not libros:

        print("No hay libros registrados.")
        return

    for libro in libros:

        libro.mostrar_info()

        print()


# ============================================================
# MENU LIBROS
# ============================================================

def menu_libros(bib):

    while True:

        print("\n===== LIBROS =====")
        print("1. Ver catálogo")
        print("2. Buscar libro")
        print("3. Agregar libro")
        print("0. Volver")

        op = input("Opción: ").strip()

        if op == "1":

            mostrar_libros(bib.mostrar_catalogo())
            
            input("\nPresiona Enter para continuar...")

        elif op == "2":

            texto = input("Título: ").strip()

            resultados = bib.buscar_libro(texto)

            if not resultados:

                print("No se encontraron libros.")

            else:

                mostrar_libros(resultados)
            
            input("\nPresiona Enter para continuar...")

        elif op == "3":

            try:

                titulo = input("Título: ")
                autor = input("Autor: ")
                categoria = input("Categoría: ")

                anio = int(input("Año: "))

                isbn = input("ISBN: ")

                bib.agregar_libro(
                    titulo,
                    autor,
                    categoria,
                    anio,
                    isbn
                )

            except ValueError as e:

                print(f"Error: {e}")

            input("\nPresiona Enter para continuar...")

        elif op == "0":

            break

        else:

            print("Opción inválida.")


# ============================================================
# MENU USUARIOS
# ============================================================

def menu_usuarios(bib):

    while True:

        print("\n===== USUARIOS =====")
        print("1. Registrar usuario")
        print("2. Listar usuarios")
        print("0. Volver")

        op = input("Opción: ").strip()

        if op == "1":

            try:

                nombre = input("Nombre: ")
                apellido = input("Apellido: ")
                tipo = input("Tipo: ")
                email = input("Email: ")

                bib.registrar_usuario(
                    nombre,
                    apellido,
                    tipo,
                    email
                )

            except ValueError as e:

                print(f"Error: {e}")

            input("\nPresiona Enter para continuar...")

        elif op == "2":

            if not bib.usuarios:

                print("No hay usuarios registrados.")

            else:

                for u in bib.usuarios:

                    u.mostrar_info()

                    print()

            input("\nPresiona Enter para continuar...")

        elif op == "0":

            break

        else:

            print("Opción inválida.")


# ============================================================
# MENU PRESTAMOS
# ============================================================

def menu_prestamos(bib):

    while True:

        print("\n===== PRÉSTAMOS =====")
        print("1. Registrar préstamo")
        print("2. Registrar devolución")
        print("3. Ver préstamos")
        print("0. Volver")

        op = input("Opción: ").strip()

        if op == "1":

            try:

                id_libro = int(input("ID libro: "))
                id_usuario = int(input("ID usuario: "))

                bib.registrar_prestamo(
                    id_libro,
                    id_usuario
                )

            except ValueError:

                print("Ingrese solo números válidos.")

            input("\nPresiona Enter para continuar...")

        elif op == "2":

            prestamos_activos = False

            for p in bib.prestamos:

                if p.estado == "activo":

                    prestamos_activos = True
                    break

            if not prestamos_activos:

                print("No hay préstamos activos.")
                continue

            try:

                id_prestamo = int(input("ID préstamo: "))

                bib.devolver_libro(id_prestamo)

            except ValueError:

                print("Ingrese solo números válidos.")

            input("\nPresiona Enter para continuar...")

        elif op == "3":

            if not bib.prestamos:

                print("No hay préstamos registrados.")

            else:

                for p in bib.prestamos:

                    p.mostrar_info()

                    print()

            input("\nPresiona Enter para continuar...")

        elif op == "0":

            break

        else:

            print("Opción inválida.")


# ============================================================
# MAIN
# ============================================================

def main():

    bib = Biblioteca()

    bib.agregar_libro("Cien años de soledad", "Gabriel García Márquez", "Novela", 1967, "978-0307474728")
    bib.agregar_libro("El principito", "Antoine de Saint-Exupéry", "Ficción", 1943, "978-0156012195")
    bib.agregar_libro("Don Quijote de la Mancha", "Miguel de Cervantes", "Clásico", 1605, "978-8420412146")
    bib.agregar_libro("1984", "George Orwell", "Distopía", 1949, "978-0451524935")
    bib.agregar_libro("Sapiens", "Yuval Noah Harari", "Historia", 2011, "978-0062316097")

    while True:

        print("\n===== BIBLIOTECA DIGITAL =====")
        print("1. Libros")
        print("2. Usuarios")
        print("3. Préstamos")
        print("0. Salir")

        op = input("Opción: ").strip()

        if op == "1":

            menu_libros(bib)
        elif op == "2":
            menu_usuarios(bib)
        elif op == "3":
            menu_prestamos(bib)
        elif op == "0":
            print("Hasta luego.")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":

    main()
