document.addEventListener('DOMContentLoaded', () => {
    const viewButtons = document.querySelectorAll('.view-btn');
    const closeBtn = document.getElementById('close-detail-btn');
    const closeSchemaBtn = document.getElementById('close-schema-detail-btn');
    const pageContainer = document.querySelector('.page-container');
    const alertNavLink = document.querySelector('[data-nav="alerts"]');
    const tabs = document.querySelectorAll('.tab');
    const cards = document.querySelectorAll('.alert-card');
    const modalTriggers = document.querySelectorAll('[data-modal-target]');
    const modals = document.querySelectorAll('.modal-overlay');
    const modalCloseButtons = document.querySelectorAll('[data-close-modal]');

    let expandedCard = null;
    let activeModal = null;

    function setFilter(filter) {
        tabs.forEach(tab => {
            tab.classList.toggle('active', tab.getAttribute('data-filter') === filter);
        });

        cards.forEach(card => {
            const category = card.getAttribute('data-category');

            if (filter === 'all' || category === filter) {
                card.style.display = 'flex';
                card.style.opacity = '0';
                requestAnimationFrame(() => {
                    card.style.transition = 'opacity 0.3s ease';
                    card.style.opacity = '1';
                });
            } else {
                card.style.display = 'none';
            }
        });
    }

    function resetAlertsView() {
        closeModal();
        document.querySelectorAll('.detail-panel').forEach(panel => panel.classList.remove('active-panel'));
        setFilter('all');
        pageContainer?.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function openModal(modalId) {
        const modal = document.getElementById(modalId);
        if (!modal) return;

        closeModal();
        modal.classList.add('is-open');
        modal.setAttribute('aria-hidden', 'false');
        document.body.classList.add('modal-open');
        activeModal = modal;
    }

    function closeModal() {
        if (!activeModal) return;

        activeModal.classList.remove('is-open');
        activeModal.setAttribute('aria-hidden', 'true');
        document.body.classList.remove('modal-open');
        activeModal = null;
    }

    viewButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const card = e.target.closest('.alert-card');
            if (!card) return;

            const category = card.getAttribute('data-category');
            // Only show detailed analysis for anomaly and schema categories
            if (category !== 'anomaly' && category !== 'schema') {
                alert('Detailed analysis view is currently only available for Anomaly and Schema events.');
                return;
            }

            // Set active panel based on category
            document.querySelectorAll('.detail-panel').forEach(p => p.classList.remove('active-panel'));
            if (category === 'anomaly') {
                document.getElementById('alert-detail-panel').classList.add('active-panel');
            } else if (category === 'schema') {
                document.getElementById('schema-detail-panel').classList.add('active-panel');
            }

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

    if (closeSchemaBtn) {
        closeSchemaBtn.addEventListener('click', () => {
            if (!expandedCard) return;
            closeExpanded();
        });
    }

    function closeExpanded(onComplete) {
        if (!expandedCard) {
            onComplete?.();
            return;
        }

        const card = expandedCard;
        
        // 1. Get current (expanded) position
        const firstRect = card.getBoundingClientRect();
        
        // 2. Clear state temporarily to find the original grid position
        document.body.classList.remove('view-mode-active');
        card.classList.remove('expanded');
        
        // Force layout recalculation
        const lastRect = card.getBoundingClientRect();
        
        // 3. INVERT: Calculate the delta and instantly move card to where it WAS (expanded)
        const dy = firstRect.top - lastRect.top;
        const dx = firstRect.left - lastRect.left;
        
        card.style.transition = 'none';
        card.style.transform = `translate(${dx}px, ${dy}px)`;
        card.style.zIndex = '50';
        
        // 4. PLAY: Reset the transform so it slides back to its natural grid position
        requestAnimationFrame(() => {
            card.style.transition = 'transform 0.5s cubic-bezier(0.2, 0.8, 0.2, 1)';
            card.style.transform = 'translate(0, 0)';
            
            setTimeout(() => {
                card.style.transition = '';
                card.style.transform = '';
                card.style.zIndex = '';
                expandedCard = null;
                onComplete?.();
            }, 500);
        });
    }

    if (alertNavLink) {
        alertNavLink.addEventListener('click', (e) => {
            e.preventDefault();
            closeExpanded(resetAlertsView);
        });
    }

    modalTriggers.forEach(trigger => {
        trigger.addEventListener('click', (e) => {
            e.preventDefault();
            openModal(trigger.getAttribute('data-modal-target'));
        });
    });

    modalCloseButtons.forEach(button => {
        button.addEventListener('click', () => {
            closeModal();
        });
    });

    modals.forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeModal();
            }
        });
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeModal();
        }
    });

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Close any expanded card first
            if (expandedCard) closeExpanded();
            setFilter(tab.getAttribute('data-filter'));
        });
    });
});
