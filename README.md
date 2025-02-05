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

**Caso houver erro ao gerar o .exe**

```
pyinstaller sisatas.spec
```
Edite sisatas.spec para colocar as imagens

```
datas=[('assets/img/logo.png', 'assets/img'),
    ('assets/img/Buscar_Fala.png', 'assets/img'),
    ('assets/img/Adicionar.png', 'assets/img'),
    ('assets/img/calendar.png', 'assets/img'),
    ('assets/img/Exportar_Dados.png', 'assets/img'),
    ('assets/img/Importar_Dados.png', 'assets/img'),
    ('assets/img/Listar_Atas.png', 'assets/img'),
    ('assets/img/logo_principal.png', 'assets/img'),
    ('assets/img/Secretarias.png', 'assets/img'),
    ('assets/img/Secretarios.png', 'assets/img'),
    ('assets/img/seta_para_baixo.png', 'assets/img')],
```
Agora recompile o .exe

```pyinstaller sisatas.spec```

Na pasta dist cole a base de dados banco_de_dados_atas.db para a pasta caso já exista dados
Pode excluir o arquivo main.spec e a pasta build

**Pasta com as versões do sistema Disponibilizadas**
H:\Projetos\Sistemas\Sisatas\Executável com banco de dados\Versões