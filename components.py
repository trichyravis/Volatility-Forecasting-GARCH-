
"""
═══════════════════════════════════════════════════════════════════════════════
STREAMLIT PROFESSIONAL DESIGN TEMPLATE - COMPONENTS
═══════════════════════════════════════════════════════════════════════════════

Pre-built, reusable UI components.
Use these to build your app faster!

Usage:
    from components import HeroHeader, SidebarNavigation, MetricsDisplay, Footer
    
    HeroHeader.render(...)
    SidebarNavigation.render(...)
"""

import streamlit as st
from typing import List, Dict, Optional, Callable
from styles import get_hero_header_html, get_metric_card_html, get_footer_html
from config import COLORS, SIDEBAR_CONFIG, SPACING

# ═══════════════════════════════════════════════════════════════════════════════
# HERO HEADER COMPONENT
# ═══════════════════════════════════════════════════════════════════════════════

class HeroHeader:
    """
    Professional hero header with emoji and text
    
    Usage:
        HeroHeader.render(
            title="YOUR APP TITLE",
            subtitle="Your subtitle",
            description="Your description",
            emoji="📊"
        )
    """
    
    @staticmethod
    def render(
        title: str,
        subtitle: str,
        description: str,
        emoji: str = "🏔️"
    ):
        """Render hero header"""
        st.markdown(
            get_hero_header_html(title, subtitle, description, emoji),
            unsafe_allow_html=True
        )
        st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR NAVIGATION COMPONENT
# ═══════════════════════════════════════════════════════════════════════════════

class SidebarNavigation:
    """
    Professional sidebar navigation with custom styling
    
    Usage:
        selected_mode = SidebarNavigation.render(
            title="SELECT MODE",
            options=["Option 1", "Option 2", "Option 3"],
            description="Choose your analysis mode"
        )
    """
    
    @staticmethod
    def render(
        title: str,
        options: List[str],
        description: str = "",
        help_text: str = ""
    ) -> str:
        """
        Render sidebar navigation with radio buttons
        
        Returns:
            Selected option
        """
        with st.sidebar:
            st.markdown("---")
            st.write(f"### 📊 {title}")
            if description:
                st.write(description)
            st.markdown("---")
            
            selected = st.radio(
                "**Select Option:**",
                options=options,
                help=help_text if help_text else None
            )
            
            st.markdown("---")
            return selected
    
    @staticmethod
    def render_section(title: str, content: str):
        """Render sidebar section with content"""
        with st.sidebar:
            st.markdown("---")
            st.write(f"**{title}**")
            st.write(content)
            st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════════
# METRICS DISPLAY COMPONENT
# ═══════════════════════════════════════════════════════════════════════════════

