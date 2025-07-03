const divRes = document.querySelector('#divRes')
const imgRes = document.querySelector('#imgRes')

const inputFile = document.querySelector('input[type="file"]')
const radioButtons = document.querySelectorAll('input[type="radio"][name="radioDetect"]');
const form = document.querySelector('#mainForm')

let coordInteresse =[0, 0] // COORDENADAS EM PORCENTAGEM (MULTIPLIQUE PELA LARGURA/ALTURA DA IMG NO BACKEND)
let arquivoDeImagem = null;

imgRes.addEventListener('click', (e) => {
    const dot = document.querySelector('.dot')
    const rect = e.target.getBoundingClientRect()

    let x = Math.floor(e.clientX - rect.left)
    let y = Math.floor(e.clientY - rect.top)

    let x_porcentagem = (x / rect.width).toFixed(2)
    let y_porcentagem = (y / rect.height).toFixed(2)

    dot.style.top = `${y+5}px`;
    dot.style.left = `${x-5}px`;
    dot.style.backgroundColor = 'red';



    coordInteresse = [Number(x_porcentagem), Number(y_porcentagem)]
})


radioButtons.forEach(radio => {
    radio.addEventListener('change', function() {

        if (Number(this.value) == 2) {
            divRes.style.display = 'block';
        } else {
            divRes.style.display = 'none';
        }
    });
});


inputFile.addEventListener('change', e => {
    arquivoDeImagem = e.target.files[0];
    
    if (arquivoDeImagem) {
        const leitor = new FileReader();

        leitor.addEventListener('load', () => {
            imgRes.setAttribute('src', leitor.result);
        })

        leitor.readAsDataURL(arquivoDeImagem);
    } else {
        imgRes.setAttribute('src', '');
    }
})


form.addEventListener('submit', e => {
    e.preventDefault();

    const formData = new FormData();

    const proporcaoSelecionadaInput = document.querySelector('input[name="radioProp"]:checked');
    const filtroSelecionadoInput = document.querySelector('input[name="radioFil"]:checked');
    const deteccaoSelecionadaInput = document.querySelector('input[name="radioDetect"]:checked');

    const valorProporcao = Number(proporcaoSelecionadaInput.value);
    const valorFiltro = Number(filtroSelecionadoInput.value);
    const valorDeteccao = Number(deteccaoSelecionadaInput.value);

    formData.append('proporcao', valorProporcao);
    formData.append('filtro', valorFiltro);
    formData.append('modoDeDeteccao', valorDeteccao);

    if (valorDeteccao === 2) {
        const larguraOriginal = imgRes.naturalWidth;
        const alturaOriginal = imgRes.naturalHeight;
        let x_na_imagem = Math.floor(coordInteresse[0] * larguraOriginal);
        let y_na_imagem = Math.floor(coordInteresse[1] * alturaOriginal);

        formData.append('coordenadaManual', JSON.stringify({x: x_na_imagem, y: y_na_imagem }));
    }


    if (!arquivoDeImagem) {
        alert('Por favor, faça o upload de uma imagem.');
        return;
    } else {

        formData.append('imagem', arquivoDeImagem);

        fetch('/editar', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {

            if (data.download_url) {
                const link = document.createElement('a');
                link.href = data.download_url;
                link.setAttribute('download', 'imagem-editada.jpg');
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            }
        })
        .catch(error => {
            console.error('Erro no fetch:', error);
            alert('Ocorreu um erro ao enviar o formulário.');
        });

    }
})
