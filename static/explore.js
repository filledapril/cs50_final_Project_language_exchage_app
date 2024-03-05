// functions for explore.html: render data, buttons action, filters action
// fetch data depends on the url in app.y -- api_explore()
// page change by button, with offset number in the url

// variables
let pathArray = window.location.pathname.split('/');
console.log(pathArray);
let offset = parseInt(pathArray[2]);
let btnNext = document.querySelector('#btnNext');
let btnPre = document.querySelector('#btnPre');
let filterPath = '/explore';
let maxOffset = 0;

// fetch posts from api
function updatePage(offset, filters = null) {
    let url = `/api/explore?offset=${offset}`;
    let options = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    };
    // when user delete post with id
    if (deletePostId && deletePostId != "") {
        url += '&delete=' + deletePostId;
        console.log('delete url', url)
    }
    // when there are filters
    if (filters && Object.keys(filters).length != 0) {
        console.log(`filtering! ${JSON.stringify(filters)}`)
        Object.keys(filters).forEach((filter,i) => {
            if (i === 0) {
                url += '&' + filter + '=' + filters[filter];
            } else {
                url += '&' + filter + '=' + filters[filter];
            }
        })
    }
    // when user checked my post box
    if (showMine) {
        if (pathArray.length === 3) {
            url += '&my=True';
        } else {
            url += '&my=True';
        }
    }
    //-----FETCH------
    console.log("updatePage running")
    fetch(url, options)
        .then(response => response.json())
        .then(data => showHtml(data))
        .catch((error) => {
            console.error('Error:', error);
        })

}


