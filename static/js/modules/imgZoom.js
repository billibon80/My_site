
function imgZoom() {
    const listCard = document.querySelectorAll('.card-answer');
    if (listCard.length > 0) {
        listCard.forEach(card => {
            let img = card.querySelector('img');
            if (img) {
                 img.addEventListener('click', () => {
                 if (img.classList.contains('card-answer-transform')) {
                    img.classList.remove('card-answer-transform') ;
                 }else {
                     img.classList.add('card-answer-transform') ;
                 }

            });
            }
        });
    }
}

export default imgZoom;