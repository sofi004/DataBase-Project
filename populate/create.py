import random
import string
import datetime
import copy
import string
from itertools import combinations

# Funçao para gerar números de telefone aleatorios
def generate_phone_number():
    return ''.join(random.choices(string.digits, k=9))

# Funçao para gerar datas de nascimento aleatorias
def generate_birth_date():
    start_date = datetime.date(1950, 1, 1)
    end_date = datetime.date(2005, 12, 31)
    return start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))

# Lista de palavras para o nome da avenida
avenue_names = [
    "Liberdade", "Sao Joao", "Alegria", "Paz", "Esperança",
    "Flor", "Amizade", "Rio", "Sol", "Mar", "Ventura",
    "Primavera", "Felicidade", "Estrada Real", "Montanha",
    "Estrela", "Caminho Verde", "Travessia", "Céu Azul",
    "Jardim", "Cascata", "Lua Cheia", "Horizonte", "Brilho",
    "Encanto", "Fantasia", "Coraçao", "Amanhecer", "Sorriso",
    "Caminho do Mar", "Fogueira", "Raio de Sol", "Oceano"
]

# Dicionario para mapear moradas a codigos postais
address_postal_dict = {}

# Funçao para gerar codigo postal no formato XXXX-XXX
def generate_postal_code():
    return f"{random.randint(1000, 9999)}-{random.randint(100, 999)}"

# Funçao para gerar moradas com codigo postal
def generate_address():
    global address_postal_dict
    address = ' '.join(random.choices(["Rua", "Avenida", "Praceta", "Travessa", "Largo"], k=1)) + ' ' + \
              ' '.join(random.choices(avenue_names, k=1)) + ' ' + \
              ' '.join(random.choices(["Lisboa", "Oeiras", "Cascais", "Loures", "Amadora", "Sintra"], k=1))
    
    # Verifica se a morada ja tem um codigo postal atribuido
    if address not in address_postal_dict:
        address_postal_dict[address] = generate_postal_code()

    # Adicionar codigo postal
    address_with_postal = ' '.join([address, address_postal_dict[address]])
    return address_with_postal
# Lista de clinicas em diferentes localidades de Lisboa
clinicas = [
    {"nome": "Hospital da Luz", "telefone": generate_phone_number(), "morada": generate_address()},
    {"nome": "Hospital de Santa Maria", "telefone": generate_phone_number(), "morada": generate_address()},
    {"nome": "Clinica Sao Francisco Xavier", "telefone": generate_phone_number(), "morada": generate_address()},
    {"nome": "Hospital de Cascais", "telefone": generate_phone_number(), "morada": generate_address()},
    {"nome": "Hospital Beatriz Angelo", "telefone": generate_phone_number(), "morada": generate_address()}
]
nomes_possiveis = ["Raimundo", "Sabrina", "Quirino", "Oscar", "Natalia", "Filomena", "Joaquim", "Igor", "Noemi", "Mogli", "Ulisses", "Ivandro", "Ruben", "Noemi", "Mauro", "Mauricio", "Manel", "Jesus", "Alice", "Denise", "Caio", "Ester", "Fernanda", "Guilherme", "Jonas", "Luan", "Ian", "Thales", "Marcia", "Marcio", "Leonardo", "Leandro", "Viviane", "Iris", "Iara", "Rihana", "Hanna", "Tiara", "Lua", "Sol", "Alina", "Dayo", "Adewale", "Amara", "Amina", "Ayodele", "Chidinma", "Ebele", "Efua", "Esi", "Femi", "Folake", "Imani", "Jabari", "Kowi", "Mandla", "Lulu", "Adebola", "Zola", "Penda", "Talib", "Nyah", "Eshe", "Nkosi", "Simba", "Balu"]
combinacoes_nomes = list(combinations(nomes_possiveis, 2))
# Dados para os enfermeiros
enfermeiros_por_clinica = 6  # Defina o número desejado de enfermeiros por clinica
enfermeiros = []
for clinica in clinicas:
    for _ in range(enfermeiros_por_clinica):
        nome = ' '.join(combinacoes_nomes.pop())
        enfermeiros.append({
            "nif": ''.join(random.choices(string.digits, k=9)),
            "nome": nome,
            "telefone": generate_phone_number(),
            "morada": generate_address(),
            "nome_clinica": clinica["nome"]
        })


