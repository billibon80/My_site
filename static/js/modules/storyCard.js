function storyCard() {
    document.querySelectorAll('.button-89').forEach( (item) => {
        item.addEventListener('click', (e) => {
            sessionStorage.setItem('storiesCardId', item.parentElement.getAttribute('id'));
        })
    });
}

export default storyCard;