INSERT INTO clinica (nome, telefone, morada)
VALUES ('sao_joao', '213313313', 'Coimbra');


INSERT INTO trabalha (nif, nome, dia_da_semana)
VALUES ('987654320', 'sao_joao', '0');

INSERT INTO consulta (ssn, nif, nome, data, hora, codigo_sns)
VALUES ('75817721399', '987654321', 'sao_joao', '2024-06-02', '15:00:00', '123456789011');

INSERT INTO medico (nif, nome, telefone, morada, especialidade)
VALUES ('987654321', 'Dr. Pedro Silva', '9876543210', 'Rua das Flores, 123', 'Pediatria');

INSERT INTO trabalha (nif, nome, dia_da_semana)
VALUES ('987654321', 'sao_joao', 1);

INSERT INTO paciente (ssn, nif, nome, telefone, morada, data_nasc)
VALUES ('12345678910', '123456789', 'João Silva', '912345678', 'Rua Exemplo, 123', '1980-01-01');

INSERT INTO observacao (id, parametro) 
VALUES (14, 'Calafrios');
(8, 'Calafrios');