/*
    Created By : Christian Merriman
    Date : 3/18/26
    Purpose : Used for the image creation page
*/


document.addEventListener('DOMContentLoaded', () => {
    //setup our ui in one ui var
    const UI = {
        genBtn: document.getElementById('image-creation-generate-btn'),
        input: document.getElementById('image-creation-prompt-input'),
        status: document.getElementById('image-creation-status-area'),
        display: document.getElementById('image-creation-display'),
        bar: document.getElementById('image-creation-server-status-bar'),
        barText: document.getElementById('image-creation-status-text'),
        dlBtn: document.getElementById('image-creation-main-download-btn'),
        gallery: document.getElementById('image-creation-history-scrollbox'),
        modal: document.getElementById("image-creation-modal"),
        modalImg: document.getElementById("image-creation-img-full"),
        modalClose: document.querySelector(".image-creation-modal-close")
    };

    //set the init state
    let state = {
        isProcessing: false,
        failCount: 0,
        zoom: { scale: 1, panning: false, pointX: 0, pointY: 0, start: { x: 0, y: 0 } }
    };

    //setup our generate button
    if (UI.genBtn) {
        UI.genBtn.onclick = () => initiateVisionGeneration(UI, state);
    }

    //setup our download button
    if (UI.dlBtn && UI.display) {
        UI.dlBtn.onclick = () => executeDownload(UI.display.src);
    }

    //this will monitor to make sure server is online. it will keep checking, incase it comes on or offline and will  then do it every 5000ms
    monitorServerStatus(UI, state);
    setInterval(() => monitorServerStatus(UI, state), 5000);

    //setup the modal and zooming for looking at our image
    if (UI.display && UI.modal && UI.modalImg) {
        UI.display.onclick = () => {
            UI.modal.style.display = "block";
            UI.modalImg.src = UI.display.src;
            state.zoom = { scale: 1, panning: false, pointX: 0, pointY: 0, start: { x: 0, y: 0 } };
            applyVisionTransform(UI.modalImg, state.zoom);
        };

        UI.modal.onwheel = (e) => {
            e.preventDefault();
            const xs = (e.clientX - state.zoom.pointX) / state.zoom.scale;
            const ys = (e.clientY - state.zoom.pointY) / state.zoom.scale;
            (e.deltaY < 0) ? (state.zoom.scale *= 1.1) : (state.zoom.scale /= 1.1);
            state.zoom.scale = Math.min(Math.max(0.5, state.zoom.scale), 10);
            state.zoom.pointX = e.clientX - xs * state.zoom.scale;
            state.zoom.pointY = e.clientY - ys * state.zoom.scale;
            applyVisionTransform(UI.modalImg, state.zoom);
        };

        UI.modalImg.onmousedown = (e) => {
            e.preventDefault();
            state.zoom.start = { x: e.clientX - state.zoom.pointX, y: e.clientY - state.zoom.pointY };
            state.zoom.panning = true;
        };

        window.onmouseup = () => state.zoom.panning = false;
        window.onmousemove = (e) => {
            if (!state.zoom.panning) return;
            state.zoom.pointX = e.clientX - state.zoom.start.x;
            state.zoom.pointY = e.clientY - state.zoom.start.y;
            applyVisionTransform(UI.modalImg, state.zoom);
        };
    }

    if (UI.modalClose) UI.modalClose.onclick = () => UI.modal.style.display = "none";
});



