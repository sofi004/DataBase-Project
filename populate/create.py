import random
import string
import datetime
import copy

# Funçao para gerar números de telefone aleatórios
def generate_phone_number():
    return ''.join(random.choices(string.digits, k=9))

# Funçao para gerar datas de nascimento aleatórias
def generate_birth_date():
    start_date = datetime.date(1950, 1, 1)
    end_date = datetime.date(2005, 12, 31)
    return start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))

# Lista de palavras para o nome da avenida
avenue_names = [
    "Liberdade", "São João", "Alegria", "Paz", "Esperança",
    "Flor", "Amizade", "Rio", "Sol", "Mar", "Ventura",
    "Primavera", "Felicidade", "Estrada Real", "Montanha",
    "Estrela", "Caminho Verde", "Travessia", "Céu Azul",
    "Jardim", "Cascata", "Lua Cheia", "Horizonte", "Brilho",
    "Encanto", "Fantasia", "Coração", "Amanhecer", "Sorriso",
    "Caminho do Mar", "Fogueira", "Raio de Sol", "Oceano"
]

# Dicionário para mapear moradas a códigos postais
address_postal_dict = {}

# Função para gerar código postal no formato XXXX-XXX
def generate_postal_code():
    return f"{random.randint(1000, 9999)}-{random.randint(100, 999)}"

# Função para gerar moradas com código postal
def generate_address():
    global address_postal_dict
    address = ' '.join(random.choices(["Rua", "Avenida", "Praceta", "Travessa", "Largo"], k=1)) + ' ' + \
              ' '.join(random.choices(avenue_names, k=1)) + ' ' + \
              ' '.join(random.choices(["Lisboa", "Oeiras", "Cascais", "Loures", "Amadora", "Sintra"], k=1))
    
    # Verifica se a morada já tem um código postal atribuído
    if address not in address_postal_dict:
        address_postal_dict[address] = generate_postal_code()

    # Adicionar código postal
    address_with_postal = ' '.join([address, address_postal_dict[address]])
    return address_with_postal
# Lista de clínicas em diferentes localidades de Lisboa
clinicas = [
    {"nome": "Hospital da Luz", "telefone": generate_phone_number(), "morada": generate_address()},
    {"nome": "Hospital de Santa Maria", "telefone": generate_phone_number(), "morada": generate_address()},
    {"nome": "Clinica Sao Francisco Xavier", "telefone": generate_phone_number(), "morada": generate_address()},
    {"nome": "Hospital de Cascais", "telefone": generate_phone_number(), "morada": generate_address()},
    {"nome": "Hospital Beatriz Angelo", "telefone": generate_phone_number(), "morada": generate_address()}
]

# Dados para os enfermeiros
enfermeiros_por_clinica = 6  # Defina o número desejado de enfermeiros por clínica
enfermeiros = []
for clinica in clinicas:
    for _ in range(enfermeiros_por_clinica):
        enfermeiros.append({
            "nif": ''.join(random.choices(string.digits, k=9)),
            "nome": ' '.join(random.choices(["Ana", "Joao", "Marta", "Pedro", "Sofia", "Tiago", "Ines", "Rui", "Carla", "Miguel"], k=2)),
            "telefone": generate_phone_number(),
            "morada": generate_address(),
            "nome_clinica": clinica["nome"]
        })


# Dados para os médicos
medicos_clinica_geral = []
medicos_outras_especialidades = []

# Gerar médicos de especialidade 'Clínica Geral'
for _ in range(20):
    medicos_clinica_geral.append({
        "nif": ''.join(random.choices(string.digits, k=9)),
        "nome": ' '.join(random.choices(["Andre", "Beatriz", "Carlos", "Diana", "Eduardo", "Francisca", "Gustavo", "Helena", "Ivo", "Joana"], k=2)),
        "telefone": generate_phone_number(),
        "morada": generate_address(),
        "especialidade": "Clinica Geral"
    })

