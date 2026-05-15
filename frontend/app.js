const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const analyzeBtn = document.getElementById('analyze-btn');
const statusContainer = document.getElementById('status-container');
const progressBar = document.getElementById('progress-bar');
const statusText = document.getElementById('status-text');
const statusPercentage = document.getElementById('status-percentage');
const resultContainer = document.getElementById('result-container');

let selectedFile = null;

// Handle Drag and Drop
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('border-black', 'bg-[#f5f5f5]');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('border-black', 'bg-[#f5f5f5]');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('border-black', 'bg-[#f5f5f5]');
    const files = e.dataTransfer.files;
    if (files.length > 0) handleFile(files[0]);
});

dropZone.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) handleFile(e.target.files[0]);
});

function handleFile(file) {
    if (!file.type.startsWith('image/')) {
        alert('Please select an image file.');
        return;
    }
    if (file.size > 10 * 1024 * 1024) {
        alert('File size exceeds 10MB limit.');
        return;
    }
    selectedFile = file;
    dropZone.innerHTML = `
        <div class="space-y-2">
            <p class="text-sm font-semibold text-black">${file.name}</p>
            <p class="text-xs text-[#737373]">Ready to analyze</p>
        </div>
    `;
    analyzeBtn.disabled = false;
    resultContainer.classList.add('hidden');
}

analyzeBtn.addEventListener('click', async () => {
    if (!selectedFile) return;

    // Reset UI
    analyzeBtn.disabled = true;
    statusContainer.classList.remove('hidden');
    updateProgress(10, 'Uploading image...');

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
        updateProgress(30, 'Analyzing visual features...');
        
        const response = await fetch('http://localhost:8000/api/analyze-product', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to analyze product');
        }

        updateProgress(70, 'Researching product data...');
        const data = await response.json();
        
        updateProgress(100, 'Complete!');
        setTimeout(() => {
            renderResults(data);
            statusContainer.classList.add('hidden');
        }, 500);

    } catch (error) {
        alert(`Error: ${error.message}`);
        analyzeBtn.disabled = false;
        statusContainer.classList.add('hidden');
    }
});

function updateProgress(percent, text) {
    progressBar.style.width = `${percent}%`;
    statusPercentage.innerText = `${percent}%`;
    if (text) statusText.innerText = text;
}

function renderResults(data) {
    document.getElementById('result-category').innerText = data.category;
    document.getElementById('result-brand').innerText = data.brand;
    document.getElementById('result-model').innerText = data.model_name;
    document.getElementById('result-desc').innerText = data.official_description || 'No description available.';
    document.getElementById('result-value').innerText = `${data.estimated_retail_value_range || 'N/A'} ${data.currency}`;
    
    const specsContainer = document.getElementById('result-specs');
    specsContainer.innerHTML = '';
    
    if (data.specifications && data.specifications.length > 0) {
        data.specifications.forEach(spec => {
            const specEl = document.createElement('div');
            specEl.className = 'flex justify-between border-b border-[#f5f5f5] pb-1';
            specEl.innerHTML = `
                <span class="text-xs text-[#737373]">${spec.label}</span>
                <span class="text-xs font-medium">${spec.value}</span>
            `;
            specsContainer.appendChild(specEl);
        });
    } else {
        specsContainer.innerHTML = '<p class="text-xs text-[#737373]">No specific specifications found.</p>';
    }

    document.getElementById('raw-json').innerText = JSON.stringify(data, null, 2);
    resultContainer.classList.remove('hidden');
    analyzeBtn.disabled = false;
}
