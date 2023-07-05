const refund_buttons = document.querySelectorAll(".refund");

refund_buttons.forEach(e => e.addEventListener('click', (ev) => {
    let transaction_id = ev.target.id;
    // make a post "form" to send the id to refund/<id>
    formData = make_form_data(transaction_id);
    submit(formData);

    
}))


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

function make_form_data(val) {
    //return a form object to send
    let formData = new FormData();
    formData.append('transaction_id', val);
    
    return formData
}

async function submit(form) {
    let csrftoken = getCookie('csrftoken');
    await fetch('/refund', {
        method : "POST",
        headers : {
            
            'X-CSRFToken' : csrftoken,
        },
        body: form
    });
    window.open("/balance", "_self")
}