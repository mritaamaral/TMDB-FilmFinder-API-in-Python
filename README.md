# 🎬 TMDB FilmFinder — Movie Search with Python & TMDB API

> Projeto educacional de busca de filmes utilizando a API pública do The Movie Database (TMDB).

---

## 📖 Sobre o Projeto

O **TMDB FilmFinder** é uma aplicação Python que consome a [API do TMDB](https://www.themoviedb.org/documentation/api) para permitir a busca e consulta de informações sobre filmes, como título, sinopse, popularidade e poster. Desenvolvido com fins educacionais, o projeto serve como introdução ao consumo de APIs REST com Python.

---

## ✨ Funcionalidades

- 🔍 Busca de filmes por título
- 📋 Exibição de informações detalhadas (título, sinopse, nota média, data de lançamento)
- 🖼️ Acesso ao caminho do poster do filme
- 🌐 Integração com a API REST do TMDB (v3)

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Descrição |
|---|---|
| Python 3 | Linguagem principal |
| Requests | Biblioteca para requisições HTTP |
| TMDB API v3 | Fonte de dados de filmes |

---

## 🚀 Como Executar

### Pré-requisitos

- Python 3.8 ou superior instalado
- Conta no [TMDB](https://www.themoviedb.org/signup) para obter uma chave de API gratuita

### 1. Clone o repositório

```bash
git clone https://github.com/mritaamaral/TMDB-FilmFinder-API-in-Python.git
cd TMDB-FilmFinder-API-in-Python
```

### 2. Instale as dependências

```bash
pip install requests
```

### 3. Configure sua chave de API

Crie um arquivo `.env` ou edite o arquivo de configuração com sua chave:

```python
API_KEY = "sua_chave_api_aqui"
```

> 💡 Para obter sua chave gratuita, acesse [developer.themoviedb.org](https://developer.themoviedb.org/docs/getting-started) e siga as instruções.

### 4. Execute o projeto

```bash
python main.py
```

---

## 📁 Estrutura do Projeto

```
TMDB-FilmFinder-API-in-Python/
├── main.py          # Ponto de entrada da aplicação
├── README.md        # Documentação do projeto
└── ...
```

---

## 📚 Aprendizados

Este projeto foi desenvolvido como parte do aprendizado em programação, cobrindo conceitos como:

- Consumo de APIs REST com Python
- Manipulação de respostas JSON
- Uso da biblioteca `requests`
- Organização básica de projetos Python

---

## 🙋‍♀️ Autora

**Maria Rita Amaral**  
Aspirante a desenvolvedora, atualmente aprendendo programação e construindo projetos práticos.

[![GitHub](https://img.shields.io/badge/GitHub-mritaamaral-181717?style=flat&logo=github)](https://github.com/mritaamaral)

---

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais. Sinta-se à vontade para estudar e se inspirar no código! 😊

---

> *"Aprender programando, um projeto de cada vez."*
