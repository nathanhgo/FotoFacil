from flask import Flask, request, render_template, jsonify, url_for
from editor import EditorDeImagem
import json
from werkzeug.utils import secure_filename
import os
import cv2

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/editar', methods=['POST'])
def editarImagem():

    filtro = request.form.get('filtro', type=int)
    proporcao = request.form.get('proporcao', type=int)
    modo_deteccao = request.form.get('modoDeDeteccao', type=int)
    imagem_file = request.files.get('imagem')

    coordenada_manual = None
    if modo_deteccao == 2:
        coordenada_str = request.form.get('coordenadaManual')
        if coordenada_str:
            coordenada_manual = json.loads(coordenada_str)
    
    print(f"Filtro recebido: {filtro}")
    print(f"Proporção: {proporcao}")
    print(f"Modo de Detecção: {modo_deteccao}")

    if coordenada_manual:
        print(f"Coordenada Manual: {coordenada_manual}")

    
    if imagem_file:
        print(f"Nome do arquivo da imagem: {imagem_file.filename}")

        filename = 'imagem_original.jpg'
        caminho_para_salvar = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        imagem_file.save(caminho_para_salvar)

        proporcao_largura, proporcao_altura = EditorDeImagem.menuProporcao(proporcao)
        print(f'{proporcao_largura} {proporcao_altura}')


        img = cv2.imread(caminho_para_salvar)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Chamando funções de edição
        if modo_deteccao == 1:
            meio_img = EditorDeImagem.definirMeioImagem(img_rgb)
        else:
            meio_img = (coordenada_manual['x'], coordenada_manual['y'])
        
        img_recortada = EditorDeImagem.recortarProporcao(img_rgb, meio_img, proporcao_largura, proporcao_altura)
        img_equalizada = EditorDeImagem.equalizarImagem(img_recortada)
        img_redimensionada = EditorDeImagem.upscaleMantendoProporcao(img_equalizada, 'nearest')

        if filtro != 0:
            img_editada = EditorDeImagem.filtrarImagem(img_redimensionada, filtro)
        else:
            img_editada = img_redimensionada

        caminho_para_salvar2 = os.path.join(app.config['UPLOAD_FOLDER'], 'imagem_editada.jpg')
        img_para_salvar = cv2.cvtColor(img_editada, cv2.COLOR_RGB2BGR)
        cv2.imwrite(caminho_para_salvar2, img_para_salvar)

        url_do_download = url_for('static', filename=f'uploads/imagem_editada.jpg')


    return jsonify({
        'message': f'form enviado com sucesso!',
        'download_url': url_do_download
    })


if __name__ == '__main__':
    app.run(debug=False)