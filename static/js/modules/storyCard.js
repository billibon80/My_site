function storyCard() {
    document.querySelectorAll('.comics__item').forEach( (item) => {
        item.addEventListener('click', (e) => {
            sessionStorage.setItem('storiesCardId', item.getAttribute('id'));
        })
    });
}

export default storyCard;