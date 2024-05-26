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

# Lista de clínicas em diferentes localidades de Lisboa
clinicas = [
    {"nome": "Hospital da Luz", "telefone": generate_phone_number(), "morada": "Avenida Almirante Reis, Lisboa"},
    {"nome": "Hospital de Santa Maria", "telefone": generate_phone_number(), "morada": "Alameda das Linhas de Torres, Lisboa"},
    {"nome": "Clinica Sao Francisco Xavier", "telefone": generate_phone_number(), "morada": "Estrada Forte do Alto Duque, Oeiras"},
    {"nome": "Hospital de Cascais", "telefone": generate_phone_number(), "morada": "Rua Doutor Alvaro Esmeriz, Cascais"},
    {"nome": "Hospital Beatriz Angelo", "telefone": generate_phone_number(), "morada": "Rua Cidade de Bolama, Loures"}
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
            "morada": ' '.join(random.choices(["Rua", "Avenida", "Praceta", "Travessa", "Largo"], k=1)) + ' ' +
                      ''.join(random.choices(string.ascii_letters, k=10)) + ', ' +
                      ' '.join(random.choices(["Lisboa", "Oeiras", "Cascais", "Loures", "Amadora", "Sintra"], k=1)),
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
        "morada": ' '.join(random.choices(["Rua", "Avenida", "Praceta", "Travessa", "Largo"], k=1)) + ' ' +
                  ''.join(random.choices(string.ascii_letters, k=10)) + ', ' +
                  ' '.join(random.choices(["Lisboa", "Oeiras", "Cascais", "Loures", "Amadora", "Sintra"], k=1)),
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
            "morada": ' '.join(random.choices(["Rua", "Avenida", "Praceta", "Travessa", "Largo"], k=1)) + ' ' +
                      ''.join(random.choices(string.ascii_letters, k=10)) + ', ' +
                      ' '.join(random.choices(["Lisboa", "Oeiras", "Cascais", "Loures", "Amadora", "Sintra"], k=1)),
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
        "morada": ' '.join(random.choices(["Rua", "Avenida", "Praceta", "Travessa", "Largo"], k=1)) + ' ' +
                  ''.join(random.choices(string.ascii_letters, k=10)) + ', ' +
                  ' '.join(random.choices(["Lisboa", "Oeiras", "Cascais", "Loures", "Amadora", "Sintra"], k=1)),
        "data_nasc": generate_birth_date()
    })

# Definindo o número mínimo de consultas por médico por dia
min_consultas_por_medico = 2

# Definindo o número mínimo de consultas por dia por clínica
min_consultas_por_dia_por_clinica = 20

# Intervalo de tempo para as consultas
inicio_2023 = datetime.date(2023, 1, 1)
fim_2024 = datetime.date(2024, 12, 31)

# Schedule patients consultations
consultas = []  # Inicialize a lista de consultas
codigos_consulta = set()  # Conjunto para rastrear códigos de consulta utilizados
codigos_consulta = set()
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
receitas = [
    {"codigo_sns": "123456789012", "medicamento": "Paracetamol", "quantidade": 2},
    {"codigo_sns": "234567890123", "medicamento": "Amoxicilina", "quantidade": 1},
    {"codigo_sns": "345678901234", "medicamento": "Ibuprofeno", "quantidade": 3}
]

# Dados para as observações
observacoes = [
    {"id_consulta": 1, "parametro": "Pressao arterial", "valor": 120},
    {"id_consulta": 2, "parametro": "Temperatura", "valor": 37.5},
    {"id_consulta": 3, "parametro": "Peso", "valor": 70}
]

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
    
    # Preencher a tabela consulta
    f.write("INSERT INTO consulta (ssn, nif, nome, data, hora, codigo_sns) VALUES\n")
    f.write(",\n".join(["('{}', '{}', '{}', '{}', '{}', '{}')".format(consulta['id'], consulta['ssn'], consulta['nif_medico'], consulta['nome_clinica'], consulta['data'], consulta['hora'], consulta['codigo_sns']) for consulta in consultas]) + ";\n")
    
    # Preencher a tabela receita
    f.write("INSERT INTO receita (codigo_sns, medicamento, quantidade) VALUES\n")
    f.write(",\n".join(["('{}', '{}', {})".format(receita['codigo_sns'], receita['medicamento'], receita['quantidade']) for receita in receitas]) + ";\n")

    # Preencher a tabela observacao
    f.write("INSERT INTO observacao (id, parametro, valor) VALUES\n")
    f.write(",\n".join(["({}, '{}', {})".format(observacao['id_consulta'], observacao['parametro'], observacao['valor']) for observacao in observacoes]) + ";\n")