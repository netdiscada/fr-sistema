# FR - Sistema de Preenchimento da Ficha e Relatório Diário

Sistema web para preenchimento automático da FR (Ficha e Relatório Diário de Serviços) da Secretaria Municipal de Serviços Urbanos e Zeladoria (SMSUZ) - Mogi das Cruzes/SP.

## Como funciona

O sistema usa o **PDF original da FR como template**. Um formulário web coleta os dados e, ao gerar, sobrepõe os campos preenchidos em cima do template, garantindo que a FR saia **idêntica ao original**. Apenas a assinatura é deixada em branco para ser preenchida manualmente após impressão.

## Estrutura

```
fr-sistema/
├── app.py                 # Backend Flask
├── template_FR.pdf        # Modelo original da FR (2 páginas)
├── requirements.txt       # Dependências Python
├── static/                # (futuro: CSS/JS separados)
├── templates/
│   └── index.html         # Formulário web
└── backups/               # PDFs gerados (opcional)
```

## Campos preenchidos automaticamente

**Página 1:**
- Número, Marca, Tombamento, Modelo, Placa
- Condutor, Cargo/Função, Unidade
- Combustível (Cheio / 3/4 / 1/2 / 1/4)
- Partida (km/Hod.), Partida - Horário, Portaria, Retorno (km/Hod.)
- Descrição dos serviços, Local(is)
- Data, Assinatura (campo deixado para preenchimento manual)

**Página 2:**
- Saída (km/Hod.), Saída - Horário, Itinerário
- Chegada (km/Hod.), Chegada - Horário

## Como rodar localmente

```bash
cd fr-sistema
pip install -r requirements.txt
python app.py
```

Acesse: http://localhost:5000

## Deploy no GitHub Pages + backend

O frontend é estático (HTML/JS). O backend precisa rodar em um servidor com Python. Opções:

1. **VPS própria** (sua Oracle A1.Flex): rode o Flask via gunicorn
2. **Render / Railway / PythonAnywhere**: hospede o Flask gratuitamente
3. **GitHub Actions**: para geração em lote via workflow

## Tecnologias

- Python + Flask (backend)
- PyMuPDF (fitz) - overlay de texto no PDF template
- HTML/CSS/JS puro (frontend, sem framework)