// showing post cards by data
function showHtml(data) {
    console.log('got data success.')
    if (data[5]) {
        window.alert("post deleted.")
    }
    const container = document.querySelector("#postsContainer");
    // Clear content
    container.innerHTML = '';
    if (data[0] == null) {
        const noResult = document.createElement('p');
        noResult.className = "alert alert-danger my-1";
        noResult.textContent = "No Result.";
        container.appendChild(noResult);
        btnPre.style.display = "none";
        btnNext.style.display = "none";
        return;
    }
    // assign each data from array
    if (data != null) {
        let posts = data[0];
        console.log(`fetch data[0] = ${data[0]}`)
        let userLiked = data[1];
        let userSaved = data[2];
        let userId = data[3];
        maxOffset = data[4];
        btnPre.style.display = "block";
        btnNext.style.display = "block";
        // display page button
        if (posts.length === 1) {
            btnPre.style.display = "none";
            btnNext.style.display = "none";
        } else {
            btnPre.style.display = "block";
            btnNext.style.display = "block";
        }
        posts.forEach(post => {
            // Create elements
            // --Card and Card body
            const card = document.createElement('div');
            card.className = "card mb-3";
            card.style.width = "auto";
            card.style.height = "auto";
            const cardBody = document.createElement('div');
            cardBody.className = "card-body";
            cardBody.style.height = "auto";
            // --TOP ROW
            const topRow = document.createElement('div');
            topRow.className = "row";
            const topRowCol1 = document.createElement('div');
            topRowCol1.className = "col";
            const speak = document.createElement('h5');
            speak.className = "card-title text-start";
            speak.id = "speak";
            const learn = document.createElement('h5');
            learn.className = "card-title mb-2 text-body-secondary text-start";
            learn.id = "learn";
            const topRowCol2 = document.createElement('div');
            topRowCol2.className = "col";
            const date = document.createElement('p');
            date.className = "card-text mt-3 text-end";
            date.id = "date";
            const intro = document.createElement('p');
            intro.className = "card-text";
            intro.id = "intro";
            // --BUTTOM ROW
            const bottomRow = document.createElement('div');
            bottomRow.className = "row";
            const bottomRowCol1 = document.createElement('div');
            bottomRowCol1.className = "col";
            const bottomRowCol1Container = document.createElement('div');
            bottomRowCol1Container.className = "d-grid gap-4 d-sm-flex";
            const btnLikes = document.createElement('button');
            btnLikes.className = "btn btn-outline-secondary like-button";
            const btnSave = document.createElement('button');
            btnSave.className = "btn btn-outline-primary save-button";
            const btnMsg = document.createElement('button');
            btnMsg.className = "btn btn-outline-info msg-button";
            btnMsg.value = `msg-box${post.postId}`;
            const bottomRowCol2 = document.createElement('div');
            bottomRowCol2.className = "col text-end";
            const userName = document.createElement('p');
            userName.className = "d-inline card-text mx-1";
            userName.id = "userName";
            const flag = document.createElement('img');
            flag.className = "d-inline";
            flag.src = post.flag;
            flag.alt = "flag";
            flag.width = "24";
            flag.height = "16";
            const email = document.createElement('p');
            email.className = "card-text";
            // --MESSAGE BOX
            const msgBox = document.createElement('div');
            msgBox.className = "form-floating row";
            msgBox.id = `msg-box${post.postId}`;
            msgBox.style.display = "none";
            const msgArea = document.createElement('textarea');
            msgArea.className = "form-control col-12 mt-3";
            msgArea.id = `msg-content${post.postId}`;
            msgArea.name = `msg-content${post.postId}`;
            msgArea.placeholder = "Send Message";
            const msgLabel = document.createElement('label');
            msgLabel.htmlFor = `msg-content${post.postId}`;
            msgLabel.id = `label${post.postId}`
            const btnSend = document.createElement('button');
            btnSend.className = "btn btn-success mx-auto col-6 mt-3 send-button";
            btnSend.value = post.postId;

            // Set button status depends on max page
            if (maxOffset == 1) {
                btnNext.style.display = "None";
                btnPre.style.display = "None";
            } else if (maxOffset > 1) {
                btnNext.style.display = "Block";
                btnPre.style.display = "Block";
            }
            // Set contents
            speak.textContent = `Speak: ${post.speak}`;
            learn.textContent = `Learn: ${post.learn}`;
            date.textContent = post.date;
            intro.textContent = post.intro;
            userName.textContent = post.username;
            email.textContent = post.email;
            btnLikes.textContent = `${post.likes} ❤️`;
            btnLikes.value = post.postId;
            btnSave.textContent = `Save`;
            btnSave.value = post.postId;
            btnMsg.textContent = "Send message";
            msgLabel.textContent = `Send message to ${post.username}...`;
            btnSend.textContent = "Confirm and Send";

            // set like and save buttons' style depends on user status
            userLiked.forEach(like => {
                if(like.postId === post.postId) {
                    btnLikes.className = "btn btn-secondary like-button";
                } else {
                    btnLikes.className = "btn btn-outline-secondary like-button";
                }
            })
            userSaved.forEach(save => {
                if(save.postId === post.postId) {
                    btnSave.className = "btn btn-primary save-button";
                    btnSave.textContent = "Saved";
                } else {
                    btnSave.className = "btn btn-outline-primary save-button";
                }
            });

            //change message button for current user's posts to delete btn
            if (userId == post.userId) {
                btnMsg.textContent = "Delete";
                btnMsg.classList.remove("btn-outline-info", "msg-button");
                btnMsg.classList.add("btn-outline-danger", "delete-post-button");
            }

            // Append to DOM
            topRowCol1.appendChild(speak);
            topRowCol1.appendChild(learn);
            topRowCol2.appendChild(date);
            topRow.appendChild(topRowCol1);
            topRow.appendChild(topRowCol2);
            bottomRowCol1Container.appendChild(btnLikes);
            bottomRowCol1Container.appendChild(btnSave);
            bottomRowCol1Container.appendChild(btnMsg);
            bottomRowCol1.appendChild(bottomRowCol1Container);
            bottomRowCol2.appendChild(userName);
            bottomRowCol2.appendChild(flag);
            bottomRowCol2.appendChild(email);
            bottomRow.appendChild(bottomRowCol1);
            bottomRow.appendChild(bottomRowCol2);
            msgBox.appendChild(msgArea);
            msgBox.appendChild(msgLabel);
            msgBox.appendChild(btnSend);
            cardBody.appendChild(topRow);
            cardBody.appendChild(intro);
            cardBody.appendChild(bottomRow);
            cardBody.appendChild(msgBox);
            card.appendChild(cardBody);
            container.appendChild(card);
        });
    }
};


