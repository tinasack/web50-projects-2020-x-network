function likeHandler(id, mylikes){

    const btn = document.getElementById(`like-${id}`);
    const count = document.getElementById(`count-${id}`)

    btn.classList.remove('bi-heart-fill', 'liked');
    btn.classList.remove('bi-heart', 'like');
    btn.classList.remove('bi-heart', 'liked');
    count.classList.remove('like');
    count.classList.remove('liked');

    if(mylikes.indexOf(id)>=0){
        var like = true;
    } else {
        var like = false;
    }
    
    if(like === true){
        fetch(`/unlike/${id}`)
        .then((response) => {
            if (!response.ok) {
                // error processing
                throw 'Error';
            }
            return response.json()
        })
        .then(result => {
            if (result.likes > 0) {
                btn.classList.add('bi-heart', 'liked');
            } else {
                btn.classList.add('bi-heart', 'like');
            }
            count.innerHTML = result.likes;
            count.classList.add('like');
        })
    } else {
        fetch(`/like/${id}`)
        .then((response) => {
            if (!response.ok) {
                // error processing
                throw 'Error';
            }
            return response.json()
        })
        .then(result => {
            result.message
            btn.classList.add('bi-heart-fill', 'liked');
            count.innerHTML = result.likes;
            count.classList.add('liked');
        })
    } 
    like = false;
};

function notAutheticated() {
    alert("You can't like this post! Please login first.");
};

function notAllowed() {
    alert("You can't like your own posts!");
};

function getCookie(name){
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if(parts.length == 2) return parts.pop().split(';').shift();
};

function editHandler(id){
    const textarea = document.getElementById(`textarea-${id}`).value;
    const content = document.getElementById(`content-${id}`);
    const modal = document.getElementById(`modal-edit-${id}`);
    fetch(`/edit/${id}`, {
        method: "POST",
        headers: {"Content-type": "application/json","X-CSRFToken": getCookie("csrftoken")},
        body: JSON.stringify({
            content: textarea
        })
    })
    .then(response => response.json())
    .then(result => {
        content.innerHTML = result.data;
        modal.classList.remove('show');
        modal.setAttribute('aria-hidden', 'true');
        modal.setAttribute('style', 'display: none');

        const modalBackdrop = document.getElementsByClassName('modal-backdrop');

        for(let i=0; i<modalBackdrop.length; i++){
            document.body.removeChild(modalBackdrop[i]);
        }
    });
};