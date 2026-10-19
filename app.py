import os
import io
from datetime import datetime
from flask import Flask, render_template, request, send_file, jsonify

import fitz  # PyMuPDF

app = Flask(__name__)

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'template_FR.pdf')

# Mapeamento: nome do campo do formulario -> (pagina, x, y, fontsize)
# Coordenadas extraídas do template (PyMuPDF: y cresce para baixo)
FIELD_MAP = {
    # Pagina 1 - Dados do veiculo
    'numero':        (1, 100, 140, 9),
    'marca':         (1, 285, 153, 9),
    'tombamento':    (1, 140, 153, 9),
    'modelo':        (1, 430, 153, 9),
    'placa':         (1, 530, 153, 9),
    'condutor':      (1, 160, 189, 9),
    'cargo':         (1, 410, 189, 9),
    'unidade':       (1, 530, 189, 9),

    # Combustivel (X na posicao aproximada)
    'combustivel_cheio':   (1, 258, 359, 9),
    'combustivel_3_4':     (1, 262, 372, 9),
    'combustivel_1_2':     (1, 262, 390, 9),
    'combustivel_1_4':     (1, 262, 406, 9),

    # Pagina 1 - Horarios e KM
    'partida_km':    (1, 60, 366, 9),
    'partida_hora':  (1, 180, 366, 9),
    'portaria':      (1, 470, 338, 9),
    'retorno_km':    (1, 60, 391, 9),

    # Pagina 1 - Assinatura e Data
    'assinatura':    (1, 285, 783, 9),
    'data':          (1, 120, 769, 9),
    'horario_portaria': (1, 440, 366, 9),

    # Pagina 1 - Descricao dos servicos
    'descricao':     (1, 80, 232, 9),
    'locais':        (1, 210, 246, 9),

    # Pagina 2 - Itinerario
    'saida_km':      (2, 40, 170, 9),
    'saida_hora':    (2, 125, 166, 9),
    'itinerario':    (2, 275, 166, 9),
    'chegada_km':    (2, 440, 170, 9),
    'chegada_hora':  (2, 515, 166, 9),
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gerar', methods=['POST'])
def gerar():
    dados = request.get_json()
    if not dados:
        return jsonify({'erro': 'Nenhum dado recebido'}), 400

    doc = fitz.open(TEMPLATE_PATH)

    for campo, valor in dados.items():
        if not valor or campo not in FIELD_MAP:
            continue
        pagina, x, y, tamanho = FIELD_MAP[campo]
        page = doc[pagina - 1]

        # Se for campo de combustivel (marcar X)
        if campo.startswith('combustivel_'):
            page.insert_text((x, y), 'X', fontsize=tamanho, color=(0, 0, 0))
        else:
            page.insert_text((x, y), str(valor), fontsize=tamanho, color=(0, 0, 0))

    # Salva em buffer de memoria
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    nome_arquivo = f"FR_preenchida_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=nome_arquivo
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
