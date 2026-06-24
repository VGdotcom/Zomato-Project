document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('pref-form');
    const ratingInput = document.getElementById('min-rating');
    const ratingVal = document.getElementById('rating-val');
    const loader = document.getElementById('loader');
    const resultsDiv = document.getElementById('results');
    const alertsDiv = document.getElementById('alerts');
    const filterChips = document.getElementById('filter-chips');
    const globalInsight = document.getElementById('global-insight');
    const budgetInput = document.getElementById('budget');

    // Food images mapped by cuisine keywords for intelligent matching
    const foodImages = {
        'italian': '/food_pasta.png',
        'pasta': '/food_pasta.png',
        'continental': '/food_pasta.png',
        'french': '/food_french.png',
        'bakery': '/food_french.png',
        'dessert': '/food_french.png',
        'fusion': '/food_fusion.png',
        'seafood': '/food_fusion.png',
        'asian': '/food_chinese.png',
        'chinese': '/food_chinese.png',
        'japanese': '/food_chinese.png',
        'thai': '/food_chinese.png',
        'indian': '/food_indian.png',
        'north indian': '/food_indian.png',
        'south indian': '/food_indian.png',
        'mughlai': '/food_indian.png',
        'biryani': '/food_indian.png',
        'cafe': '/food_cafe.png',
        'coffee': '/food_cafe.png',
        'healthy': '/food_fusion.png',
        'salad': '/food_fusion.png',
        'mediterranean': '/food_fusion.png',
    };

    // Default images pool for random assignment
    const defaultImages = [
        '/food_pasta.png',
        '/food_french.png',
        '/food_fusion.png',
        '/food_indian.png',
        '/food_chinese.png',
        '/food_cafe.png',
    ];

    // Track used images to prevent repetition
    let usedImages = new Set();
    
    // Reset used images on new search
    form.addEventListener('submit', () => {
        usedImages.clear();
    });

    // Get a food image based on cuisine type, ensuring strict uniqueness
    function getFoodImage(cuisine, index) {
        let selectedImg = null;
        
        // 1. Try to find a matching cuisine image that hasn't been used
        if (cuisine) {
            const lower = cuisine.toLowerCase();
            for (const [key, img] of Object.entries(foodImages)) {
                if (lower.includes(key) && !usedImages.has(img)) {
                    selectedImg = img;
                    break;
                }
            }
        }
        
        // 2. If no unused match found, pick the first unused default image
        if (!selectedImg) {
            for (const img of defaultImages) {
                if (!usedImages.has(img)) {
                    selectedImg = img;
                    break;
                }
            }
        }
        
        // 3. Fallback if somehow all 6 images are used (highly unlikely for top 3)
        if (!selectedImg) {
            selectedImg = defaultImages[index % defaultImages.length];
        }
        
        usedImages.add(selectedImg);
        return selectedImg;
    }

    // Update rating label
    ratingInput.addEventListener('input', (e) => {
        ratingVal.textContent = parseFloat(e.target.value).toFixed(1);
    });

    // Budget toggle handling
    document.querySelectorAll('.budget-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.budget-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            budgetInput.value = btn.dataset.value;
        });
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Collect data
        const locationVal = document.getElementById('loc').value;
        const budgetVal = budgetInput.value;
        const ratingValNum = parseFloat(ratingInput.value);
        const cuisineVal = document.getElementById('cuisine').value.trim();
        const notesVal = document.getElementById('notes').value.trim();

        const payload = {
            location: locationVal,
            budget: budgetVal,
            min_rating: ratingValNum,
            cuisine: cuisineVal || null,
            custom_notes: notesVal || null
        };

        // Reset UI
        alertsDiv.innerHTML = '';
        resultsDiv.innerHTML = '';
        loader.classList.remove('hidden');
        globalInsight.classList.add('hidden');
        
        // Format budget label
        const budgetLabels = { low: 'Low Budget', medium: 'Medium Budget', high: 'High Budget' };
        const budgetLabel = budgetLabels[budgetVal] || 'Medium Budget';
        
        // Populate filter chips
        filterChips.innerHTML = `
            <div class="filter-chip">📍 ${locationVal}</div>
            ${cuisineVal ? `<div class="filter-chip">${cuisineVal}</div>` : ''}
            <div class="filter-chip">${budgetLabel}</div>
            <div class="filter-chip highlight">⭐ ${ratingValNum.toFixed(1)}+</div>
        `;
        filterChips.classList.remove('hidden');

        try {
            const res = await fetch('/api/recommend', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            let data;
            const textResponse = await res.text();
            try {
                data = JSON.parse(textResponse);
            } catch (e) {
                if (textResponse.includes("Your space")) {
                    throw new Error("The AI backend service is currently unavailable or waking up. Please try again in a few moments.");
                }
                throw new Error("Received an invalid response from the server.");
            }
            
            if (!res.ok) {
                throw new Error(data?.detail || 'Failed to fetch recommendations');
            }

            loader.classList.add('hidden');
            if (data.fallbacks && data.fallbacks.length > 0) {
                renderAlerts(data.fallbacks, 'warning');
            }
            
            if (!data.recommendations || data.recommendations.length === 0) {
                alertsDiv.innerHTML = `<div class="alert error"><span>🚨</span> <div>No restaurants found matching your criteria in this location. Please try relaxing your constraints.</div></div>`;
                return;
            }

            // Show global insight
            const cuisineText = cuisineVal ? `${cuisineVal} cuisine` : 'dining';
            document.getElementById('global-insight-text').textContent = `Based on your preference for ${cuisineText} in ${locationVal} with a ${budgetVal} budget, I've curated these top selections known for authentic flavors and great ambiance.`;
            globalInsight.classList.remove('hidden');

            renderRecommendations(data.recommendations);
        } catch (err) {
            loader.classList.add('hidden');
            alertsDiv.innerHTML = `<div class="alert error"><span>❌</span> <div>${err.message}</div></div>`;
        }
    });

    function renderAlerts(messages, type) {
        messages.forEach(msg => {
            const div = document.createElement('div');
            div.className = `alert ${type}`;
            div.innerHTML = `<span>⚠️</span> <div>${msg}</div>`;
            alertsDiv.appendChild(div);
        });
    }

    function renderRecommendations(recs) {
        recs.forEach((rec, index) => {
            const card = document.createElement('div');
            const isFeatured = index === 0;
            card.className = `epicurean-card ${isFeatured ? 'featured' : ''}`;
            card.style.animationDelay = `${index * 0.1}s`;
            
            // Format cost
            const costStr = rec.cost ? `₹${rec.cost.toLocaleString()} for two` : 'Cost N/A';
            
            // Format rationale to remove double quotes if present
            let rationaleText = rec.rationale || '';
            rationaleText = rationaleText.replace(/^"|"$/g, '');
            
            // Get appropriate food image
            const imgSrc = getFoodImage(rec.cuisine, index);
            
            // Generate a fake review count for visual richness
            const reviewCount = Math.floor(Math.random() * 200) + 50;

            if (isFeatured) {
                // Featured card — horizontal layout with image
                card.innerHTML = `
                    <div class="card-image">
                        <span class="card-rank">#${rec.rank} Match</span>
                        <img src="${imgSrc}" alt="${rec.name} — signature dish" loading="lazy">
                    </div>
                    <div class="card-content">
                        <div class="card-header">
                            <h3 class="card-title">${rec.name}</h3>
                            <button class="bookmark-icon" aria-label="Save ${rec.name}">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>
                            </button>
                        </div>
                        <div class="card-meta">
                            <span class="rating">⭐ ${rec.rating}</span>
                            <span class="rating-count">(${reviewCount})</span>
                            <span class="dot">•</span>
                            <span>${rec.cuisine || 'Various'}</span>
                            <span class="dot">•</span>
                            <span>${costStr}</span>
                        </div>
                        <div class="ai-insight">
                            <p><span class="ai-insight-icon">
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline; margin-right:4px;"><circle cx="12" cy="12" r="10"></circle><circle cx="12" cy="12" r="4"></circle></svg>
                            </span> "${rationaleText}"</p>
                        </div>
                        <div class="card-actions">
                            <button class="btn-secondary">Menu</button>
                            <button class="btn-solid">Reserve</button>
                        </div>
                    </div>
                `;
            } else {
                // Standard card — vertical layout with image
                card.innerHTML = `
                    <div class="card-image">
                        <span class="card-rank">#${rec.rank} Match</span>
                        <img src="${imgSrc}" alt="${rec.name} — signature dish" loading="lazy">
                    </div>
                    <div class="card-content">
                        <h3 class="card-title">${rec.name}</h3>
                        <div class="card-meta">
                            <span class="rating">⭐ ${rec.rating}</span>
                            <span class="dot">•</span>
                            <span>${rec.cuisine || 'Various'}</span>
                            <span class="dot">•</span>
                            <span>${costStr}</span>
                        </div>
                        <div class="ai-insight">
                            <p>"${rationaleText}"</p>
                        </div>
                        <button class="btn-outline-full">View Details</button>
                    </div>
                `;
            }
            
            resultsDiv.appendChild(card);
        });
    }
});
