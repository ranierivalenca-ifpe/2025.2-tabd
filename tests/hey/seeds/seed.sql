CREATE DATABASE tabd;

-- Switch to the newly created database
\c tabd;

CREATE TABLE clientes (
    id SERIAL PRIMARY KEY, -- auto-incrementing ID
    nome VARCHAR(100) NOT NULL, 
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(100) NOT NULL,
    telefone VARCHAR(15),
    endereco TEXT
);

CREATE TABLE restaurantes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    endereco TEXT NOT NULL,
    telefone VARCHAR(15)
);

CREATE TABLE produtos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    preco DECIMAL(10, 2) NOT NULL,
    restaurante_id INT REFERENCES restaurantes(id)
);

CREATE TABLE pedidos (
    id SERIAL PRIMARY KEY,
    cliente_id INT REFERENCES clientes(id),
    restaurante_id INT REFERENCES restaurantes(id),
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'Pendente',
    total DECIMAL(10, 2) NOT NULL
);

CREATE TABLE itens_pedido (
    id SERIAL PRIMARY KEY,
    pedido_id INT REFERENCES pedidos(id),
    produto_id INT REFERENCES produtos(id),
    quantidade INT NOT NULL,
    preco_unitario DECIMAL(10, 2) NOT NULL
);

CREATE TABLE entregadores (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    telefone VARCHAR(15),
    veiculo VARCHAR(50)
);

CREATE TABLE entregas (
    id SERIAL PRIMARY KEY,
    pedido_id INT REFERENCES pedidos(id),
    entregador_id INT REFERENCES entregadores(id),
    data_entrega TIMESTAMP,
    status VARCHAR(50) DEFAULT 'A Caminho'
);


-- Indexes for performance optimization
CREATE INDEX idx_clientes_email ON clientes(email);
CREATE INDEX idx_restaurantes_nome ON restaurantes(nome);
CREATE INDEX idx_pedidos_cliente_id ON pedidos(cliente_id);
CREATE INDEX idx_pedidos_restaurante_id ON pedidos(restaurante_id);
CREATE INDEX idx_itens_pedido_pedido_id ON itens_pedido(pedido_id);
CREATE INDEX idx_itens_pedido_produto_id ON itens_pedido(produto_id);
CREATE INDEX idx_entregas_pedido_id ON entregas(pedido_id);
CREATE INDEX idx_entregas_entregador_id ON entregas(entregador_id);

-- Testing Queries
-- Número de pedidos nos últimos 30 dias por restaurante
SELECT id, data, status
FROM pedidos
WHERE data >= NOW() - INTERVAL '30 days'
ORDER BY data DESC;

--
SELECT date_trunc('day', data) AS dia, SUM(total) AS receita
FROM pedidos
WHERE data >= NOW() - INTERVAL '30 days'
GROUP BY 1
ORDER BY 1;

--
-- create materialized view mais_vendidos_mat as
SELECT r.id as rest_id, r.nome as restaurante, pr.id as item_id, pr.nome as item, SUM(i.quantidade) AS qtd_vendida
    , SUM(i.quantidade * pr.preco) AS receita
FROM itens_pedido i
JOIN pedidos p   ON p.id = i.pedido_id
JOIN restaurantes r ON r.id = p.restaurante_id
JOIN produtos pr ON pr.id = i.produto_id
WHERE p.data >= NOW() - INTERVAL '30 days'
GROUP BY r.id, r.nome, pr.id, pr.nome, pr.preco
ORDER BY qtd_vendida DESC;