# ============================================================
#  BIBLIOTECA DIGITAL
#  Asignatura: Estructura de Datos
#  Universidad Tecnológica de Bolívar
#  Integrantes: Juan F. De Avila, José Vega, Santiago Cabarcas
#  Docente: Rafael Monterroza
# ============================================================
#
#  Dependencias:
#      pip install mysql-connector-python
#
#  Antes de ejecutar, asegúrate de haber corrido el script
#  biblioteca_db.sql en tu servidor MySQL.
# ============================================================

from datetime import date, timedelta


# ============================================================
# 1. CLASES DE DOMINIO (POO)
# ============================================================

class Libro:
    """Representa un libro."""

    def __init__(self, id_libro, titulo, autor, categoria,
                 anio_publicacion, isbn=None, estado_disponible=True):

        self.id_libro = id_libro
        self.titulo = titulo
        self.autor = autor
        self.categoria = categoria
        self.anio_publicacion = anio_publicacion
        self.isbn = isbn
        self.estado_disponible = estado_disponible

    # GETTERS

    def get_id_libro(self):
        return self.id_libro

    def get_titulo(self):
        return self.titulo

    def get_autor(self):
        return self.autor

    def get_categoria(self):
        return self.categoria

    def get_anio_publicacion(self):
        return self.anio_publicacion

    def get_isbn(self):
        return self.isbn

    def get_estado_disponible(self):
        return self.estado_disponible

    # SETTERS

    def set_estado_disponible(self, estado):
        self.estado_disponible = estado

    # OTROS

    def mostrar_info(self):
        estado = "Disponible" if self.estado_disponible else "Prestado"

        print(f"[{self.id_libro}] {self.titulo}")
        print(f"Autor      : {self.autor}")
        print(f"Categoría  : {self.categoria}")
        print(f"Año        : {self.anio_publicacion}")
        print(f"ISBN       : {self.isbn if self.isbn else 'N/A'}")
        print(f"Estado     : {estado}")

    def __str__(self):
        return f"{self.titulo} - {self.autor}"


# ============================================================

class NodoPrestamo:

    def __init__(self, prestamo):
        self.prestamo = prestamo
        self.siguiente = None


class Prestamo:

    def __init__(self, id_prestamo, libro, usuario,
                 fecha_prestamo, fecha_devolucion_esperada,
                 fecha_devolucion_real=None,
                 estado='activo'):

        self.id_prestamo = id_prestamo
        self.libro = libro
        self.usuario = usuario
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion_esperada = fecha_devolucion_esperada
        self.fecha_devolucion_real = fecha_devolucion_real
        self.estado = estado

    # GETTERS

    def get_id_prestamo(self):
        return self.id_prestamo

    def get_libro(self):
        return self.libro

    def get_usuario(self):
        return self.usuario

    def get_fecha_prestamo(self):
        return self.fecha_prestamo

    def get_fecha_devolucion_esperada(self):
        return self.fecha_devolucion_esperada

    def get_estado(self):
        return self.estado

    # SETTERS

    def set_estado(self, estado):
        self.estado = estado

    def set_fecha_devolucion_real(self, fecha):
        self.fecha_devolucion_real = fecha

    # OTROS

    def mostrar_info(self):

        print(f"Préstamo #{self.id_prestamo}")
        print(f"Libro      : {self.libro.get_titulo()}")
        print(f"Usuario    : {self.usuario.get_nombre()} {self.usuario.get_apellido()}")
        print(f"Fecha      : {self.fecha_prestamo}")
        print(f"Vence      : {self.fecha_devolucion_esperada}")
        print(f"Estado     : {self.estado}")


# ============================================================

class ListaEnlazadaPrestamos:

    def __init__(self):
        self.cabeza = None
        self.tamano = 0

    def agregar(self, prestamo):

        nuevo = NodoPrestamo(prestamo)

        nuevo.siguiente = self.cabeza
        self.cabeza = nuevo

        self.tamano += 1

    def listar_todos(self):

        prestamos = []

        actual = self.cabeza

        while actual:
            prestamos.append(actual.prestamo)
            actual = actual.siguiente

        return prestamos

    def listar_activos(self):

        activos = []

        actual = self.cabeza

        while actual:

            if actual.prestamo.get_estado() == 'activo':
                activos.append(actual.prestamo)

            actual = actual.siguiente

        return activos


# ============================================================

