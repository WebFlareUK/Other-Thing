// Handle signature canvas and testimonial star rating
(function(){
    const canvas = document.getElementById('signatureCanvas');
    const form = document.getElementById('signoffForm');
    
    // Form validation
    if (form) {
        form.addEventListener('submit', function(e) {
            const projectSatisfaction = document.getElementById('id_project_satisfaction');
            const portfolioPermission = document.getElementById('id_portfolio_permission');
            
            if (!projectSatisfaction.checked || !portfolioPermission.checked) {
                e.preventDefault();
                alert('Please confirm both Project Satisfaction and Portfolio Permission to proceed.');
                return false;
            }
            
            // If we have a canvas, ensure there's a signature
            if (canvas) {
                // use hasSignature (set while drawing) to determine if user signed
                if (!window.__hasSignature) {
                    e.preventDefault();
                    alert('Please provide your signature before submitting.');
                    return false;
                }
                // store the signature data URL into the hidden input
                const signatureData = canvas.toDataURL('image/png');
                const dataInput = document.getElementById('signatureData');
                if (dataInput) dataInput.value = signatureData;
            }
        });
    }

    if (canvas) {
    const ctx = canvas.getContext('2d');
    let isDrawing = false;
    let lastX = 0, lastY = 0;
    // track whether the user has drawn on the canvas at least once
    window.__hasSignature = false;

        function resizeCanvas(){
            const rect = canvas.getBoundingClientRect();
            canvas.width = rect.width;
            canvas.height = rect.height;
        }
        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);

        function start(e){
            isDrawing = true;
            const rect = canvas.getBoundingClientRect();
            const x = (e.clientX || (e.touches && e.touches[0].clientX)) - rect.left;
            const y = (e.clientY || (e.touches && e.touches[0].clientY)) - rect.top;
            lastX = x; lastY = y;
        }
        function draw(e){
            if(!isDrawing) return;
            e.preventDefault();
            const rect = canvas.getBoundingClientRect();
            const x = (e.clientX || (e.touches && e.touches[0].clientX)) - rect.left;
            const y = (e.clientY || (e.touches && e.touches[0].clientY)) - rect.top;
            ctx.strokeStyle = '#1e293b';
            ctx.lineWidth = 2;
            ctx.lineCap = 'round';
            ctx.beginPath();
            ctx.moveTo(lastX, lastY);
            ctx.lineTo(x, y);
            ctx.stroke();
            lastX = x; lastY = y;
            window.__hasSignature = true;
        }
        function stop(){ isDrawing = false; }

        canvas.addEventListener('mousedown', start);
        canvas.addEventListener('mousemove', draw);
        canvas.addEventListener('mouseup', stop);
        canvas.addEventListener('mouseout', stop);
        canvas.addEventListener('touchstart', start);
        canvas.addEventListener('touchmove', draw);
        canvas.addEventListener('touchend', stop);

        document.getElementById('clearSignature').addEventListener('click', function(e){
            ctx.clearRect(0,0,canvas.width,canvas.height);
            window.__hasSignature = false;
            const dataInput = document.getElementById('signatureData');
            if (dataInput) dataInput.value = '';
        });
    }

    // Star rating
    const stars = document.querySelectorAll('.star');
    stars.forEach(star => {
        star.addEventListener('click', function(e){
            e.stopPropagation();
            const rating = parseInt(this.dataset.rating, 10);
            stars.forEach(s => s.classList.toggle('active', parseInt(s.dataset.rating,10) <= rating));
            // create or set hidden input for rating
            let ratingInput = document.getElementById('id_rating');
            if (!ratingInput) {
                ratingInput = document.createElement('input');
                ratingInput.type = 'hidden';
                ratingInput.name = 'rating';
                ratingInput.id = 'id_rating';
                document.getElementById('signoffForm').appendChild(ratingInput);
            }
            ratingInput.value = rating;
        });
    });

    // Prevent testimonial area clicks from toggling parent checkbox
    const testimonialContainers = document.querySelectorAll('.testimonial-container');
    testimonialContainers.forEach(c => c.addEventListener('click', function(e){ e.stopPropagation(); }));

})();

// Toggle checkbox visual and actual input (keeps both in sync)
function toggleCheckbox(container) {
    // container is the .checkbox-header or the .checkbox-item element
    let item = container;
    if (!item.classList.contains('checkbox-item')) {
        item = container.closest('.checkbox-item');
    }
    if (!item) return;

    const input = item.querySelector('input[type="checkbox"]');
    // if there's no input rendered (e.g., using Django's hidden widgets), try name-based
    if (!input) {
        // try common fields inside this block
        const labels = item.querySelectorAll('.checkbox-title');
        if (labels.length) {
            // attempt to match by the title text
            // iterate inputs in form and find matching name (best-effort)
            const form = document.getElementById('signoffForm');
            if (form) {
                const allInputs = form.querySelectorAll('input[type="checkbox"]');
                // naive toggle: toggle first checkbox inside this block by index
                if (allInputs.length) {
                    allInputs[0].checked = !allInputs[0].checked;
                    item.classList.toggle('checked', allInputs[0].checked);
                }
            }
            return;
        }
    }

    // toggle the actual input if present
    if (input) {
        input.checked = !input.checked;
        item.classList.toggle('checked', input.checked);
    }
}

// Initialize checkbox visuals based on actual inputs on load
document.addEventListener('DOMContentLoaded', function(){
    const items = document.querySelectorAll('.checkbox-item');
    items.forEach(item => {
        const input = item.querySelector('input[type="checkbox"]');
        if (input && input.checked) {
            item.classList.add('checked');
        }
    });

    // Attach print button handler: expand compact services before printing so descriptions are included
    const printBtn = document.getElementById('printPdfBtn');
    if (printBtn) {
        printBtn.addEventListener('click', function(e){
            // expand all compact details so descriptions show in print
            const details = document.querySelectorAll('details.compact-services');
            details.forEach(d => { try { d.open = true; } catch (err) {} });
            // small delay to allow layout to update
            setTimeout(function(){ window.print(); }, 120);
        });
    }
});
