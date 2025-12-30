
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
    Simple, clean, professional footer component
    Minimal design - no fancy effects
    """
    
    @staticmethod
    def render(
        title: str,
        description: str,
        author: str,
        social_links: Optional[Dict[str, str]] = None,
        disclaimer: str = ""
    ):
        """Render simple, clean footer"""
        
        # Simple CSS - minimal styling
        st.markdown("""
        <style>
        .footer-simple {
            text-align: center;
            padding: 2rem 1rem;
            margin-top: 3rem;
        }
        
        .footer-title {
            color: #003366;
            font-size: 22px;
            font-weight: 700;
            margin: 0 0 0.3rem 0;
            letter-spacing: 0.5px;
        }
        
        .footer-subtitle {
            color: #0077b5;
            font-size: 14px;
            font-weight: 500;
            margin: 0.3rem 0 0 0;
        }
        
        .footer-author {
            color: #666;
            font-size: 13px;
            margin: 0.8rem 0 1.5rem 0;
        }
        
        .footer-buttons {
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin: 1.5rem 0;
            flex-wrap: wrap;
        }
        
        .footer-btn {
            display: inline-block;
            padding: 0.6rem 1.5rem;
            border-radius: 6px;
            color: white;
            text-decoration: none;
            font-weight: 600;
            font-size: 14px;
            transition: all 0.2s;
            border: none;
            cursor: pointer;
        }
        
        .footer-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }
        
        .btn-linkedin {
            background: #0077b5;
        }
        
        .btn-linkedin:hover {
            background: #005a87;
        }
        
        .btn-github {
            background: #2d2d2d;
        }
        
        .btn-github:hover {
            background: #1a1a1a;
        }
        
        .footer-disclaimer {
            background: #fff8dc;
            border: 2px solid #ffc107;
            border-radius: 8px;
            padding: 1rem;
            margin: 1.5rem 0;
            font-size: 12px;
            color: #333;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }
        
        .footer-divider {
            height: 1px;
            background: #e0e0e0;
            margin: 1.5rem 0;
        }
        
        .footer-copyright {
            color: #999;
            font-size: 12px;
            margin: 1rem 0 0.3rem 0;
        }
        
        .footer-credit {
            color: #aaa;
            font-size: 12px;
            margin: 0.3rem 0;
            font-style: italic;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Render
        st.markdown('<div class="footer-simple">', unsafe_allow_html=True)
        
        # Title section
        st.markdown(f'<p class="footer-title">{title}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="footer-subtitle">{description}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="footer-author">{author}</p>', unsafe_allow_html=True)
        
        # Buttons
        if social_links:
            st.markdown('<div class="footer-buttons">', unsafe_allow_html=True)
            
            for name, url in social_links.items():
                if name == "LinkedIn":
                    emoji = "🔗"
                    btn_class = "footer-btn btn-linkedin"
                elif name == "GitHub":
                    emoji = "🐙"
                    btn_class = "footer-btn btn-github"
                else:
                    emoji = "📧"
                    btn_class = "footer-btn btn-linkedin"
                
                st.markdown(
                    f'<a href="{url}" target="_blank" class="{btn_class}">{emoji} {name}</a>',
                    unsafe_allow_html=True
                )
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Divider
        st.markdown('<div class="footer-divider"></div>', unsafe_allow_html=True)
        
        # Disclaimer
        if disclaimer:
            st.markdown(
                f'<div class="footer-disclaimer"><strong>⚠️ DISCLAIMER:</strong> {disclaimer}</div>',
                unsafe_allow_html=True
            )
        
        # Copyright
        st.markdown('<p class="footer-copyright">© 2025 The Mountain Path - World of Finance | All Rights Reserved</p>', unsafe_allow_html=True)
        st.markdown('<p class="footer-credit">Built with ❤️ using Streamlit, GARCH & EGARCH Models</p>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)


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
