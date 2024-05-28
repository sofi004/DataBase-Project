#!/usr/bin/python3
# Copyright (c) BDist Development Team
# Distributed under the terms of the Modified BSD License.
import os
import datetime
import json
from logging.config import dictConfig

from flask import Flask, jsonify, request
from psycopg.rows import namedtuple_row
from psycopg_pool import ConnectionPool

# Use the DATABASE_URL environment variable if it exists, otherwise use the default.
# Use the format postgres://username:password@hostname/database_name to connect to the database.

DATABASE_URL = os.environ.get("DATABASE_URL", "postgres://postgres:postgres@postgres/saude")

pool = ConnectionPool(
    conninfo=DATABASE_URL,
    kwargs={
        "autocommit": True,  # If True don’t start transactions automatically.
        "row_factory": namedtuple_row,
    },
    min_size=4,
    max_size=10,
    open=True,
    # check=ConnectionPool.check_connection,
    name="postgres_pool",
    timeout=5,
)

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s:%(lineno)s - %(funcName)20s(): %(message)s",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }
)

app = Flask(__name__)
app.config.from_prefixed_env()
log = app.logger

@app.route("/", methods=("GET",))
def list_clinics():
    "Show all clinics"
    try:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                clinics = cur.execute(
                    """
                    SELECT nome, morada
                    FROM clinica;
                    """,
                    {},
                ).fetchall()
                log.debug(f"Found {cur.rowcount} rows.")

        if not clinics:
            log.error("No clinics found.")
            raise ValueError("No clinics available to show.")

    except ValueError as e:
        response = jsonify({'error': str(e)})
        response.status_code = 404
        return response

    return jsonify(clinics), 200


@app.route("/c/<clinica>/", methods=("GET",))
def list_especialidades_clinica(clinica):
    "Mostra as especialidades de uma clinica"
    try:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                # Check if the clinic exists
                clinic_exists = cur.execute(
                    """
                    SELECT 1
                    FROM clinica
                    WHERE nome = %(clinica)s;
                    """,
                    {"clinica": clinica}
                ).fetchone()

                if not clinic_exists:
                    log.error(f"Clinic {clinica} does not exist.")
                    raise ValueError(f"Clinic {clinica} does not exist.")

                # Fetch especialidades if the clinic exists
                especialidades = cur.execute(
                    """
                    SELECT DISTINCT especialidade
                    FROM trabalha t
                    JOIN medico m ON m.nif = t.nif
                    JOIN clinica c ON t.nome = c.nome
                    WHERE c.nome = %(clinica)s;
                    """,
                    {"clinica": clinica}
                ).fetchall()
                log.debug(f"Found {cur.rowcount} rows.")

                if not especialidades:
                    log.error(f"No especialidades found for clinic {clinica}.")
                    raise ValueError(f"No especialidades found for clinic {clinica}.")

    except ValueError as e:
        response = jsonify({'error': str(e)})
        response.status_code = 404
        return response

    return jsonify(especialidades), 200

@app.route("/c/<clinica>/<especialidade>/", methods=("GET",))

def list_horarios_medicos_clinica(clinica, especialidade):
    "Lista os médicos da clinica e da especialidade disponiveis"
    try:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                                # Verifica se há médicos na clínica e especialidade especificada
                cur.execute(
                    """
                    SELECT m.nif, m.nome AS nome_medico
                    FROM medico m
                    JOIN trabalha t ON m.nif = t.nif
                    WHERE m.especialidade = %(especialidade)s
                    AND t.nome = %(clinica)s
                    """,
                    {"clinica": clinica, "especialidade": especialidade}
                )
                medicos_clinica = cur.fetchall()
                if not medicos_clinica:
                    raise ValueError("Nenhum médico encontrado para a clínica e especialidade especificada.")
                cur.execute(
                    """
                    WITH medicos_clinica AS (
                        SELECT m.nif, m.nome AS nome_medico
                        FROM medico m
                        JOIN trabalha t ON m.nif = t.nif
                        WHERE m.especialidade = %(especialidade)s
                        AND t.nome = %(clinica)s
                        ),
                    horarios_ocupados AS (
                        SELECT c.nif, c.data, c.hora
                        FROM consulta c
                        JOIN medicos_clinica mc ON c.nif = mc.nif
                        WHERE c.nome = 'sao_joao'
                    ),
                    horarios_disponiveis AS (
                        SELECT mc.nif, h.data, h.hora,
                            ROW_NUMBER() OVER (PARTITION BY mc.nif ORDER BY h.data, h.hora) AS row_num
                        FROM medicos_clinica mc
                        CROSS JOIN horario h
                        LEFT JOIN horarios_ocupados ho ON mc.nif = ho.nif AND h.data = ho.data AND h.hora = ho.hora
                        WHERE ho.nif IS NULL AND h.data > current_date
                    )
                    SELECT mc.nif, mc.nome_medico, hd.data, hd.hora
                    FROM medicos_clinica mc
                    JOIN horarios_disponiveis hd ON mc.nif = hd.nif
                    WHERE hd.row_num <= 3
                    ORDER BY mc.nif, hd.data, hd.hora;
                    """,
                 {"clinica": clinica, "especialidade": especialidade}
                 )
                medicos_horarios = cur.fetchall()
                log.debug(f"Found {len(medicos_horarios)} rows.")
                # Group the schedules by doctor's NIF to check the count
                from collections import defaultdict
                horarios_por_medico = defaultdict(list)
                for nif, nome_medico, data, hora in medicos_horarios:
                    horarios_por_medico[nif].append((nome_medico, data, hora))
                
                # Check if every doctor has at least 3 available schedules
                for nif, horarios in horarios_por_medico.items():
                    if len(horarios) < 3:
                        raise ValueError(f"O médico com NIF {nif} não tem pelo menos 3 horários disponíveis.")
        return jsonify(str(medicos_horarios))
    except Exception as e:
        log.error(f"An error occurred: {e}")
        return jsonify({"Oops": str(e)}), 500
        #return jsonify({"error": "An error occurred while fetching the data."}), 500



