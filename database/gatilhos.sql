DELIMITER //
-- Pós evento
CREATE TRIGGER trg_repoe_livro AFTER UPDATE 
ON emprestimos 
FOR EACH ROW 
BEGIN 
	IF NEW.status_emprestimo = "devolvido" THEN
		UPDATE livros SET quantidade_disponivel = quantidade_disponivel + 1 WHERE id_livro = OLD.livro_id;
	END IF;
END // 

CREATE TRIGGER 
trg_tira_livro AFTER INSERT
ON emprestimos
FOR EACH ROW
BEGIN
	UPDATE livros SET quantidade_disponivel = quantidade_disponivel - 1 WHERE id_livro = NEW.livro_id;
END //

-- triggers validação
-- Impedir quantidade negativa de livros

create trigger trg_corrige_quantidade_livro
before insert on livros
for each row
begin
    if NEW.quantidade_disponivel < 0 then
        set NEW.quantidade_disponivel = 0;
    end if;
end//

-- Ajustar ISBN com tamanho diferente de 13 (se não tiver 13 caracteres , ele vira 0)

create trigger trg_corrige_isbn
before insert on livros
for each row
begin
    if length(NEW.isbn) < 13 then 
        set NEW.isbn = '0000000000000';
    end if;
end//

-- Ajustar data futura (se estiver no futuro coloque na data atual)

create trigger trg_corrige_ano_publicacao_livro
before insert on livros
for each row
begin
    if NEW.ano_publicacao > year(curdate()) then
        set NEW.ano_publicacao = year(curdate());
    end if;
    
end//

-- Impedir títulos de livros vazios

create trigger trg_livros_titulo_validacao
before insert on livros
for each row
begin
    set NEW.titulo = trim(NEW.titulo);

    if NEW.titulo = '' then
        set NEW.titulo = 'TÍTULO NÃO INFORMADO';
    end if;
end;
//


-- Impedir multa negativa do usuário

create trigger trg_usuarios_multa_validacao
before insert on usuarios
for each row
begin
    if NEW.multa_atual < 0 then
        set NEW.multa_atual = 0;
    end if;
end;
//
