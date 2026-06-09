// ===============================
// COPY TO CLIPBOARD
// ===============================

function copyText(text){

    navigator.clipboard.writeText(text);

    alert("Copied Successfully!");

}


// ===============================
// PASSWORD GENERATOR
// ===============================

function generatePassword(){

    let chars =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*";

    let password = "";

    for(let i=0;i<16;i++){

        password += chars.charAt(
            Math.floor(
                Math.random()*chars.length
            )
        );

    }

    document.getElementById(
        "generatedPassword"
    ).value = password;

}


// ===============================
// PASSWORD STRENGTH CHECKER
// ===============================

function checkStrength(){

    let password =
    document.getElementById(
        "passwordInput"
    ).value;

    let result =
    document.getElementById(
        "strength"
    );

    let score = 0;

    if(password.length >= 8)
        score++;

    if(/[A-Z]/.test(password))
        score++;

    if(/[0-9]/.test(password))
        score++;

    if(/[!@#$%^&*]/.test(password))
        score++;

    if(score <= 1){

        result.innerText = "Weak";
        result.style.color = "red";

    }
    else if(score == 2){

        result.innerText = "Medium";
        result.style.color = "orange";

    }
    else{

        result.innerText = "Strong";
        result.style.color = "lightgreen";

    }

}


// ===============================
// SEARCH TABLE
// ===============================

function searchTable(){

    let input =
    document.getElementById(
        "search"
    ).value.toLowerCase();

    let rows =
    document.querySelectorAll(
        "#vaultTable tr"
    );

    rows.forEach((row,index)=>{

        if(index===0) return;

        let text =
        row.innerText.toLowerCase();

        row.style.display =
        text.includes(input)
        ? ""
        : "none";

    });

}