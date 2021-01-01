/*1. matching password and confirm password
  2. validating and notice users when they use less than 10 chars for the password */
function checkPasswordMatch() {
    let password = document.getElementById('newPass').value;
    let confirmPassword = document.getElementById('confirmPass').value;

    if (password != confirmPassword) {
        document.getElementById('password_match1').style.color = 'red';
        document.getElementById('password_match1').innerHTML = '*Password do not match!';
    } else {
        document.getElementById('password_match1').innerHTML = ' ';
    }

    if (password.length < 10) {
        document.getElementById('password_match2').style.color = 'red';
        document.getElementById('password_match2').innerHTML = '*Use at least 10 characters.';
    } else {
        document.getElementById('password_match2').innerHTML = ' ';
    }
}

// /*disable register button if do not agree with terms and condition*/
// function checkMe() {
//     let checker = document.getElementById('check-me');
//     let btn = document.getElementById('reg-btn');

//     if (checker.checked == true) {
//         btn.disabled = false;
//     } else {
//         btn.disabled = true;
//     }
// }
