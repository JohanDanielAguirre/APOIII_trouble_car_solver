# -*- coding: utf-8 -*-
"""firstversion_bayes.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1bA7cTTILr26r3khbjWmMarXY-92jS-Lb
"""

#pip install pgmpy

from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
from experta import *


class Match(Fact):
    """Info about the vechicle."""
    pass

model = BayesianNetwork([
    ('Switch_Sound', 'Starting_Problems'),
    ('Battery_Test', 'Starting_Problems'),
    ('Physical_Switch_Damage', 'Starting_Problems'),
    ('Starter_Sound', 'Starting_Problems'),
    ('Manual_Start', 'Starting_Problems')
])

# 2. Definir las tablas de probabilidad condicional (CPTs)
# Probabilidad de cada causa (prior)
cpd_switch_sound = TabularCPD(
    variable='Switch_Sound', variable_card=2,
    values=[[0.25], [0.75]],
    state_names={'Switch_Sound': ['Yes', 'No']}
)

cpd_battery_test = TabularCPD(
    variable='Battery_Test', variable_card=2,
    values=[[0.5], [0.5]],
    state_names={'Battery_Test': ['Pass', 'Fail']}
)

cpd_physical_switch_damage = TabularCPD(
    variable='Physical_Switch_Damage', variable_card=2,
    values=[[0.1], [0.9]],
    state_names={'Physical_Switch_Damage': ['Yes', 'No']}
)

cpd_starter_sound = TabularCPD(
    variable='Starter_Sound', variable_card=2,
    values=[[0.1], [0.9]],
    state_names={'Starter_Sound': ['Normal', 'Weird']}
)

cpd_manual_start = TabularCPD(
    variable='Manual_Start', variable_card=2,
    values=[[0.05], [0.95]],
    state_names={'Manual_Start': ['Possible', 'Not_Possible']}
)

# Probabilidad condicional para el problema de arranque basado en las causas
cpd_starting_problems = TabularCPD(
    variable='Starting_Problems', variable_card=2,
    values=[
        # Probabilidad de "Yes" (problema)
        [0.9, 0.6, 0.7, 0.4, 0.3, 0.8, 0.5, 0.4, 0.6, 0.2, 0.9, 0.5, 0.7, 0.4, 0.3, 0.6, 0.8, 0.4, 0.6, 0.3, 0.7, 0.4, 0.8, 0.3, 0.5, 0.4, 0.6, 0.7, 0.3, 0.5, 0.6, 0.4],
        # Probabilidad de "No" (sin problema)
        [0.1, 0.4, 0.3, 0.6, 0.7, 0.2, 0.5, 0.6, 0.4, 0.8, 0.1, 0.5, 0.3, 0.6, 0.7, 0.4, 0.2, 0.6, 0.4, 0.7, 0.3, 0.6, 0.2, 0.7, 0.5, 0.6, 0.4, 0.3, 0.7, 0.5, 0.4, 0.6]
    ],
    evidence=['Switch_Sound', 'Battery_Test', 'Physical_Switch_Damage', 'Starter_Sound', 'Manual_Start'],
    evidence_card=[2, 2, 2, 2, 2],
    state_names={
        'Starting_Problems': ['Yes', 'No'],
        'Switch_Sound': ['Yes', 'No'],
        'Battery_Test': ['Pass', 'Fail'],
        'Physical_Switch_Damage': ['Yes', 'No'],
        'Starter_Sound': ['Normal', 'Weird'],
        'Manual_Start': ['Possible', 'Not_Possible']
    }
)

# 3. Agregar los CPDs al modelo
model.add_cpds(
    cpd_switch_sound, cpd_battery_test, cpd_physical_switch_damage,
    cpd_starter_sound, cpd_manual_start, cpd_starting_problems
)

model.add_edges_from([
    ('AC_Filter', 'AC_Odors'),
    ('AC_Hoses', 'AC_Odors'),
    ('AC_Internal_Mode', 'AC_Odors'),
    ('AC_Test', 'AC_Hot_Air'),
    ('AC_Fuses', 'AC_Hot_Air'),
    ('AC_Current_Connection', 'AC_Hot_Air'),
    ('AC_Refrigerant_Level', 'AC_Hot_Air'),
    ('AC_Slow_Electrical_Systems', 'AC_Hot_Air')
])

# Definir las tablas de probabilidad condicional (CPTs) para Aire Acondicionado

# Malos olores
cpd_ac_filter = TabularCPD(
    variable='AC_Filter', variable_card=2,
    values=[[0.4], [0.6]],
    state_names={'AC_Filter': ['Obstructed', 'Clean']}
)

cpd_ac_hoses = TabularCPD(
    variable='AC_Hoses', variable_card=2,
    values=[[0.2], [0.8]],
    state_names={'AC_Hoses': ['Damaged', 'Intact']}
)

