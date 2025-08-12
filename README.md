# 🐶 CinTaxError

**CinTaxError** é um jogo 2D desenvolvido em Python usando Pygame, onde você controla **Byte**, um cachorro aventureiro que precisa coletar petiscos enquanto evita inimigos.
Se Byte entrar na área de dano de um inimigo, ele começará a persegui-lo!

---

## 🎯 Objetivo do Jogo

* Controlar o personagem **Byte** usando o teclado.
* Coletar todos os petiscos espalhados pelo mapa.
* Evitar a aproximação dos inimigos, pois eles irão correr atrás de você ao detectar sua presença.
* Chegar ao final vivo, utilizando estratégias para escapar das perseguições.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* **Pygame** – Biblioteca para criação de jogos 2D.
* **PyTMX** – Biblioteca para carregamento de mapas criados no Tiled.
* **Tiled Map Editor** – Utilizado para criar os mapas do jogo.

---

## 📂 Estrutura do Projeto

```
📁 projeto
 ├── main.py              # Arquivo principal do jogo
 ├── Player.py            # Lógica e animação do personagem Byte
 ├── Inimigo.py           # Lógica e IA dos inimigos
 ├── imagens/             # Sprites e telas do jogo
 ├── data/maps/           # Mapas criados no Tiled (.tmx)
 ├── requirements.txt     # Dependências do projeto
 └── README.md            # Este arquivo
```

---

## 📦 Instalação e Execução

### 1️⃣ Pré-requisitos

* Python 3.x instalado ([Download Python](https://www.python.org/downloads/))
* Pip (gerenciador de pacotes do Python)

### 2️⃣ Clonar o repositório

```bash
git clone https://github.com/seu-usuario/byte-adventure.git
cd byte-adventure
```

### 3️⃣ Criar ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 4️⃣ Instalar dependências

```bash
pip install -r requirements.txt
```

### 5️⃣ Executar o jogo

```bash
python main.py
```

---

## 🎮 Controles

* **Setas direcionais** → Movimento do Byte
* **ESC** → Sair do jogo

---

## 📋 Dependências (requirements.txt)

```txt
pygame
pytmx
```

---

## 👥 Autores

Projeto desenvolvido pela turma de **Introdução à Programação**, como exercício prático para aplicar conceitos de lógica, POO e bibliotecas gráficas.
