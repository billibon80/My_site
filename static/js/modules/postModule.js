import {bodyOverflowHidden} from '../script.js'
import * as video from './videoPanel.js'

function postModule() {
    try {
        document.querySelectorAll('.modalblock').forEach(modalblock => {
            modalblock.querySelector('.btn-outside').addEventListener('click', () => {

               const modal = modalblock.querySelector('.modal');
               modal.classList.add('show');
               bodyOverflowHidden('hidden');

               const btn_play = modal.querySelector('[data-btnName="btn-play-video"]'),
                     btn_pause = modal.querySelector('[data-btnName="btn-pause-video"]');


               if (btn_play && btn_pause) {
                   video.playVideo(modal);
                   btn_play.style.background = 'red';
                   video.videoPanel(modal, btn_play, btn_pause);
               }


               const btn_close = modalblock.querySelector('[data-btnName="close-modal"]')
               btn_close.addEventListener('click', () => {
                    modal.classList.remove('show');
                    video.pauseVideo(modal);
                    bodyOverflowHidden('auto');

               })

                if (modalblock.querySelector('[data-btnName="arrow-btn"]')) {
                    modalblock.querySelector('[data-btnName="arrow-btn"]')
                    .addEventListener('click', () => {
                        bodyOverflowHidden('auto');
                    })
                }

            })
        });
    } catch (e) {
        console.log('postModule error', e);
    }
}

export default postModule;