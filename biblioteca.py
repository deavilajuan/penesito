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

import mysql.connector
from mysql.connector import Error
from datetime import date, timedelta


# ============================================================
# 1. CLASES DE DOMINIO (POO)
# ============================================================

class Libro:
    """Representa un libro en el catálogo."""

    def __init__(self, id_libro, titulo, autor, categoria,
                 anio_publicacion, isbn=None, estado_disponible=True):
        self.id_libro          = id_libro
        self.titulo            = titulo
        self.autor             = autor
        self.categoria         = categoria
        self.anio_publicacion  = anio_publicacion
        self.isbn              = isbn
        self.estado_disponible = estado_disponible

    def mostrar_info(self):
        estado = "Disponible" if self.estado_disponible else "Prestado"
        print(f"  [{self.id_libro}] {self.titulo}")
        print(f"       Autor    : {self.autor}")
        print(f"       Categoría: {self.categoria}  |  Año: {self.anio_publicacion}")
        print(f"       ISBN     : {self.isbn or 'N/A'}  |  Estado: {estado}")

    def __str__(self):
        return f"Libro({self.id_libro}, '{self.titulo}', '{self.autor}')"


# ------------------------------------------------------------

class NodoPrestamo:
    """Nodo de la lista enlazada de préstamos."""

    def __init__(self, prestamo):
        self.prestamo = prestamo
        self.siguiente = None


class Prestamo:
    """Registra la relación entre un usuario y un libro."""

    def __init__(self, id_prestamo, libro: Libro, usuario,
                 fecha_prestamo, fecha_devolucion_esperada,
                 fecha_devolucion_real=None, estado='activo'):
        self.id_prestamo               = id_prestamo
        self.libro                     = libro
        self.usuario                   = usuario
        self.fecha_prestamo            = fecha_prestamo
        self.fecha_devolucion_esperada = fecha_devolucion_esperada
        self.fecha_devolucion_real     = fecha_devolucion_real
        self.estado                    = estado  # activo | completado | vencido

    def mostrar_info(self):
        print(f"  Préstamo #{self.id_prestamo}")
        print(f"    Libro  : {self.libro.titulo}")
        print(f"    Desde  : {self.fecha_prestamo}  →  "
              f"Vence: {self.fecha_devolucion_esperada}")
        print(f"    Estado : {self.estado.upper()}")


# ------------------------------------------------------------

class ListaEnlazadaPrestamos:
    """Lista enlazada simple para el historial de préstamos de un usuario."""

    def __init__(self):
        self.cabeza  = None
        self.tamaño = 0

    def agregar(self, prestamo: Prestamo):
        nuevo = NodoPrestamo(prestamo)
        nuevo.siguiente = self.cabeza
        self.cabeza   = nuevo
        self.tamaño  += 1

    def buscar_por_id(self, id_prestamo) -> Prestamo | None:
        actual = self.cabeza
        while actual:
            if actual.prestamo.id_prestamo == id_prestamo:
                return actual.prestamo
            actual = actual.siguiente
        return None

    def listar_activos(self):
        activos = []
        actual  = self.cabeza
        while actual:
            if actual.prestamo.estado == 'activo':
                activos.append(actual.prestamo)
            actual = actual.siguiente
        return activos

    def listar_todos(self):
        todos  = []
        actual = self.cabeza
        while actual:
            todos.append(actual.prestamo)
            actual = actual.siguiente
        return todos


# ------------------------------------------------------------

class Usuario:
    """Modela un usuario del sistema."""

    def __init__(self, id_usuario, nombre, apellido, tipo_usuario,
                 email, fecha_registro=None, activo=True):
        self.id_usuario     = id_usuario
        self.nombre         = nombre
        self.apellido       = apellido
        self.tipo_usuario   = tipo_usuario   # estudiante | docente | administrativo
        self.email          = email
        self.fecha_registro = fecha_registro or date.today()
        self.activo         = activo
        self.historial      = ListaEnlazadaPrestamos()

    def agregar_prestamo(self, prestamo: Prestamo):
        self.historial.agregar(prestamo)

    def prestamos_activos(self):
        return self.historial.listar_activos()

    def mostrar_info(self):
        print(f"  [{self.id_usuario}] {self.nombre} {self.apellido}")
        print(f"       Tipo : {self.tipo_usuario}  |  Email: {self.email}")
        print(f"       Activo: {'Sí' if self.activo else 'No'}")

    def __str__(self):
        return f"Usuario({self.id_usuario}, '{self.nombre} {self.apellido}')"


