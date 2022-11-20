import storyList from './modules/storyList.js';
import letterScript from './modules/letter-script.js';
import novel from './modules/novel.js';
import post from './modules/post.js';


export function bodyOverflowHidden (value) {
        document.querySelector('body').style.overflow =  value;
    }


window.addEventListener("DOMContentLoaded", () => {

    try {
        if (document.querySelector('#stories'))
            storyList();
    }catch(e) {
        console.log('storyList error', e);
    }

    try {
        letterScript();
    }catch(e) {
        console.log('letterScript error', e);
    }

     try {
        if (document.querySelector('#novel'))
            novel();
    }catch(e) {
        console.log('novel error', e);
    }

    try {
        if (document.querySelector('#postContent'))
            post();
    }catch(e) {
        console.log('stories content error', e);
    }


    document.querySelector('#stories').addEventListener('click', (e)=> {
        function link_stories (selector,position) {
            if(document.querySelector(selector)) {
                if (sessionStorage.getItem('storiesCardId'))
                    selector = "#" + sessionStorage.getItem('storiesCardId')
                let cardLink = document.querySelector(selector);
                cardLink.scrollIntoView({block: position, behavior: 'smooth'});
                cardLink.classList.add('blueShadow');
            }

        }

        e.preventDefault();
        if (document.querySelector('#storiesTitle')) {
          link_stories('#addStories', 'end');
        } else {
            fetch(`/home`)
            .then(response => response.text())
            .then(tab => {
                document.querySelector('body').innerHTML = tab;
            })
            .then(() => {

                storyList();
                letterScript();
                setTimeout(() => { link_stories('.inner', 'end')}, 500);

            })

        }

    });




});