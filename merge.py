import sys

def build():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update navigation to use # and data attributes for toggling
    # We replace any href="insights.html" in sidebar
    content = content.replace('<a href="insights.html" class="nav-item">', '<a href="#" class="nav-item" data-nav="insights">')
    content = content.replace('<a href="index.html" class="nav-item active" data-nav="alerts">', '<a href="#" class="nav-item active" data-nav="alerts">')
    content = content.replace('<a href="index.html" class="nav-item" data-nav="alerts">', '<a href="#" class="nav-item" data-nav="alerts">')

    # Ensure Insights tab has data-nav="insights" if it was original
    content = content.replace('<a href="#" class="nav-item">\n                    <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"\n                        stroke-linecap="round" stroke-linejoin="round">\n                        <line x1="18" y1="20" x2="18" y2="10"></line>\n                        <line x1="12" y1="20" x2="12" y2="4"></line>\n                        <line x1="6" y1="20" x2="6" y2="14"></line>\n                    </svg>\n                    <span>Insights</span>\n                </a>', 
                              '<a href="#" class="nav-item" data-nav="insights">\n                    <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"\n                        stroke-linecap="round" stroke-linejoin="round">\n                        <line x1="18" y1="20" x2="18" y2="10"></line>\n                        <line x1="12" y1="20" x2="12" y2="4"></line>\n                        <line x1="6" y1="20" x2="6" y2="14"></line>\n                    </svg>\n                    <span>Insights</span>\n                </a>')

    # 2. Add IDs to the views
    content = content.replace('<div class="page-content">', '<div id="alerts-view" class="page-content">', 1)

    # 3. We need to close alerts-view and inject insights-view.
    # Where does alerts-view end? It's inside page-container. 
    # Let's search for "</div>\n            </div>\n\n            <div id=\"schema-accept-modal" or similar.
    # Actually, we can use a known marker. 
    # Alerts view ends when page-container ends. 
    # The last element inside page-content is usually the cards-list or detail panels.
    # Let's search for the end of schema-detail-panel.
    
    # "</div>\n                        </div>\n\n                    <!-- Schema Detail Panel (Starts Hidden) -->"
    
    # Let's just find the closing tag corresponding to page-content. It's difficult with regex.
    # But wait, modal overlays start with `<div id="...modal" class="modal-overlay"`. These are outside page-container?
    # Let's look at index.html content again. 
    marker = '<div id="accept-modal" class="modal-overlay"'
    if marker not in content:
        marker = '<div id="reject-modal" class="modal-overlay"'
        
    idx = content.find(marker)
    
    # Walk backwards to find the closing div of page-content and page-container
    # index.html structure at the end:
    # </div> (page-content)
    # </div> (page-container)
    # <div id="reject-modal" ...
    
    insert_idx = content.rfind('</div>\n            </div>', 0, idx)
    
    if insert_idx == -1:
        print("Cannot find insertion point.")
        return

    insights_html = """
                <div id="insights-view" class="page-content" style="display: none;">
                    
                    <!-- Top KPIs -->
                    <div class="brief-title" style="margin-top: 10px; margin-bottom: 24px;">
                        <h2 style="color: #0f172a; font-size: 22px;">Key metrics</h2>
                    </div>
                    <div class="kpi-container" style="gap: 20px;">
                        <!-- KPI 1 -->
                        <div class="kpi-card" style="border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); padding: 24px 24px 0 24px; border: 1px solid #e2e8f0; display: flex; flex-direction: column; min-height: 150px; overflow: hidden; padding-bottom: 0;">
                            <div style="flex: 1;">
                                <div style="display: flex; justify-content: space-between; align-items:center;">
                                    <div class="kpi-label" style="font-size: 14px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px;">Total Revenue</div>
                                    <div class="badge" style="background-color: #ecfdf5; color: #10b981; border: 1px solid #a7f3d0; font-size: 13px; font-weight: 700; padding: 4px 10px;">↑ 18%</div>
                                </div>
                                <div class="kpi-value" style="font-size: 38px; color: #0f172a; font-weight: 800; margin-top: 12px;">$1.1M</div>
                            </div>
                            <svg viewBox="0 0 100 30" preserveAspectRatio="none" style="width: calc(100% + 48px); margin-left: -24px; height: 40px; margin-top: 16px; margin-bottom: -5px;">
                                <path d="M0 30 Q 20 15, 40 25 T 80 15 T 100 5 L 100 40 L 0 40 Z" fill="url(#grad-green)" opacity="0.2"></path>
                                <path d="M0 30 Q 20 15, 40 25 T 80 15 T 100 5" fill="none" stroke="#10b981" stroke-width="2.5"></path>
                                <defs>
                                    <linearGradient id="grad-green" x1="0" x2="0" y1="0" y2="1">
                                        <stop offset="0%" stop-color="#10b981" stop-opacity="1"/>
                                        <stop offset="100%" stop-color="#10b981" stop-opacity="0"/>
                                    </linearGradient>
                                </defs>
                            </svg>
                        </div>
                        
                        <!-- KPI 2 -->
                        <div class="kpi-card" style="border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); padding: 24px 24px 0 24px; border: 1px solid #e2e8f0; display: flex; flex-direction: column; min-height: 150px; overflow: hidden; padding-bottom: 0;">
                            <div style="flex: 1;">
                                <div style="display: flex; justify-content: space-between; align-items:center;">
                                    <div class="kpi-label" style="font-size: 14px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px;">Promotion Impact</div>
                                    <div class="badge" style="background-color: #ecfdf5; color: #10b981; border: 1px solid #a7f3d0; font-size: 13px; font-weight: 700; padding: 4px 10px;">↑ 6.8%</div>
                                </div>
                                <div class="kpi-value" style="font-size: 38px; color: #0f172a; font-weight: 800; margin-top: 12px;">42.5%</div>
                            </div>
                            <svg viewBox="0 0 100 30" preserveAspectRatio="none" style="width: calc(100% + 48px); margin-left: -24px; height: 40px; margin-top: 16px; margin-bottom: -5px;">
                                <path d="M0 25 Q 15 15, 30 20 T 60 10 T 100 5 L 100 40 L 0 40 Z" fill="url(#grad-green2)" opacity="0.2"></path>
                                <path d="M0 25 Q 15 15, 30 20 T 60 10 T 100 5" fill="none" stroke="#10b981" stroke-width="2.5"></path>
                                <defs>
                                    <linearGradient id="grad-green2" x1="0" x2="0" y1="0" y2="1">
                                        <stop offset="0%" stop-color="#10b981" stop-opacity="1"/>
                                        <stop offset="100%" stop-color="#10b981" stop-opacity="0"/>
                                    </linearGradient>
                                </defs>
                            </svg>
                        </div>
                        
                        <!-- KPI 3 -->
                        <div class="kpi-card" style="border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); padding: 24px 24px 0 24px; border: 1px solid #e2e8f0; display: flex; flex-direction: column; min-height: 150px; overflow: hidden; padding-bottom: 0;">
                            <div style="flex: 1;">
                                <div style="display: flex; justify-content: space-between; align-items:center;">
                                    <div class="kpi-label" style="font-size: 14px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px;">HCP Engagement</div>
                                    <div class="badge" style="background-color: #ecfdf5; color: #10b981; border: 1px solid #a7f3d0; font-size: 13px; font-weight: 700; padding: 4px 10px;">↑ 9.5%</div>
                                </div>
                                <div class="kpi-value" style="font-size: 38px; color: #0f172a; font-weight: 800; margin-top: 12px;">9,200</div>
                            </div>
                            <svg viewBox="0 0 100 30" preserveAspectRatio="none" style="width: calc(100% + 48px); margin-left: -24px; height: 40px; margin-top: 16px; margin-bottom: -5px;">
                                <path d="M0 28 Q 20 20, 50 15 T 100 5 L 100 40 L 0 40 Z" fill="url(#grad-green3)" opacity="0.2"></path>
                                <path d="M0 28 Q 20 20, 50 15 T 100 5" fill="none" stroke="#10b981" stroke-width="2.5"></path>
                                <defs>
                                    <linearGradient id="grad-green3" x1="0" x2="0" y1="0" y2="1">
                                        <stop offset="0%" stop-color="#10b981" stop-opacity="1"/>
                                        <stop offset="100%" stop-color="#10b981" stop-opacity="0"/>
                                    </linearGradient>
                                </defs>
                            </svg>
                        </div>
                        
                        <!-- KPI 4 -->
                        <div class="kpi-card" style="border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); padding: 24px 24px 0 24px; border: 1px solid #e2e8f0; display: flex; flex-direction: column; min-height: 150px; overflow: hidden; padding-bottom: 0;">
                            <div style="flex: 1;">
                                <div style="display: flex; justify-content: space-between; align-items:center;">
                                    <div class="kpi-label" style="font-size: 14px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px;">Pipeline Health</div>
                                    <div class="badge" style="background-color: #fef2f2; color: #ef4444; border: 1px solid #fecaca; font-size: 13px; font-weight: 700; padding: 4px 10px;">↓ -1.2%</div>
                                </div>
                                <div class="kpi-value" style="font-size: 38px; color: #0f172a; font-weight: 800; margin-top: 12px;">98.2%</div>
                            </div>
                            <svg viewBox="0 0 100 30" preserveAspectRatio="none" style="width: calc(100% + 48px); margin-left: -24px; height: 40px; margin-top: 16px; margin-bottom: -5px;">
                                <path d="M0 5 Q 30 10, 60 20 T 100 28 L 100 40 L 0 40 Z" fill="url(#grad-red)" opacity="0.15"></path>
                                <path d="M0 5 Q 30 10, 60 20 T 100 28" fill="none" stroke="#ef4444" stroke-width="2.5"></path>
                                <defs>
                                    <linearGradient id="grad-red" x1="0" x2="0" y1="0" y2="1">
                                        <stop offset="0%" stop-color="#ef4444" stop-opacity="1"/>
                                        <stop offset="100%" stop-color="#ef4444" stop-opacity="0"/>
                                    </linearGradient>
                                </defs>
                            </svg>
                        </div>
                    </div>

                    <!-- AI Insights List -->
                    <div class="brief-title" style="margin-top: 32px; margin-bottom: 24px; align-items: center; display: flex; gap: 10px;">
                        <div style="width: 4px; height: 20px; background-color: #10b981; border-radius: 2px;"></div>
                        <h2 style="color: #0f172a; font-size: 18px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin: 0;">AI-Generated Insights</h2>
                    </div>

                    <div class="cards-list" style="gap: 20px;">
                        <!-- Insight 1 -->
                        <div class="alert-card" style="box-shadow: 0 2px 6px rgba(0,0,0,0.04); border-radius: 12px; overflow: hidden; border: 1px solid #e2e8f0; display: flex; transition: transform 0.2s, box-shadow 0.2s; cursor: default; background: #fff;">
                            <div class="card-accent" style="width: 6px; background-color: #ef4444; flex-shrink: 0;"></div>
                            <div class="card-inner" style="padding: 24px 32px; width: 100%; display: flex; flex-direction: column; gap: 8px;">
                                <div style="display: flex; gap: 10px; align-items: center; margin-bottom: 2px;">
                                    <span class="badge" style="background-color: #334155; color: white; padding: 6px 12px; font-size: 12px; font-weight: 600; border-radius: 20px;">Sales driver</span>
                                    <span class="badge" style="background-color: #fee2e2; color: #ef4444; padding: 4px 12px; font-size: 12px; font-weight: 600; border-radius: 20px; border: 1px solid #fecaca;">Critical</span>
                                </div>
                                <h3 style="font-size: 22px; font-weight: 700; margin: 8px 0; color: #0f172a;">New Promotional Channel Impact</h3>
                                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px; font-size: 15px; color: #15803d;">
                                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle></svg>
                                    <span style="font-weight: 600;">Promotion module</span>
                                </div>
                                <div style="font-size: 16px; color: #475569; line-height: 1.6; margin-bottom: 24px;">
                                    The introduction of the SAMPLES channel has emerged as the primary driver of the uplift in sales value, expanding promotional coverage.
                                </div>
                                <div style="border-top: 1px solid #f1f5f9; padding-top: 16px;">
                                    <a href="#" style="color: #15803d; font-weight: 700; font-size: 15px; text-decoration: none; display: flex; align-items: center; gap: 8px; width: fit-content; transition: color 0.2s;">
                                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                                        Deep dive
                                    </a>
                                </div>
                            </div>
                        </div>

                        <!-- Insight 2 -->
                        <div class="alert-card" style="box-shadow: 0 2px 6px rgba(0,0,0,0.04); border-radius: 12px; overflow: hidden; border: 1px solid #e2e8f0; display: flex; transition: transform 0.2s, box-shadow 0.2s; cursor: default; background: #fff;">
                            <div class="card-accent" style="width: 6px; background-color: #f59e0b; flex-shrink: 0;"></div>
                            <div class="card-inner" style="padding: 24px 32px; width: 100%; display: flex; flex-direction: column; gap: 8px;">
                                <div style="display: flex; gap: 10px; align-items: center; margin-bottom: 2px;">
                                    <span class="badge" style="background-color: #334155; color: white; padding: 6px 12px; font-size: 12px; font-weight: 600; border-radius: 20px;">Engagement trend</span>
                                    <span class="badge" style="background-color: #fef3c7; color: #d97706; padding: 4px 12px; font-size: 12px; font-weight: 600; border-radius: 20px; border: 1px solid #fde68a;">High</span>
                                </div>
                                <h3 style="font-size: 22px; font-weight: 700; margin: 8px 0; color: #0f172a;">Increased Activity in Existing Channels</h3>
                                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px; font-size: 15px; color: #047857;">
                                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle></svg>
                                    <span style="font-weight: 600;">HCP engagement</span>
                                </div>
                                <div style="font-size: 16px; color: #475569; line-height: 1.6; margin-bottom: 24px;">
                                    Higher activity across existing promotional channels—particularly increased call frequency—has enhanced HCP engagement and contributed to sales growth.
                                </div>
                                <div style="border-top: 1px solid #f1f5f9; padding-top: 16px;">
                                    <a href="#" style="color: #047857; font-weight: 700; font-size: 15px; text-decoration: none; display: flex; align-items: center; gap: 8px; width: fit-content; transition: color 0.2s;">
                                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                                        Deep dive
                                    </a>
                                </div>
                            </div>
                        </div>

                        <!-- Insight 3 -->
                        <div class="alert-card" style="box-shadow: 0 2px 6px rgba(0,0,0,0.04); border-radius: 12px; overflow: hidden; border: 1px solid #e2e8f0; display: flex; transition: transform 0.2s, box-shadow 0.2s; cursor: default; background: #fff;">
                            <div class="card-accent" style="width: 6px; background-color: #3b82f6; flex-shrink: 0;"></div>
                            <div class="card-inner" style="padding: 24px 32px; width: 100%; display: flex; flex-direction: column; gap: 8px;">
                                <div style="display: flex; gap: 10px; align-items: center; margin-bottom: 2px;">
                                    <span class="badge" style="background-color: #334155; color: white; padding: 6px 12px; font-size: 12px; font-weight: 600; border-radius: 20px;">Field effectiveness</span>
                                    <span class="badge" style="background-color: #f1f5f9; color: #475569; padding: 4px 12px; font-size: 12px; font-weight: 600; border-radius: 20px; border: 1px solid #e2e8f0;">Info</span>
                                </div>
                                <h3 style="font-size: 22px; font-weight: 700; margin: 8px 0; color: #0f172a;">Strengthened RTE Engagement</h3>
                                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px; font-size: 15px; color: #1d4ed8;">
                                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle></svg>
                                    <span style="font-weight: 600;">RTE module</span>
                                </div>
                                <div style="font-size: 16px; color: #475569; line-height: 1.6; margin-bottom: 24px;">
                                    An increase in RTE engagements has improved point‑of‑care interactions, strengthening HCP reach and supporting higher prescription generation.
                                </div>
                                <div style="border-top: 1px solid #f1f5f9; padding-top: 16px;">
                                    <a href="#" style="color: #1d4ed8; font-weight: 700; font-size: 15px; text-decoration: none; display: flex; align-items: center; gap: 8px; width: fit-content; transition: color 0.2s;">
                                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                                        Deep dive
                                    </a>
                                </div>
                            </div>
                        </div>

                        <!-- Insight 4 -->
                        <div class="alert-card" style="box-shadow: 0 2px 6px rgba(0,0,0,0.04); border-radius: 12px; overflow: hidden; border: 1px solid #e2e8f0; display: flex; transition: transform 0.2s, box-shadow 0.2s; cursor: default; background: #fff;">
                            <div class="card-accent" style="width: 6px; background-color: #3b82f6; flex-shrink: 0;"></div>
                            <div class="card-inner" style="padding: 24px 32px; width: 100%; display: flex; flex-direction: column; gap: 8px;">
                                <div style="display: flex; gap: 10px; align-items: center; margin-bottom: 2px;">
                                    <span class="badge" style="background-color: #334155; color: white; padding: 6px 12px; font-size: 12px; font-weight: 600; border-radius: 20px;">Market trend</span>
                                    <span class="badge" style="background-color: #f1f5f9; color: #475569; padding: 4px 12px; font-size: 12px; font-weight: 600; border-radius: 20px; border: 1px solid #e2e8f0;">Info</span>
                                </div>
                                <h3 style="font-size: 22px; font-weight: 700; margin: 8px 0; color: #0f172a;">Prescriber growth supporting sales</h3>
                                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px; font-size: 15px; color: #1d4ed8;">
                                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle></svg>
                                    <span style="font-weight: 600;">HCP segmentation</span>
                                </div>
                                <div style="font-size: 16px; color: #475569; line-height: 1.6; margin-bottom: 24px;">
                                    Rising prescription volumes from Segment D (low‑prescribing) HCPs, combined with favorable market conditions, have reinforced the overall sales uplift.
                                </div>
                                <div style="border-top: 1px solid #f1f5f9; padding-top: 16px;">
                                    <a href="#" style="color: #1d4ed8; font-weight: 700; font-size: 15px; text-decoration: none; display: flex; align-items: center; gap: 8px; width: fit-content; transition: color 0.2s;">
                                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                                        Deep dive
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
"""

    new_content = content[:insert_idx] + "</div>" + insights_html + content[insert_idx:]
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("re-written successfully")

build()