# Gerar médicos de outras especialidades
outras_especialidades = ["Ortopedia", "Cardiologia", "Pediatria", "Ginecologia", "Dermatologia"]
for especialidade in outras_especialidades:
    for _ in range(8):
        medicos_outras_especialidades.append({
            "nif": ''.join(random.choices(string.digits, k=9)),
            "nome": ' '.join(random.choices(["Marta", "Ricardo", "Sara", "Tomas", "Vanessa", "Xavier", "Yara", "Ze"], k=2)),
            "telefone": generate_phone_number(),
            "morada": generate_address(),
            "especialidade": especialidade
        })

# Juntar todos os médicos
medicos = medicos_clinica_geral + medicos_outras_especialidades

# Função para verificar se um médico já está agendado em outra clínica no mesmo dia da semana
def medico_agendado_outro_clinica(medico_nif, clinica, dia_da_semana):
    for outro_dia in clinica:
        if outro_dia != dia_da_semana and medico_nif in clinica[outro_dia]:
            return True
    return False

# Lista para armazenar dados da tabela 'trabalha'
trabalha_data = []

# Distribuir os médicos em clínicas e dias da semana, evitando que um médico trabalhe em duas clínicas no mesmo dia
for medico in medicos:
    # Selecionar aleatoriamente duas clínicas onde o médico trabalhará
    clinicas_medico = random.sample(clinicas, 2)
    for clinica in clinicas_medico:
        # Selecionar aleatoriamente um dia da semana
        dia_da_semana = random.randint(1, 7)
        while medico_agendado_outro_clinica(medico["nif"], clinica, dia_da_semana):
            dia_da_semana = random.randint(1, 7)
        clinica.setdefault(dia_da_semana, []).append(medico["nif"])
        trabalha_data.append({
            "nif_medico": medico["nif"],
            "nome_clinica": clinica["nome"],
            "dia_da_semana": dia_da_semana
        })

# Verificar se cada clínica tem pelo menos 8 médicos por dia da semana
for clinica in clinicas:
    # Inicializar a lista para cada dia da semana
    for dia_da_semana in range(1, 8):
        clinica.setdefault(dia_da_semana, [])
    
    # Verificar se cada clínica tem pelo menos 8 médicos por dia da semana
    for dia_da_semana in range(1, 8):
        while len(clinica[dia_da_semana]) < 8:
            medico = random.choice(medicos)["nif"]
            if medico not in clinica[dia_da_semana]:
                clinica[dia_da_semana].append(medico)
                trabalha_data.append({
                    "nif_medico": medico,
                    "nome_clinica": clinica["nome"],
                    "dia_da_semana": dia_da_semana
                })

# Dados para os pacientes
pacientes = []
nomes_utilizados = set()

for _ in range(5000):
    # Gerar um nome único
    nome = None
    while nome is None or nome in nomes_utilizados:
        nome = ' '.join(random.choices([
    "Ana", "Beatriz", "Carla", "Daniela", "Eduarda", "Fabio", "Gabriel", "Helena", "Ines", "Joao",
    "Katia", "Luis", "Manuel", "Nuno", "Olivia", "Pedro", "Quintino", "Rita", "Sara", "Tiago",
    "Ursula", "Vitor", "Xavier", "Yara", "Ze", "Sofia", "Catarina", "Antonio", "Rafael", "Rafaela",
    "Manuela", "Patricia", "Pedra", "Sandra", "Francisca", "Francisco", "Simao", "Rodrigo", "Santiago",
    "Ramon", "Cinderela", "Tatiana", "Tomas", "Arminda", "Mario", "Gabriela", "Isa", "Sthefania", "Andre",
    "Silvia", "Diana", "Laura", "Felipe", "Claudia", "Marta", "Leonor", "Ricardo", "Bernardo", "Dinis",
    "Kevin", "Gustavo", "Vanessa", "Luciana", "Bruno", "Elisabete", "Tania", "Edmundo", "Edgar", "Ronaldo",
    "Toni", "Sergio", "Marcelo", "Rui", "Renata", "Artur", "Barbara", "Fatima", "Nalia", "Carolina", "Hugo",
    "Danilo", "Nelson", "Liliana", "Roberto", "Paulo", "Lucas", "Miguel", "Henrique", "Samuel", "Juliana"], k=2))
    
    nomes_utilizados.add(nome)  # Adicionar o nome utilizado ao conjunto

    pacientes.append({
        "ssn": ''.join(random.choices(string.digits, k=11)),
        "nif": ''.join(random.choices(string.digits, k=9)),
        "nome": nome,
        "telefone": generate_phone_number(),
        "morada": generate_address(),
        "data_nasc": generate_birth_date()
    })