// handle my posts
let showMine = false;
function filterPosts() {
    if (document.querySelector("#myPosts").checked){
        console.log("select my post")
        showMine = true;
        updatePage(offset, filters)
    } else {
        showMine = false;
        updatePage(offset, filters)
    }
}
document.querySelector("#myPosts").addEventListener('change', filterPosts);

// handle delete my post
let deletePostId;
document.addEventListener('click', function(e) {
    let deletePostButton = e.target.matches(".delete-post-button")
    if (deletePostButton) {
        deletePostId = e.target.value.split('msg-box')[1];
        //get user current offset
        let currentPath = window.location.search.split('/')
        let currentOffset = currentPath[currentPath.length - 1]
        console.log('current offset', currentOffset);
        console.log('delete my post: ', deletePostId);
        updatePage(currentOffset, filters);
    }
})


// handle filter button
let filters = {};
document.querySelector("#filterBtn").addEventListener('click', function(e) {
    console.log("filter button click");
    filters = {};
    offset = 1;
    filterPath = '/explore';
    let speak = document.querySelector('#filterSpeak');
    let learn = document.querySelector('#filterLearn');
    let country = document.querySelector('#filterCountry');
    let errorText = document.querySelector('.errorText');
    // when no filter selected
    if(!speak.value && !learn.value && !country.value) {
        console.log("no filters selected")
        speak.style.color = "red";
        learn.style.color = "red";
        country.style.color = "red";
        errorText.style.display = "block";
        errorText.innerHTML = "Select at lease one condition.";
        history.pushState({}, '', '/explore/' + offset);
        e.preventDefault();
    } else {
        errorText.style.display = "none";
        errorText.innerHTML = "";
    };

    // insert selected objcts
    if(speak.value && speak.value !== "all") {
        filters.speak = speak.value;
    };
    if(learn.value && learn.value !== "all") {
        filters.learn = learn.value;
    };
    if(country.value && country.value !== "all") {
        filters.country = country.value;
    };
    // update path with filters
    if (filters && Object.keys(filters).length != 0) {
        Object.keys(filters).forEach((filter, i) => {
            if (filters[filter]) {
                if (i === 0) {
                    filterPath += '?' + filter + '=' + filters[filter];
                } else {
                    filterPath += '&' + filter + '=' + filters[filter];
                }
            }
        })
        filterPath += '/' + offset;
        history.pushState({}, '', filterPath);
    };
    console.log(`path array = ${pathArray}, filters object = ${filters}`);
    updatePage(offset, filters);
    e.preventDefault();
});
// get initial(reload) and each page(by button)
function getData(changeInOffset) {
    console.log(`getData running, maxOffset=${maxOffset}`)
    // handle next data
    if (changeInOffset) {
        if (maxOffset == 1) {
            btnNext.classList.add("disabled");
            btnNext.textContent = "No more pages";
            btnPre.classList.add("disabled");
            btnPre.textContent = "It's first page";
        }
        if (offset < maxOffset) {
            btnNext.classList.remove("disabled");
            offset += 1;
            // update url filter or not
            if (filters && Object.keys(filters).length != 0) {
                filterPath = '/explore';
                Object.keys(filters).forEach((filter, i) => {
                    if (filters[filter]) {
                        if (i === 0) {
                            filterPath += '?' + filter + '=' + filters[filter];
                        } else {
                            filterPath += '&' + filter + '=' + filters[filter];
                        }
                    }
                })
                filterPath += '/' + offset;
                history.pushState({}, '', filterPath);
            } else {
                history.pushState({}, '', '/explore/' + offset);
            };
        };
        //last page
        if (offset == maxOffset) {
            btnNext.classList.add("disabled");
            btnNext.textContent = "No more pages";
        };
    };

    // handle previous data
    if (!changeInOffset) {
        if (offset > 1) {
            btnPre.classList.remove("disabled");
            offset -= 1;
            // update url filter or not
            if (filters && Object.keys(filters).length != 0) {
                filterPath = '/explore';
                Object.keys(filters).forEach((filter, i) => {
                    if (filters[filter]) {
                        if (i === 0) {
                            filterPath += '?' + filter + '=' + filters[filter];
                        } else {
                            filterPath += '&' + filter + '=' + filters[filter];
                        }
                    }
                })
                filterPath += '/' + offset;
                history.pushState({}, '', filterPath);
            } else {
                history.pushState({}, '', '/explore/' + offset);
            };
        };
        //first page
        if (offset == 1) {
            btnPre.classList.add("disabled");
            btnPre.textContent = "It's first page";
        };
    };
    // display button
    if (offset != maxOffset && offset < maxOffset) {
        btnNext.classList.remove("disabled");
        btnNext.textContent = "Next";
    }
    if (offset != 1 && offset > 1) {
        btnPre.classList.remove("disabled");
        btnPre.textContent = "Previous";
    }
    // fetch data from api with offset number
    if (filters && Object.keys(filters).length != 0){
        console.log(`filtering, ${filters}`)
        updatePage(offset, filters);
    } else {
        updatePage(offset);
    }

}
// page first load and reload
window.onload = function() {
    filters = {};
    getData(false);
};
// change pages
document.querySelector("#btnNext").addEventListener('click', function() {
    getData(true);
    });
