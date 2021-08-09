/*!
* Start Bootstrap - Clean Blog v5.1.0 (https://startbootstrap.com/theme/clean-blog)
* Copyright 2013-2021 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-clean-blog/blob/master/LICENSE)
*/
/* script fancy form for questions */

// Questions Array
//const questions = [
//  { question: 'Enter Your First Name' },
//  { question: 'Enter Your Last Name' },
//  { question: 'Enter Your Email', pattern: /\S+@\S+\.\S+/ },
//  { question: 'Create A Password', type: 'password' }
//];
//
//// Transition Times
//const shakeTime = 100; // Shake Transition Time
//const switchTime = 200; // Transition Between Questions
//
//// Init Position At First Question
//let position = 0;
//
//// Init DOM Elements
//const formBox = document.querySelector('#form-box');
//const nextBtn = document.querySelector('#next-btn');
//const prevBtn = document.querySelector('#prev-btn');
//const inputGroup = document.querySelector('#input-group');
//const inputField = document.querySelector('#input-field');
//const inputLabel = document.querySelector('#input-label');
//const inputProgress = document.querySelector('#input-progress');
//const progress = document.querySelector('#progress-bar');
//
//// EVENTS
//
//// Get Question On DOM Load
//
//document.addEventListener('DOMContentLoaded', getQuestion);
//
//// Next Button Click
//window.addEventListener('load',function(){
//    document.getElementById('next-btn').addEventListener("click", validate, false);
//});
//
//// Input Field Enter Click
//inputField.addEventListener('keyup', e => {
//  if (e.keyCode == 13) {
//    validate();
//  }
//});
//
//// FUNCTIONS
//
//// Get Question From Array & Add To Markup
//function getQuestion() {
//  // Get Current Question
//  inputLabel.innerHTML = questions[position].question;
//  // Get Current Type
//  inputField.type = questions[position].type || 'text';
//  // Get Current Answer
//  inputField.value = questions[position].answer || '';
//  // Focus On Element
//  inputField.focus();
//
//  // Set Progress Bar Width - Variable to the questions length
//  progress.style.width = (position * 100) / questions.length + '%';
//
//  // Add User Icon OR Back Arrow Depending On Question
//  prevBtn.className = position ? 'fas fa-arrow-left' : 'fas fa-user';
//
//  showQuestion();
//}
//
//// Display Question To User
//function showQuestion() {
//  inputGroup.style.opacity = 1;
//  inputProgress.style.transition = '';
//  inputProgress.style.width = '100%';
//}
//
//// Hide Question From User
//function hideQuestion() {
//  inputGroup.style.opacity = 0;
//  inputLabel.style.marginLeft = 0;
//  inputProgress.style.width = 0;
//  inputProgress.style.transition = 'none';
//  inputGroup.style.border = null;
//}
//
//// Transform To Create Shake Motion
//function transform(x, y) {
//  formBox.style.transform = `translate(${x}px, ${y}px)`;
//}
//
//// Validate Field
//function validate() {
//  // Make Sure Pattern Matches If There Is One
//  if (!inputField.value.match(questions[position].pattern || /.+/)) {
//    inputFail();
//  } else {
//    inputPass();
//  }
//}
//
//// Field Input Fail
//function inputFail() {
//  formBox.className = 'error';
//  // Repeat Shake Motion -  Set i to number of shakes
//  for (let i = 0; i < 6; i++) {
//    setTimeout(transform, shakeTime * i, ((i % 2) * 2 - 1) * 20, 0);
//    setTimeout(transform, shakeTime * 6, 0, 0);
//    inputField.focus();
//  }
//}
//
//// Field Input Passed
//function inputPass() {
//  formBox.className = '';
//  setTimeout(transform, shakeTime * 0, 0, 10);
//  setTimeout(transform, shakeTime * 1, 0, 0);
//
//  // Store Answer In Array
//  questions[position].answer = inputField.value;
//  // Input field
//
//  // Increment Position
//  position++;
//
//  // If New Question, Hide Current and Get Next
//  if (questions[position]) {
//    hideQuestion();
//    getQuestion();
//  } else {
//    // Remove If No More Questions
//    hideQuestion();
//    formBox.className = 'close';
//    progress.style.width = '100%';
//
//    // Form Complete
//    formComplete();
//  }
//}
//
//// All Fields Complete - Show h1 end
//function formComplete() {
//  const h1 = document.createElement('h1');
//  h1.classList.add('end');
//  h1.appendChild(
//    document.createTextNode(
//      `Thanks ${
//        questions[0].answer
//      } ты ответила на все вопросы молодец 😉😉`
//    )
//  );
//  setTimeout(() => {
//    formBox.parentElement.appendChild(h1);
//    setTimeout(() => (h1.style.opacity = 1), 50);
//  }, 1000);
//  const input_q = document.createElement('input')
//  input_q.classList.add('show')
//}


/* end fancy form */
(function ($) {

    // message_letter
    container.onmouseover = container.onmouseout = handler;

    function handler(event) {

      function str(el) {
        if (!el) return "null"
        return el.className || el.tagName;
      }

      log.value += event.type + ':  ' +
        'target=' + str(event.target) +
        ',  relatedTarget=' + str(event.relatedTarget) + "\n";
      log.scrollTop = log.scrollHeight;

      if (event.type == 'mouseover') {
        event.target.style.background = 'pink'
      }
      if (event.type == 'mouseout') {
        event.target.style.background = ''
      }
    }

    "use strict"; // Start of use strict

    // Floating label headings for the contact form
    $("body").on("input propertychange", ".floating-label-form-group", function (e) {
        $(this).toggleClass("floating-label-form-group-with-value", !!$(e.target).val());
    }).on("focus", ".floating-label-form-group", function () {
        $(this).addClass("floating-label-form-group-with-focus");
    }).on("blur", ".floating-label-form-group", function () {
        $(this).removeClass("floating-label-form-group-with-focus");
    });

    // Show the navbar when the page is scrolled up
    var MQL = 992;

    //primary navigation slide-in effect
    if ($(window).width() > MQL) {
        var headerHeight = $('#mainNav').height();
        $(window).on('scroll', {
                previousTop: 0
            },
            function () {
                var currentTop = $(window).scrollTop();
                //check if user is scrolling up
                if (currentTop < this.previousTop) {
                    //if scrolling up...
                    if (currentTop > 0 && $('#mainNav').hasClass('is-fixed')) {
                        $('#mainNav').addClass('is-visible');
                    } else {
                        $('#mainNav').removeClass('is-visible is-fixed');
                    }
                } else if (currentTop > this.previousTop) {
                    //if scrolling down...
                    $('#mainNav').removeClass('is-visible');
                    if (currentTop > headerHeight && !$('#mainNav').hasClass('is-fixed')) $('#mainNav').addClass('is-fixed');
                }
                this.previousTop = currentTop;
            });
    }

})(jQuery); // End of use strict


