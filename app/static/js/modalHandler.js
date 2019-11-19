let posts = document.getElementsByClassName('post');
let images = [];
[...posts].forEach(post => {
    poso = {
        'postImg': post.children[0].children[0],
        'link': post.children[0].children[0].src
    }
    images.push(poso);
});
images.forEach(image => {
    image.postImg.addEventListener('click', () => makeModal(image));
})
function makeModal(image) {
    const modal = document.createElement('section');
    const imgEl = document.createElement('img');
    const exBut = document.createElement('button');
    exBut.innerText = 'X';
    exBut.addEventListener('click', e => e.target.parentNode.remove());
    modal.classList.add('modal');
    imgEl.src = image.link;
    modal.appendChild(imgEl);
    modal.appendChild(exBut);
    document.body.appendChild(modal);
}