cpd_ac_internal_mode = TabularCPD(
    variable='AC_Internal_Mode', variable_card=2,
    values=[[0.2], [0.8]],
    state_names={'AC_Internal_Mode': ['External', 'Internal']}
)

cpd_ac_odors = TabularCPD(
    variable='AC_Odors', variable_card=2,
    values=[
        # Odors (Yes)    No Odors
        [0.9, 0.7, 0.8, 0.5, 0.4, 0.3, 0.3, 0.1],
        [0.1, 0.3, 0.2, 0.5, 0.6, 0.7, 0.7, 0.9]
    ],
    evidence=['AC_Filter', 'AC_Hoses', 'AC_Internal_Mode'],
    evidence_card=[2, 2, 2],
    state_names={
        'AC_Odors': ['Yes', 'No'],
        'AC_Filter': ['Obstructed', 'Clean'],
        'AC_Hoses': ['Damaged', 'Intact'],
        'AC_Internal_Mode': ['External', 'Internal']
    }
)


# Aire caliente
cpd_ac_test = TabularCPD(
    variable='AC_Test', variable_card=2,
    values=[[0.1], [0.9]],
    state_names={'AC_Test': ['Done', 'Not_Done']}
)

cpd_ac_fuses = TabularCPD(
    variable='AC_Fuses', variable_card=2,
    values=[[0.3], [0.7]],
    state_names={'AC_Fuses': ['Burned', 'Good']}
)

cpd_ac_current_connection = TabularCPD(
    variable='AC_Current_Connection', variable_card=2,
    values=[[0.15], [0.85]],
    state_names={'AC_Current_Connection': ['Bad', 'Good']}
)

cpd_ac_refrigerant_level = TabularCPD(
    variable='AC_Refrigerant_Level', variable_card=3,
    values=[[0.35], [0.4], [0.25]],
    state_names={'AC_Refrigerant_Level': ['Low', 'Medium', 'High']}
)

cpd_ac_slow_electrical_systems = TabularCPD(
    variable='AC_Slow_Electrical_Systems', variable_card=2,
    values=[[0.1], [0.9]],
    state_names={'AC_Slow_Electrical_Systems': ['Slow', 'Normal']}
)

cpd_ac_hot_air = TabularCPD(
    variable='AC_Hot_Air', variable_card=2,
    values=[
        # Probabilidad de "Yes" (Hot Air)
        [0.8, 0.6, 0.7, 0.5, 0.4, 0.3, 0.2, 0.1, 0.7, 0.5, 0.6, 0.4, 0.3, 0.2, 0.4, 0.5,
         0.6, 0.7, 0.3, 0.4, 0.2, 0.1, 0.5, 0.6, 0.8, 0.7, 0.5, 0.4, 0.3, 0.6, 0.7, 0.5,
         0.8, 0.9, 0.7, 0.6, 0.5, 0.3, 0.4, 0.2, 0.6, 0.7, 0.5, 0.4, 0.3, 0.2, 0.8, 0.6],
        # Probabilidad de "No" (No Hot Air)
        [0.2, 0.4, 0.3, 0.5, 0.6, 0.7, 0.8, 0.9, 0.3, 0.5, 0.4, 0.6, 0.7, 0.8, 0.6, 0.5,
         0.4, 0.3, 0.7, 0.6, 0.8, 0.9, 0.5, 0.4, 0.2, 0.3, 0.5, 0.6, 0.7, 0.4, 0.3, 0.5,
         0.2, 0.1, 0.3, 0.4, 0.5, 0.7, 0.6, 0.8, 0.4, 0.3, 0.5, 0.6, 0.7, 0.8, 0.2, 0.4]
    ],
    evidence=['AC_Test', 'AC_Fuses', 'AC_Current_Connection', 'AC_Refrigerant_Level', 'AC_Slow_Electrical_Systems'],
    evidence_card=[2, 2, 2, 3, 2],
    state_names={
        'AC_Hot_Air': ['Yes', 'No'],
        'AC_Test': ['Done', 'Not_Done'],
        'AC_Fuses': ['Burned', 'Good'],
        'AC_Current_Connection': ['Bad', 'Good'],
        'AC_Refrigerant_Level': ['Low', 'Medium', 'High'],
        'AC_Slow_Electrical_Systems': ['Slow', 'Normal']
    }
)

model.add_cpds(cpd_ac_filter, cpd_ac_hoses, cpd_ac_internal_mode, cpd_ac_odors,
               cpd_ac_test, cpd_ac_fuses, cpd_ac_current_connection, cpd_ac_refrigerant_level,
               cpd_ac_slow_electrical_systems, cpd_ac_hot_air)