class Usuario:

    def __init__(self, id_usuario, nombre, apellido,
                 tipo_usuario, email,
                 fecha_registro=None,
                 activo=True):

        self.id_usuario = id_usuario
        self.nombre = nombre
        self.apellido = apellido
        self.tipo_usuario = tipo_usuario
        self.email = email
        self.fecha_registro = fecha_registro if fecha_registro else date.today()
        self.activo = activo

        self.historial = ListaEnlazadaPrestamos()

    # GETTERS

    def get_id_usuario(self):
        return self.id_usuario

    def get_nombre(self):
        return self.nombre

    def get_apellido(self):
        return self.apellido

    def get_tipo_usuario(self):
        return self.tipo_usuario

    def get_email(self):
        return self.email

    def get_fecha_registro(self):
        return self.fecha_registro

    def get_historial(self):
        return self.historial

    # OTROS

    def agregar_prestamo(self, prestamo):
        self.historial.agregar(prestamo)

    def mostrar_info(self):

        print(f"[{self.id_usuario}] {self.nombre} {self.apellido}")
        print(f"Tipo       : {self.tipo_usuario}")
        print(f"Email      : {self.email}")
        print(f"Activo     : {'Sí' if self.activo else 'No'}")


# ============================================================
# 2. ÁRBOL BINARIO DE BÚSQUEDA
# ============================================================

class NodoABB:

    def __init__(self, libro):
        self.libro = libro
        self.izq = None
        self.der = None


class ArbolBinarioBusqueda:

    def __init__(self):

        self.raiz = None
        self.total = 0

    def get_total(self):
        return self.total

    # INSERTAR

    def insertar(self, libro):

        self.raiz = self.__insertar_rec(self.raiz, libro)

    def __insertar_rec(self, nodo, libro):

        if nodo is None:
            self.total += 1
            return NodoABB(libro)

        clave = libro.get_titulo().lower()
        clave_nodo = nodo.libro.get_titulo().lower()

        if clave < clave_nodo:
            nodo.izq = self.__insertar_rec(nodo.izq, libro)

        elif clave > clave_nodo:
            nodo.der = self.__insertar_rec(nodo.der, libro)

        return nodo

    # BUSCAR TÍTULO EXACTO

    def buscar_titulo(self, titulo):

        return self.__buscar_rec(self.raiz, titulo.lower())

    def __buscar_rec(self, nodo, titulo):

        if nodo is None:
            return None

        clave = nodo.libro.get_titulo().lower()

        if titulo == clave:
            return nodo.libro

        if titulo < clave:
            return self.__buscar_rec(nodo.izq, titulo)

        return self.__buscar_rec(nodo.der, titulo)

    # BUSCAR PARCIAL

    def buscar_titulo_parcial(self, fragmento):

        resultados = []

        self.__buscar_parcial_rec(
            self.raiz,
            fragmento.lower(),
            resultados
        )

        return resultados

    def __buscar_parcial_rec(self, nodo, fragmento, resultados):

        if nodo is None:
            return

        self.__buscar_parcial_rec(nodo.izq, fragmento, resultados)

        if fragmento in nodo.libro.get_titulo().lower():
            resultados.append(nodo.libro)

        self.__buscar_parcial_rec(nodo.der, fragmento, resultados)

    # RECORRIDO

    def in_orden(self):

        libros = []

        self.__in_orden_rec(self.raiz, libros)

        return libros

    def __in_orden_rec(self, nodo, libros):

        if nodo is None:
            return

        self.__in_orden_rec(nodo.izq, libros)

        libros.append(nodo.libro)

        self.__in_orden_rec(nodo.der, libros)

    # ELIMINAR

    def eliminar(self, titulo):

        self.raiz, eliminado = self.__eliminar_rec(
            self.raiz,
            titulo.lower()
        )

        if eliminado:
            self.total -= 1

        return eliminado

    def __eliminar_rec(self, nodo, titulo):

        if nodo is None:
            return nodo, False

        clave = nodo.libro.get_titulo().lower()

        if titulo < clave:

            nodo.izq, eliminado = self.__eliminar_rec(
                nodo.izq,
                titulo
            )

            return nodo, eliminado

        elif titulo > clave:

            nodo.der, eliminado = self.__eliminar_rec(
                nodo.der,
                titulo
            )

            return nodo, eliminado

        else:

            # sin hijos izquierdos

            if nodo.izq is None:
                return nodo.der, True

            # sin hijos derechos

            if nodo.der is None:
                return nodo.izq, True

            # dos hijos

            sucesor = self.__minimo(nodo.der)

            nodo.libro = sucesor.libro

            nodo.der, _ = self.__eliminar_rec(
                nodo.der,
                sucesor.libro.get_titulo().lower()
            )

            return nodo, True

    def __minimo(self, nodo):

        while nodo.izq:
            nodo = nodo.izq

        return nodo


