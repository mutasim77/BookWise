// send email JS
let emailBtn = document.querySelector('#btn');

//! on click 
emailBtn.addEventListener('click', () => {
    if (document.querySelector('#subject').value && document.querySelector('textarea').value) {
        let name = document.getElementById('name');
        let subject = document.getElementById('subject');
        let msg = document.querySelector('textarea');
        document.querySelector('.error').classList.add('hide');
        sendEmail(name.value, subject.value, msg.value);
    } else {
        document.querySelector('.error').classList.remove('hide');
    }
});

//! send function 
function sendEmail(name, subject, message) {
    emailjs.send("service_jz3bx2m", "template_ttx2qm8", {
        from_name: name,
        to_name: subject,
        message: message,
    }).then(() => {
        swal("Good job!", "Your message sent successfully!", "success");
        for (input of document.querySelectorAll('input')) {
            input.value = '';
        }
        document.querySelector('textarea').value = '';
    })
}

//! connect EmailJS
(function () {
    emailjs.init("X3BPJCY7nlOfu8BcY");
})();