model.add_edges_from([
    ('Light_Switch', 'Light_Issue'),
    ('Light_Connector', 'Light_Issue'),
    ('Light_Fuses', 'Light_Issue'),
    ('Light_Battery', 'Light_Issue'),
    ('Light_Bulbs', 'Light_Issue')
])


# Definir las tablas de probabilidad condicional (CPTs) para Luces del Vehículo

# Switch de luces
cpd_light_switch = TabularCPD(
    variable='Light_Switch', variable_card=2,
    values=[[0.15], [0.85]],
    state_names={'Light_Switch': ['Mispressed', 'Correct']}
)

# Conector de luces
cpd_light_connector = TabularCPD(
    variable='Light_Connector', variable_card=2,
    values=[[0.2], [0.8]],
    state_names={'Light_Connector': ['Disconnected', 'Connected']}
)

# Fusibles de luces
cpd_light_fuses = TabularCPD(
    variable='Light_Fuses', variable_card=2,
    values=[[0.4], [0.6]],
    state_names={'Light_Fuses': ['Burned', 'Good']}
)

# Batería
cpd_light_battery = TabularCPD(
    variable='Light_Battery', variable_card=2,
    values=[[0.2], [0.8]],
    state_names={'Light_Battery': ['Low', 'Charged']}
)

# Bombillas quemadas
cpd_light_bulbs = TabularCPD(
    variable='Light_Bulbs', variable_card=2,
    values=[[0.05], [0.95]],
    state_names={'Light_Bulbs': ['Burned', 'Good']}
)

# Problema en las luces (salida principal para este grupo)
cpd_light_issue = TabularCPD(
    variable='Light_Issue', variable_card=2,
    values=[
        # Probabilidad de "Yes" (Lights Issue)
        [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.1, 0.2, 0.1, 0.6, 0.5, 0.7, 0.3, 0.2, 0.1,
         0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.5, 0.4, 0.3, 0.2, 0.7, 0.8, 0.6, 0.5],
        # Probabilidad de "No" (No Issue)
        [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.9, 0.8, 0.9, 0.4, 0.5, 0.3, 0.7, 0.8, 0.9,
         0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.5, 0.6, 0.7, 0.8, 0.3, 0.2, 0.4, 0.5]
    ],
    evidence=['Light_Switch', 'Light_Connector', 'Light_Fuses', 'Light_Battery', 'Light_Bulbs'],
    evidence_card=[2, 2, 2, 2, 2],
    state_names={
        'Light_Issue': ['Yes', 'No'],
        'Light_Switch': ['Mispressed', 'Correct'],
        'Light_Connector': ['Disconnected', 'Connected'],
        'Light_Fuses': ['Burned', 'Good'],
        'Light_Battery': ['Low', 'Charged'],
        'Light_Bulbs': ['Burned', 'Good']
    }
)

# Agregar los CPDs al modelo
model.add_cpds(
    cpd_light_switch, cpd_light_connector, cpd_light_fuses,
    cpd_light_battery, cpd_light_bulbs, cpd_light_issue
)

model.add_edges_from([
    ('Engine_Hoses', 'Engine_Issue'),
    ('Fuel_Level', 'Engine_Issue'),
    ('Injectors', 'Engine_Issue'),
    ('Ignition_Coil', 'Engine_Issue'),
])

# Definir las tablas de probabilidad condicional (CPTs) para Problemas de Motor

# Fugas en las mangueras
cpd_engine_hoses = TabularCPD(
    variable='Engine_Hoses', variable_card=2,
    values=[[0.3], [0.7]],
    state_names={'Engine_Hoses': ['Leaking', 'Sealed']}
)

# Nivel de combustible
cpd_fuel_level = TabularCPD(
    variable='Fuel_Level', variable_card=3,
    values=[[0.2], [0.3], [0.5]],
    state_names={'Fuel_Level': ['Low', 'Medium', 'High']}
)

# Estado de los inyectores
cpd_injectors = TabularCPD(
    variable='Injectors', variable_card=2,
    values=[[0.25], [0.75]],
    state_names={'Injectors': ['Damaged', 'Good']}
)

# Estado de la bobina de encendido
cpd_ignition_coil = TabularCPD(
    variable='Ignition_Coil', variable_card=2,
    values=[[0.15], [0.85]],
    state_names={'Ignition_Coil': ['Burned', 'Good']}
)