# ============================================================
# 2. ÁRBOL BINARIO DE BÚSQUEDA (ABB) — catálogo de libros
# ============================================================

class NodoABB:
    """Nodo del árbol binario de búsqueda."""

    def __init__(self, libro: Libro):
        self.libro    = libro
        self.izq      = None
        self.der      = None


class ArbolBinarioBusqueda:
    """
    ABB ordenado por título (alfabético).
    Soporta: insertar, buscar, eliminar, recorrido in-orden.
    """

    def __init__(self):
        self.raiz = None
        self.total = 0

    # --- Insertar ---
    def insertar(self, libro: Libro):
        self.raiz = self.__insertar_rec(self.raiz, libro)
        self.total += 1

    def __insertar_rec(self, nodo, libro):
        if nodo is None:
            return NodoABB(libro)
        clave     = libro.titulo.lower()
        clave_nod = nodo.libro.titulo.lower()
        if clave < clave_nod:
            nodo.izq = self.__insertar_rec(nodo.izq, libro)
        elif clave > clave_nod:
            nodo.der = self.__insertar_rec(nodo.der, libro)
        else:
            # Título duplicado: actualizar referencia
            nodo.libro = libro
        return nodo

    # --- Buscar por título exacto ---
    def buscar_titulo(self, titulo: str) -> Libro | None:
        return self.__buscar_rec(self.raiz, titulo.lower())

    def __buscar_rec(self, nodo, titulo_lower):
        if nodo is None:
            return None
        clave = nodo.libro.titulo.lower()
        if titulo_lower == clave:
            return nodo.libro
        if titulo_lower < clave:
            return self.__buscar_rec(nodo.izq, titulo_lower)
        return self.__buscar_rec(nodo.der, titulo_lower)

    # --- Búsqueda parcial por título (contiene la cadena) ---
    def buscar_titulo_parcial(self, fragmento: str) -> list[Libro]:
        resultados = []
        self.__buscar_parcial_rec(self.raiz, fragmento.lower(), resultados)
        return resultados

    def __buscar_parcial_rec(self, nodo, fragmento, resultados):
        if nodo is None:
            return
        self.__buscar_parcial_rec(nodo.izq, fragmento, resultados)
        if fragmento in nodo.libro.titulo.lower():
            resultados.append(nodo.libro)
        self.__buscar_parcial_rec(nodo.der, fragmento, resultados)

    # --- Buscar por autor (recorrido completo) ---
    def buscar_autor(self, autor: str) -> list[Libro]:
        resultados = []
        self.__buscar_campo_rec(self.raiz, autor.lower(),
                                lambda l: l.autor.lower(), resultados)
        return resultados

    # --- Buscar por categoría ---
    def buscar_categoria(self, categoria: str) -> list[Libro]:
        resultados = []
        self.__buscar_campo_rec(self.raiz, categoria.lower(),
                                lambda l: l.categoria.lower(), resultados)
        return resultados

    def __buscar_campo_rec(self, nodo, valor, extractor, resultados):
        if nodo is None:
            return
        self.__buscar_campo_rec(nodo.izq, valor, extractor, resultados)
        if valor in extractor(nodo.libro):
            resultados.append(nodo.libro)
        self.__buscar_campo_rec(nodo.der, valor, extractor, resultados)

    # --- Eliminar ---
    def eliminar(self, titulo: str):
        self.raiz, eliminado = self.__eliminar_rec(self.raiz, titulo.lower())
        if eliminado:
            self.total -= 1
        return eliminado

    def __eliminar_rec(self, nodo, titulo_lower):
        if nodo is None:
            return nodo, False
        clave = nodo.libro.titulo.lower()
        if titulo_lower < clave:
            nodo.izq, ok = self.__eliminar_rec(nodo.izq, titulo_lower)
            return nodo, ok
        if titulo_lower > clave:
            nodo.der, ok = self.__eliminar_rec(nodo.der, titulo_lower)
            return nodo, ok
        # Nodo encontrado
        if nodo.izq is None:
            return nodo.der, True
        if nodo.der is None:
            return nodo.izq, True
        # Dos hijos: reemplazar con el mínimo del subárbol derecho
        sucesor = self.__minimo(nodo.der)
        nodo.libro = sucesor.libro
        nodo.der, _ = self.__eliminar_rec(nodo.der, sucesor.libro.titulo.lower())
        return nodo, True

    def __minimo(self, nodo):
        while nodo.izq:
            nodo = nodo.izq
        return nodo

    # --- Recorrido in-orden (orden alfabético) ---
    def in_orden(self) -> list[Libro]:
        libros = []
        self.__in_orden_rec(self.raiz, libros)
        return libros

    def __in_orden_rec(self, nodo, libros):
        if nodo is None:
            return
        self.__in_orden_rec(nodo.izq, libros)
        libros.append(nodo.libro)
        self.__in_orden_rec(nodo.der, libros)


