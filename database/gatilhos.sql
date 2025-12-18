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