class MetricsDisplay:
    """
    Display metrics in a grid layout with professional styling
    
    Usage:
        MetricsDisplay.render_metrics([
            {"title": "Metric 1", "value": "100", "emoji": "📊"},
            {"title": "Metric 2", "value": "95", "emoji": "📈"},
            {"title": "Metric 3", "value": "85", "emoji": "⭐", "highlight": True},
        ])
    """
    
    @staticmethod
    def render_metrics(
        metrics: List[Dict],
        columns: int = 5,
        title: str = "METRICS"
    ):
        """
        Render metrics in a grid
        
        Args:
            metrics: List of dicts with keys: title, value, emoji, description, highlight
            columns: Number of columns
            title: Section title
        """
        if title:
            st.markdown(f"### 🎯 {title}")
        
        cols = st.columns(columns)
        
        for idx, metric in enumerate(metrics):
            with cols[idx % columns]:
                st.markdown(
                    get_metric_card_html(
                        title=metric.get("title", ""),
                        value=metric.get("value", ""),
                        description=metric.get("description", ""),
                        emoji=metric.get("emoji", "📊"),
                        highlight=metric.get("highlight", False)
                    ),
                    unsafe_allow_html=True
                )
    
    @staticmethod
    def render_single_metric(title: str, value: str, description: str = ""):
        """Render a single metric"""
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(
                f"""
                <div style="
                    background: linear-gradient(135deg, #003d70 0%, #005a9d 100%);
                    padding: 2rem;
                    border-radius: 15px;
                    text-align: center;
                    color: white;
                ">
                    <h3 style="color: white; margin: 0;">{title}</h3>
                    <h1 style="color: {COLORS['accent_gold']}; margin: 0.5rem 0;">{value}</h1>
                    <p style="color: white; margin: 0; font-size: 12px;">{description}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

# ═══════════════════════════════════════════════════════════════════════════════
# TABS COMPONENT
# ═══════════════════════════════════════════════════════════════════════════════

class TabsDisplay:
    """
    Professional tabs display component
    
    Usage:
        TabsDisplay.render({
            "Tab 1": lambda: st.write("Content 1"),
            "Tab 2": lambda: st.write("Content 2"),
            "Tab 3": lambda: st.write("Content 3"),
        })
    """
    
    @staticmethod
    def render(
        tabs: Dict[str, Callable],
        title: str = ""
    ):
        """
        Render tabs
        
        Args:
            tabs: Dict with tab_name: render_function
            title: Section title
        """
        if title:
            st.markdown(f"### {title}")
        
        tab_list = list(tabs.keys())
        tab_objects = st.tabs(tab_list)
        
        for tab_obj, tab_name in zip(tab_objects, tab_list):
            with tab_obj:
                tabs[tab_name]()

# ═══════════════════════════════════════════════════════════════════════════════
# CARD COMPONENT
# ═══════════════════════════════════════════════════════════════════════════════

class CardDisplay:
    """
    Professional card display component
    
    Usage:
        CardDisplay.render_card(
            title="Card Title",
            content="Card content",
            icon="📊"
        )
    """
    
    @staticmethod
    def render_card(
        title: str,
        content: str,
        icon: str = "📊",
        highlight: bool = False
    ):
        """Render a single card"""
        if highlight:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #003d70 0%, #005a9d 100%);
                border: 2px solid {COLORS['accent_gold']};
                padding: 1.5rem;
                border-radius: 15px;
                color: white;
            ">
                <h3 style="color: white; margin-top: 0;">{icon} {title}</h3>
                <p style="color: white;">{content}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #003d70 0%, #005a9d 100%);
                padding: 1.5rem;
                border-radius: 15px;
                color: white;
            ">
                <h3 style="color: white; margin-top: 0;">{icon} {title}</h3>
                <p style="color: white;">{content}</p>
            </div>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def render_cards_grid(
        cards: List[Dict],
        columns: int = 3,
        title: str = ""
    ):
        """
        Render multiple cards in a grid
        
        Args:
            cards: List of dicts with title, content, icon
            columns: Number of columns
            title: Section title
        """
        if title:
            st.markdown(f"### {title}")
        
        cols = st.columns(columns)
        
        for idx, card in enumerate(cards):
            with cols[idx % columns]:
                CardDisplay.render_card(
                    title=card.get("title", ""),
                    content=card.get("content", ""),
                    icon=card.get("icon", "📊"),
                    highlight=card.get("highlight", False)
                )

# ═══════════════════════════════════════════════════════════════════════════════
# STATS COMPONENT
# ═══════════════════════════════════════════════════════════════════════════════

class StatsDisplay:
    """
    Display key statistics with styling
    
    Usage:
        StatsDisplay.render([
            {"label": "Total Users", "value": "1,234"},
            {"label": "Active Sessions", "value": "567"},
        ])
    """
    
    @staticmethod
    def render(stats: List[Dict], columns: int = 4):
        """Render statistics"""
        cols = st.columns(columns)
        
        for idx, stat in enumerate(stats):
            with cols[idx % columns]:
                st.metric(
                    label=stat.get("label", ""),
                    value=stat.get("value", ""),
                    delta=stat.get("delta"),
                    help=stat.get("help")
                )

# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER COMPONENT
# ═══════════════════════════════════════════════════════════════════════════════

class Footer:
    """
    Premium footer component with enhanced design styling
    Improved layout, spacing, typography, and visual hierarchy
    """
    
    @staticmethod
    def render(
        title: str,
        description: str,
        author: str,
        social_links: Optional[Dict[str, str]] = None,
        disclaimer: str = ""
    ):
        """Render premium footer with enhanced design"""
        
        # Apply premium CSS styling
        st.markdown("""
        <style>
        
        /* FOOTER CONTAINER */
        .footer-wrapper {
            background: linear-gradient(180deg, rgba(0, 51, 102, 0.02) 0%, rgba(0, 77, 128, 0.03) 100%);
            padding: 3rem 2rem;
            margin-top: 4rem;
            border-top: 3px solid #003366;
            border-bottom: 1px solid #e0e0e0;
        }
        
        .footer-content {
            max-width: 900px;
            margin: 0 auto;
            text-align: center;
        }
        
        /* TITLE SECTION */
        .footer-title-section {
            margin-bottom: 1.5rem;
        }
        
        .footer-main-title {
            color: #003366;
            font-size: 26px;
            font-weight: 900;
            margin: 0 0 0.3rem 0;
            letter-spacing: 1px;
            text-transform: uppercase;
            word-spacing: 0.1em;
        }
        
        .footer-subtitle {
            color: #0077b5;
            font-size: 15px;
            font-weight: 600;
            margin: 0.3rem 0 0 0;
            letter-spacing: 0.5px;
        }
        
        .footer-author {
            color: #666;
            font-size: 13px;
            margin: 0.8rem 0 0 0;
            font-weight: 500;
        }
        
        /* BUTTONS SECTION - PREMIUM STYLING */
        .footer-buttons-wrapper {
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin: 2rem 0;
            flex-wrap: wrap;
        }
        
        .footer-button {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 0.75rem 2rem;
            border-radius: 8px;
            color: white;
            text-decoration: none;
            font-weight: 700;
            font-size: 15px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            border: none;
            cursor: pointer;
            white-space: nowrap;
            position: relative;
            overflow: hidden;
        }
        
        .footer-button::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }
        
        .footer-button:hover::before {
            width: 300px;
            height: 300px;
        }
        
        .footer-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        }
        
        .footer-button:active {
            transform: translateY(-1px);
        }
        
        .footer-button-linkedin {
            background: linear-gradient(135deg, #0077b5 0%, #00a0d2 100%);
        }
        
        .footer-button-linkedin:hover {
            background: linear-gradient(135deg, #005a87 0%, #0077b5 100%);
        }
        
        .footer-button-github {
            background: linear-gradient(135deg, #2d2d2d 0%, #434343 100%);
        }
        
        .footer-button-github:hover {
            background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        }
        
        .footer-button-email {
            background: linear-gradient(135deg, #0077b5 0%, #00a0d2 100%);
        }
        
        .footer-button-email:hover {
            background: linear-gradient(135deg, #005a87 0%, #0077b5 100%);
        }
        
        .footer-button span {
            position: relative;
            z-index: 1;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        /* DISCLAIMER SECTION - ENHANCED */
        .footer-disclaimer-wrapper {
            margin: 2rem 0;
        }
        
        .footer-disclaimer {
            background: linear-gradient(135deg, #fffbea 0%, #fff8dc 100%);
            border: 2px solid #ffc107;
            border-radius: 12px;
            padding: 1.25rem 1.5rem;
            font-size: 13px;
            color: #333;
            line-height: 1.6;
            text-align: center;
            box-shadow: 0 2px 8px rgba(255, 193, 7, 0.15);
            font-weight: 500;
        }
        
        .footer-disclaimer-title {
            font-weight: 700;
            color: #d9a90a;
            margin-bottom: 0.5rem;
            font-size: 14px;
        }
        
        /* DIVIDER */
        .footer-divider {
            height: 1px;
            background: linear-gradient(90deg, transparent 0%, #003366 50%, transparent 100%);
            margin: 2rem 0;
        }
        
        /* FOOTER CREDIT SECTION */
        .footer-credit-section {
            margin-top: 2rem;
        }
        
        .footer-copyright {
            color: #777;
            font-size: 12px;
            margin: 0.5rem 0;
            font-weight: 500;
            letter-spacing: 0.3px;
        }
        
        .footer-credit {
            color: #999;
            font-size: 12px;
            margin: 0.5rem 0 0 0;
            font-style: italic;
            font-weight: 400;
        }
        
        /* PREMIUM BORDER TOP */
        .footer-top-border {
            height: 3px;
            background: linear-gradient(90deg, #003366 0%, #0077b5 50%, #003366 100%);
            margin-bottom: 2rem;
            border-radius: 2px;
        }
        
        /* RESPONSIVE */
        @media (max-width: 768px) {
            .footer-wrapper {
                padding: 2rem 1rem;
            }
            
            .footer-main-title {
                font-size: 22px;
                letter-spacing: 0.5px;
            }
            
            .footer-subtitle {
                font-size: 14px;
            }
            
            .footer-button {
                padding: 0.65rem 1.5rem;
                font-size: 13px;
            }
            
            .footer-buttons-wrapper {
                gap: 0.75rem;
            }
        }
        
        @media (max-width: 480px) {
            .footer-wrapper {
                padding: 1.5rem 1rem;
                margin-top: 2rem;
            }
            
            .footer-main-title {
                font-size: 18px;
                letter-spacing: 0px;
                word-spacing: 0em;
            }
            
            .footer-subtitle {
                font-size: 13px;
            }
            
            .footer-author {
                font-size: 12px;
            }
            
            .footer-button {
                padding: 0.6rem 1.2rem;
                font-size: 12px;
            }
            
            .footer-buttons-wrapper {
                gap: 0.5rem;
                margin: 1.5rem 0;
            }
            
            .footer-disclaimer {
                padding: 1rem;
                font-size: 12px;
            }
        }
        
        </style>
        """, unsafe_allow_html=True)
        
        # RENDER FOOTER STRUCTURE
        st.markdown('<div class="footer-wrapper">', unsafe_allow_html=True)
        st.markdown('<div class="footer-content">', unsafe_allow_html=True)
        
        # TOP DECORATIVE BORDER
        st.markdown('<div class="footer-top-border"></div>', unsafe_allow_html=True)
        
        # TITLE SECTION
        st.markdown('<div class="footer-title-section">', unsafe_allow_html=True)
        st.markdown(f'<p class="footer-main-title">{title}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="footer-subtitle">{description}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="footer-author">{author}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # SOCIAL BUTTONS
        if social_links:
            st.markdown('<div class="footer-buttons-wrapper">', unsafe_allow_html=True)
            
            for name, url in social_links.items():
                if name == "LinkedIn":
                    emoji = "🔗"
                    css_class = "footer-button footer-button-linkedin"
                elif name == "GitHub":
                    emoji = "🐙"
                    css_class = "footer-button footer-button-github"
                else:
                    emoji = "📧"
                    css_class = "footer-button footer-button-email"
                
                st.markdown(
                    f'<a href="{url}" target="_blank" class="{css_class}"><span>{emoji} {name}</span></a>',
                    unsafe_allow_html=True
                )
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # DIVIDER
        st.markdown('<div class="footer-divider"></div>', unsafe_allow_html=True)
        
        # DISCLAIMER
        if disclaimer:
            st.markdown('<div class="footer-disclaimer-wrapper">', unsafe_allow_html=True)
            st.markdown(f'<div class="footer-disclaimer"><div class="footer-disclaimer-title">⚠️ DISCLAIMER:</div>{disclaimer}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # CREDIT SECTION
        st.markdown('<div class="footer-credit-section">', unsafe_allow_html=True)
        st.markdown('<p class="footer-copyright">© 2025 The Mountain Path - World of Finance | All Rights Reserved</p>', unsafe_allow_html=True)
        st.markdown('<p class="footer-credit">Built with ❤️ using Streamlit, GARCH & EGARCH Models</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # CLOSE CONTAINERS
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# EXPANDER COMPONENT (ENHANCED)
# ═══════════════════════════════════════════════════════════════════════════════

class ExpanderSection:
    """
    Professional expander section component
    
    Usage:
        with ExpanderSection.render("Section Title"):
            st.write("Content here")
    """
    
    @staticmethod
    def render(title: str, icon: str = "📌"):
        """Render expander section"""
        return st.expander(f"{icon} {title}")

# ═══════════════════════════════════════════════════════════════════════════════
# DATA TABLE COMPONENT
# ═══════════════════════════════════════════════════════════════════════════════

class DataDisplay:
    """
    Display data in professional tables
    
    Usage:
        DataDisplay.render_table(dataframe, title="Data Table")
    """
    
    @staticmethod
    def render_table(data, title: str = "", use_container_width: bool = True):
        """Render data table"""
        if title:
            st.markdown(f"### 📊 {title}")
        
        st.dataframe(data, use_container_width=use_container_width)
    
    @staticmethod
    def render_metric_table(
        data: List[Dict],
        title: str = "",
        color_scheme: Dict = None
    ):
        """Render metrics table with custom colors"""
        if title:
            st.markdown(f"### 📊 {title}")
        
        import pandas as pd
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# HOW TO USE THESE COMPONENTS
# ═══════════════════════════════════════════════════════════════════════════════

"""
QUICK START:

1. Basic setup:
   import streamlit as st
   from styles import apply_main_styles
   from components import HeroHeader, SidebarNavigation, MetricsDisplay, Footer
   
   st.set_page_config(...)
   apply_main_styles()
   
   # Render hero header
   HeroHeader.render(
       title="YOUR APP",
       subtitle="Subtitle",
       description="Description",
       emoji="📊"
   )

2. Sidebar navigation:
   mode = SidebarNavigation.render(
       title="NAVIGATION",
       options=["Option 1", "Option 2"],
       description="Choose an option"
   )
   
   SidebarNavigation.render_section(
       title="About",
       content="Your content here"
   )

3. Display metrics:
   MetricsDisplay.render_metrics([
       {"title": "Metric 1", "value": "100/100", "emoji": "📊"},
       {"title": "Metric 2", "value": "95/100", "emoji": "📈"},
       {"title": "Metric 3", "value": "85/100", "emoji": "⭐", "highlight": True},
   ])

4. Tabs:
   TabsDisplay.render({
       "Tab 1": lambda: st.write("Content 1"),
       "Tab 2": lambda: st.write("Content 2"),
   })

5. Cards:
   CardDisplay.render_cards_grid([
       {"title": "Card 1", "content": "Content", "icon": "📊"},
       {"title": "Card 2", "content": "Content", "icon": "📈"},
   ], columns=2)

6. Footer:
   Footer.render(
       title="YOUR APP",
       description="Description",
       author="Your Name",
       social_links={"LinkedIn": "url", "GitHub": "url"},
       disclaimer="Your disclaimer"
   )

All components are automatically styled from config.py!
"""