# ============================================================
# 3. LISTA ENLAZADA DE USUARIOS
# ============================================================

class NodoUsuario:
    def __init__(self, usuario: Usuario):
        self.usuario   = usuario
        self.siguiente = None


class ListaEnlazadaUsuarios:
    """Lista enlazada simple para gestión de usuarios."""

    def __init__(self):
        self.cabeza = None
        self.tamaño = 0

    def agregar(self, usuario: Usuario):
        nuevo           = NodoUsuario(usuario)
        nuevo.siguiente = self.cabeza
        self.cabeza   = nuevo
        self.tamaño  += 1

    def buscar_por_id(self, id_usuario: int) -> Usuario | None:
        actual = self.cabeza
        while actual:
            if actual.usuario.id_usuario == id_usuario:
                return actual.usuario
            actual = actual.siguiente
        return None

    def buscar_por_email(self, email: str) -> Usuario | None:
        actual = self.cabeza
        while actual:
            if actual.usuario.email.lower() == email.lower():
                return actual.usuario
            actual = actual.siguiente
        return None

    def listar_todos(self) -> list[Usuario]:
        usuarios = []
        actual   = self.cabeza
        while actual:
            usuarios.append(actual.usuario)
            actual = actual.siguiente
        return usuarios

    def eliminar(self, id_usuario: int) -> bool:
        actual   = self.cabeza
        anterior = None
        while actual:
            if actual.usuario.id_usuario == id_usuario:
                if anterior:
                    anterior.siguiente = actual.siguiente
                else:
                    self.cabeza = actual.siguiente
                self.tamaño -= 1
                return True
            anterior = actual
            actual   = actual.siguiente
        return False


# ============================================================
# 4. MÓDULOS DE INTEGRACIÓN MySQL
# ============================================================

class ModuloConexion:
    """Gestiona la conexión con MySQL."""

    def __init__(self, host='localhost', port=3306,
                 user='root', password='', database='biblioteca_digital'):
        self.__config = {
            'host':     host,
            'port':     port,
            'user':     user,
            'password': password,
            'database': database,
        }
        self.__conexion = None

    def conectar(self):
        try:
            self.__conexion = mysql.connector.connect(**self.__config)
            if self.__conexion.is_connected():
                print("✔ Conexión a MySQL establecida.")
                return True
        except Error as e:
            print(f"✘ Error al conectar a MySQL: {e}")
        return False

    def desconectar(self):
        if self.__conexion and self.__conexion.is_connected():
            self.__conexion.close()
            print("✔ Conexión a MySQL cerrada.")

    def cursor(self, dictionary=True):
        return self.__conexion.cursor(dictionary=dictionary)

    def commit(self):
        self.__conexion.commit()

    def rollback(self):
        self.__conexion.rollback()

    def get_conexion(self):
        return self.__conexion


# ------------------------------------------------------------