# Definindo o número mínimo de consultas por médico por dia
min_consultas_por_medico = 2

# Definindo o número mínimo de consultas por dia por clínica
min_consultas_por_dia_por_clinica = 20

# Intervalo de tempo para as consultas
inicio_2023 = datetime.date(2023, 1, 1)
inicio_2024 = datetime.date(2024, 1, 1)
fim_2024 = datetime.date(2024, 12, 31)

horas = [datetime.time(8, 0), datetime.time(8, 30), datetime.time(9, 0), datetime.time(9, 30),
        datetime.time(10, 0), datetime.time(10, 30), datetime.time(11, 0), datetime.time(11, 30),
        datetime.time(12, 0), datetime.time(12, 30), datetime.time(14, 0), datetime.time(14, 30),
        datetime.time(15, 0), datetime.time(15, 30), datetime.time(16, 0), datetime.time(16, 30),
        datetime.time(17, 0), datetime.time(17, 30), datetime.time(18, 0), datetime.time(18, 30)]
horarios = []
current_date = inicio_2024
while current_date <= fim_2024:
    for hora_consulta in horas:
        horarios.append({
            "data": current_date,
            "hora": hora_consulta,
        })
    current_date += datetime.timedelta(days=1)


# Schedule patients consultations
consultas = []  # Inicialize a lista de consultas
codigos_consulta = set()  # Conjunto para rastrear códigos de consulta utilizados
id = 0
paciente_nr = 0
while id < 5000:
    current_date = inicio_2023
    while current_date <= fim_2024:
        dia = current_date.weekday() + 1
        for clinica in clinicas:
            nr_consultas = 0
            while nr_consultas < 20:
                nr_consultas_por_medico = 0
                while nr_consultas_por_medico < 2:
                    for trabalha in trabalha_data:
                        if(nr_consultas >= 20):
                            break
                        if (trabalha["nome_clinica"] == clinica["nome"]) and (trabalha["dia_da_semana"] == dia):
                            medico = trabalha["nif_medico"]
                            # Gerar um código único de consulta
                            codigo_sns = ''.join(random.choices(string.digits, k=12))
                            while codigo_sns in codigos_consulta:
                                codigo_sns = ''.join(random.choices(string.digits, k=12))
                            # Gerar uma hora aleatória para a consulta
                            hora_aleatoria = datetime.time(random.randint(8, 19), random.choice([0, 30]))

                            # Verificar se a hora aleatória está dentro dos intervalos permitidos
                            hora_consulta = None
                            if 8 <= hora_aleatoria.hour < 13 or 14 <= hora_aleatoria.hour < 19:
                                minutos = hora_aleatoria.minute // 30 * 30  # Ajustar para o intervalo de meia hora
                                hora_consulta = datetime.time(hora_aleatoria.hour, minutos)
                            else:
                                # Se estiver fora dos intervalos 8-13 e 14-19 horas, ajuste para o intervalo mais próximo
                                if hora_aleatoria.hour < 8:
                                    hora_consulta = datetime.time(8, 0)  # Ajuste para o início do intervalo
                                elif hora_aleatoria.hour >= 19:
                                    hora_consulta = datetime.time(19, 0)  # Ajuste para o final do intervalo
                                elif hora_aleatoria.hour >= 13 and hora_aleatoria.hour < 14:
                                    hora_consulta = datetime.time(15, 30)
                            if paciente_nr >= 5000:
                                paciente_nr = 0
                            consultas.append({
                                "id": id,
                                "ssn": pacientes[paciente_nr]["ssn"],
                                "nif_medico": medico,
                                "nome_clinica": trabalha["nome_clinica"],
                                "data": current_date,
                                "hora": hora_consulta,
                                "codigo_sns": codigo_sns
                            })
                            nr_consultas += 1
                            paciente_nr += 1
                            id += 1
                            # Adicionar o código de consulta à lista de códigos utilizados
                            codigos_consulta.add(codigo_sns)
                    nr_consultas_por_medico += 1
        # Passar para o próximo dia
        current_date += datetime.timedelta(days=1)
    if(id >= 5000):
        break


