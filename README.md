### # Sisatas
Sistema para gerir Atas para o Prefeito Sandro.
O sistema é um executável que rodará no Notebook do Prefeito.
**O banco de dados** é salvo no arquivo: banco_de_dados.db.
Para carregar um banco de dados já existente, importe por dentro do sistema a base de dados.

## Rodar localmente

Crie um ambiente virtual

```
python -m venv venv
```
Ative o ambiente virtual e instale os requirements

```
venv\Scripts\activate
pip install -r requirements.txt

```

**Run terminal**

```
python sisatas.py
```

**Gerar .exe da aplicação no terminal**

```
pyinstaller -w --onefile --add-data "assets/img/logo.png;assets/img" sisatas.py

```

Na pasta dist cole a base de dados banco_de_dados_atas.db para a pasta caso já exista dados
Pode excluir o arquivo main.spec e a pasta build

**Pasta com as versões do sistema Disponibilizadas**
H:\Projetos\Sistemas\Sisatas\Executável com banco de dados\Versões