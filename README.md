### # Sisatas

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
pyinstaller --onefile -w sisatas.py

```

Na pasta dist cole a base de dados atas.db para a pasta caso já exista dados
Pode excluir o arquivo main.spec e a pasta build