# Problema del motor (salida principal para este grupo)
cpd_engine_issue = TabularCPD(
    variable='Engine_Issue', variable_card=2,
    values=[
        # Probabilidad de "Yes" (Engine Issue)
        [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.05, 0.02, 0.01,
         0.85, 0.75, 0.65, 0.55, 0.45, 0.35, 0.25, 0.15, 0.05, 0.02, 0.01, 0.005],
        # Probabilidad de "No" (No Issue)
        [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.98, 0.99,
         0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95, 0.98, 0.99, 0.995],
    ],
    evidence=['Engine_Hoses', 'Fuel_Level', 'Injectors', 'Ignition_Coil'],
    evidence_card=[2, 3, 2, 2],
    state_names={
        'Engine_Issue': ['Yes', 'No'],
        'Engine_Hoses': ['Leaking', 'Sealed'],
        'Fuel_Level': ['Low', 'Medium', 'High'],
        'Injectors': ['Damaged', 'Good'],
        'Ignition_Coil': ['Burned', 'Good'],
    }
)

# Agregar los CPDs al modelo
model.add_cpds(
    cpd_engine_hoses, cpd_fuel_level, cpd_injectors,
    cpd_ignition_coil, cpd_engine_issue
)

# Extender la estructura de la red con los nodos para Problemas Eléctricos
model.add_edges_from([
    ('Battery', 'Electrical_Issue'),
    ('Alternator', 'Electrical_Issue'),
    ('Wiring', 'Electrical_Issue'),
])

# Definir las tablas de probabilidad condicional (CPTs) para Problemas Eléctricos

# Estado de la batería
cpd_battery = TabularCPD(
    variable='Battery', variable_card=2,
    values=[[0.5], [0.5]],
    state_names={'Battery': ['Low', 'Charged']}
)

# Estado del alternador
cpd_alternator = TabularCPD(
    variable='Alternator', variable_card=2,
    values=[[0.2], [0.8]],
    state_names={'Alternator': ['Damaged', 'Good']}
)

# Estado del cableado
cpd_wiring = TabularCPD(
    variable='Wiring', variable_card=2,
    values=[[0.3], [0.7]],
    state_names={'Wiring': ['Defective', 'Good']}
)

# Problema eléctrico (salida principal para este grupo)
cpd_electrical_issue = TabularCPD(
    variable='Electrical_Issue', variable_card=2,
    values=[
        # Electrical Issue (Yes)   No Issue
        [0.9, 0.7, 0.8, 0.6, 0.4, 0.2, 0.1, 0.05],
        [0.1, 0.3, 0.2, 0.4, 0.6, 0.8, 0.9, 0.95],
    ],
    evidence=['Battery', 'Alternator', 'Wiring'],
    evidence_card=[2, 2, 2],
    state_names={
        'Electrical_Issue': ['Yes', 'No'],
        'Battery': ['Low', 'Charged'],
        'Alternator': ['Damaged', 'Good'],
        'Wiring': ['Defective', 'Good'],
    }
)

# Agregar los CPDs al modelo
model.add_cpds(
    cpd_battery, cpd_alternator, cpd_wiring, cpd_electrical_issue
)

# Validar el modelo
assert model.check_model()


# Crear un objeto de inferencia
inference = VariableElimination(model)


