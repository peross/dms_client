"""Modern UI styles for the DMS Client application."""

# Modern color scheme
COLORS = {
    'primary': '#2563eb',      # Blue
    'primary_hover': '#1d4ed8',
    'secondary': '#64748b',    # Gray
    'background': '#ffffff',
    'surface': '#f8fafc',
    'border': '#e2e8f0',
    'text_primary': '#0f172a',
    'text_secondary': '#64748b',
    'success': '#10b981',
    'warning': '#f59e0b',
    'error': '#ef4444',
    'hover': '#f1f5f9',
    'selected': '#dbeafe',
}


def get_modern_stylesheet():
    """Get the modern stylesheet for the application."""
    return f"""
    /* Main Window */
    QMainWindow {{
        background-color: {COLORS['background']};
    }}
    
    /* Menu Bar */
    QMenuBar {{
        background-color: {COLORS['surface']};
        border-bottom: 1px solid {COLORS['border']};
        padding: 4px;
        spacing: 4px;
    }}
    
    QMenuBar::item {{
        background-color: transparent;
        padding: 6px 12px;
        border-radius: 4px;
    }}
    
    QMenuBar::item:selected {{
        background-color: {COLORS['hover']};
    }}
    
    QMenuBar::item:pressed {{
        background-color: {COLORS['selected']};
    }}
    
    QMenu {{
        background-color: {COLORS['background']};
        border: 1px solid {COLORS['border']};
        border-radius: 6px;
        padding: 4px;
    }}
    
    QMenu::item {{
        padding: 8px 24px 8px 32px;
        border-radius: 4px;
    }}
    
    QMenu::item:selected {{
        background-color: {COLORS['selected']};
    }}
    
    QMenu::item:checked {{
        background-color: {COLORS['selected']};
    }}
    
    QMenu::separator {{
        height: 1px;
        background-color: {COLORS['border']};
        margin: 4px 8px;
    }}
    
    /* Status Bar */
    QStatusBar {{
        background-color: {COLORS['surface']};
        border-top: 1px solid {COLORS['border']};
        padding: 4px;
    }}
    
    /* Buttons */
    QPushButton {{
        background-color: {COLORS['primary']};
        color: white;
        border: none;
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: 500;
        min-width: 100px;
    }}
    
    QPushButton:hover {{
        background-color: {COLORS['primary_hover']};
    }}
    
    QPushButton:pressed {{
        background-color: {COLORS['primary_hover']};
    }}
    
    QPushButton:disabled {{
        background-color: {COLORS['border']};
        color: {COLORS['text_secondary']};
    }}
    
    QPushButton[styleClass="secondary"] {{
        background-color: {COLORS['surface']};
        color: {COLORS['text_primary']};
        border: 1px solid {COLORS['border']};
    }}
    
    QPushButton[styleClass="secondary"]:hover {{
        background-color: {COLORS['hover']};
    }}
    
    /* Line Edit (Text Input) */
    QLineEdit {{
        background-color: {COLORS['background']};
        border: 2px solid {COLORS['border']};
        border-radius: 6px;
        padding: 8px 12px;
        font-size: 14px;
        selection-background-color: {COLORS['selected']};
    }}
    
    QLineEdit:focus {{
        border-color: {COLORS['primary']};
    }}
    
    QLineEdit:disabled {{
        background-color: {COLORS['surface']};
        color: {COLORS['text_secondary']};
    }}
    
    /* Labels */
    QLabel {{
        color: {COLORS['text_primary']};
    }}
    
    QLabel[styleClass="heading"] {{
        font-size: 18px;
        font-weight: 600;
        color: {COLORS['text_primary']};
    }}
    
    QLabel[styleClass="subheading"] {{
        font-size: 14px;
        font-weight: 500;
        color: {COLORS['text_secondary']};
    }}
    
    QLabel[styleClass="muted"] {{
        color: {COLORS['text_secondary']};
    }}
    
    /* List View */
    QListView {{
        background-color: {COLORS['background']};
        border: 1px solid {COLORS['border']};
        border-radius: 6px;
        padding: 4px;
        outline: none;
    }}
    
    QListView::item {{
        padding: 8px;
        border-radius: 4px;
        margin: 2px;
    }}
    
    QListView::item:hover {{
        background-color: {COLORS['hover']};
    }}
    
    QListView::item:selected {{
        background-color: {COLORS['selected']};
        color: {COLORS['text_primary']};
    }}
    
    QListView::item:selected:active {{
        background-color: {COLORS['primary']};
        color: white;
    }}
    
    /* Tree View */
    QTreeView {{
        background-color: {COLORS['background']};
        border: 1px solid {COLORS['border']};
        border-radius: 6px;
        padding: 4px;
        outline: none;
        selection-background-color: {COLORS['selected']};
    }}
    
    QTreeView::item {{
        padding: 4px;
        border-radius: 4px;
    }}
    
    QTreeView::item:hover {{
        background-color: {COLORS['hover']};
    }}
    
    QTreeView::item:selected {{
        background-color: {COLORS['selected']};
    }}
    
    QTreeView::branch {{
        background-color: transparent;
    }}
    
    QTreeView::branch:has-siblings:!adjoins-item {{
        border-image: url(:/images/branch-vline.png) 0;
    }}
    
    QTreeView::branch:has-siblings:adjoins-item {{
        border-image: url(:/images/branch-more.png) 0;
    }}
    
    QTreeView::branch:!has-children:!has-siblings:adjoins-item {{
        border-image: url(:/images/branch-end.png) 0;
    }}
    
    QTreeView::branch:has-children:!has-siblings:closed,
    QTreeView::branch:closed:has-children:has-siblings {{
        border-image: none;
        image: url(:/images/branch-closed.png);
    }}
    
    QTreeView::branch:open:has-children:!has-siblings,
    QTreeView::branch:open:has-children:has-siblings {{
        border-image: none;
        image: url(:/images/branch-open.png);
    }}
    
    QHeaderView::section {{
        background-color: {COLORS['surface']};
        color: {COLORS['text_primary']};
        padding: 8px;
        border: none;
        border-bottom: 2px solid {COLORS['border']};
        font-weight: 600;
    }}
    
    /* Dialog */
    QDialog {{
        background-color: {COLORS['background']};
    }}
    
    /* Scroll Bar */
    QScrollBar:vertical {{
        background-color: {COLORS['surface']};
        width: 12px;
        border: none;
        border-radius: 6px;
    }}
    
    QScrollBar::handle:vertical {{
        background-color: {COLORS['border']};
        border-radius: 6px;
        min-height: 30px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background-color: {COLORS['secondary']};
    }}
    
    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    
    QScrollBar:horizontal {{
        background-color: {COLORS['surface']};
        height: 12px;
        border: none;
        border-radius: 6px;
    }}
    
    QScrollBar::handle:horizontal {{
        background-color: {COLORS['border']};
        border-radius: 6px;
        min-width: 30px;
    }}
    
    QScrollBar::handle:horizontal:hover {{
        background-color: {COLORS['secondary']};
    }}
    
    QScrollBar::add-line:horizontal,
    QScrollBar::sub-line:horizontal {{
        width: 0px;
    }}
    """

