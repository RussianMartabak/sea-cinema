let booked_seats = [];
let age_form = document.querySelector("#ageInput");
let name_form = document.querySelector("#nameInput");
let age_rating = parseInt(document.querySelector("#ageRating").text);
let seat_buttons = document.querySelectorAll(".empty_seat");
let confirm_button = document.querySelector("#confirm")



//make the seat button clickable first!!!!!
seat_buttons.forEach(e => e.addEventListener('click', (ev) => {
    if (booked_seats.length < 6) {
        let seat_number = ev.target.textContent;
        booked_seats.push(seat_number);
        console.log(seat_number);
        ev.target.style.background = "blue";
    }
    
}, {once : true}))


confirm_button.addEventListener('click', (ev) => {
    console.log(form_is_valid());
    let formData = make_form_data()
    if (form_is_valid) {
        submit(formData)
    }
})

function make_form_data() {
    //return a form object to send
    let formData = new FormData();
    formData.append('booked_seats', booked_seats);
    formData.append('name', name_form.value);
    return formData
}


function form_is_valid() {
    //confirm none is empty, age is good, etc
    if (booked_seats.length != 0 &&
        age_form.value != "" && parseInt(age_form.value) >= 18 &&
        name_form.value != "") {
        
        return true
    }
    else {
        return false
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function submit(form) {
    let csrftoken = getCookie('csrftoken');
    await fetch('/booking', {
        method : "POST",
        headers : {
            
            'X-CSRFToken' : csrftoken,
        },
        body: form
    });
    window.open("/payment", "_self")
}