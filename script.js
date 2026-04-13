document.addEventListener('DOMContentLoaded', () => {
    const viewButtons = document.querySelectorAll('.view-btn');
    const closeBtn = document.getElementById('close-detail-btn');
    const pageContainer = document.querySelector('.page-container');

    let expandedCard = null;

    viewButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const card = e.target.closest('.alert-card');
            if (!card) return;

            // PREPARE: Get initial positions of the card being expanded
            const firstRect = card.getBoundingClientRect();

            // Set state for CSS structural changes
            document.body.classList.add('view-mode-active');
            card.classList.add('expanded');

            // Force layout recalculation to get the target structural positions
            requestAnimationFrame(() => {
                const lastRect = card.getBoundingClientRect();
                
                // INVERT: Calculate difference and instantly translate card back to start
                const dy = firstRect.top - lastRect.top;
                
                // We don't need horizontal since it usually just spans the width, but just in case
                const dx = firstRect.left - lastRect.left;

                card.style.transition = 'none';
                card.style.transform = `translate(${dx}px, ${dy}px)`;
                
                // Keep the card on top of others z-index wise during animation
                card.style.zIndex = '50';

                // PLAY: Remove the invert transform and let it smoothly transition to 0,0
                requestAnimationFrame(() => {
                    card.style.transition = 'transform 0.5s cubic-bezier(0.2, 0.8, 0.2, 1)';
                    card.style.transform = 'translate(0, 0)';
                    
                    // Reset z-index and transition after animation completes
                    setTimeout(() => {
                        card.style.transition = '';
                        card.style.zIndex = '';
                        
                        // Scroll to top just in case
                        pageContainer.scrollTo({ top: 0, behavior: 'smooth' });
                    }, 500);
                });
            });

            expandedCard = card;
        });
    });

    closeBtn.addEventListener('click', () => {
        if (!expandedCard) return;
        closeExpanded();
    });

    function closeExpanded() {
        document.body.classList.remove('view-mode-active');
        expandedCard.classList.remove('expanded');
        expandedCard = null;
    }

    // --- Filter Logic ---
    const tabs = document.querySelectorAll('.tab');
    const cards = document.querySelectorAll('.alert-card');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Close any expanded card first
            if (expandedCard) closeExpanded();

            // Update active tab
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            const filter = tab.getAttribute('data-filter');

            cards.forEach(card => {
                const category = card.getAttribute('data-category');
                
                if (filter === 'all' || category === filter) {
                    card.style.display = 'flex';
                    // Optional: add a small fade-in animation
                    card.style.opacity = '0';
                    requestAnimationFrame(() => {
                        card.style.transition = 'opacity 0.3s ease';
                        card.style.opacity = '1';
                    });
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
});