class DiagnosticoVehiculos(KnowledgeEngine):
    #  ----------------------------
    #  1. Problemas de Arranque
    #  ----------------------------
    @Rule(Match(Switch_Sound="yes"))
    def rule_car_not_starting(self):
        # Calcular probabilidad con la evidencia
        prob = inference.query(variables=['Starting_Problems'], evidence={'Switch_Sound': 'Yes'})
        prob_yes = prob.values[0]  # Probabilidad de "Yes"
        print(f"Debido a que el switch hace un ruido raro, es necesario realizar mantenimiento. Probabilidad: {prob_yes:.2f}")

    @Rule(AND(Match(Battery_Test="fail"), Match(Switch_Sound="no")))
    def rule_weird_switch_sound(self):
        # Calcular probabilidad con la evidencia
        prob = inference.query(variables=['Starting_Problems'], evidence={'Battery_Test': 'Fail', 'Switch_Sound': 'No'})
        prob_yes = prob.values[0]  # Probabilidad de "Yes"
        print(f"Debido a que el test de batería falló, es posible que se deba cambiar la batería. Probabilidad: {prob_yes:.2f}")

    @Rule(AND(Match(Physical_Switch_Damage="yes"), Match(Switch_Sound="no"), Match(Battery_Test="pass")))
    def rule_dry_sound_failed_battery(self):
        # Calcular probabilidad con la evidencia
        prob = inference.query(variables=['Starting_Problems'], evidence={
            'Physical_Switch_Damage': 'Yes',
            'Switch_Sound': 'No',
            'Battery_Test': 'Pass'
        })
        prob_yes = prob.values[0]  # Probabilidad de "Yes"
        print(f"Es posible que el problema sea el switch o la llave debido al mal estado; necesitan ser ajustados. Probabilidad: {prob_yes:.2f}")

    @Rule(OR(Match(Starter_Sound="weird"), Match(Manual_Start="not_possible")))
    def rule_call_expert(self):
        # Calcular probabilidad con la evidencia
        prob = inference.query(variables=['Starting_Problems'], evidence={
            'Starter_Sound': 'Weird',
            'Manual_Start': 'Not_Possible'
        })
        prob_yes = prob.values[0]  # Probabilidad de "Yes"
        print(f"Se debe llamar un experto para realizar el reemplazo del sistema de arranque. Probabilidad: {prob_yes:.2f}")


    # ----------------------------
    # 2. Problemas de Aire Acondicionado
    # ----------------------------

    # Malos Olores
    @Rule(Match(AC_Odors="yes"))
    def rule_ac_bad_smell(self):
        prob = inference.query(variables=['AC_Odors'], evidence={'AC_Odors': 'Yes'})
        prob_yes = prob.values[0]
        print(f"El aire acondicionado huele mal. Revisa si el filtro está obstruido o las mangueras están dañadas. Probabilidad: {prob_yes:.2f}")

    @Rule(AND(Match(AC_Odors="yes"), Match(AC_Filter="obstructed")))
    def rule_ac_dirty_filter(self):
        prob = inference.query(variables=['AC_Odors'], evidence={'AC_Odors': 'Yes', 'AC_Filter': 'Obstructed'})
        prob_yes = prob.values[0]
        print(f"El aire acondicionado huele mal debido a un filtro obstruido. Límpialo o reemplázalo. Probabilidad: {prob_yes:.2f}")

    @Rule(AND(Match(AC_Hoses="damaged"), Match(AC_Filter="obstructed")))
    def rule_external_air_infiltration(self):
        prob = inference.query(variables=['AC_Odors'], evidence={'AC_Hoses': 'Damaged', 'AC_Filter': 'Obstructed'})
        prob_yes = prob.values[0]
        print(f"El aire externo está inundando el sistema (puede incluir olores como aceite quemado o gasolina). Probabilidad: {prob_yes:.2f}")

    @Rule(Match(AC_Internal_Mode="external"))
    def rule_hot_air_from_ac(self):
        prob = inference.query(variables=['AC_Odors'], evidence={'AC_Internal_Mode': 'External'})
        prob_yes = prob.values[0]
        print(f"El vehículo está usando aire de la calle, ingresando consigo malos olores externos. Probabilidad: {prob_yes:.2f}")

    # Aire Caliente
    @Rule(Match(AC_Hot_Air="not_done"))
    def rule_hot_air_test_not_done(self):
        prob = inference.query(variables=['AC_Hot_Air'], evidence={'AC_Test': 'Not_Done'})
        prob_yes = prob.values[0]
        print(f"La prueba no se realizó. Realice la prueba del A/C. Probabilidad: {prob_yes:.2f}")

    @Rule(AND(Match(AC_Hot_Air="done"), Match(AC_Fuses="burned")))
    def rule_hot_air_ac_fuses(self):
        prob = inference.query(variables=['AC_Hot_Air'], evidence={'AC_Test': 'Done', 'AC_Fuses': 'Burned'})
        prob_yes = prob.values[0]
        print(f"Los fusibles están quemados. Reemplázalos. Probabilidad: {prob_yes:.2f}")

    @Rule(Match(AC_Slow_Electrical_Systems="bad"))
    def rule_slow_electrical_systems(self):
        prob = inference.query(variables=['AC_Hot_Air'], evidence={'AC_Slow_Electrical_Systems': 'Slow'})
        prob_yes = prob.values[0]
        print(f"El sistema eléctrico es lento. El empate debe ser reemplazado. Probabilidad: {prob_yes:.2f}")

    @Rule(OR(Match(AC_Refrigerant_Level="low"), Match(AC_Refrigerant_Level="medium")))
    def rule_low_refrigerant(self):
        prob = inference.query(variables=['AC_Hot_Air'], evidence={'AC_Refrigerant_Level': 'Low'})
        prob_yes = prob.values[0]
        print(f"Se debe realizar una recarga de refrigerante. Probabilidad: {prob_yes:.2f}")

    @Rule(Match(AC_Current_Connection="bad"))
    def rule_bad_current_connection(self):
        prob = inference.query(variables=['AC_Hot_Air'], evidence={'AC_Current_Connection': 'Bad'})
        prob_yes = prob.values[0]
        print(f"Verifique que el empate que lleva la corriente al compresor está bien conectado. Probabilidad: {prob_yes:.2f}")

    # ----------------------------
    # 3. Problemas con las Luces
    # ----------------------------
    @Rule(Match(Light_Switch="correct"))
    def rule_lights_not_working(self):
        prob = inference.query(variables=['Light_Issue'], evidence={'Light_Switch': 'Correct'})
        prob_yes = prob.values[0]
        print(f"Las luces no funcionan. Revisa el conector, los fusibles y las bombillas. Probabilidad: {prob_yes:.2f}")

    @Rule(AND(Match(Light_Connector="disconnected"), Match(Light_Switch="correct")))
    def rule_light_switch_mispressed(self):
        prob = inference.query(variables=['Light_Issue'], evidence={'Light_Connector': 'Disconnected', 'Light_Switch': 'Correct'})
        prob_yes = prob.values[0]
        print(f"Las luces no funcionan porque el conector no está bien puesto. Ajústalo correctamente. Probabilidad: {prob_yes:.2f}")

    @Rule(Match(Light_Fuses="burned"))
    def rule_flickering_lights(self):
        prob = inference.query(variables=['Light_Issue'], evidence={'Light_Fuses': 'Burned'})
        prob_yes = prob.values[0]
        print(f"El fusible está quemado, debe ser reemplazado. Probabilidad: {prob_yes:.2f}")

    @Rule(Match(Light_Battery="Low"))
    def rule_flickering_lights_bad_wiring(self):
        prob = inference.query(variables=['Light_Issue'], evidence={'Light_Battery': 'Low'})
        prob_yes = prob.values[0]
        print(f"La batería está baja y debe ser recargada. Probabilidad: {prob_yes:.2f}")

    @Rule(Match(Light_Bulbs="burned"))
    def rule_Light_Bulbs(self):
        prob = inference.query(variables=['Light_Issue'], evidence={'Light_Bulbs': 'Burned'})
        prob_yes = prob.values[0]
        print(f"Las bombillas están quemadas y deben ser reemplazadas. Probabilidad: {prob_yes:.2f}")

    # ----------------------------
    # 4. Problemas de Motor
    # ----------------------------

    @Rule(Match(Engine_Hoses="leaking"))
    def rule_engine_hoses_leaking(self):
        prob = inference.query(variables=['Engine_Issue'], evidence={'Engine_Hoses': 'Leaking'})
        prob_yes = prob.values[0]
        print(f"El motor no funciona debido a fugas en las mangueras. Sella las fugas. Probabilidad: {prob_yes:.2f}")

    @Rule(Match(Fuel_Level="low"))
    def rule_Fuel_Level(self):
        prob = inference.query(variables=['Engine_Issue'], evidence={'Fuel_Level': 'Low'})
        prob_yes = prob.values[0]
        print(f"Debes tanquear el auto. Probabilidad: {prob_yes:.2f}")

    @Rule(AND(Match(Engine_Hoses="sealed"), Match(Fuel_Level="medium"), Match(Injectors="damaged")))
    def rule_engine_combined_issue(self):
        prob = inference.query(
            variables=['Engine_Issue'],
            evidence={'Engine_Hoses': 'Sealed', 'Fuel_Level': 'Medium', 'Injectors': 'Damaged'}
        )
        prob_yes = prob.values[0]
        print(f"El motor no funciona. Hay bajo nivel de combustible y los inyectores están dañados. Corrige ambos. Probabilidad: {prob_yes:.2f}")

    @Rule(AND(Match(Engine_Hoses="sealed"), Match(Fuel_Level="high"), Match(Injectors="damaged")))
    def rule_engine_combined_issue2(self):
        prob = inference.query(
            variables=['Engine_Issue'],
            evidence={'Engine_Hoses': 'Sealed', 'Fuel_Level': 'High', 'Injectors': 'Damaged'}
        )
        prob_yes = prob.values[0]
        print(f"El motor no funciona. Los inyectores están dañados. Corrígelos. Probabilidad: {prob_yes:.2f}")

    @Rule(Match(Ignition_Coil="burned"))
    def rule_Ignition_Coil(self):
        prob = inference.query(variables=['Engine_Issue'], evidence={'Ignition_Coil': 'Burned'})
        prob_yes = prob.values[0]
        print(f"Debes reemplazar la bobina de encendido. Probabilidad: {prob_yes:.2f}")

    # ----------------------------
    # 5. Problemas Eléctricos
    # ----------------------------

    @Rule(Match(Battery="low"))
    def rule_electrical_issues(self):
        prob = inference.query(variables=['Electrical_Issue'], evidence={'Battery': 'Low'})
        prob_yes = prob.values[0]
        print(f"Es probable que este sea el problema, la batería no tiene la carga suficiente y debe ser reemplazada o cargada de nuevo. Probabilidad: {prob_yes:.2f}")

    @Rule(AND(Match(Battery="charged"), Match(Alternator="damaged")))
    def rule_combined_electrical_issue_alternator(self):
        prob = inference.query(
            variables=['Electrical_Issue'],
            evidence={'Battery': 'Charged', 'Alternator': 'Damaged'}
        )
        prob_yes = prob.values[0]
        print(f"Los problemas eléctricos causados posiblemente sean por el alternador dañado. Debe ser reemplazado. Probabilidad: {prob_yes:.2f}")

    @Rule(AND(Match(Battery="charged"), Match(Alternator="good"), Match(Wiring="defective")))
    def rule_combined_electrical_issue(self):
        prob = inference.query(
            variables=['Electrical_Issue'],
            evidence={'Battery': 'Charged', 'Alternator': 'Good', 'Wiring': 'Defective'}
        )
        prob_yes = prob.values[0]
        print(f"Los problemas eléctricos causados posiblemente sean por el cableado averiado. Debe llamar a un electricista experto para que el mismo haga el cambio del cableado. Probabilidad: {prob_yes:.2f}")


