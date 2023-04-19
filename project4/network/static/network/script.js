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

function saveEdit(id, newContent){
    const button = document.getElementById(`edit-save-${id}`);
    const input = newContent;
    const content = document.getElementById(`content-${id}`);
    content.classList.remove('editable');
    fetch(`/edit/${id}`, {
        method: "POST",
        headers: {"Content-type": "application/json","X-CSRFToken": getCookie("csrftoken")},
        body: JSON.stringify({
            content: input
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result.message);
        content.innerHTML = result.data;
        content.classList.add('readonly');
        button.innerHTML = `<button class="button edit-btn" type="button"  onclick="makeEdit('{{post.id}}')">Edit</button>`;
    });
};

function makeEdit(id){
    const content = document.getElementById(`content-${id}`);
    content.classList.remove('readonly');
    content.classList.add('editable');
    content.readOnly = false;
    //set inputfield on focus and cursor position to the end of line
    var len = content.value.length;
    if (content.setSelectionRange) {
        content.focus();
        content.setSelectionRange(len, len);
    } else if (content.createTextRange) {
        var range = content.createTextRange();
        range.collapse(true);
        range.moveEnd('character', len);
        range.moveStart('character', len);
        range.select();
    }
};

function edit(id){
    var newContent = document.getElementById(`content-${id}`).value;
    console.log(newContent);
    const button = document.getElementById(`edit-save-${id}`);
    button.innerHTML = `<button class="button edit-btn" type="button" onclick="saveEdit('${id}', '${newContent}')">save</button>`;
}