# ============================================================
# 3. LISTA ENLAZADA DE USUARIOS
# ============================================================

class NodoUsuario:

    def __init__(self, usuario):

        self.usuario = usuario
        self.siguiente = None


class ListaEnlazadaUsuarios:

    def __init__(self):

        self.cabeza = None
        self.tamano = 0

    def get_tamano(self):
        return self.tamano

    def agregar(self, usuario):

        nuevo = NodoUsuario(usuario)

        nuevo.siguiente = self.cabeza
        self.cabeza = nuevo

        self.tamano += 1

    def buscar_por_id(self, id_usuario):

        actual = self.cabeza

        while actual:

            if actual.usuario.get_id_usuario() == id_usuario:
                return actual.usuario

            actual = actual.siguiente

        return None

    def listar_todos(self):

        usuarios = []

        actual = self.cabeza

        while actual:

            usuarios.append(actual.usuario)

            actual = actual.siguiente

        return usuarios


# ============================================================
# 4. BIBLIOTECA
# ============================================================

class Biblioteca:

    def __init__(self):

        self.abb_libros = ArbolBinarioBusqueda()

        self.lista_usuarios = ListaEnlazadaUsuarios()

        self.prestamos = []

        self.next_id_libro = 1
        self.next_id_usuario = 1
        self.next_id_prestamo = 1

    # ========================================================
    # LIBROS
    # ========================================================

    def agregar_libro(self, titulo, autor,
                      categoria, anio, isbn=None):

        libro = Libro(
            self.next_id_libro,
            titulo,
            autor,
            categoria,
            anio,
            isbn
        )

        self.abb_libros.insertar(libro)

        self.next_id_libro += 1

        print("Libro agregado correctamente.")

    def listar_catalogo(self):

        return self.abb_libros.in_orden()

    def buscar_libro(self, titulo):

        return self.abb_libros.buscar_titulo_parcial(titulo)

    def eliminar_libro(self, titulo):

        eliminado = self.abb_libros.eliminar(titulo)

        if eliminado:
            print("Libro eliminado.")
        else:
            print("Libro no encontrado.")

    # ========================================================
    # USUARIOS
    # ========================================================

    def registrar_usuario(self, nombre,
                           apellido,
                           tipo,
                           email):

        # verificar email duplicado

        for u in self.lista_usuarios.listar_todos():

            if u.get_email().lower() == email.lower():
                print("Ese email ya existe.")
                return

        usuario = Usuario(
            self.next_id_usuario,
            nombre,
            apellido,
            tipo,
            email
        )

        self.lista_usuarios.agregar(usuario)

        self.next_id_usuario += 1

        print("Usuario registrado.")

    def listar_usuarios(self):

        return self.lista_usuarios.listar_todos()

    # ========================================================
    # PRÉSTAMOS
    # ========================================================

    def registrar_prestamo(self,
                           id_libro,
                           id_usuario,
                           dias=14):

        libro = None

        for l in self.abb_libros.in_orden():

            if l.get_id_libro() == id_libro:
                libro = l
                break

        usuario = self.lista_usuarios.buscar_por_id(id_usuario)

        if libro is None:
            print("Libro no encontrado.")
            return

        if usuario is None:
            print("Usuario no encontrado.")
            return

        if not libro.get_estado_disponible():
            print("Libro no disponible.")
            return

        hoy = date.today()

        vence = hoy + timedelta(days=dias)

        prestamo = Prestamo(
            self.next_id_prestamo,
            libro,
            usuario,
            hoy,
            vence
        )

        libro.set_estado_disponible(False)

        usuario.agregar_prestamo(prestamo)

        self.prestamos.append(prestamo)

        self.next_id_prestamo += 1

        print("Préstamo registrado.")

    def registrar_devolucion(self, id_prestamo):

        for p in self.prestamos:

            if p.get_id_prestamo() == id_prestamo:

                if p.get_estado() != 'activo':
                    print("El préstamo ya fue completado.")
                    return

                p.set_estado('completado')

                p.set_fecha_devolucion_real(date.today())

                p.get_libro().set_estado_disponible(True)

                print("Devolución registrada.")

                return

        print("Préstamo no encontrado.")

    def historial_usuario(self, id_usuario):

        usuario = self.lista_usuarios.buscar_por_id(id_usuario)

        if usuario is None:
            return []

        return usuario.get_historial().listar_todos()