//handles the logic for generation
async function initiateVisionGeneration(UI, state) {
    //prevent clicks if already processing
    if (state.isProcessing) return;

    //setup the prompt and trim whats not needed
    const prompt = UI.input.value.trim();
    if (!prompt) {
        if (UI.status) {
             UI.status.innerText = "ERROR: INPUT REQUIRED";
             if (UI.bar) UI.bar.className = 'image-creation-status-offline';
        }
        return;
    }

    //get our csrfToken
    const csrfToken = typeof getCookie === 'function' ? getCookie('csrftoken') : null;
    if (!csrfToken) {
        if (UI.status) {
            UI.status.innerText = "SECURITY ERROR: TOKEN MISSING";
            if (UI.bar) UI.bar.className = 'image-creation-status-offline';
        }
        return; 
    }

    //start the process
    state.isProcessing = true;
    if (UI.genBtn) UI.genBtn.disabled = true;
    
    if (UI.bar) UI.bar.className = 'image-creation-status-busy';
    if (UI.status) UI.status.innerText = "UP-LINKING TO FLUX SERVER...";
    
    //now attempt to generate the image with POST to django backend
    try {
        const response = await fetch('/ocp/generate_vision/', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken 
            },
            body: JSON.stringify({ prompt: prompt })
        });

        if (response.status === 403) {
            if (UI.status) UI.status.innerText = "ERROR: ACCESS FORBIDDEN (CSRF)";
            if (UI.bar) UI.bar.className = 'image-creation-status-offline';
            return;
        }

        const data = await response.json();

        //we get our data (image) handle it
        if (data.status === 'success') {
            if (UI.display) {
                UI.display.src = data.image_url;
                UI.display.style.display = 'block';
            }
            if (UI.dlBtn) UI.dlBtn.style.display = 'block';
            
            if (UI.bar) UI.bar.className = 'image-creation-status-online';
            if (UI.status) UI.status.innerText = "VISION GENERATED SUCCESSFULLY";
            
            //update our gallery of images we have created while on this page
            updateVisionGallery(data.image_url, UI);
        } else {
            if (UI.status) UI.status.innerText = "ERROR: GENERATION FAILED";
            if (UI.bar) UI.bar.className = 'image-creation-status-offline';
        }

    } catch (err) {
        console.error("OCP UPLINK CRITICAL FAILURE:", err);
        if (UI.status) UI.status.innerText = "CRITICAL: CONNECTION TIMEOUT";
        if (UI.bar) UI.bar.className = 'image-creation-status-offline';
    } finally {
        //reset processing state
        state.isProcessing = false;
        
        //final button check - keep it disabled if link was lost during generation
        setTimeout(() => {
            monitorServerStatus(UI, state);
        }, 3000);
    }
}

//handles check for the server if its online or offline
async function monitorServerStatus(UI, state) {
    //stop heartbeat from modifying UI if we are in the middle of a generation
    if (!UI.bar || !UI.barText || state.isProcessing) return;
    
    try {
        //setup an abort if needed and then check for server
        const ctrl = new AbortController();
        const timeout = setTimeout(() => ctrl.abort(), 2000);
        const response = await fetch('/ocp/health_check/', { signal: ctrl.signal });
        clearTimeout(timeout);
        
        //we got our response
        if (response.ok) {
            const data = await response.json();
            
            //if connection was found setup the html
            if (data.engine_link === 'established') {
                state.failCount = 0;
                UI.bar.className = 'image-creation-status-online';
                UI.barText.innerText = "LINK ESTABLISHED";
                
                //only re-enable if we are NOT processing
                if (!state.isProcessing && UI.genBtn) {
                    UI.genBtn.disabled = false;
                }
            } else {
                throw new Error("Engine Offline"); 
            }
        } else { 
            throw new Error("Server Error"); 
        }
    } catch (err) {
        state.failCount++;
        if (state.failCount >= 2) {
            UI.bar.className = 'image-creation-status-offline';
            UI.barText.innerText = "LINK SEVERED";
            
            //if the link is severed, the button MUST be disabled
            if (UI.genBtn) UI.genBtn.disabled = true;
            
            if (UI.status && !state.isProcessing) {
                UI.status.innerText = "OFFLINE: CHECK ENGINE STATUS";
            }
        }
    }
}

//will handle displaying images created by the user during this load of the page
function updateVisionGallery(url, UI) {
    if (!UI.gallery) return;
    const thumb = document.createElement('img');
    thumb.src = url;
    thumb.className = 'image-creation-history-thumb active';
    
    document.querySelectorAll('.image-creation-history-thumb').forEach(t => t.classList.remove('active'));

    thumb.onclick = () => {
        document.querySelectorAll('.image-creation-history-thumb').forEach(t => t.classList.remove('active'));
        thumb.classList.add('active');
        if (UI.display) {
            UI.display.src = thumb.src;
            UI.display.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
        if (UI.status) UI.status.innerText = "RETRIEVING ARCHIVED VISION DATA...";
    };
    UI.gallery.prepend(thumb);
}


//appying transformation to the image
function applyVisionTransform(element, state) {
    if (!element) return;
    element.style.transform = `translate(${state.pointX}px, ${state.pointY}px) scale(${state.scale})`;
}

//handles downloading the image
async function executeDownload(url) {
    if (!url || url === "" || url.includes('undefined')) return;
    try {
        //gets the image link and saves it to the computer
        const response = await fetch(url);
        const blob = await response.blob();
        const blobUrl = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = blobUrl;
        link.download = `OCP-VISION-${Date.now()}.png`; 
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(blobUrl);
    } catch (err) {
        console.error("OCP Download protocol failed:", err);
        window.open(url, '_blank');
    }
}