document.querySelector("#btnPre").addEventListener('click', function() {
    getData(false);
    });

// handle like click
document.addEventListener('click', function(event) {
    if (event.target.matches('.like-button')) {
        console.log('clicked like');
        let postId = event.target.value;
        fetch('/like-action', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                post_id: postId
            }),
        })
        .then(res => res.json())
        .then(data => {
            if (data.isLiked) {
                event.target.textContent = `${data.post[0]["likes"]} ❤️`;
                event.target.classList.remove("btn-outline-secondary");
                event.target.classList.add("btn-secondary");
            } else if (!data.isLiked) {
                event.target.textContent = `${data.post[0]["likes"]} ❤️`;
                event.target.classList.remove("btn-secondary");
                event.target.classList.add("btn-outline-secondary");
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        })
    }
});

// handle save button
document.addEventListener("click", function(e) {
    if (e.target.matches(".save-button")) {
        console.log('click save')
        let postId = e.target.value;
        console.log(`save: ${postId}`);
        fetch('/save-action', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                post_id: postId
            }),
        })
        .then(res => res.json())
        .then(data => {
            if(data.isSaved) {
                e.target.textContent = "Saved";
                e.target.classList.remove("btn-outline-primary");
                e.target.classList.add("btn-primary");
            } else if (!data.isSaved) {
                e.target.textContent = "Save";
                e.target.classList.remove("btn-primary");
                e.target.classList.add("btn-outline-primary");
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        })
    }
})

// message button show box
let boxOpened = {};
document.addEventListener('click', function(e) {
    if (e.target.matches(".msg-button")) {
        console.log('click msg')
        let boxName = e.target.value;
        let msgBox = document.querySelector(`#${boxName}`);
        if (boxOpened[boxName]) {
            msgBox.style.display = "none";
            e.target.textContent = "Send Message";
        } else {
            msgBox.style.display = "block";
            e.target.textContent = "Close👇🏻";
        }
        boxOpened[boxName] = !boxOpened[boxName];
    }
});

//handle send button
document.addEventListener('click', function(e) {
    if (e.target.matches(".send-button")) {
        console.log('click send');
        let postId = e.target.value;
        let message = document.querySelector(`#msg-content${postId}`);
        let label = document.querySelector(`#label${postId}`);
        if (message.value == "") {
            label.textContent = "Message can not be empty."
            e.preventDefault()
        }
        fetch('/send-message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                post_id: postId,
                message: message.value
            }),
        })
        .then(res => res.json())
        .then(data => {
            if (data.isSent) {
                label.textContent = "message has been sent successfully!"
                e.target
            } else if (!data.isSent) {
                label.textContent = "Somthing woring. Please try again later."
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        })
    }
});
