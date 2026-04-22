import sys

js_to_inject = """

        // ── DYNAMIC GALLERY INJECTION (Decap CMS) ──
        function fetchGalleryData() {
            fetch('data/gallery.json')
                .then(res => res.json())
                .then(data => {
                    if(data && data.items) {
                        renderGallery(data.items);
                    }
                })
                .catch(err => {
                    console.error("Error loading gallery JSON:", err);
                    document.getElementById('dynamic-gallery-root').innerHTML = "<div style='color:red; text-align:center;'>Error loading gallery.</div>";
                });
        }

        function renderGallery(items) {
            let html = '';
            items.forEach(item => {
                const id = item.id;
                html += `
                <div class="review-card" id="review-card-${id}">
                    <div class="review-image">
                        <img src="${item.image}" alt="${item.title}" />
                    </div>
                    <div class="review-body">
                        <div class="review-header">
                            <div class="review-title-area">
                                <div class="review-number">Image ${id < 10 ? '0'+id : id}</div>
                                <div class="review-title">${item.title}</div>
                            </div>
                            <div class="checkbox-area">
                                <input type="checkbox" id="check-${id}" onchange="toggleApproval(${id}, this)">
                                <label for="check-${id}">
                                    <span class="check-icon">✓</span>
                                    Photo Approved
                                </label>
                            </div>
                        </div>
                        <div class="review-divider"></div>
                        <div class="comment-section">
                            <h4>💬 Comments</h4>
                            <div class="comment-input-area">
                                <textarea id="input-${id}" rows="2" placeholder="Write your comment about this image..."></textarea>
                                <button class="comment-btn" onclick="addComment(${id})">Send</button>
                            </div>
                            <div class="comments-list" id="comments-${id}">
                                <div class="no-comments">No comments yet. Be the first to review!</div>
                            </div>
                        </div>
                    </div>
                </div>`;
            });
            document.getElementById('dynamic-gallery-root').innerHTML = html;
            // Now that DOM elements exist, hook up saved comments and boxes!
            if(typeof loadSavedState === 'function') {
                loadSavedState(); 
            }
        }
        
"""

def process(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the `setTimeout(fetchLiveData, 150);` to also trigger the gallery load
        target = "setTimeout(fetchLiveData, 150);"
        replacement = target + "\\n        setTimeout(fetchGalleryData, 200);" + js_to_inject
        
        # also we need to disable the original loadSavedState() that fire automatically on window load!
        # wait! Did the original script fire it automatically? let's look for "window.onload = loadSavedState;"
        target2 = "loadSavedState();"
        # We don't want to replace string definitions, only calls. Actually, let's just let it be called later.

        new_content = content.replace(target, replacement)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        print(f"Successfully injected JS into {filepath}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

process('index.html')
process('dashboard.html')
