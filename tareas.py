import csv
import os

class Tarea:
    def __init__(self, id, descripcion, prioridad, categoria="General"):
        self.id = id
        self.descripcion = descripcion
        self.prioridad = prioridad
        self.completada = False
        self.categoria = categoria

class Nodo:
    def __init__(self, tarea):
        self.tarea = tarea
        self.siguiente = None

class ListaEnlazada:
    def __init__(self):
        self.cabeza = None
        self.id_actual = 1

    def esta_vacia(self):
        return self.cabeza is None

    def agregar_tarea(self, descripcion, prioridad, categoria):

        if not self.buscar_tarea_descripcion(descripcion):

            self.contador_de_total += 1
            tarea = Tarea(self.id_actual, descripcion, prioridad, categoria)
            nuevo_nodo = Nodo(tarea)
            self.id_actual += 1

            if self.esta_vacia() or tarea.prioridad > self.cabeza.tarea.prioridad:
                nuevo_nodo.siguiente = self.cabeza
                self.cabeza = nuevo_nodo
            else:
                actual = self.cabeza
                while actual.siguiente is not None and actual.siguiente.tarea.prioridad >= tarea.prioridad:
                    actual = actual.siguiente
                nuevo_nodo.siguiente = actual.siguiente
                actual.siguiente = nuevo_nodo

            print("Tarea agregada con éxito.")

        else:

            print("La tarea ya existe")

    def buscar_tarea_descripcion(self,texto):
        actual = self.cabeza
        while actual != None:
            if actual.tarea.descripcion==texto:
                return True
            actual = actual.siguiente
        return False

    def buscar_tarea_id(self,id)->Tarea:# retorna una tarea en caso de encontrarla, sino retorna false
        tarea = False
        actual = self.cabeza
        while actual != None:
            if actual.tarea.id==id:
                tarea = actual.tarea
            actual = actual.siguiente
        return tarea

    def completar_tarea(self, id):
        tarea = self.buscar_tarea_id(id)
        tarea.completada = True
        self.contador_de_pendi -= 1

    def eliminar_tarea(self, id):
        if self.buscar_tarea_id(id)!=False:    
            
            actual = self.cabeza
            previo = None
            while actual is not None:
                if actual.tarea.id == id:
                    if previo is None:
                        self.cabeza = actual.siguiente
                    else:
                        previo.siguiente = actual.siguiente
                    if actual.tarea.completada == False:
                    self.contador_de_total -= 1
                    print(f"Tarea eliminada: {actual.tarea.descripcion}")
                    return
                previo = actual
                actual = actual.siguiente
            print(f"Tarea con ID {id} no encontrada.")
        
        else:
            
            print("La tarea NO existe.")

    def mostrar_tareas(self):
        actual = self.cabeza
        if actual is None:
            print("No hay tareas")
        while actual is not None:
            self.mostrar_una_tarea(actual.tarea)
            actual = actual.siguiente

    def mostrar_tareas_pendientes(self):
        actual = self.cabeza
        if actual is None:
            print("No hay tareas")
        while actual is not None:
            if not actual.tarea.completada:
                self.mostrar_una_tarea(actual.tarea)
            actual = actual.siguiente
        
    def mostrar_una_tarea(self,tarea):
        estado = "Completada" if tarea.completada else "Pendiente"
        print(f"ID: {tarea.id}, Descripción: {tarea.descripcion}, Prioridad: {tarea.prioridad}, Categoría: {tarea.categoria}, Estado: {estado}")

    def mostrar_tareas_descripcion(self,text)->None:
        actual = self.cabeza
        while actual is not None:
            if(text in actual.tarea.descripcion):
                self.mostrar_una_tarea(actual.tarea)
            actual = actual.siguiente
    # F unciones estadisticas:
    def contar_tareas_pendientes_lineal(self)->int:
        actual = self.cabeza
        contador = 0
        while actual is not None:
            if(actual.tarea.completada == False):
                contador += 1
            actual = actual.siguiente
        return contador
    
    def contar_tareas_pendientes_cte(self)->int:
        pass
        
    def mostrar_estadisticas(self)->None:
    pass

    # Carga y guardado de archivos
    def guardar_en_csv(self, archivo):
        with open(archivo, mode='w', newline='') as file:
            writer = csv.writer(file)
            actual = self.cabeza
            while actual is not None:
                writer.writerow([actual.tarea.id, actual.tarea.descripcion, actual.tarea.prioridad, actual.tarea.categoria, actual.tarea.completada])
                actual = actual.siguiente
        print(f"Tareas guardadas en {archivo} con éxito.")

    def cargar_desde_csv(self, archivo):
        if not os.path.exists(archivo):
            print(f"Archivo {archivo} no encontrado.")
            return
        with open(archivo, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                id, descripcion, prioridad, categoria, completada = int(row[0]), row[1], int(row[2]), row[3], row[4] == 'True'
                tarea = Tarea(id, descripcion, prioridad, categoria)
                tarea.completada = completada
                self.agregar_tarea_existente(tarea)
            print(f"Tareas cargadas desde {archivo} con éxito.")

    def agregar_tarea_existente(self, tarea):

        if not self.buscar_tarea_descripcion(tarea.descripcion):
        
            if tarea.completada is not True:
                self.contador_de_pendi += 1
            nuevo_nodo = Nodo(tarea)
            if self.esta_vacia() or tarea.prioridad > self.cabeza.tarea.prioridad:
                nuevo_nodo.siguiente = self.cabeza
                self.cabeza = nuevo_nodo
            else:
                actual = self.cabeza
                while actual.siguiente is not None and actual.siguiente.tarea.prioridad >= tarea.prioridad:
                    actual = actual.siguiente
                nuevo_nodo.siguiente = actual.siguiente
                actual.siguiente = nuevo_nodo
    
            if tarea.id >= self.id_actual:
                self.id_actual = tarea.id + 1
        
        else:
            
            print("La tarea NO existe.")

def menu():
    print("\nMenú:")
    print("1. Agregar tarea")
    print("2. Completar tarea")
    print("3. Eliminar tarea")
    print("4. Mostrar todas las tareas")
    print("5. Mostrar tareas pendientes")
    print("6. Guardar tareas en archivo CSV")
    print("7. Cargar tareas desde archivo CSV")
    print("8. Salir")

def main():
    lista_tareas = ListaEnlazada()
    archivo_csv = 'tareas.csv'

    # Cargar tareas desde CSV si el archivo existe
    lista_tareas.cargar_desde_csv(archivo_csv)

    while True:
        menu()
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            descripcion = input("Ingrese la descripción de la tarea: ")
            while True:
                try:
                    prioridad = int(input("Ingrese la prioridad de la tarea (1 = baja, 2 = media, 3 = alta): "))
                    if prioridad in [1, 2, 3]:
                        break
                    else:
                        print("Por favor, ingrese un número entre 1 y 3.")
                except ValueError:
                    print("Entrada no válida. Debe ingresar un número entero.")
            
            categoria = input("Ingrese la categoría de la tarea: ")
            lista_tareas.agregar_tarea(descripcion, prioridad, categoria)
        
        elif opcion == "2":
            while True:
                try:
                    id_tarea = int(input("Ingrese el ID de la tarea a completar: "))
                    lista_tareas.completar_tarea(id_tarea)
                    break
                except ValueError:
                    print("Entrada no válida. Debe ingresar un número entero.")
                except Exception as e:
                    print(f"Error: {e}")
                    break
        
        elif opcion == "3":
            while True:
                try:
                    id_tarea = int(input("Ingrese el ID de la tarea a eliminar: "))
                    lista_tareas.eliminar_tarea(id_tarea)
                    break
                except ValueError:
                    print("Entrada no válida. Debe ingresar un número entero.")
                except Exception as e:
                    print(f"Error: {e}")
                    break

        elif opcion == "4":
            lista_tareas.mostrar_tareas()
        
        elif opcion == "5":
            lista_tareas.mostrar_tareas_pendientes()
        
        elif opcion == "6":
            lista_tareas.guardar_en_csv(archivo_csv)
        
        elif opcion == "7":
            lista_tareas.cargar_desde_csv(archivo_csv)
        
        elif opcion == "8":
            print("Saliendo del sistema de gestión de tareas.")
            break
        
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")


if __name__ == "__main__":
    main()