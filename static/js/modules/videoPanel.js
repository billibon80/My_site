export function playVideo(selector) {
    if(selector.querySelector('video'))
         selector.querySelector('video').play();


}

export function pauseVideo(selector) {
    if(selector.querySelector('video'))
         selector.querySelector('video').pause();


}

export function videoPanel(selector, btn_play, btn_pause) {

        btn_play.addEventListener('click', () => {
           playVideo(selector, btn_play, btn_pause);
            btn_play.style.background = 'red';
            btn_pause.style.background = '';
        })

        btn_pause.addEventListener('click', () => {
            pauseVideo(selector, btn_play, btn_pause);
            btn_play.style.background = '';
            btn_pause.style.background = 'red';
        })

}




