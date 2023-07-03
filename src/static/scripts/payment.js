const confirmButton = document.querySelector('#confirm');
const testText = document.querySelector('#test');
const poorModalTrigger = document.querySelector('#poorModalTrigger');
const successModalTrigger = document.querySelector('#successModalTrigger');

confirmButton.addEventListener('click', (ev) => {
    //do something
    form = make_form_data();
    response = submit(form);
    
    response.then(
        function(result){
            result.text().then(
                result => {
                    if (result === "epic fail") {
                        poorModalTrigger.click();
                    }
                    else {
                        successModalTrigger.click();
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

    
})



function make_form_data() {
    //return a form object to send
    let formData = new FormData();
    formData.append('sieg', 'heil');
    
    return formData
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
    return await fetch('/payment', {
        method : "POST",
        headers : {
            
            'X-CSRFToken' : csrftoken,
        },
        body: form
    });

}