# ============================================================
# 5. INTERFAZ
# ============================================================

def separador(titulo=""):

    print("\n" + "=" * 50)

    if titulo:
        print(titulo)
        print("=" * 50)


def mostrar_libros(libros):

    if not libros:
        print("Sin resultados.")
        return

    for libro in libros:
        libro.mostrar_info()
        print()


def menu_libros(bib):

    while True:

        separador("GESTIÓN DE LIBROS")

        print("1. Ver catálogo")
        print("2. Buscar libro")
        print("3. Agregar libro")
        print("4. Eliminar libro")
        print("0. Volver")

        op = input("Opción: ")

        if op == '1':

            mostrar_libros(bib.listar_catalogo())

        elif op == '2':

            texto = input("Título: ")

            resultados = bib.buscar_libro(texto)

            mostrar_libros(resultados)

        elif op == '3':

            titulo = input("Título: ")
            autor = input("Autor: ")
            categoria = input("Categoría: ")

            try:
                anio = int(input("Año: "))
            except ValueError:
                print("Ingrese un número válido.")
                continue

            isbn = input("ISBN (opcional): ")

            if isbn == "":
                isbn = None

            bib.agregar_libro(
                titulo,
                autor,
                categoria,
                anio,
                isbn
            )

        elif op == '4':

            titulo = input("Título exacto: ")

            bib.eliminar_libro(titulo)

        elif op == '0':
            break

        else:
            print("Opción inválida.")


# ============================================================

def menu_usuarios(bib):

    while True:

        separador("GESTIÓN DE USUARIOS")

        print("1. Listar usuarios")
        print("2. Registrar usuario")
        print("3. Historial usuario")
        print("0. Volver")

        op = input("Opción: ")

        if op == '1':

            usuarios = bib.listar_usuarios()

            for u in usuarios:
                u.mostrar_info()
                print()

        elif op == '2':

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

        elif op == '3':

            try:
                uid = int(input("ID usuario: "))
            except ValueError:
                print("Ingrese un número válido.")
                continue

            historial = bib.historial_usuario(uid)

            if not historial:
                print("Sin historial.")
            else:
                for p in historial:
                    p.mostrar_info()
                    print()

        elif op == '0':
            break

        else:
            print("Opción inválida.")


# ============================================================

def menu_prestamos(bib):

    while True:

        separador("GESTIÓN DE PRÉSTAMOS")

        print("1. Registrar préstamo")
        print("2. Registrar devolución")
        print("0. Volver")

        op = input("Opción: ")

        if op == '1':

            try:
                id_libro = int(input("ID libro: "))
                id_usuario = int(input("ID usuario: "))
            except ValueError:
                print("Ingrese números válidos.")
                continue

            dias = input("Días préstamo (14): ")

            try:
                dias = int(dias) if dias else 14
            except ValueError:
                print("Número inválido.")
                continue

            bib.registrar_prestamo(
                id_libro,
                id_usuario,
                dias
            )

        elif op == '2':

            try:
                id_prestamo = int(input("ID préstamo: "))
            except ValueError:
                print("Número inválido.")
                continue

            bib.registrar_devolucion(id_prestamo)

        elif op == '0':
            break

        else:
            print("Opción inválida.")


# ============================================================
# MAIN
# ============================================================

def main():

    bib = Biblioteca()

    while True:

        separador("BIBLIOTECA DIGITAL")

        print("1. Libros")
        print("2. Usuarios")
        print("3. Préstamos")
        print("0. Salir")

        op = input("Opción: ")

        if op == '1':
            menu_libros(bib)

        elif op == '2':
            menu_usuarios(bib)

        elif op == '3':
            menu_prestamos(bib)

        elif op == '0':

            print("Hasta luego.")
            break

        else:
            print("Opción inválida.")


# ============================================================

if __name__ == '__main__':
    main()