def diagnosticar_problemas_arranque(expert_system):

    Switch_Sound= input("¿El switch hace un sonido extraño como un chillido? (Yes/No): ").lower()
    expert_system.declare(Match(Switch_Sound=Switch_Sound))
    expert_system.run()

    if Switch_Sound == "no":
        Battery_Test = input("¿El test de bateria paso o fallo? (Pass/Fail): ").lower()
        expert_system.declare(Match(Battery_Test=Battery_Test))
        expert_system.run()

        if Battery_Test == "pass":
            Physical_Switch_Damage = input("¿El switch tiene daños físicos o la llave queda floja? (Yes/No): ").lower()
            expert_system.declare(Match(Physical_Switch_Damage=Physical_Switch_Damage))
            expert_system.run()

            if Physical_Switch_Damage == "no":
                Starter_Sound = input("¿Al encender el vehiculo se escucha un sonido raspado o normal? (Weir/Normal) ").lower()
                expert_system.declare(Match(Starter_Sound=Starter_Sound))
                expert_system.run()

                if Starter_Sound == "normal":
                      Manual_Start = input("¿El vehículo puede arrancar empujándolo? (Possible/Not_Possible): ").lower()
                      expert_system.declare(Match(Manual_Start=Manual_Start))
                      expert_system.run()