# Dados para os médicos
medicos_clinica_geral = []
medicos_outras_especialidades = []

# Gerar médicos de especialidade 'Clinica Geral'
for _ in range(20):
    nome = ' '.join(combinacoes_nomes.pop())
    medicos_clinica_geral.append({
        "nif": ''.join(random.choices(string.digits, k=9)),
        "nome": nome,
        "telefone": generate_phone_number(),
        "morada": generate_address(),
        "especialidade": "Clinica Geral"
    })

# Gerar médicos de outras especialidades
outras_especialidades = ["Ortopedia", "Cardiologia", "Pediatria", "Ginecologia", "Dermatologia"]
for especialidade in outras_especialidades:
    for _ in range(8):
        nome = ' '.join(combinacoes_nomes.pop())
        medicos_outras_especialidades.append({
            "nif": ''.join(random.choices(string.digits, k=9)),
            "nome": nome,
            "telefone": generate_phone_number(),
            "morada": generate_address(),
            "especialidade": especialidade
        })

# Juntar todos os médicos
medicos = medicos_clinica_geral + medicos_outras_especialidades

# Funçao para verificar se um médico ja esta agendado em outra clinica no mesmo dia da semana
def medico_agendado_outro_clinica(medico_nif, dia_da_semana):
    for trabalho in trabalha_data:
        if(trabalho["nif"] == medico_nif and trabalho["dia_da_semana"] == dia_da_semana):
            return True
    return False

# Lista para armazenar dados da tabela 'trabalha'
trabalha_data = []

# Distribuir os médicos em clinicas e dias da semana, evitando que um médico trabalhe em duas clinicas no mesmo dia
for medico in medicos:
    # Selecionar aleatoriamente duas clinicas onde o médico trabalhara
    clinicas_medico = random.sample(clinicas, 2)
    for clinica in clinicas_medico:
        # Selecionar aleatoriamente um dia da semana
        dia_da_semana = random.randint(0, 6)
        while medico_agendado_outro_clinica(medico["nif"], dia_da_semana):
            dia_da_semana = random.randint(0, 6)
        clinica.setdefault(dia_da_semana, []).append(medico["nif"])
        trabalha_data.append({
            "nif": medico["nif"],
            "nome": clinica["nome"],
            "dia_da_semana": dia_da_semana
        })

