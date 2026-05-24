# ============================================================
#  BIBLIOTECA DIGITAL — VERSIÓN FINAL CORREGIDA
# ============================================================
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


def validar_año(año):
    if año < 1000 or año > 2026:
        raise ValueError("Año inválido.")
    return año


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
# CLASE LIBRO
# ============================================================

class Libro:

    _id = 1

    def __init__(self, titulo, autor, categoria, año, isbn=None):

        self.__id = Libro._id
        Libro._id += 1

        self.__titulo = validar_texto(titulo, "Título")
        self.__autor = validar_texto(autor, "Autor")
        self.__categoria = validar_texto(categoria, "Categoría")
        self.__año = validar_año(año)
        self.__isbn = isbn if isbn else "N/A"
        self.__disponible = True

    def get_id(self):
        return self.__id

    def get_titulo(self):
        return self.__titulo

    def get_autor(self):
        return self.__autor

    def get_categoria(self):
        return self.__categoria

    def get_año(self):
        return self.__año

    def get_disponible(self):
        return self.__disponible

    def set_disponible(self, estado):
        self.__disponible = estado

    def mostrar_info(self):

        estado = "Disponible" if self.__disponible else "Prestado"

        print(f"[{self.__id}] {self.__titulo}")
        print(f"Autor      : {self.__autor}")
        print(f"Categoría  : {self.__categoria}")
        print(f"Año        : {self.__año}")
        print(f"ISBN       : {self.__isbn}")
        print(f"Estado     : {estado}")


# ============================================================
# PRESTAMOS
# ============================================================

class Prestamo:

    _id = 1

    def __init__(self, libro, usuario, dias=14):

        self.__id = Prestamo._id
        Prestamo._id += 1

        self.__libro = libro
        self.__usuario = usuario
        self.__fecha_prestamo = date.today()
        self.__fecha_devolucion = date.today() + timedelta(days=dias)
        self.__estado = "activo"

    def get_id(self):
        return self.__id

    def get_libro(self):
        return self.__libro

    def get_usuario(self):
        return self.__usuario

    def get_estado(self):
        return self.__estado

    def devolver(self):

        self.__estado = "completado"
        self.__libro.set_disponible(True)

    def mostrar_info(self):

        print(f"Préstamo #{self.__id}")
        print(f"Libro      : {self.__libro.get_titulo()}")
        print(f"Usuario    : {self.__usuario.get_nombre()}")
        print(f"Estado     : {self.__estado}")
        print(f"Vence      : {self.__fecha_devolucion}")


# ============================================================
# USUARIO
# ============================================================

class Usuario:

    _id = 1

    def __init__(self, nombre, apellido, tipo, email):

        self.__id = Usuario._id
        Usuario._id += 1

        self.__nombre = validar_texto(nombre, "Nombre")
        self.__apellido = validar_texto(apellido, "Apellido")
        self.__tipo = validar_tipo_usuario(tipo)
        self.__email = validar_email(email)

        self.__prestamos = []

    def get_id(self):
        return self.__id

    def get_nombre(self):
        return self.__nombre

    def get_email(self):
        return self.__email

    def get_prestamos(self):
        return self.__prestamos

    def agregar_prestamo(self, prestamo):
        self.__prestamos.append(prestamo)

    def prestamos_activos(self):

        activos = []

        for p in self.__prestamos:

            if p.get_estado() == "activo":
                activos.append(p)

        return activos

    def mostrar_info(self):

        print(f"[{self.__id}] {self.__nombre} {self.__apellido}")
        print(f"Tipo   : {self.__tipo}")
        print(f"Email  : {self.__email}")


# ============================================================
# ABB
# ============================================================

class NodoABB:

    def __init__(self, libro):

        self.libro = libro
        self.izq = None
        self.der = None


