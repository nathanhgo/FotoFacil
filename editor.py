import cv2

class EditorDeImagem:
  @staticmethod
  def menuProporcao(opc): # Usuário escolhe a proporção desejada

      if opc == 1:
        proporcao_largura = 4
        proporcao_altura = 5

      elif opc == 2:
        proporcao_largura = 9
        proporcao_altura = 16

      elif opc == 3:
        proporcao_largura = 16
        proporcao_altura = 9

      elif opc == 4:
        proporcao_largura = 1
        proporcao_altura = 1

      return proporcao_largura, proporcao_altura


  @staticmethod
  def definirMeioImagem(img):

    img_base = img.copy() # img colorida

    face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml") # definir o objeto procurado

    face = face_classifier.detectMultiScale(
        img_base, scaleFactor=1.1, minNeighbors=10, minSize=(40, 40) # procurar objeto na imagem (gera vetor com posições)
    )

    for (x, y, w, h) in face:
        cv2.rectangle(img_base, (x, y), (x + w, y + h), (0, 255, 0), 2) # desenhar retângulo nas posições


    try: # Se for encontrado algum rosto, definir o meio dele
      meiox_face = int(face[0][0] + (face[0][2] / 2))
      meioy_face = int(face[0][1] + (face[0][3] / 2))

    except: # Se não, ignorar
      meiox_face = 0
      meioy_face = 0

    return meiox_face, meioy_face

  @staticmethod
  def recortarProporcao(img, ponto, proporcao_largura, proporcao_altura):
      altura_original, largura_original = img.shape[:2]
      x_centro, y_centro = ponto

      # Calcular altura e largura do recorte baseado na proporção
      altura_baseada_na_largura = int((largura_original * proporcao_altura) / proporcao_largura) # Ex: (1920 * 9) / 16) = 1080

      if altura_baseada_na_largura <= altura_original:
          largura_recorte = largura_original
          altura_recorte = altura_baseada_na_largura
      else:
          largura_recorte = int((altura_original * proporcao_largura) / proporcao_altura) # Ex: (1080 * 16) / 9) = 1920
          altura_recorte = altura_original

      # Calcular limites do recorte ao redor do ponto
      x1 = int(x_centro - largura_recorte / 2)
      x2 = int(x_centro + largura_recorte / 2)
      y1 = int(y_centro - altura_recorte / 2)
      y2 = int(y_centro + altura_recorte / 2)

      # Garantir que o recorte fique dentro da imagem
      x1 = max(0, min(largura_original - largura_recorte, x1))
      x2 = x1 + largura_recorte
      y1 = max(0, min(altura_original - altura_recorte, y1))
      y2 = y1 + altura_recorte

      recorte = img[y1:y2, x1:x2] # para recorte simples img[0:altura_recorte, 0:largura_recorte]

      return recorte

  def filtrarImagem(img, tipo):
    if tipo == 1: # Vermelho
      com_filtro = img.copy()
      com_filtro[:, :, 1] = 0  # Zera o canal verde
      com_filtro[:, :, 2] = 0  # Zera o canal azul

    elif tipo == 2: # Verde
      com_filtro = img.copy()
      com_filtro[:, :, 2] = 0  # Zera o canal azul
      com_filtro[:, :, 0] = 0  # Zera o canal vermelho

    elif tipo == 3: # Azul
      com_filtro = img.copy()
      com_filtro[:, :, 1] = 0  # Zera o canal verde
      com_filtro[:, :, 0] = 0  # Zera o canal vermelho

    else: # Cinza
      com_filtro = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    return com_filtro

  def equalizarImagem(img):
    # Converter de RGB para YCrCb (Y = Brilho, Cr = Vermelho, Cb = Azul)
    img_ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB) # Utilizado pq permite tratar as cores e a luminância de forma separada
    y, cr, cb = cv2.split(img_ycrcb)

    y_eq = cv2.equalizeHist(y) # Equalizar o canal de brilho

    img_ycrcb_eq = cv2.merge((y_eq, cr, cb)) # Juntar os canais equalizados

    img_rgb_eq = cv2.cvtColor(img_ycrcb_eq, cv2.COLOR_YCR_CB2BGR) # Converter de volta para RGB

    return img_rgb_eq

  def upscaleMantendoProporcao(img, metodo='lanczos'):
    proporcoes = {
        (1, 1): (1000, 1000),
        (4, 5): (1080, 1350),
        (9, 16): (1080, 1920),
        (16, 9): (1920, 1080)
    }

    altura, largura = img.shape[:2]
    proporcao_atual = round(largura/altura, 2)

    proporcao_encontrada = None
    for (w, h), (min_larg, min_alt) in proporcoes.items():
      prop = round(w/h, 2)
      if abs(proporcao_atual - prop) <= 0.1:
        proporcao_encontrada = (w, h)
        tamanho_minimo = (min_larg, min_alt)
        break

    if not proporcao_encontrada: # Proporção não reconhecida
      return img

    if largura >= min_larg and altura >= min_alt: # Imagem já está maior que o tamanho mínimo
      return img

    escala_largura = min_larg / largura
    escala_altura = min_alt / altura
    escala = max(escala_largura, escala_altura)

    nova_largura = int(largura * escala)
    nova_altura = int(altura * escala)

    metodos = {
        'linear': cv2.INTER_LINEAR,
        'cubic': cv2.INTER_CUBIC,
        'lanczos': cv2.INTER_LANCZOS4,
        'nearest': cv2.INTER_NEAREST
    }

    print(metodos[metodo])

    if metodo in metodos:
      img_redimensionada = cv2.resize(img, (nova_largura, nova_altura), interpolation=metodos[metodo])

    return img_redimensionada