class ModuloCarga:
    """Carga datos de MySQL y construye las estructuras en memoria."""

    def __init__(self, modulo_conexion: ModuloConexion):
        self.__mc = modulo_conexion

    def cargar_libros(self, abb: ArbolBinarioBusqueda):
        cursor = self.__mc.cursor()
        cursor.execute("SELECT * FROM libros")
        filas = cursor.fetchall()
        cursor.close()
        for f in filas:
            libro = Libro(
                id_libro          = f['id_libro'],
                titulo            = f['titulo'],
                autor             = f['autor'],
                categoria         = f['categoria'],
                anio_publicacion  = f['anio_publicacion'],
                isbn              = f['isbn'],
                estado_disponible = bool(f['estado_disponible'])
            )
            abb.insertar(libro)
        print(f"  → {abb.get_total()} libro(s) cargado(s) en el ABB.")

    def cargar_usuarios(self, lista: ListaEnlazadaUsuarios):
        cursor = self.__mc.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE activo = TRUE")
        filas = cursor.fetchall()
        cursor.close()
        for f in filas:
            usuario = Usuario(
                id_usuario     = f['id_usuario'],
                nombre         = f['nombre'],
                apellido       = f['apellido'],
                tipo_usuario   = f['tipo_usuario'],
                email          = f['email'],
                fecha_registro = f['fecha_registro'],
                activo         = bool(f['activo'])
            )
            lista.agregar(usuario)
        print(f"  → {lista.get_tamaño()} usuario(s) cargado(s) en la lista enlazada.")

    def cargar_prestamos(self, lista_usuarios: ListaEnlazadaUsuarios,
                         abb: ArbolBinarioBusqueda) -> list:
        cursor = self.__mc.cursor()
        cursor.execute("""
            SELECT p.*, l.titulo AS libro_titulo, u.nombre, u.apellido
            FROM prestamos p
            JOIN libros   l ON p.id_libro   = l.id_libro
            JOIN usuarios u ON p.id_usuario = u.id_usuario
        """)
        filas = cursor.fetchall()
        cursor.close()
        prestamos = []
        for f in filas:
            libro   = abb.buscar_titulo(f['libro_titulo'])
            usuario = lista_usuarios.buscar_por_id(f['id_usuario'])
            if libro and usuario:
                prestamo = Prestamo(
                    id_prestamo               = f['id_prestamo'],
                    libro                     = libro,
                    usuario                   = usuario,
                    fecha_prestamo            = f['fecha_prestamo'],
                    fecha_devolucion_esperada = f['fecha_devolucion_esperada'],
                    fecha_devolucion_real     = f['fecha_devolucion_real'],
                    estado                    = f['estado']
                )
                usuario.agregar_prestamo(prestamo)
                prestamos.append(prestamo)
        print(f"  → {len(prestamos)} préstamo(s) cargado(s).")
        return prestamos


# ------------------------------------------------------------

