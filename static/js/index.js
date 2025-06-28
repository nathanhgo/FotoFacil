const imgRes = document.querySelector('#imgRes')

let coordInteresse =[0, 0] // COORDENADAS EM PORCENTAGEM (MULTIPLIQUE PELA LARGURA/ALTURA DA IMG NO BACKEND)

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

    console.log(`Clicou em x:${x} y:${y}`)
    console.log(`Em Porcentagem x:${x_porcentagem} y:${y_porcentagem}`)

    coordInteresse = [x_porcentagem, y_porcentagem]
    console.log(typeof(coordInteresse))
})