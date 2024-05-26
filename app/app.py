#!/usr/bin/python3
# Copyright (c) BDist Development Team
# Distributed under the terms of the Modified BSD License.
import os
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


def is_decimal(s):
    """Returns True if string is a parseable float number."""
    try:
        float(s)
        return True
    except ValueError:
        return False

@app.route("/", methods=("GET",))

def list_clinics():
    "Show all clinics"
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

    return jsonify(clinics), 200


@app.route("/c/<clinica>/", methods=("GET",))

def list_especialidades_clinica(clinica):
    "Mostra as especialidades de uma clinica"
    with pool.connection() as conn:
        with conn.cursor() as cur:
            especialidades = cur.execute(
                """
                SELECT DISTINCT especialidade
                FROM trabalha t
                JOIN medico m on m.nif = t.nif
                JOIN clinica c ON t.nome = c.nome
                WHERE c.nome = %(clinica)s;
                """,
                {"clinica": clinica},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")

    return jsonify(especialidades), 200

@app.route("/c/<clinica>/<especialidade>/", methods=("GET",))

def list_horarios_medicos_clinica(clinica, especialidade):
    "Lista os médicos da clinia e da especialidade disponiveis"
    with pool.connection() as conn:
        with conn.cursor() as cur:
            especialidades = cur.execute(
                """
WITH 
medicos_clinica AS (
    SELECT m.nif, m.nome AS nome_medico
    FROM medico m
    JOIN trabalha t ON m.nif = t.nif
    WHERE m.especialidade = %(especialidade)s
    AND t.nome = %(clinica)s
),
horarios_ocupados AS (
    SELECT nif, data, hora
    FROM consulta
),
horarios_disponiveis AS (
    SELECT 
        mc.nif, 
        mc.nome_medico, 
        generate_series(current_date, current_date + interval '30 day', interval '1 day')::date AS data,
        (generate_series(0, 10) * interval '1 hour' + time '08:00:00')::time AS hora
    FROM medicos_clinica mc
),
primeiros_tres_disponiveis AS (
    SELECT 
        hd.nif, 
        hd.nome_medico, 
        hd.data, 
        hd.hora,
        ROW_NUMBER() OVER (PARTITION BY hd.nif ORDER BY hd.data, hd.hora) AS rn
    FROM horarios_disponiveis hd
    LEFT JOIN horarios_ocupados ho ON hd.nif = ho.nif AND hd.data = ho.data AND hd.hora = ho.hora
    WHERE ho.nif IS NULL
)
SELECT 
    nif, 
    nome_medico, 
    data, 
    hora
FROM 
    primeiros_tres_disponiveis
WHERE rn <= 3
ORDER BY nif, data, hora;



                """,
                {"clinica": clinica, "especialidade": especialidade},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")

    return jsonify(especialidades), 200


@app.route("/a/<clinica>/registar/", methods=["PUT", "POST"])
def regista_marcacao_clinica(clinica):
    # Obtém os dados da solicitação
    
    ssn_paciente = request.args.get("ssn_paciente")
    nif_medico = request.args.get("nif_medico")
    data_consulta = request.args.get("data")
    hora_consulta = request.args.get("hora")

    if not ssn_paciente or not nif_medico or not data_consulta or not hora_consulta:
        return jsonify({"error": "Missing required parameters"}), 400

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

                return jsonify({"message": "Consulta registrada com sucesso", "codigo_sns": 0}), 201

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
                    
                    DELETE FROM consulta c
                    WHERE c.ssn = %s and c.nif = %s and c.nome = %s and c.data = %s and c.hora = %s

                    """,
                    (ssn_paciente, nif_medico, clinica, data_consulta, hora_consulta),)
                conn.commit()

                return jsonify({"message": "Consulta apagada com sucesso", "codigo_sns": 0}), 201
    except Exception as e:
        log.error(f"Error deleting consultation: {e}")
        return jsonify({"error": "Internal server error"}), 500
'''
@app.route("/", methods=("GET",))
@app.route("/accounts", methods=("GET",))
def account_index():
    """Show all the accounts, most recent first."""

    with pool.connection() as conn:
        with conn.cursor() as cur:
            accounts = cur.execute(
                """
                SELECT account_number, branch_name, balance
                FROM account
                ORDER BY account_number DESC;
                """,
                {},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")

    return jsonify(accounts), 200




'''
@app.route("/ping", methods=("GET",))
def ping():
    log.debug("ping!")
    return jsonify({"message": "pong!", "status": "success"})


if __name__ == "__main__":
    app.run()
