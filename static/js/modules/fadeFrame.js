
function fadeFrame() {
    const frame=document.querySelectorAll('.message_pack');

    if (frame.length > 0) {
          let numFrame = frame.length - 1;
          if (!sessionStorage.getItem('fadeFrame'))
              sessionStorage.setItem('fadeFrame', -1)

          let earlNum = parseInt(sessionStorage.getItem('fadeFrame'));
          if ( earlNum + 1 == numFrame) {
              frame[numFrame].style.setProperty('--animation', 'frame_message 2s 6 normal');
              sessionStorage.setItem('fadeFrame', earlNum + 1);
          }
    } else {
      sessionStorage.setItem('fadeFrame', -1)

    }
}

export default fadeFrame;