# Dados para as receitas
medicamentos = ["Paracetamol", "Amoxicilina", "Ibuprofeno",
        "Metformina", "Atorvastatina", "Omeprazol"]

receitas = []

# Gerando receitas para ~80% das consultas
for consulta in consultas[:round(len(consultas) * 0.8)]:
    codigo_sns = consulta['codigo_sns']  # Supondo que cada consulta tem um código SNS

    # Número de medicamentos por receita (entre 1 e 6)
    num_medicamentos = random.randint(1, 6)

    medicamentos_choice = random.sample(medicamentos, num_medicamentos)
    quantidades = [random.randint(1, 3) for _ in range(num_medicamentos)]
    
    for medicamento, quantidade in zip(medicamentos_choice, quantidades):
        receitas.append({
            'codigo_sns': codigo_sns,
            'medicamento': medicamento,
            'quantidade': quantidade
        })


# Dados para as observações
observacoes = []

# Parâmetros para sintomas e métricas
sintomas_parametros = ["Dor de cabeça", "Febre", "Náusea", "Tontura", "Fadiga", "Dor abdominal",
"Tosse", "Dor no peito", "Dificuldade para respirar", "Perda de apetite", "Suores noturnos",
"Inchaço", "Dor nas articulações", "Erupção cutânea", "Calafrios", "Perda de peso", "Palpitações",
"Diarreia", "Constipação", "Vômito", "Dores musculares", "Olhos vermelhos", "Dor de garganta", "Congestão nasal", 
"Secreção nasal", "Prurido", "Vertigem", "Dor lombar", "Dificuldade para urinar", "Hemorragia", "Rigidez", "Falta de coordenação",
"Perda de equilíbrio", "Alteração na visão", "Zumbido no ouvido", "Manchas na pele", "Tremores", "Fraqueza",
"Ansiedade", "Depressão", "Insônia", "Sonolência excessiva", "Problemas de memória", "Irritabilidade", "Sensibilidade à luz",
"Dor nos dentes", "Sensação de queimação", "Dor ao engolir", "Formigamento", "Cãibras"]

metricas_parametros = ["Temperatura corporal", "Pressão arterial sistólica", "Pressão arterial diastólica", "Frequência cardíaca",
"Frequência respiratória", "Saturação de oxigênio", "Nível de glicose no sangue", "Índice de massa corporal", "Peso corporal", 
"Altura", "Nível de colesterol total", "Nível de HDL", "Nível de LDL", "Triglicerídeos", "Hemoglobina", "Hematócrito", 
"Leucócitos", "Plaquetas", "Creatinina sérica", "Taxa de filtração glomerular"]

fault_sintomas = copy.deepcopy(sintomas_parametros) 
fault_metricas = copy.deepcopy(metricas_parametros)
for consulta in consultas:
    consulta_id = consulta['id']
    num_sintomas = random.randint(1, 5)
    num_metricas = random.randint(0, 3)
    sintomas_escolhidos = random.sample(sintomas_parametros, num_sintomas)
    metricas_escolhidas = random.sample(metricas_parametros, num_metricas)
    for sintoma in sintomas_escolhidos:
        observacoes.append({
            "id": consulta_id,
            "parametro": sintoma,
            "valor": None  # Sintomas não têm valor
        })
        if sintoma in fault_sintomas:
            fault_sintomas.remove(sintoma)
    
    for metrica in metricas_escolhidas:
        observacoes.append({
            "id": consulta_id,
            "parametro": metrica,
            "valor": round(random.uniform(0, 100), 2)  # Valor aleatório para métricas
        })
        if metrica in fault_metricas:
            fault_metricas.remove(metrica)