def diagnosticar_problemas_ac(expert_system):

    respuesta = input("¿A que tema esta relacionado tu problema de aire? (badOdor/hotAir): ").lower()
    if respuesta == "badodor":

      # Malos olores

      ACOdors = input("¿El aire acondicionado está soltando malos olores? (Yes/No): ").lower()
      expert_system.declare(Match(ACOdors=ACOdors))
      expert_system.run()

      if ACOdors == "yes":
          AC_Filter = input("¿Como se encuentra el filtro de aire acondicionado? (Obstructed/Clean): ").lower()
          expert_system.declare(Match(AC_Filter=AC_Filter))
          expert_system.run()

          if AC_Filter == "obstructed":
            AC_Hoses = input("¿Cual es el estado físico del filtro? (Damaged/Intact): ").lower()
            expert_system.declare(Match(AC_Hoses=AC_Hoses))
            expert_system.run()

            if AC_Hoses == "intact":
              AC_Internal_Mode = input("¿En que modo se encuentra el sistema de aire? (External/Internal): ").lower()
              expert_system.declare(Match(AC_Internal_Mode=AC_Internal_Mode))
              expert_system.run()

    elif respuesta == "hotair":

      # Aire caliente

      AC_Hot_Air = input("¿La prueba de aire ya fue realizada? (Done/Not_Done): ").lower()
      expert_system.declare(Match(AC_Hot_Air=AC_Hot_Air))
      expert_system.run()

      if AC_Hot_Air == "done":
          AC_Fuses = input("¿Cual es el estado del fuse de aire acondicionado? (Burned/Good): ").lower()
          expert_system.declare(Match(AC_Fuses=AC_Fuses))
          expert_system.run()

          if AC_Fuses == "good":
            AC_Slow_Electrical_Systems1 = input("¿Cual es el estado del empate que lleva la corriente al compresor? (Bad/Good): ").lower()
            expert_system.declare(Match(AC_Slow_Electrical_Systems1=AC_Slow_Electrical_Systems1))
            expert_system.run()

            if AC_Slow_Electrical_Systems1 == "good":
                AC_Refrigerant_Level = input("¿Que tan alto esta el nivel de refrigerante, respecto al (<10%)? (Low/Medium/High): ").lower()
                expert_system.declare(Match(AC_Refrigerant_Level=AC_Refrigerant_Level))
                expert_system.run()

                if AC_Refrigerant_Level == "high":
                  AC_Slow_Electrical_Systems = input("¿Que tal siente la respuesta de los sistemas electricos del vehiculo? (Slow/Normal): ").lower()
                  expert_system.declare(Match(AC_Slow_Electrical_Systems=AC_Slow_Electrical_Systems))
                  expert_system.run()

    else:
        print("Opción no válida. Por favor, inténtelo de nuevo.")