class ModuloPersistencia:
    """Traduce operaciones en memoria a consultas SQL."""

    def __init__(self, modulo_conexion: ModuloConexion):
        self.__mc = modulo_conexion

    # --- Libros ---
    def insertar_libro(self, libro: Libro) -> int | None:
        try:
            cursor = self.__mc.cursor()
            sql = """INSERT INTO libros
                     (titulo, autor, categoria, anio_publicacion, isbn, estado_disponible)
                     VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (
                libro.get_titulo(), libro.get_autor(), libro.get_categoria(),
                libro.get_anio_publicacion(), libro.get_isbn(), libro.get_estado_disponible()
            ))
            self.__mc.commit()
            new_id = cursor.lastrowid
            cursor.close()
            return new_id
        except Error as e:
            self.__mc.rollback()
            print(f"✘ Error al insertar libro: {e}")
            return None

    def actualizar_estado_libro(self, id_libro: int, disponible: bool):
        try:
            cursor = self.__mc.cursor()
            cursor.execute(
                "UPDATE libros SET estado_disponible = %s WHERE id_libro = %s",
                (disponible, id_libro)
            )
            self.__mc.commit()
            cursor.close()
        except Error as e:
            self.__mc.rollback()
            print(f"✘ Error al actualizar libro: {e}")

    def eliminar_libro(self, id_libro: int) -> bool:
        try:
            cursor = self.__mc.cursor()
            cursor.execute(
                "DELETE FROM libros WHERE id_libro = %s", (id_libro,)
            )
            self.__mc.commit()
            ok = cursor.rowcount > 0
            cursor.close()
            return ok
        except Error as e:
            self.__mc.rollback()
            print(f"✘ Error al eliminar libro: {e}")
            return False

    # --- Usuarios ---
    def insertar_usuario(self, usuario: Usuario) -> int | None:
        try:
            cursor = self.__mc.cursor()
            sql = """INSERT INTO usuarios
                     (nombre, apellido, tipo_usuario, email, fecha_registro)
                     VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(sql, (
                usuario.get_nombre(), usuario.get_apellido(),
                usuario.get_tipo_usuario(), usuario.get_email(), usuario.get_fecha_registro()
            ))
            self.__mc.commit()
            new_id = cursor.lastrowid
            cursor.close()
            return new_id
        except Error as e:
            self.__mc.rollback()
            print(f"✘ Error al insertar usuario: {e}")
            return None

    # --- Préstamos ---
    def insertar_prestamo(self, prestamo: Prestamo) -> int | None:
        try:
            cursor = self.__mc.cursor()
            sql = """INSERT INTO prestamos
                     (id_libro, id_usuario, fecha_prestamo,
                      fecha_devolucion_esperada, estado)
                     VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(sql, (
                prestamo.get_libro().get_id_libro(),
                prestamo.get_usuario().get_id_usuario(),
                prestamo.get_fecha_prestamo(),
                prestamo.get_fecha_devolucion_esperada(),
                prestamo.get_estado()
            ))
            self.__mc.commit()
            new_id = cursor.lastrowid
            cursor.close()
            return new_id
        except Error as e:
            self.__mc.rollback()
            print(f"✘ Error al insertar préstamo: {e}")
            return None

    def devolver_prestamo(self, id_prestamo: int, fecha_real: date):
        try:
            cursor = self.__mc.cursor()
            cursor.execute("""
                UPDATE prestamos
                SET estado = 'completado', fecha_devolucion_real = %s
                WHERE id_prestamo = %s
            """, (fecha_real, id_prestamo))
            self.__mc.commit()
            cursor.close()
        except Error as e:
            self.__mc.rollback()
            print(f"✘ Error al registrar devolución: {e}")


# ============================================================
# 5. CLASE BIBLIOTECA — coordinador principal
# ============================================================

class Biblioteca:
    """
    Contenedor principal del sistema.
    Coordina el ABB de libros, la lista de usuarios y
    los préstamos activos.
    """

    def __init__(self, modulo_conexion: ModuloConexion):
        self.__abb_libros       = ArbolBinarioBusqueda()
        self.__lista_usuarios   = ListaEnlazadaUsuarios()
        self.__prestamos        = []          # lista Python de Prestamo
        self.__mc               = modulo_conexion
        self.__persistencia     = ModuloPersistencia(modulo_conexion)

    # ---- CARGA INICIAL ----

    def cargar_datos(self):
        print("\n── Cargando datos desde MySQL ──")
        carga = ModuloCarga(self.__mc)
        carga.cargar_libros(self.__abb_libros)
        carga.cargar_usuarios(self.__lista_usuarios)
        self.__prestamos = carga.cargar_prestamos(
            self.__lista_usuarios, self.__abb_libros
        )
        print("── Carga completada ──\n")

    # ---- GESTIÓN DE LIBROS ----

    def agregar_libro(self, titulo, autor, categoria,
                      anio_publicacion, isbn=None) -> Libro | None:
        # Crear objeto temporal para persistir
        libro_temp = Libro(0, titulo, autor, categoria, anio_publicacion, isbn)
        new_id = self.__persistencia.insertar_libro(libro_temp)
        if new_id:
            libro = Libro(new_id, titulo, autor, categoria,
                          anio_publicacion, isbn)
            self.__abb_libros.insertar(libro)
            print(f"✔ Libro '{titulo}' agregado con ID {new_id}.")
            return libro
        return None

    def buscar_libro_titulo(self, titulo: str):
        resultado = self.__abb_libros.buscar_titulo_parcial(titulo)
        return resultado

    def buscar_libro_autor(self, autor: str):
        return self.__abb_libros.buscar_autor(autor)

    def buscar_libro_categoria(self, categoria: str):
        return self.__abb_libros.buscar_categoria(categoria)

    def listar_catalogo(self):
        return self.__abb_libros.in_orden()

    def eliminar_libro(self, titulo: str) -> bool:
        libro = self.__abb_libros.buscar_titulo(titulo)
        if not libro:
            print(f"✘ Libro '{titulo}' no encontrado.")
            return False
        # Verificar préstamos activos
        for p in self.__prestamos:
            if p.get_libro().get_id_libro() == libro.get_id_libro() and p.get_estado() == 'activo':
                print(f"✘ El libro tiene préstamos activos. No se puede eliminar.")
                return False
        ok_db = self.__persistencia.eliminar_libro(libro.get_id_libro())
        if ok_db:
            self.__abb_libros.eliminar(titulo)
            print(f"✔ Libro '{titulo}' eliminado.")
        return ok_db

    # ---- GESTIÓN DE USUARIOS ----

    def registrar_usuario(self, nombre, apellido, tipo_usuario, email) -> Usuario | None:
        usuario_temp = Usuario(0, nombre, apellido, tipo_usuario, email)
        new_id = self.__persistencia.insertar_usuario(usuario_temp)
        if new_id:
            usuario = Usuario(new_id, nombre, apellido, tipo_usuario, email)
            self.__lista_usuarios.agregar(usuario)
            print(f"✔ Usuario '{nombre} {apellido}' registrado con ID {new_id}.")
            return usuario
        return None

    def buscar_usuario_id(self, id_usuario: int) -> Usuario | None:
        return self.__lista_usuarios.buscar_por_id(id_usuario)

    def listar_usuarios(self):
        return self.__lista_usuarios.listar_todos()

    # ---- GESTIÓN DE PRÉSTAMOS ----

    def registrar_prestamo(self, id_libro: int, id_usuario: int,
                           dias_prestamo: int = 14) -> Prestamo | None:
        # Buscar libro por ID en el ABB (recorrido)
        libro = None
        for l in self.__abb_libros.in_orden():
            if l.get_id_libro() == id_libro:
                libro = l
                break

        usuario = self.__lista_usuarios.buscar_por_id(id_usuario)

        if not libro:
            print("✘ Libro no encontrado.")
            return None
        if not usuario:
            print("✘ Usuario no encontrado.")
            return None
        if not libro.get_estado_disponible():
            print(f"✘ El libro '{libro.get_titulo()}' no está disponible.")
            return None

        hoy     = date.today()
        vence   = hoy + timedelta(days=dias_prestamo)
        prestamo_temp = Prestamo(0, libro, usuario, hoy, vence)
        new_id  = self.__persistencia.insertar_prestamo(prestamo_temp)

        if new_id:
            prestamo = Prestamo(new_id, libro, usuario, hoy, vence)
            # Actualizar estado en memoria y BD
            libro.set_estado_disponible(False)
            self.__persistencia.actualizar_estado_libro(libro.get_id_libro(), False)
            usuario.agregar_prestamo(prestamo)
            self.__prestamos.append(prestamo)
            print(f"✔ Préstamo registrado (ID {new_id}). "
                  f"Vence: {vence}")
            return prestamo
        return None

    def registrar_devolucion(self, id_prestamo: int) -> bool:
        prestamo = None
        for p in self.__prestamos:
            if p.get_id_prestamo() == id_prestamo:
                prestamo = p
                break

        if not prestamo:
            print("✘ Préstamo no encontrado.")
            return False
        if prestamo.get_estado() != 'activo':
            print("✘ El préstamo ya fue completado o está vencido.")
            return False

        hoy = date.today()
        prestamo.set_estado('completado')
        prestamo.set_fecha_devolucion_real(hoy)
        prestamo.get_libro().set_estado_disponible(True)

        self.__persistencia.devolver_prestamo(id_prestamo, hoy)
        self.__persistencia.actualizar_estado_libro(
            prestamo.get_libro().get_id_libro(), True
        )
        print(f"✔ Devolución registrada. Libro '{prestamo.get_libro().get_titulo()}' disponible.")
        return True

    def historial_usuario(self, id_usuario: int):
        usuario = self.__lista_usuarios.buscar_por_id(id_usuario)
        if not usuario:
            print("✘ Usuario no encontrado.")
            return []
        return usuario.get_historial().listar_todos()


# ============================================================
# 6. INTERFAZ DE CONSOLA (menú principal)
# ============================================================

def separador(titulo=""):
    print("\n" + "═" * 55)
    if titulo:
        print(f"  {titulo}")
        print("═" * 55)

def mostrar_libros(libros):
    if not libros:
        print("  (Sin resultados)")
    for l in libros:
        l.mostrar_info()
        print()

def menu_libros(bib: Biblioteca):
    while True:
        separador("GESTIÓN DE LIBROS")
        print("  1. Ver catálogo completo")
        print("  2. Buscar por título")
        print("  3. Buscar por autor")
        print("  4. Buscar por categoría")
        print("  5. Agregar libro")
        print("  6. Eliminar libro")
        print("  0. Volver")
        op = input("\n  Opción: ").strip()

        if op == '1':
            separador("CATÁLOGO")
            mostrar_libros(bib.listar_catalogo())

        elif op == '2':
            t = input("  Título (o fragmento): ").strip()
            mostrar_libros(bib.buscar_libro_titulo(t))

        elif op == '3':
            a = input("  Autor (o fragmento): ").strip()
            mostrar_libros(bib.buscar_libro_autor(a))

        elif op == '4':
            c = input("  Categoría: ").strip()
            mostrar_libros(bib.buscar_libro_categoria(c))

        elif op == '5':
            titulo  = input("  Título       : ").strip()
            autor   = input("  Autor        : ").strip()
            cat     = input("  Categoría    : ").strip()
            anio    = int(input("  Año publicación: ").strip())
            isbn    = input("  ISBN (Enter para omitir): ").strip() or None
            bib.agregar_libro(titulo, autor, cat, anio, isbn)

        elif op == '6':
            titulo = input("  Título exacto: ").strip()
            bib.eliminar_libro(titulo)

        elif op == '0':
            break

def menu_usuarios(bib: Biblioteca):
    while True:
        separador("GESTIÓN DE USUARIOS")
        print("  1. Listar usuarios")
        print("  2. Registrar usuario")
        print("  3. Ver historial de préstamos")
        print("  0. Volver")
        op = input("\n  Opción: ").strip()

        if op == '1':
            separador("USUARIOS REGISTRADOS")
            for u in bib.listar_usuarios():
                u.mostrar_info()
                print()

        elif op == '2':
            nombre   = input("  Nombre   : ").strip()
            apellido = input("  Apellido : ").strip()
            print("  Tipos: estudiante / docente / administrativo")
            tipo     = input("  Tipo     : ").strip()
            email    = input("  Email    : ").strip()
            bib.registrar_usuario(nombre, apellido, tipo, email)

        elif op == '3':
            uid = int(input("  ID del usuario: ").strip())
            historial = bib.historial_usuario(uid)
            if historial:
                separador("HISTORIAL")
                for p in historial:
                    p.mostrar_info()
                    print()
            else:
                print("  (Sin préstamos registrados)")

        elif op == '0':
            break

def menu_prestamos(bib: Biblioteca):
    while True:
        separador("GESTIÓN DE PRÉSTAMOS")
        print("  1. Registrar préstamo")
        print("  2. Registrar devolución")
        print("  0. Volver")
        op = input("\n  Opción: ").strip()

        if op == '1':
            id_libro   = int(input("  ID del libro  : ").strip())
            id_usuario = int(input("  ID del usuario: ").strip())
            dias       = input("  Días de préstamo (Enter = 14): ").strip()
            dias       = int(dias) if dias else 14
            bib.registrar_prestamo(id_libro, id_usuario, dias)

        elif op == '2':
            id_prestamo = int(input("  ID del préstamo: ").strip())
            bib.registrar_devolucion(id_prestamo)

        elif op == '0':
            break

def main():
    separador("BIBLIOTECA DIGITAL — UTB")
    print("  Ingresa los datos de conexión a MySQL:")
    host     = input("  Host     (localhost): ").strip() or 'localhost'
    port     = input("  Puerto   (3306)     : ").strip() or '3306'
    user     = input("  Usuario  (root)     : ").strip() or 'root'
    password = input("  Contraseña          : ").strip()
    database = input("  Base de datos (biblioteca_digital): ").strip() \
               or 'biblioteca_digital'

    mc = ModuloConexion(host, int(port), user, password, database)
    if not mc.conectar():
        print("No se pudo conectar. Verifica los datos e inténtalo de nuevo.")
        return

    bib = Biblioteca(mc)
    bib.cargar_datos()

    while True:
        separador("MENÚ PRINCIPAL")
        print("  1. Libros")
        print("  2. Usuarios")
        print("  3. Préstamos")
        print("  0. Salir")
        op = input("\n  Opción: ").strip()

        if   op == '1': menu_libros(bib)
        elif op == '2': menu_usuarios(bib)
        elif op == '3': menu_prestamos(bib)
        elif op == '0':
            mc.desconectar()
            print("\n¡Hasta luego!\n")
            break
        else:
            print("  Opción inválida.")

if __name__ == '__main__':
    main()
