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


@app.route("/accounts/<account_number>/update", methods=("GET",))
def account_update_view(account_number):
    """Show the page to update the account balance."""

    with pool.connection() as conn:
        with conn.cursor() as cur:
            account = cur.execute(
                """
                SELECT account_number, branch_name, balance
                FROM account
                WHERE account_number = %(account_number)s;
                """,
                {"account_number": account_number},
            ).fetchone()
            log.debug(f"Found {cur.rowcount} rows.")

    # At the end of the `connection()` context, the transaction is committed
    # or rolled back, and the connection returned to the pool.

    if account is None:
        return jsonify({"message": "Account not found.", "status": "error"}), 404

    return jsonify(account), 200


@app.route(
    "/accounts/<account_number>/update",
    methods=(
        "PUT",
        "POST",
    ),
)
def account_update_save(account_number):
    """Update the account balance."""

    balance = request.args.get("balance")

    error = None

    if not balance:
        error = "Balance is required."
    if not is_decimal(balance):
        error = "Balance is required to be decimal."

    if error is not None:
        return jsonify({"message": error, "status": "error"}), 400
    else:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE account
                    SET balance = %(balance)s
                    WHERE account_number = %(account_number)s;
                    """,
                    {"account_number": account_number, "balance": balance},
                )
                # The result of this statement is persisted immediately by the database
                # because the connection is in autocommit mode.
                log.debug(f"Updated {cur.rowcount} rows.")

                if cur.rowcount == 0:
                    return (
                        jsonify({"message": "Account not found.", "status": "error"}),
                        404,
                    )

        # The connection is returned to the pool at the end of the `connection()` context but,
        # because it is not in a transaction state, no COMMIT is executed.

        return "", 204


@app.route(
    "/accounts/<account_number>/delete",
    methods=(
        "DELETE",
        "POST",
    ),
)
def account_delete(account_number):
    """Delete the account."""

    with pool.connection() as conn:
        with conn.cursor() as cur:
            try:
                with conn.transaction():
                    # BEGIN is executed, a transaction started
                    cur.execute(
                        """
                        DELETE FROM depositor
                        WHERE account_number = %(account_number)s;
                        """,
                        {"account_number": account_number},
                    )
                    cur.execute(
                        """
                        DELETE FROM account
                        WHERE account_number = %(account_number)s;
                        """,
                        {"account_number": account_number},
                    )
                    # These two operations run atomically in the same transaction
            except Exception as e:
                return jsonify({"message": str(e), "status": "error"}), 500
            else:
                # COMMIT is executed at the end of the block.
                # The connection is in idle state again.
                log.debug(f"Deleted {cur.rowcount} rows.")

                if cur.rowcount == 0:
                    return (
                        jsonify({"message": "Account not found.", "status": "error"}),
                        404,
                    )

    # The connection is returned to the pool at the end of the `connection()` context

    return "", 204

'''
@app.route("/ping", methods=("GET",))
def ping():
    log.debug("ping!")
    return jsonify({"message": "pong!", "status": "success"})


if __name__ == "__main__":
    app.run()