# Preencher os parâmetros restantes como sintomas em consultas que ainda têm espaço
while fault_sintomas:
    for consulta in consultas:
        consulta_id = consulta['id']
        if len([obs for obs in observacoes if obs['id'] == consulta_id and obs['parametro'] in sintomas_parametros]) < 5:
            sintoma = fault_sintomas.pop()
            observacoes.append({
                "id": consulta_id,
                "parametro": sintoma,
                "valor": None  # Sintomas não têm valor
            })
            break

# Preencher os parâmetros restantes como métricas em consultas que ainda têm espaço
while fault_metricas:
    for consulta in consultas:
        consulta_id = consulta['id']
        if len([obs for obs in observacoes if obs['id'] == consulta_id and obs['parametro'] in metricas_parametros]) < 3:
            metrica = fault_metricas.pop()
            observacoes.append({
                "id": consulta_id,
                "parametro": metrica,
                "valor": round(random.uniform(0, 100), 2)  # Valor aleatório para métricas
            })
            break

# Escrever os dados gerados para um arquivo SQL
with open("dados.sql", "w") as f:
    # Preencher a tabela clinica
    f.write("INSERT INTO clinica (nome, telefone, morada) VALUES\n")
    f.write(",\n".join(["('{}', '{}', '{}')".format(clinica['nome'], clinica['telefone'], clinica['morada']) for clinica in clinicas]) + ";\n")

    # Preencher a tabela enfermeiro
    f.write("INSERT INTO enfermeiro (nif, nome, telefone, morada, nome_clinica) VALUES\n")
    f.write(",\n".join(["('{}', '{}', '{}', '{}', '{}')".format(enfermeiro['nif'], enfermeiro['nome'], enfermeiro['telefone'], enfermeiro['morada'], enfermeiro['nome_clinica']) for enfermeiro in enfermeiros]) + ";\n")
    
    # Preencher a tabela medico
    f.write("INSERT INTO medico (nif, nome, telefone, morada, especialidade) VALUES\n")
    f.write(",\n".join(["('{}', '{}', '{}', '{}', '{}')".format(medico['nif'], medico['nome'], medico['telefone'], medico['morada'], medico['especialidade']) for medico in medicos]) + ";\n")
    
    # Preencher a tabela trabalha
    f.write("INSERT INTO trabalha (nif_medico, nome_clinica, dia_da_semana) VALUES\n")
    f.write(",\n".join(["('{}', '{}', {})".format(trabalha['nif_medico'], trabalha['nome_clinica'], trabalha['dia_da_semana']) for trabalha in trabalha_data]) + ";\n")

    # Preencher a tabela paciente
    f.write("INSERT INTO paciente (ssn, nif, nome, telefone, morada, data_nasc) VALUES\n")
    f.write(",\n".join(["('{}', '{}', '{}', '{}', '{}', '{}')".format(paciente['ssn'], paciente['nif'], paciente['nome'], paciente['telefone'], paciente['morada'], paciente['data_nasc']) for paciente in pacientes]) + ";\n")
    
    # Preencher a tabela horario
    f.write("INSERT INTO horario (data, hora) VALUES\n")
    f.write(",\n".join(["('{}', '{}')".format(horario['data'], horario['hora'])for horario in horarios]) + ";\n")

    # Preencher a tabela consulta
    f.write("INSERT INTO consulta (ssn, nif, nome, data, hora, codigo_sns) VALUES\n")
    f.write(",\n".join(["('{}', '{}', '{}', '{}', '{}', '{}')".format(consulta['id'], consulta['ssn'], consulta['nif_medico'], consulta['nome_clinica'], consulta['data'], consulta['hora'], consulta['codigo_sns']) for consulta in consultas]) + ";\n")
    
    # Preencher a tabela receita
    f.write("INSERT INTO receita (codigo_sns, medicamento, quantidade) VALUES\n")
    f.write(",\n".join(["('{}', '{}', {})".format(receita['codigo_sns'], receita['medicamento'], receita['quantidade']) for receita in receitas]) + ";\n")

    # Preencher a tabela observacao
    f.write("INSERT INTO observacao (id, parametro, valor) VALUES\n")
    f.write(",\n".join(["({}, '{}', {})".format(observacao['id'], observacao['parametro'], observacao['valor']) for observacao in observacoes]) + ";\n")