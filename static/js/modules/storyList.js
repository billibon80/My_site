import storyCard from './storyCard.js';

function storyList () {

    if (sessionStorage.getItem('stories')) {
        let numStories = parseInt(sessionStorage.getItem('stories'));
        sessionStorage.setItem('stories', numStories);
        addStories(numStories);

    }

   document.querySelector('#addStories').addEventListener('click', () => {
          let dataStories = document.querySelector('#addStories .inner'),
              numStories = parseInt(dataStories.dataset.stories) + 3;
          if (sessionStorage.getItem('stories'))
              numStories = parseInt(sessionStorage.getItem('stories'))  + 3;

          sessionStorage.setItem('stories', numStories);
          addStories(numStories);

    })

    function addStories(i) {
        if (document.querySelector('#storyList')) {
            fetch(`/getStories/${i}`)
            .then(response => response.text())
            .then(tab => {
                document.querySelector('#storyList').innerHTML = tab;
            })
            .then(() => {
                if(document.querySelector('#storyList .comics__grid').dataset.btfade == "True") {
                    document.querySelector('#addStories').setAttribute('disabled','disabled')
                }
                storyCard();
            })
        }

    }

}

export default storyList;