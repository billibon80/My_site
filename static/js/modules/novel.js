//$(document).ready(function() {
//    $("div.bhoechie-tab-menu>div.list-group>a").click(function(e) {
//        e.preventDefault();
//        $(this).siblings('a.active').removeClass("active");
//        $(this).addClass("active");
//        var index = $(this).index();
//        $("div.bhoechie-tab>div.bhoechie-tab-content").removeClass("active");
//        $("div.bhoechie-tab>div.bhoechie-tab-content").eq(index).addClass("active");
//    });
//});
//
//$(document).ready(function() {
//    $("#carouselExampleFade>.carousel-control-next").click(function(e) {
//        e.preventDefault();
//        var elemCount  = document.getElementsByClassName("carousel-inner")[0].childElementCount;
//        console.log(elemCount);
//        if ($('div.carousel-item.active').index() == elemCount - 1){
//            var index = 0;
//        }else {
//            var index = $('div.carousel-item.active').index() + 1;}
//        $("div.container>div.bhoechie-tab-content").removeClass("active");
//        $("div.container>div.bhoechie-tab-content").eq(index).addClass("active");
//    });
// $("#carouselExampleFade>.carousel-control-prev").click(function(e) {
//        e.preventDefault();
//        if ($('div.carousel-item.active').index() == -1){
//            var index = 0;
//        }else {
//            var index = $('div.carousel-item.active').index() - 1;}
//        $("div.container>div.bhoechie-tab-content").removeClass("active");
//        $("div.container>div.bhoechie-tab-content").eq(index).addClass("active");
//    });
//});
//

function novel() {
    function addTemplateHtml(selector, templateHtml) {
         if(document.querySelector(selector)) {
            document.querySelector(selector).innerHTML = templateHtml;
        }
    }

    function addNovel(i) {
            fetch(`/getNovel/${i}`)
            .then(response => response.text())
            .then(tab => {
                addTemplateHtml('.text-novel', tab)
            })
            .then(() => {
                document.querySelector('.btn-close-novel').addEventListener('click', () => {
                    fetch('/getTemplateNovel')
                    .then(response => response.text())
                    .then(tab => {
                       addTemplateHtml('.text-novel', tab);
                    })
                    .then(() => {
                     cleanClassNovel(document.querySelector('.text-novel-movePosition'));
                     document.querySelector('body').style.overflow = 'auto';
                     checkResize ();
                     checkPosition();
                     button89();
                    })
                })
            })
        }

    function addListNovel(i) {
        fetch(`/novel/${i}`)
            .then(response => response.text())
            .then(tab => {
                addTemplateHtml('#novel', tab);
            })
            .then(() => {
                button89();
            })

    };

    function checkPosition() {
         function removedClass (classDel, classAdd) {
              document.querySelectorAll(`.${classDel}`).forEach(item => {
                    item.classList.add(classAdd);
                    item.classList.remove(classDel);
                })
         }
         if (pageYOffset >= _offsetYTop) {
            removedClass ('absolute', 'fixed');

        } else if (pageYOffset < _offsetYTop) {
           removedClass ('fixed', 'absolute')
        }
    };

    function cleanClassNovel(el) {
        const classArray = ['text-novel-movePosition', 'fixed', 'absolute'];
        classArray.forEach(element => el.classList.remove(element));
    }

    function button89 () {

        document.querySelectorAll(".button-89").forEach((item) => {

            item.addEventListener('click', () => {
            addNovel(parseInt(item.parentElement.parentElement.parentElement.id));
            document.querySelectorAll('li').forEach((li) => {
                cleanClassNovel(li);

            })
            const li = item.parentElement.parentElement.parentElement;
            li.classList.add('text-novel-movePosition')
             if (pageYOffset >= _offsetYTop) {
                    li.classList.add('fixed');

                } else if (pageYOffset < _offsetYTop) {
                    li.classList.add('absolute');
             }
             checkResize ();
        })
        });

         document.querySelector('.novel__btn').addEventListener('click', () => {
              let numNovels;
              if (sessionStorage.getItem('novels')) {
                  numNovels = parseInt(sessionStorage.getItem('novels'))  + 2;
              } else {
                  numNovels = 4;
              }

              sessionStorage.setItem('novels', numNovels);
              addListNovel(numNovels);
        });

    }

    function checkResize () {
        if (window.innerWidth <= 1200) {
             if(document.querySelector('.text-novel-movePosition')) {
                  document.querySelector('.text-novel').style.display = 'block';
                  document.querySelector('body').style.overflow = 'hidden';
             } else {
                 document.querySelector('body').style.overflow = 'auto';
                 document.querySelector('.text-novel').style.display = 'none';
             }

        } else {
             document.querySelector('body').style.overflow = 'auto';
             document.querySelector('.text-novel').style.display = 'block';
        }
    }

    let _offsetYTop = 532;
    window.addEventListener('scroll', () => {
         checkPosition();
    });

    if (sessionStorage.getItem('novels')) {
        addListNovel(parseInt(sessionStorage.getItem('novels')) );
    }

    window.addEventListener('resize', () => {
        checkResize ();
        checkPosition();
    })


    button89();
    checkPosition();
}

export default novel;