class ABB:

    def __init__(self):

        self.raiz = None

    def insertar(self, libro):

        self.raiz = self._insertar(self.raiz, libro)

    def _insertar(self, nodo, libro):

        if nodo is None:
            return NodoABB(libro)

        if libro.get_titulo().lower() < nodo.libro.get_titulo().lower():
            nodo.izq = self._insertar(nodo.izq, libro)

        else:
            nodo.der = self._insertar(nodo.der, libro)

        return nodo

    def eliminar(self, titulo):

        self.raiz = self._eliminar(
            self.raiz,
            titulo.lower()
        )

    def _eliminar(self, nodo, titulo):

        if nodo is None:
            return None

        if titulo < nodo.libro.get_titulo().lower():

            nodo.izq = self._eliminar(
                nodo.izq,
                titulo
            )

        elif titulo > nodo.libro.get_titulo().lower():

            nodo.der = self._eliminar(
                nodo.der,
                titulo
            )

        else:

            # Sin hijos
            if nodo.izq is None and nodo.der is None:
                return None

            # Un hijo
            if nodo.izq is None:
                return nodo.der

            if nodo.der is None:
                return nodo.izq

            # Dos hijos
            sucesor = self._minimo(nodo.der)

            nodo.libro = sucesor.libro

            nodo.der = self._eliminar(
                nodo.der,
                sucesor.libro.get_titulo().lower()
            )

        return nodo

    def _minimo(self, nodo):

        while nodo.izq:
            nodo = nodo.izq

        return nodo

    def inorden(self):

        libros = []

        self._inorden(self.raiz, libros)

        return libros

    def _inorden(self, nodo, libros):

        if nodo:

            self._inorden(nodo.izq, libros)

            libros.append(nodo.libro)

            self._inorden(nodo.der, libros)

    def buscar_titulo(self, texto):

        resultados = []

        self._buscar(self.raiz, texto.lower(), resultados)

        return resultados

    def _buscar(self, nodo, texto, resultados):

        if nodo:

            self._buscar(nodo.izq, texto, resultados)

            if texto in nodo.libro.get_titulo().lower():
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

        print("Libro agregado correctamente.")

    def listar_libros(self):

        return self.libros.inorden()

    def buscar_libro(self, texto):

        return self.libros.buscar_titulo(texto)

    def buscar_libro_por_id(self, id_libro):

        for libro in self.listar_libros():

            if libro.get_id() == id_libro:
                return libro

        return None

    def eliminar_libro(self, titulo):

        for p in self.prestamos:

            if (
                p.get_libro().get_titulo().lower() == titulo.lower()
                and p.get_estado() == "activo"
            ):

                print("No se puede eliminar. Tiene préstamos activos.")
                return
            
        libro = None
        
        for l in self.listar_libros():
            if l.get_titulo().lower() == titulo.lower():
                libro = l
                break

        if libro is None:
            print ("Libro no encontrado")
            return
        
        self.libros.eliminar(titulo)
            

        print("Libro eliminado correctamente")

    # --------------------------------------------------------
    # USUARIOS
    # --------------------------------------------------------

    def registrar_usuario(self, nombre, apellido, tipo, email):

        for u in self.usuarios:

            if u.get_email().lower() == email.lower():
                print("Ese correo ya existe.")
                return

        usuario = Usuario(
            nombre,
            apellido,
            tipo,
            email
        )

        self.usuarios.append(usuario)

        print("Usuario registrado correctamente.")

    def buscar_usuario(self, id_usuario):

        for u in self.usuarios:

            if u.get_id() == id_usuario:
                return u

        return None

    # --------------------------------------------------------
    # PRESTAMOS
    # --------------------------------------------------------

    def registrar_prestamo(self, id_libro, id_usuario, dias=14):

        libro = self.buscar_libro_por_id(id_libro)
        usuario = self.buscar_usuario(id_usuario)

        if libro is None:
            print("Libro no encontrado.")
            return

        if usuario is None:
            print("Usuario no encontrado.")
            return

        if not libro.get_disponible():
            print("Libro no disponible.")
            return

        if len(usuario.prestamos_activos()) >= Biblioteca.LIMITE_PRESTAMOS:
            print("El usuario alcanzó el límite de préstamos.")
            return

        prestamo = Prestamo(libro, usuario, dias)

        libro.set_disponible(False)

        usuario.agregar_prestamo(prestamo)

        self.prestamos.append(prestamo)

        print("Préstamo registrado correctamente.")

    def devolver_libro(self, id_prestamo):

        for p in self.prestamos:

            if p.get_id() == id_prestamo:

                if p.get_estado() != "activo":
                    print("El préstamo ya fue completado.")
                    return

                p.devolver()

                print("Devolución realizada.")
                return

        print("Préstamo no encontrado.")


# ============================================================
# INTERFAZ
# ============================================================

def mostrar_libros(libros):

    if not libros:
        print("Sin resultados.")
        return

    for libro in libros:

        libro.mostrar_info()

        print()


def menu_libros(bib):

    while True:

        print("\\n===== LIBROS =====")
        print("1. Ver catálogo")
        print("2. Buscar libro")
        print("3. Agregar libro")
        print("4. Eliminar libro")
        print("0. Volver")

        op = input("Opción: ").strip()

        if op == "1":

            mostrar_libros(bib.listar_libros())

        elif op == "2":

            texto = input("Título: ").strip()

            mostrar_libros(bib.buscar_libro(texto))

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

        elif op == "4":
             
             titulo = input("Título del libro a eliminar: ")
             bib.eliminar_libro(titulo)

        elif op == "0":
            break

        else:
            print("Opción inválida.")


def menu_usuarios(bib):

    while True:

        print("\\n===== USUARIOS =====")
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

        elif op == "2":

            for u in bib.usuarios:

                u.mostrar_info()

                print()

        elif op == "0":
            break

        else:
            print("Opción inválida.")


def menu_prestamos(bib):

    while True:

        print("\\n===== PRÉSTAMOS =====")
        print("1. Registrar préstamo")
        print("2. Registrar devolución")
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

        elif op == "2":

            try:

                id_prestamo = int(input("ID préstamo: "))

                bib.devolver_libro(id_prestamo)

            except ValueError:

                print("Ingrese solo números válidos.")

        elif op == "0":
            break

        else:
            print("Opción inválida.")


# ============================================================
# MAIN
# ============================================================

def main():

    bib = Biblioteca()

    while True:

        print("\\n===== BIBLIOTECA DIGITAL =====")
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
