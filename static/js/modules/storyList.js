function storyList () {

   document.querySelector('#addStories').addEventListener('click', () => {
          let dataStories = document.querySelector('#addStories .inner'),
              numStories = parseInt(dataStories.dataset.stories) + 3;

          dataStories.dataset.stories = numStories;
          addStories(numStories);

    })

    function addStories(i) {
        fetch(`/getStories/${i}`)
        .then(response => response.text())
        .then(tab => {
            document.querySelector('#storyList').innerHTML = tab;
        })
        .then(() => {
            if(document.querySelector('#storyList .comics__grid').dataset.btfade == "True") {
                document.querySelector('#addStories').setAttribute('disabled','disabled')
            }
        })
    }

}

export default storyList;