let booked_seats = [];

let seat_buttons = document.querySelectorAll(".empty_seat");
let confirm_button = document.querySelector("#confirm");
let info_text = document.querySelector("#infoText");



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
    if (form_is_valid()) {
        response = submit(formData);
        response.then(
            function(result){
                result.text().then(
                    result => {
                        if (result === "fail") {
                            info_text.textContent = "You are underaged"
                        }
                        else {
                            window.open("/payment", "_self")
                        }
                        console.log(result)
                    },
                    error => console.log(error)
                );
            },
            function(error){
                console.log(error);
            }
        )

    }
})

function make_form_data() {
    //return a form object to send
    let formData = new FormData();
    formData.append('booked_seats', booked_seats);
    
    return formData
}


function form_is_valid() {
    //confirm none is empty, age is good, etc
    if (booked_seats.length != 0) {
        
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
    return await fetch('/booking', {
        method : "POST",
        headers : {
            
            'X-CSRFToken' : csrftoken,
        },
        body: form
    });
    
}