def diagnosticar_problemas_luces(expert_system):

    # Flujo de preguntas
    Light_Switch = input("¿El sistema de encendido de luces está presionado correctamente? (Mispressed/Correct): ").lower()
    expert_system.declare(Match(Light_Switch=Light_Switch))
    expert_system.run()

    if Light_Switch == "correct":
      Light_Connector = input("¿Cual es el estado del conector de las luces? (Connected/Disconnected): ").lower()
      expert_system.declare(Match(Light_Connector=Light_Connector))
      expert_system.run()

      if Light_Connector == "connected":
        Light_Fuses = input("¿Cual es el estado delbuster 'lights'? (Burned/Good): ").lower()
        expert_system.declare(Match(Light_Fuses=Light_Fuses))
        expert_system.run()

        if Light_Fuses == "good":
          Light_Battery = input("¿Cual es el estado de carga de la batería? (Low/Charged): ").lower()
          expert_system.declare(Match(Light_Battery=Light_Battery))
          expert_system.run()

          if Light_Battery == "charged":
            Light_Bulbs = input("¿Cual es el estado de las luces? (Burned/Good): ").lower()
            expert_system.declare(Match(Light_Bulbs=Light_Bulbs))
            expert_system.run()


def diagnosticar_problemas_motor(expert_system):

    Engine_Hoses = input("¿Cual es el estado de las mangueras del motor? (Leaking/Sealed): ").lower()
    expert_system.declare(Match(Engine_Hoses=Engine_Hoses))
    expert_system.run()

    if Engine_Hoses == "sealed":
        Fuel_Level = input("¿Cual es el nivel de combustible (<1/4 tanque)? (Low/Medium/High): ").lower()
        expert_system.declare(Match(Fuel_Level=Fuel_Level))
        expert_system.run()

        if Fuel_Level == "low":
            Injectors = input("¿Cual es el estado de los inyectores? (Damaged/Good): ").lower()
            expert_system.declare(Match(Injectors=Injectors))
            expert_system.run()

            if Injectors == "good":
                Ignition_Coil = input("¿Cual es el estado de la bobina de encendido? (Burned/Good): ").lower()
                expert_system.declare(Match(Ignition_Coil=Ignition_Coil))
                expert_system.run()


def diagnosticar_problemas_electricos(expert_system):

  Battery = input("¿Cual es el nivel de carga de la bateria? (Low/Charged): ").lower()
  expert_system.declare(Match(Battery=Battery))
  expert_system.run()

  if Battery == "charged":
    Alternator = input("¿Cual es el estado del alternador? (Damaged/Good): ").lower()
    expert_system.declare(Match(Alternator=Alternator))
    expert_system.run()

    if Alternator == "good":
      Wiring = input("¿Cual es el estado del cableado? (Defective/Good): ").lower()
      expert_system.declare(Match(Wiring=Wiring))
      expert_system.run()



def diagnosticar_problemas(sistema, expert_system):
    if sistema == "1":
        diagnosticar_problemas_arranque(expert_system)
    elif sistema == "2":
        diagnosticar_problemas_ac(expert_system)
    elif sistema == "3":
        diagnosticar_problemas_luces(expert_system)
    elif sistema == "4":
        diagnosticar_problemas_motor(expert_system)
    elif sistema == "5":
        diagnosticar_problemas_electricos(expert_system)
    else:
        print("Opción no válida. Por favor, inténtelo de nuevo.")

def main():
    while True:

        expert_system = DiagnosticoVehiculos()
        expert_system.reset()

        print("\nBienvenido al sistema experto de diagnóstico de vehículos")

        print("Seleccione el sistema a diagnosticar:")
        print("1. Problemas de arranque")
        print("2. Problemas de aire acondicionado")
        print("3. Problemas de luces")
        print("4. Problemas de motor")
        print("5. Problemas eléctricos")
        print("6. Salir")

        opcion = input("Ingrese el número de su opción: ").strip()

        if opcion == "6":
            print("Gracias por usar el sistema experto de diagnóstico de vehículos. ¡Hasta luego!")
            break

        # Ejecutar diagnóstico basado en la opción seleccionada
        diagnosticar_problemas(opcion, expert_system)

        # Preguntar si desea diagnosticar otro sistema
        otra_opcion = input("\n¿Desea diagnosticar otro sistema? (si/no): ").lower()
        if otra_opcion != "si":
            print("Gracias por usar el sistema experto de diagnóstico de vehículos. ¡Hasta luego!")
            break

if __name__ == "__main__":
    main()