@app.route("/a/<clinica>/registar/", methods=["PUT", "POST"])
def regista_marcacao_clinica(clinica):
    # Obtém os dados da solicitação
    ssn_paciente = request.args.get("ssn_paciente")
    nif_medico = request.args.get("nif_medico")
    data_consulta = request.args.get("data")
    hora_consulta = request.args.get("hora")
    if not ssn_paciente or not nif_medico or not data_consulta or not hora_consulta:
        return jsonify({"error": "Missing required parameters"}), 400
    # Convert data_consulta to a datetime object for comparison
    data_hora_consulta_str = f"{data_consulta} {hora_consulta}"
    data_hora_consulta_dt = datetime.datetime.strptime(data_hora_consulta_str, '%Y-%m-%d %H:%M')
    # Get the current date
    current_date = datetime.datetime.now()
    # Check if data_consulta is before the current date
    if data_hora_consulta_dt <= current_date:
        return jsonify({"error": "Consulta date should be after the current date"}), 400
    try:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                # Verificar se o horário está disponível
                cur.execute("""
                    SELECT 1 
                    FROM consulta 
                    WHERE nif = %s 
                    AND data = %s 
                    AND hora = %s
                """, (nif_medico, data_consulta, hora_consulta))
                if cur.fetchone():
                    return jsonify({"error": "O médico não está disponível no horário especificado."}), 409
                # Inserir a nova consulta
                cur.execute("""
                    INSERT INTO consulta (ssn, nif, nome, data, hora)
                    VALUES (%s, %s, %s, %s, %s)
                """, (ssn_paciente, nif_medico, clinica, data_consulta, hora_consulta))
                conn.commit()
                return jsonify({"message": "Consulta registrada com sucesso"}), 201
    except Exception as e:
        log.error(f"Error registering consultation: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/a/<clinica>/cancelar/", methods=("DELETE",))
def cancela_consulta(clinica):
    "Cancela uma consulta já marcada"
    ssn_paciente = request.args.get("ssn_paciente")
    nif_medico = request.args.get("nif_medico")
    data_consulta = request.args.get("data")
    hora_consulta = request.args.get("hora")
    if not ssn_paciente or not nif_medico or not data_consulta or not hora_consulta:
        return jsonify({"error": "Missing required parameters"}), 400
    # Convert data_consulta to a datetime object for comparison
    data_hora_consulta_str = f"{data_consulta} {hora_consulta}"
    data_hora_consulta_dt = datetime.datetime.strptime(data_hora_consulta_str, '%Y-%m-%d %H:%M')
    # Get the current date
    current_date = datetime.datetime.now()
    # Check if data_consulta is equal to or older than the current date
    if data_hora_consulta_dt >= current_date:
        return jsonify({"error": "Cannot cancel a consulta that has already occurred"}), 400
    try:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                # Verificar se a consulta existe
                cur.execute(
                    """
                    SELECT COUNT(*) FROM consulta c
                    WHERE c.ssn = %s and c.nif = %s and c.nome = %s and c.data = %s and c.hora = %s
                    """,
                    (ssn_paciente, nif_medico, clinica, data_consulta, hora_consulta)
                )
                count = cur.fetchone()[0]

                if count == 0:
                    return jsonify({"error": "Consulta não encontrada"}), 404

                cur.execute(
                    """
                    SELECT codigo_sns, id
                    FROM consulta
                    WHERE ssn = %s AND nif = %s AND nome = %s AND data = %s AND hora = %s
                    """,
                    (ssn_paciente, nif_medico, clinica, data_consulta, hora_consulta)
                )
                consulta_info = cur.fetchone()
                codigo_sns = consulta_info[0]
                id_consulta = consulta_info[1]
                # Deleting associated Receita records
                cur.execute(
                    """
                    DELETE FROM receita
                    WHERE codigo_sns = %s
                    """,
                    (codigo_sns,)
                )
                # Deleting associated Observacao records
                cur.execute(
                    """
                    DELETE FROM observacao
                    WHERE id_consulta = %s
                    """,
                    (id_consulta,)
                )
                cur.execute(
                    """
                    DELETE FROM consulta c
                    WHERE c.ssn = %s and c.nif = %s and c.nome = %s and c.data = %s and c.hora = %s
                    """,
                    (ssn_paciente, nif_medico, clinica, data_consulta, hora_consulta),)
                conn.commit()
                return jsonify({"message": "Consulta apagada com sucesso"}), 201
    except Exception as e:
        log.error(f"Error deleting consultation: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run()
