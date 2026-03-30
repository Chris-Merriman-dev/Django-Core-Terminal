/*
    Created By : Christian Merriman
    Date : 3/18/26
    Purpose : Used for handling the asset feed page - Refactored for logic parity with image_creation.js
*/

//global window hooks
window.openModal = (imgSrc) => AssetManager.open(imgSrc);
window.closeModal = () => AssetManager.close();

document.addEventListener('DOMContentLoaded', () => {
    AssetManager.init();
});

const AssetManager = {
    ui: {
        modal: null,
        modalImg: null,
        closeBtn: null
    },

    //state mirrored from image_creation.js for consistent zoom behavior
    state: {
        zoom: { scale: 1, panning: false, pointX: 0, pointY: 0, start: { x: 0, y: 0 } }
    },

    init: function() {
        console.log("[OCP_SYSTEM]: Initializing Asset Feed Controller...");
        
        this.ui.modal = document.getElementById("imageModal");
        this.ui.modalImg = document.getElementById("img01");
        this.ui.closeBtn = document.querySelector(".close");

        if (this.ui.modal && this.ui.modalImg) {
            this.setupZoomEvents();
        }
    },

    open: function(imgSrc) {
        if (!this.ui.modal || !this.ui.modalImg) return;

        //reset state (matches image_creation.js)
        this.state.zoom = { scale: 1, panning: false, pointX: 0, pointY: 0, start: { x: 0, y: 0 } };
        
        //set the source
        this.ui.modalImg.src = imgSrc;

        //set display to flex BEFORE applying transform 
        //this ensures the browser knows the image dimensions for centering
        this.ui.modal.style.display = "flex"; 

        //reset the transform to neutral
        this.applyTransform();
    },

    close: function() {
        if (this.ui.modal) {
            this.ui.modal.style.display = "none";
            this.state.zoom.panning = false;
        }
    },

    //using the refined transform function from image_creation.js
    applyTransform: function() {
        const el = this.ui.modalImg;
        const z = this.state.zoom;
        if (!el) return;
        el.style.transform = `translate(${z.pointX}px, ${z.pointY}px) scale(${z.scale})`;
    },

    //setup our zoom for images
    setupZoomEvents: function() {
        const UI = this.ui;
        const state = this.state;

        //close only if the user clicks the actual background (the modal div), 
        //NOT the image or caption.
        UI.modal.onclick = (e) => {
            if (e.target === UI.modal) {
                this.close();
            }
        };

        //close button
        if (UI.closeBtn) UI.closeBtn.onclick = () => this.close();

        //escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === "Escape") this.close();
        });

        //setup scroll for zooming
        UI.modal.onwheel = (e) => {
            e.preventDefault();
            const xs = (e.clientX - state.zoom.pointX) / state.zoom.scale;
            const ys = (e.clientY - state.zoom.pointY) / state.zoom.scale;
            (e.deltaY < 0) ? (state.zoom.scale *= 1.1) : (state.zoom.scale /= 1.1);
            state.zoom.scale = Math.min(Math.max(0.5, state.zoom.scale), 10);
            state.zoom.pointX = e.clientX - xs * state.zoom.scale;
            state.zoom.pointY = e.clientY - ys * state.zoom.scale;
            this.applyTransform();
        };

        //setup mouse Down (Start Pan)
        UI.modalImg.onmousedown = (e) => {
            e.preventDefault();
            //stop the click from traveling up to the modal background
            e.stopPropagation(); 
            
            state.zoom.start = { 
                x: e.clientX - state.zoom.pointX, 
                y: e.clientY - state.zoom.pointY 
            };
            state.zoom.panning = true;
            UI.modalImg.style.cursor = "grabbing";
        };

        //global Mouse Up
        window.onmouseup = () => {
            state.zoom.panning = false;
            if (UI.modalImg) UI.modalImg.style.cursor = "zoom-in";
        };

        //global Mouse Move
        window.onmousemove = (e) => {
            if (!state.zoom.panning) return;
            state.zoom.pointX = e.clientX - state.zoom.start.x;
            state.zoom.pointY = e.clientY - state.zoom.start.y;
            this.applyTransform();
        };
    }
};

//will toggle the comments for the assetfeed
function toggleComments(assetId) {
    const drawer = document.getElementById(`comment-section-${assetId}`);
    drawer.style.display = (drawer.style.display === "block") ? "none" : "block";
}

//allows user to submit new comments
function submitComment(event, assetId) {
    event.preventDefault();

    const input = document.getElementById(`input-${assetId}`);
    const content = input.value;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    //post our comment to the django backend
    fetch(`/asset/${assetId}/comment/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: new URLSearchParams({'content': content})
    })
    .then(response => response.json())
    .then(data => {
        //we got the response so setup the new comment
        if (data.status === 'success') {
            const list = document.querySelector(`#comment-section-${assetId} .assetfeed-comment-list`);
            if(list){
                const newComment = `
                    <div class="assetfeed-comment-item">
                        <span class="value">[${data.author.toUpperCase()}]:</span>
                        <span class="content">${data.content}</span>
                        <br>
                        <small class="label">${data.timestamp}</small>
                    </div>
                `;
                list.insertAdjacentHTML('beforeend', newComment);
            }

            //make sure to update the comment count by 1
            const assetCount = document.getElementById(`count-${assetId}`);
            if (assetCount) {
                let currentCount = parseInt(assetCount.innerText) || 0;
                assetCount.innerText = currentCount + 1;
            }
            input.value = '';
        }
    });
}