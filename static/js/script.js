import storyList from './modules/storyList.js';

window.addEventListener("DOMContentLoaded", () => {
    try {
        storyList();
    }catch(e) {
        console.log('storyList error', e)
    }

});