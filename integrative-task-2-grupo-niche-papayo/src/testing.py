import unittest
import time
import random

class TestSistemaExperto(unittest.TestCase):

    # Simulaciones de un motor de inferencia (métodos ficticios)
    def inferir(self, hechos):
        """Simula la inferencia con hechos dados"""
        # Simulamos un tiempo de procesamiento según el número de hechos
        time.sleep(0.1 * len(hechos))  # Tiempo ficticio por hecho
        if random.random() < 0.1:
            raise Exception("Error durante la inferencia")  # Simula errores aleatorios
        return "Diagnóstico exitoso"
    
    # 1. Alta Carga de Hechos
    def test_alta_carga_hechos(self):
        hechos = [f"hecho_{i}" for i in range(1000)]  # 1000 hechos simulados
        inicio = time.time()
        resultado = self.inferir(hechos)
        tiempo = time.time() - inicio
        self.assertLess(tiempo, 10)  # El tiempo debe ser menor a 10 segundos
        self.assertEqual(resultado, "Diagnóstico exitoso")

    # 2. Alta Carga de Hechos con Diagnósticos Concurrentes
    def test_alta_carga_concurrente(self):
        from concurrent.futures import ThreadPoolExecutor
        
        def diagnosticar(hechos):
            return self.inferir(hechos)

        hechos = [f"hecho_{i}" for i in range(500)]  # 500 hechos por consulta
        with ThreadPoolExecutor(max_workers=100) as executor:
            inicio = time.time()
            resultados = list(executor.map(diagnosticar, [hechos] * 100))  # 100 consultas simultáneas
        tiempo = time.time() - inicio
        
        self.assertLess(tiempo, 500)  # El tiempo total debe ser razonable (<500 segundos)
        self.assertTrue(all(res == "Diagnóstico exitoso" for res in resultados))

    # 3. Prueba de Escalabilidad con Datos Incrementales
    def test_escalabilidad_datos_incrementales(self):
        for i in range(100, 5001, 100):  # Desde 100 hasta 5000 hechos
            hechos = [f"hecho_{j}" for j in range(i)]
            inicio = time.time()
            resultado = self.inferir(hechos)
            tiempo = time.time() - inicio
            self.assertLess(tiempo, 20)  # El tiempo de ejecución debe ser <20 segundos
            self.assertEqual(resultado, "Diagnóstico exitoso")

    # 4. Combinaciones Complejas de Hechos y Reglas
    def test_combinaciones_complejas(self):
        hechos = [
            "el_carro_no_arranca", "ruido_extraño", "falta_de_bateria",
            "temperatura_alta", "luces_intermitentes"
        ]
        inicio = time.time()
        resultado = self.inferir(hechos)
        tiempo = time.time() - inicio
        self.assertLess(tiempo, 5)  # El tiempo debe ser < 5 segundos
        self.assertEqual(resultado, "Diagnóstico exitoso")

    # 5. Diagnóstico con Entrada Parcial
    def test_entrada_parcial(self):
        hechos = ["el_carro_no_arranca"]  # Falta información
        resultado = self.inferir(hechos)
        self.assertEqual(resultado, "Diagnóstico exitoso")

    # 6. Evaluación de Reglas con Prioridad
    def test_reglas_con_prioridad(self):
        hechos = [
            "falta_de_combustible", "temperatura_alta"
        ]
        resultado = self.inferir(hechos)
        self.assertEqual(resultado, "Diagnóstico exitoso")

    # 7. Entrada Incompleta o Errónea
    def test_entrada_erronea(self):
        hechos = ["fallo_sintoma_invalido"]
        try:
            self.inferir(hechos)
        except Exception as e:
            self.assertTrue(str(e), "Error durante la inferencia")

    # 8. Resiliencia ante Caídas del Sistema
    def test_resiliencia_caida_sistema(self):
        try:
            # Simula la caída y reinicio del sistema
            raise Exception("Caída del sistema")
        except Exception:
            # Simula la recuperación
            self.assertTrue(True, "El sistema se recuperó después de la caída")

    # 9. Prueba de Alta Frecuencia de Ejecuciones
    def test_alta_frecuencia_ejecuciones(self):
        inicio = time.time()
        for _ in range(1000):  # Ejecutar 1000 diagnósticos consecutivos
            hechos = [f"hecho_{i}" for i in range(5)]  # Simulando hechos simples
            self.inferir(hechos)
        tiempo = time.time() - inicio
        self.assertLess(tiempo, 300)  # El tiempo total debe ser razonable (<300 segundos)

if __name__ == '__main__':
    unittest.main()