# Verificar se cada clinica tem pelo menos 8 médicos por dia da semana
for clinica in clinicas:
    # Inicializar a lista para cada dia da semana
    for dia_da_semana in range(0, 7):
        clinica.setdefault(dia_da_semana, [])
    
    # Verificar se cada clinica tem pelo menos 8 médicos por dia da semana
    for dia_da_semana in range(0, 7):
        while len(clinica[dia_da_semana]) < 8:
            medico = random.choice(medicos)["nif"]
            if medico not in clinica[dia_da_semana]:
                clinica[dia_da_semana].append(medico)
                if not (medico_agendado_outro_clinica(medico, dia_da_semana)):
                    trabalha_data.append({
                        "nif": medico,
                        "nome": clinica["nome"],
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

# Definindo o número minimo de consultas por médico por dia
min_consultas_por_medico = 2

# Definindo o número minimo de consultas por dia por clinica
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
codigos_consulta = set()  # Conjunto para rastrear codigos de consulta utilizados
criterios_unicos = set()  # Conjunto para rastrear critérios únicos
id = 0
paciente_nr = 0
while id < 5000:
    current_date = inicio_2023
    while current_date <= fim_2024:
        dia = current_date.weekday()
        for clinica in clinicas:
            nr_consultas = 0
            while nr_consultas < 20:
                nr_consultas_por_medico = 0
                while nr_consultas_por_medico < 2:
                    for trabalha in trabalha_data:
                        if(nr_consultas >= 20):
                            break
                        if (trabalha["nome"] == clinica["nome"]) and (trabalha["dia_da_semana"] == dia):
                            medico = trabalha["nif"]
                            # Gerar um codigo único de consulta
                            codigo_sns = ''.join(random.choices(string.digits, k=12))
                            while codigo_sns in codigos_consulta:
                                codigo_sns = ''.join(random.choices(string.digits, k=12))
                            # Gerar uma hora aleatoria para a consulta
                            hora_aleatoria = datetime.time(random.randint(8, 19), random.choice([0, 30]))

                            # Verificar se a hora aleatoria esta dentro dos intervalos permitidos
                            hora_consulta = None
                            if 8 <= hora_aleatoria.hour < 13 or 14 <= hora_aleatoria.hour < 19:
                                minutos = hora_aleatoria.minute // 30 * 30  # Ajustar para o intervalo de meia hora
                                hora_consulta = datetime.time(hora_aleatoria.hour, minutos)
                            else:
                                # Se estiver fora dos intervalos 8-13 e 14-19 horas, ajuste para o intervalo mais proximo
                                if hora_aleatoria.hour < 8:
                                    hora_consulta = datetime.time(8, 0)  # Ajuste para o inicio do intervalo
                                elif hora_aleatoria.hour >= 19:
                                    hora_consulta = datetime.time(19, 0)  # Ajuste para o final do intervalo
                                elif hora_aleatoria.hour >= 13 and hora_aleatoria.hour < 14:
                                    hora_consulta = datetime.time(15, 30)

                            if paciente_nr >= 5000:
                                paciente_nr = 0

                            chave_unica = (medico, current_date, hora_consulta, clinica["nome"])
                            if chave_unica not in criterios_unicos:
                                consultas.append({
                                    "ssn": pacientes[paciente_nr]["ssn"],
                                    "nif": medico,
                                    "nome": trabalha["nome"],
                                    "data": current_date,
                                    "hora": hora_consulta,
                                    "codigo_sns": codigo_sns
                                })
                                nr_consultas += 1
                                paciente_nr += 1
                                id += 1
                                criterios_unicos.add(chave_unica)
                                # Adicionar o codigo de consulta à lista de codigos utilizados
                                codigos_consulta.add(codigo_sns)
                            
                    nr_consultas_por_medico += 1
        # Passar para o proximo dia
        current_date += datetime.timedelta(days=1)
    if(id >= 5000):
        break


# Dados para as receitas
medicamentos = ["Paracetamol", "Amoxicilina", "Ibuprofeno",
        "Metformina", "Atorvastatina", "Omeprazol"]

receitas = []

# Gerando receitas para ~80% das consultas
for consulta in consultas[:round(len(consultas) * 0.8)]:
    codigo_sns = consulta['codigo_sns']  # Supondo que cada consulta tem um codigo SNS

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


# Dados para as observaçoes
observacoes = []

# Parâmetros para sintomas e métricas
sintomas_parametros = ["Dor de cabeça", "Febre", "Nausea", "Tontura", "Fadiga", "Dor abdominal",
"Tosse", "Dor no peito", "Dificuldade para respirar", "Perda de apetite", "Suores noturnos",
"Inchaço", "Dor nas articulaçoes", "Erupçao cutânea", "Calafrios", "Perda de peso", "Palpitaçoes",
"Diarreia", "Constipaçao", "Vomito", "Dores musculares", "Olhos vermelhos", "Dor de garganta", "Congestao nasal", 
"Secreçao nasal", "Prurido", "Vertigem", "Dor lombar", "Dificuldade para urinar", "Hemorragia", "Rigidez", "Falta de coordenaçao",
"Perda de equilibrio", "Alteraçao na visao", "Zumbido no ouvido", "Manchas na pele", "Tremores", "Fraqueza",
"Ansiedade", "Depressao", "Insonia", "Sonolencia excessiva", "Problemas de memoria", "Irritabilidade", "Sensibilidade a luz",
"Dor nos dentes", "Sensaçao de queimaçao", "Dor ao engolir", "Formigamento", "Caibras"]

metricas_parametros = ["Temperatura corporal", "Pressao arterial sistolica", "Pressao arterial diastolica", "Frequencia cardiaca",
"Frequencia respiratoria", "Saturaçao de oxigenio", "Nivel de glicose no sangue", "indice de massa corporal", "Peso corporal", 
"Altura", "Nivel de colesterol total", "Nivel de HDL", "Nivel de LDL", "Triglicerideos", "Hemoglobina", "Hematocrito", 
"Leucocitos", "Plaquetas", "Creatinina serica", "Taxa de filtraçao glomerular"]

fault_sintomas = copy.deepcopy(sintomas_parametros) 
fault_metricas = copy.deepcopy(metricas_parametros)
count = 1
for consulta in consultas:
    consulta_id = count
    num_sintomas = random.randint(1, 5)
    num_metricas = random.randint(0, 3)
    sintomas_escolhidos = random.sample(sintomas_parametros, num_sintomas)
    metricas_escolhidas = random.sample(metricas_parametros, num_metricas)
    for sintoma in sintomas_escolhidos:
        observacoes.append({
            "id": consulta_id,
            "parametro": sintoma,
            "valor": None  # Sintomas nao tem valor
        })
        if sintoma in fault_sintomas:
            fault_sintomas.remove(sintoma)
    
    for metrica in metricas_escolhidas:
        observacoes.append({
            "id": consulta_id,
            "parametro": metrica,
            "valor": round(random.uniform(0, 100), 2)  # Valor aleatorio para métricas
        })
        if metrica in fault_metricas:
            fault_metricas.remove(metrica)
    count += 1

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
    f.write("INSERT INTO trabalha (nif, nome, dia_da_semana) VALUES\n")
    f.write(",\n".join(["('{}', '{}', {})".format(trabalha['nif'], trabalha['nome'], trabalha['dia_da_semana']) for trabalha in trabalha_data]) + ";\n")

    # Preencher a tabela paciente
    f.write("INSERT INTO paciente (ssn, nif, nome, telefone, morada, data_nasc) VALUES\n")
    f.write(",\n".join(["('{}', '{}', '{}', '{}', '{}', '{}')".format(paciente['ssn'], paciente['nif'], paciente['nome'], paciente['telefone'], paciente['morada'], paciente['data_nasc']) for paciente in pacientes]) + ";\n")
    
    # Preencher a tabela horario
    f.write("INSERT INTO horario (data, hora) VALUES\n")
    f.write(",\n".join(["('{}', '{}')".format(horario['data'], horario['hora'])for horario in horarios]) + ";\n")

    # Preencher a tabela consulta
    f.write("INSERT INTO consulta (ssn, nif, nome, data, hora, codigo_sns) VALUES\n")
    f.write(",\n".join(["('{}', '{}', '{}', '{}', '{}', '{}')".format(consulta['ssn'], consulta['nif'], consulta['nome'], consulta['data'], consulta['hora'], consulta['codigo_sns']) for consulta in consultas]) + ";\n")
    
    # Preencher a tabela receita
    f.write("INSERT INTO receita (codigo_sns, medicamento, quantidade) VALUES\n")
    f.write(",\n".join(["('{}', '{}', {})".format(receita['codigo_sns'], receita['medicamento'], receita['quantidade']) for receita in receitas]) + ";\n")

    # Preencher a tabela observacao
    sintomas_observacoes = []
    metricas_observacoes = []
    for observacao in observacoes:
        if observacao['valor'] is None:
            sintomas_observacoes.append("({}, '{}')".format(observacao['id'], observacao['parametro']))
        else:
            metricas_observacoes.append("({}, '{}', {})".format(observacao['id'], observacao['parametro'], observacao['valor']))

    if sintomas_observacoes:
        f.write("INSERT INTO observacao (id, parametro) VALUES\n")
        f.write(",\n".join(sintomas_observacoes) + ";\n")

    if metricas_observacoes:
        f.write("INSERT INTO observacao (id, parametro, valor) VALUES\n")
        f.write(",\n".join(metricas_observacoes) + ";\n")