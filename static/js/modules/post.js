import postModule from './postModule.js'
import fadeFrame from './fadeFrame.js'
import imgZoom from './imgZoom.js'

function post() {
    const idPost = document.querySelector('#postNum').dataset.postnum;

    function changedArrArgs(arr, args, value) {
                    arr.forEach((item, index) => {
                        if( item.includes(args)) {
                            let nItem = item.split('=');
                            if(args === 'msg_id'){
                                nItem[1] = parseInt(nItem[1]) + value ;
                            }else if(args === 'answer') {
                                  if (value) {
                                      let nv = value.toString().split(',').filter(item => !isNaN(item));
                                      let na = decodeURIComponent(nItem[1]).split(',')
                                      na.push(...nv)
                                      nItem[1] = na.join(',')
                                  }
                            }
                            arr[index] = nItem.join('=');
                        }

                    })
               }

    function linkScroll (linkSelector, position='start') {
         if(document.querySelector(linkSelector)) {
            document.querySelector(linkSelector).scrollIntoView({block: 'start', behavior: 'smooth'});
         }
    }

    function getPost (linkPost) {
         fetch(linkPost)
            .then(response => response.text())
            .then(tab => {
                document.querySelector('#postContent .container').innerHTML = tab;
            })
            .then(() => {
                setClickButtonInput();
                setClickAnchor();
                setPostContent(linkPost, idPost);
                postModule();
                fadeFrame();
                imgZoom();
                linkScroll('#newstring');
            })
    }

    function setPostContent(linkPost, idPost) {
        let obj = {};

        if(sessionStorage.getItem('postContent'))
            obj = sessionStorage.getItem('postContent');

        if (obj.length > 0)
            obj = JSON.parse(obj);

        obj[idPost] = linkPost;
        const json = JSON.stringify(obj);

        sessionStorage.setItem('postContent', json);
    }

    function strip(str) {
        let arr = str.split(" ");
            return  arr.filter(item => item).join(' ');

    }

    function setClickAnchor() {

        document.querySelectorAll('#postContent a').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();
                let link = anchor.href;
                let arrLink = link.split('?');
                let arr_args = arrLink[1].split('&');

                changedArrArgs(arr_args, 'answer', anchor.dataset.choice)

                getPost(`${arrLink[0]}?${arr_args.join('&')}`);

            })
        });
    }

    function setClickButtonInput() {
        try {

            // add click for Input feedback answer form

             document.querySelector('#next-btn.input').addEventListener('click', (e) => {
                e.preventDefault();
                const r_answer = document.querySelector('input[name="r_answer"]').value.split(',').map(item => strip(item.toLowerCase())),
                      answer_form = strip(document.querySelector('#input-field').value.toLowerCase()),
                      num_link_message = document.querySelector('input[name="num_link"]').value.split(',').map(item => parseInt(item));

                let link = document.querySelector('#next-btn.input').form.action;
                let arrLink = link.split('?');
                let arr_args = arrLink[1].split('&');
                let pos = 0;

               if (r_answer.filter(word => word == answer_form).length > 0) {
                    pos = 1
                };
//               if (isNaN(num_link_message[pos])) {
//
//                   changedArrArgs(arr_args, 'msg_id', -1);
//
//
//                };

               changedArrArgs(arr_args, 'answer', num_link_message[pos]);
             if (!isNaN(num_link_message[pos]))
                getPost (`${arrLink[0]}?${arr_args.join('&')}`);


            document.querySelector('#input-field').addEventListener('input', (e) => {
               e.target.value = document.querySelector('#input-field').value;
            })
        })


        } catch(e) { console.log(e)}
    }


     postModule();
     setClickButtonInput();
     setClickAnchor();
     fadeFrame();
     imgZoom();
     linkScroll('#newstring');

//    if (sessionStorage.getItem('postContent'))
//         if(JSON.parse(sessionStorage.getItem('postContent'))[idPost])
//            getPost(JSON.parse(sessionStorage.getItem('postContent'))[idPost])

}

export default post;