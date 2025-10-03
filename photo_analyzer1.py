import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageFilter
from dotenv import load_dotenv
import os
import base64
import requests
import json

class SimplePhotoAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 AI Photo Analyzer Pro")
        self.root.geometry("1400x900")
        self.root.configure(bg='#0a0a0a')
        self.root.minsize(1200, 800)
        
        # Load environment variables (robust to bad encodings or missing file)
        try:
            dotenv_path = os.path.join(os.getcwd(), ".env")
            if os.path.exists(dotenv_path):
                load_dotenv(dotenv_path=dotenv_path, encoding="utf-8")
            else:
                load_dotenv(encoding="utf-8")
        except Exception:
            # Ignore dotenv read errors so the app can still run
            pass
        # Default API keys (load from environment; leave empty if not provided)
        self.default_chatgpt_key = os.getenv("OPENAI_API_KEY", "")
        self.default_imagedescriber_key = os.getenv("IMAGEDESCRIBER_API_KEY", "")
        
        self.api_key = self.default_chatgpt_key
        self.api_key_var = tk.StringVar()
        
        # API provider selection
        self.api_provider = tk.StringVar(value="chatgpt")  # Default to ChatGPT
        
        # Current image path
        self.current_image_path = None
        
        # Create GUI elements
        self.create_modern_ui()
        
        # Center the window
        self.center_window()
        
        # Load sample image for better visual appeal
        self.load_sample_image()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_modern_ui(self):
        """Create modern, impressive UI"""
        # Main container with gradient effect
        main_container = tk.Frame(self.root, bg='#0f0f0f')
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Header section
        self.create_header(main_container)
        
        # Content area with three columns
        content_frame = tk.Frame(main_container, bg='#0f0f0f')
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(15, 0))
        
        # Configure grid weights - responsive layout
        content_frame.grid_columnconfigure(0, weight=1, minsize=320)
        content_frame.grid_columnconfigure(1, weight=2, minsize=600)
        content_frame.grid_columnconfigure(2, weight=2, minsize=450)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Left panel - Controls
        self.create_control_panel(content_frame)
        
        # Center panel - Image display
        self.create_image_panel(content_frame)
        
        # Right panel - Analysis results
        self.create_results_panel(content_frame)
        
        # Bottom status bar
        self.create_status_bar(main_container)
    
    def create_header(self, parent):
        """Create modern header with gradient and glow effect"""
        header_frame = tk.Frame(parent, bg='#0f0f0f', height=120)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        header_frame.pack_propagate(False)
        
        # Animated gradient bar at top
        top_bar = tk.Frame(header_frame, bg='#00ff88', height=4)
        top_bar.pack(fill=tk.X)
        
        # Title frame with glow effect background
        title_container = tk.Frame(header_frame, bg='#1a1a1a', bd=0)
        title_container.pack(expand=True, fill=tk.BOTH, padx=20, pady=15)
        title_container.grid_columnconfigure(0, weight=1)
        title_container.grid_columnconfigure(1, weight=0)
        
        # Main title with shadow effect
        title_label = tk.Label(title_container, 
                              text="🤖 AI Photo Analyzer Pro",
                              bg='#1a1a1a',
                              fg='#00ff88',
                              font=('Segoe UI', 36, 'bold'))
        title_label.grid(row=0, column=0, sticky='w', padx=(0, 10), pady=(15, 5))
        
        # Subtitle with better visibility
        subtitle_label = tk.Label(title_container,
                                 text="✨ Advanced AI-Powered Image Analysis • Powered by GPT-4 Vision ✨",
                                 bg='#1a1a1a',
                                 fg='#aaaaaa',
                                 font=('Segoe UI', 12))
        subtitle_label.grid(row=1, column=0, sticky='w', pady=(0, 15))

        # About button on the right side
        about_btn = tk.Button(title_container,
                              text="ℹ️  About",
                              bg='#1a1a1a',
                              fg='#00d4ff',
                              font=('Segoe UI', 11, 'bold'),
                              relief='flat',
                              bd=0,
                              cursor='hand2',
                              activebackground='#1a1a1a',
                              highlightthickness=0,
                              command=self.open_about_modal)
        about_btn.grid(row=0, column=1, rowspan=2, sticky='e', padx=(10, 0))
        
        # Multi-colored separator
        separator_frame = tk.Frame(header_frame, height=3)
        separator_frame.pack(fill=tk.X)
        
        colors = ['#00ff88', '#00d4ff', '#ff4757']
        for i, color in enumerate(colors):
            seg = tk.Frame(separator_frame, bg=color, height=3)
            seg.place(relx=i/3, rely=0, relwidth=1/3, relheight=1)
    
    def create_control_panel(self, parent):
        """Create left control panel with enhanced design"""
        control_frame = tk.Frame(parent, bg='#1a1a1a', relief='flat', bd=0)
        control_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 8))
        
        # Add subtle border glow
        border_frame = tk.Frame(control_frame, bg='#00ff88', bd=0)
        border_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        inner_frame = tk.Frame(border_frame, bg='#1a1a1a')
        inner_frame.pack(fill=tk.BOTH, expand=True)
        
        # Panel title with icon
        title_frame = tk.Frame(inner_frame, bg='#252525', bd=0)
        title_frame.pack(fill=tk.X, pady=(0, 15))
        
        title_label = tk.Label(title_frame,
                              text="📁 Import & Controls",
                              bg='#252525',
                              fg='#00d4ff',
                              font=('Segoe UI', 15, 'bold'))
        title_label.pack(pady=15)
        
        # Control buttons
        self.create_control_buttons(inner_frame)
        
        # Image info section
        self.create_image_info(inner_frame)
    
    def create_control_buttons(self, parent):
        """Create control buttons with modern styling"""
        button_frame = tk.Frame(parent, bg='#1a1a1a')
        button_frame.pack(fill=tk.X, padx=15, pady=20)
        
        # Import button with gradient effect
        import_container = tk.Frame(button_frame, bg='#00d4ff', bd=0)
        import_container.pack(fill=tk.X, pady=10)
        
        self.import_btn = tk.Button(import_container,
                                   text="📁 Import Photo",
                                   bg='#00d4ff',
                                   fg='white',
                                   font=('Segoe UI', 13, 'bold'),
                                   relief='flat',
                                   bd=0,
                                   cursor='hand2',
                                   height=2,
                                   activebackground='#00a8cc',
                                   command=self.import_photo)
        self.import_btn.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Analyze button
        analyze_container = tk.Frame(button_frame, bg='#00ff88', bd=0)
        analyze_container.pack(fill=tk.X, pady=10)
        
        self.analyze_btn = tk.Button(analyze_container,
                                    text="🤖 Analyze with AI",
                                    bg='#00ff88',
                                    fg='#000000',
                                    font=('Segoe UI', 13, 'bold'),
                                    relief='flat',
                                    bd=0,
                                    cursor='hand2',
                                    height=2,
                                    state='disabled',
                                    activebackground='#00cc66',
                                    command=self.analyze_photo)
        self.analyze_btn.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Clear button
        clear_container = tk.Frame(button_frame, bg='#ff4757', bd=0)
        clear_container.pack(fill=tk.X, pady=10)
        
        self.clear_btn = tk.Button(clear_container,
                                  text="🗑️  Clear",
                                  bg='#ff4757',
                                  fg='white',
                                  font=('Segoe UI', 13, 'bold'),
                                  relief='flat',
                                  bd=0,
                                  cursor='hand2',
                                  height=2,
                                  activebackground='#ee3742',
                                  command=self.clear_image)
        self.clear_btn.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Add hover effects
        self.add_button_hover_effects()
    
    def add_button_hover_effects(self):
        """Add hover effects to buttons"""
        def create_hover(widget, enter_color, leave_color):
            widget.bind('<Enter>', lambda e: e.widget.configure(bg=enter_color))
            widget.bind('<Leave>', lambda e: e.widget.configure(bg=leave_color))
        
        create_hover(self.import_btn, '#00a8cc', '#00d4ff')
        create_hover(self.analyze_btn, '#00cc66', '#00ff88')
        create_hover(self.clear_btn, '#ee3742', '#ff4757')
    
    def create_image_info(self, parent):
        """Create image information display"""
        info_frame = tk.Frame(parent, bg='#1a1a1a')
        info_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(10, 15))
        
        # Info header
        info_header = tk.Frame(info_frame, bg='#252525', bd=0)
        info_header.pack(fill=tk.X)
        
        info_title = tk.Label(info_header,
                             text="📊 Image Information",
                             bg='#252525',
                             fg='#00d4ff',
                             font=('Segoe UI', 13, 'bold'))
        info_title.pack(anchor='w', padx=10, pady=12)
        
        # Info text with border
        text_container = tk.Frame(info_frame, bg='#00d4ff', bd=0)
        text_container.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.info_text = tk.Text(text_container,
                                bg='#0f0f0f',
                                fg='#c0c0c0',
                                font=('Consolas', 10),
                                height=10,
                                relief='flat',
                                bd=0,
                                wrap=tk.WORD,
                                padx=10,
                                pady=10)
        self.info_text.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.info_text.insert('1.0', '📌 Sample Image Loaded\n\n☑️ Ready to import your own image!')
    
    def create_image_panel(self, parent):
        """Create center image display panel"""
        image_frame = tk.Frame(parent, bg='#1a1a1a', relief='flat', bd=0)
        image_frame.grid(row=0, column=1, sticky='nsew', padx=8)
        
        # Border glow effect
        border_frame = tk.Frame(image_frame, bg='#00d4ff', bd=0)
        border_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        inner_frame = tk.Frame(border_frame, bg='#1a1a1a')
        inner_frame.pack(fill=tk.BOTH, expand=True)
        
        # Image title
        title_frame = tk.Frame(inner_frame, bg='#252525', bd=0)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(title_frame,
                              text="🖼️  Image Preview",
                              bg='#252525',
                              fg='#00d4ff',
                              font=('Segoe UI', 15, 'bold'))
        title_label.pack(pady=15)
        
        # Image display area with dark background
        self.image_display_frame = tk.Frame(inner_frame, bg='#0a0a0a', relief='flat', bd=0)
        self.image_display_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Image label
        self.image_label = tk.Label(self.image_display_frame,
                                   text="",
                                   bg='#0a0a0a',
                                   fg='#666666',
                                   font=('Segoe UI', 14),
                                   justify='center')
        self.image_label.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
    
    def create_api_key_section(self, parent):
        """Create OpenAI API key input section with provider selection"""
        api_frame = tk.Frame(parent, bg='#252525', relief='flat', bd=0)
        api_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        # Border effect
        border = tk.Frame(api_frame, bg='#00ff88', height=2)
        border.pack(fill=tk.X)
        
        inner = tk.Frame(api_frame, bg='#1a1a1a')
        inner.pack(fill=tk.X, padx=2, pady=2)
        
        # API Key title
        api_title = tk.Label(inner,
                            text="🔑 API Configuration",
                            bg='#1a1a1a',
                            fg='#00ff88',
                            font=('Segoe UI', 13, 'bold'))
        api_title.pack(pady=(12, 8))
        
        # API Provider Selection
        provider_frame = tk.Frame(inner, bg='#1a1a1a')
        provider_frame.pack(fill=tk.X, padx=12, pady=(0, 10))
        
        provider_label = tk.Label(provider_frame,
                                 text="Select API Provider:",
                                 bg='#1a1a1a',
                                 fg='#c0c0c0',
                                 font=('Segoe UI', 10))
        provider_label.pack(anchor='w', pady=(0, 5))
        
        # Radio buttons for provider selection
        radio_frame = tk.Frame(provider_frame, bg='#1a1a1a')
        radio_frame.pack(fill=tk.X)
        
        chatgpt_radio = tk.Radiobutton(radio_frame,
                                      text="ChatGPT-4 (OpenAI)",
                                      variable=self.api_provider,
                                      value="chatgpt",
                                      bg='#1a1a1a',
                                      fg='#00d4ff',
                                      selectcolor='#0f0f0f',
                                      activebackground='#1a1a1a',
                                      activeforeground='#00d4ff',
                                      font=('Segoe UI', 10),
                                      command=self.on_provider_change)
        chatgpt_radio.pack(side=tk.LEFT, padx=(0, 20))
        
        imagedescriber_radio = tk.Radiobutton(radio_frame,
                                             text="ImageDescriber.online",
                                             variable=self.api_provider,
                                             value="imagedescriber",
                                             bg='#1a1a1a',
                                             fg='#00d4ff',
                                             selectcolor='#0f0f0f',
                                             activebackground='#1a1a1a',
                                             activeforeground='#00d4ff',
                                             font=('Segoe UI', 10),
                                             command=self.on_provider_change)
        imagedescriber_radio.pack(side=tk.LEFT)
        
        # API Key input frame
        input_frame = tk.Frame(inner, bg='#1a1a1a')
        input_frame.pack(fill=tk.X, padx=12, pady=(0, 10))
        
        # API Key entry
        entry_container = tk.Frame(input_frame, bg='#00d4ff', bd=0)
        entry_container.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        
        self.api_key_entry = tk.Entry(entry_container,
                                     textvariable=self.api_key_var,
                                     bg='#0f0f0f',
                                     fg='#ffffff',
                                     font=('Consolas', 10),
                                     relief='flat',
                                     bd=0,
                                     show='*',
                                     insertbackground='#00ff88')
        self.api_key_entry.pack(fill=tk.BOTH, expand=True, padx=2, pady=2, ipady=8)
        
        # Set/Update button
        btn_container = tk.Frame(input_frame, bg='#00ff88', bd=0)
        btn_container.pack(side=tk.RIGHT)
        
        self.api_btn = tk.Button(btn_container,
                                text="Set Key",
                                bg='#00ff88',
                                fg='#000000',
                                font=('Segoe UI', 10, 'bold'),
                                relief='flat',
                                bd=0,
                                cursor='hand2',
                                command=self.update_api_key)
        self.api_btn.pack(padx=2, pady=2, ipadx=10, ipady=8)
        
        # Status indicator
        self.api_status_label = tk.Label(inner,
                                        text="✅ API Key Ready (ChatGPT Default)",
                                        bg='#1a1a1a',
                                        fg='#00ff88',
                                        font=('Segoe UI', 10))
        self.api_status_label.pack(pady=(0, 12))
    
    def on_provider_change(self):
        """Handle API provider change"""
        provider = self.api_provider.get()
        if provider == "chatgpt":
            # Set default ChatGPT key if no custom key
            if not self.api_key_var.get():
                self.api_key = self.default_chatgpt_key
            self.api_status_label.configure(
                text="✅ ChatGPT Selected - Using Default Key" if not self.api_key_var.get() else "✅ ChatGPT Selected",
                fg='#00ff88'
            )
        else:
            # Set default ImageDescriber key if no custom key
            if not self.api_key_var.get():
                self.api_key = self.default_imagedescriber_key
                self.api_status_label.configure(
                    text="✅ ImageDescriber - Using Default Key",
                    fg='#00ff88'
                )
            else:
                self.api_status_label.configure(
                    text="✅ ImageDescriber Selected",
                    fg='#00ff88'
                )
        self.update_status_bar()
    
    def update_api_key(self):
        """Update the API key"""
        new_key = self.api_key_var.get().strip()
        provider = self.api_provider.get()
        
        if provider == "chatgpt":
            if len(new_key) < 20 and new_key != "":
                self.api_status_label.configure(text="❌ Invalid ChatGPT API Key", fg='#ff4757')
                return
            
            if new_key == "":
                # Use default key
                self.api_key = self.default_chatgpt_key
                self.api_status_label.configure(text="✅ Using Default ChatGPT Key", fg='#00ff88')
            else:
                self.api_key = new_key
                self.api_status_label.configure(text="✅ ChatGPT API Key Updated", fg='#00ff88')
        else:  # imagedescriber
            if new_key == "":
                # Use default key
                self.api_key = self.default_imagedescriber_key
                self.api_status_label.configure(text="✅ Using Default ImageDescriber Key", fg='#00ff88')
            elif len(new_key) < 20:
                self.api_status_label.configure(text="❌ Invalid ImageDescriber Key", fg='#ff4757')
                return
            else:
                self.api_key = new_key
                self.api_status_label.configure(text="✅ ImageDescriber API Key Set", fg='#00ff88')
        
        # Update status bar
        self.update_status_bar()
    
    def create_results_panel(self, parent):
        """Create right results panel"""
        results_frame = tk.Frame(parent, bg='#1a1a1a', relief='flat', bd=0)
        results_frame.grid(row=0, column=2, sticky='nsew', padx=(8, 0))
        
        # Border glow
        border_frame = tk.Frame(results_frame, bg='#00ff88', bd=0)
        border_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        inner_frame = tk.Frame(border_frame, bg='#1a1a1a')
        inner_frame.pack(fill=tk.BOTH, expand=True)
        
        # API Key Input Section
        self.create_api_key_section(inner_frame)
        
        # Results title
        title_frame = tk.Frame(inner_frame, bg='#252525', bd=0)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(title_frame,
                              text="🧠 AI Analysis Results",
                              bg='#252525',
                              fg='#00ff88',
                              font=('Segoe UI', 15, 'bold'))
        title_label.pack(pady=15)
        
        # Results text area with scrollbar
        text_frame = tk.Frame(inner_frame, bg='#1a1a1a')
        text_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Custom scrollbar
        scrollbar_container = tk.Frame(text_frame, bg='#00d4ff', width=14)
        scrollbar_container.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        
        scrollbar = tk.Scrollbar(scrollbar_container, bg='#1a1a1a', troughcolor='#0f0f0f',
                                activebackground='#00ff88', bd=0, width=12)
        scrollbar.pack(fill=tk.Y, padx=1, pady=1)
        
        # Results text with border
        text_container = tk.Frame(text_frame, bg='#00d4ff', bd=0)
        text_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.results_text = tk.Text(text_container,
                                   bg='#0f0f0f',
                                   fg='#e0e0e0',
                                   font=('Segoe UI', 11),
                                   wrap=tk.WORD,
                                   relief='flat',
                                   bd=0,
                                   yscrollcommand=scrollbar.set,
                                   selectbackground='#00d4ff',
                                   selectforeground='white',
                                   padx=15,
                                   pady=15)
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        scrollbar.config(command=self.results_text.yview)
        
        # Initial message
        welcome_msg = """🚀 Welcome to AI Photo Analyzer Pro!

Import an image to get started with advanced AI analysis.

Features:
• Object and scene recognition
• Detailed descriptions
• Color and mood analysis
• Context understanding
• Professional insights

Your OpenAI API is ready! 🟢"""
        
        self.results_text.insert('1.0', welcome_msg)
    
    def create_status_bar(self, parent):
        """Create modern status bar"""
        status_frame = tk.Frame(parent, bg='#1a1a1a', relief='flat', bd=0)
        status_frame.pack(fill=tk.X, pady=(15, 0))
        
        # Top border
        border = tk.Frame(status_frame, bg='#00ff88', height=2)
        border.pack(fill=tk.X)
        
        inner = tk.Frame(status_frame, bg='#1a1a1a')
        inner.pack(fill=tk.X)
        
        self.status_var = tk.StringVar()
        self.status_var.set("🔮 Ready - Import a photo to begin AI analysis")
        
        status_label = tk.Label(inner,
                               textvariable=self.status_var,
                               bg='#1a1a1a',
                               fg='#c0c0c0',
                               font=('Segoe UI', 10),
                               anchor='w')
        status_label.pack(side=tk.LEFT, padx=15, pady=12)
        
        # API status indicator
        self.api_status_bar = tk.Label(inner,
                                      text="🟢 API Connected",
                                      bg='#1a1a1a',
                                      fg='#00ff88',
                                      font=('Segoe UI', 10, 'bold'))
        self.api_status_bar.pack(side=tk.RIGHT, padx=15, pady=12)
    
    def update_status_bar(self):
        """Update the status bar API indicator"""
        provider = self.api_provider.get()
        
        if provider == "chatgpt":
            if self.api_key and len(self.api_key) > 20:
                is_default = (self.api_key == self.default_chatgpt_key)
                if is_default:
                    self.api_status_bar.configure(text="🟠 ChatGPT (Default Key)", fg='#ffaa00')
                else:
                    self.api_status_bar.configure(text="🟢 ChatGPT API Connected", fg='#00ff88')
            else:
                self.api_status_bar.configure(text="❌ ChatGPT - No Key", fg='#ff4757')
        else:  # imagedescriber
            if self.api_key and len(self.api_key) > 20:
                is_default = (self.api_key == self.default_imagedescriber_key)
                if is_default:
                    self.api_status_bar.configure(text="🟠 ImageDescriber (Default Key)", fg='#ffaa00')
                else:
                    self.api_status_bar.configure(text="🟢 ImageDescriber Connected", fg='#00ff88')
            else:
                self.api_status_bar.configure(text="❌ ImageDescriber - No Key", fg='#ff4757')
    
    def import_photo(self):
        """Import photo with file dialog"""
        file_types = [
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.webp"),
            ("All files", "*.*")
        ]
        
        file_path = filedialog.askopenfilename(
            title="Select an Image File",
            filetypes=file_types
        )
        
        if file_path:
            self.load_image(file_path)
    
    def load_image(self, image_path):
        """Load and display image"""
        try:
            if not os.path.exists(image_path):
                messagebox.showerror("Error", "File not found!")
                return
            
            # Load original image
            original_image = Image.open(image_path)
            
            # Create display version
            display_image = original_image.copy()
            
            # Convert to RGB if necessary
            if display_image.mode != 'RGB':
                display_image = display_image.convert('RGB')
            
            # Calculate size for display
            max_width, max_height = 600, 550
            img_width, img_height = display_image.size
            
            scale = min(max_width/img_width, max_height/img_height)
            if scale < 1 or scale > 1:
                new_width = int(img_width * scale)
                new_height = int(img_height * scale)
                display_image = display_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(display_image)
            
            # Update image display
            self.image_label.configure(image=photo, text="", compound='center')
            self.image_label.image = photo
            
            # Store current image path
            self.current_image_path = image_path
            
            # Enable analyze button
            self.analyze_btn.configure(state="normal", bg='#00ff88')
            
            # Update image info
            self.update_image_info(original_image)
            
            # Update status
            filename = os.path.basename(image_path)
            self.status_var.set(f"📁 Loaded: {filename} - Ready for AI analysis")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")
            self.status_var.set("❌ Error loading image")
    
    def update_image_info(self, image):
        """Update image information display"""
        try:
            width, height = image.size
            mode = image.mode
            format_name = image.format or "Unknown"
            file_size = os.path.getsize(self.current_image_path)
            
            info_text = f"""📏 Dimensions: {width} × {height} px
📊 Format: {format_name}
🎨 Purpose: UI Demonstration
💾 File Size: {file_size / 1024:.1f} KB

🎯 Ready to import your own image!"""
            
            self.info_text.delete('1.0', tk.END)
            self.info_text.insert('1.0', info_text)
            
        except Exception as e:
            self.info_text.delete('1.0', tk.END)
            self.info_text.insert('1.0', f"Error: {str(e)}")
    
    def analyze_photo(self):
        """Analyze photo with AI"""
        if not self.current_image_path:
            messagebox.showwarning("Warning", "Please import a photo first!")
            return
        
        provider = self.api_provider.get()
        
        # Update UI for analysis
        self.analyze_btn.configure(state="disabled", bg='#7f8c8d', text="🤖 Analyzing...")
        provider_name = "ChatGPT-4" if provider == "chatgpt" else "ImageDescriber.online"
        self.status_var.set(f"🧠 {provider_name} is analyzing your image... Please wait")
        self.results_text.delete('1.0', tk.END)
        self.results_text.insert('1.0', f"🤖 AI Analysis in Progress ({provider_name})...\n\nPlease wait while our advanced AI analyzes your image.")
        self.root.update()
        
        try:
            if provider == "chatgpt":
                result = self.analyze_with_chatgpt(self.current_image_path)
                service_tag = "\n\n" + "="*50 + "\n🤖 Generated by: ChatGPT-4 (OpenAI)"
            else:
                result = self.analyze_with_imagedescriber(self.current_image_path)
                service_tag = "\n\n" + "="*50 + "\n🤖 Generated by: ImageDescriber.online"
            
            if "insufficient_quota" in result.lower() or "429" in result or "error" in result.lower():
                result = self.analyze_image_fallback(self.current_image_path)
                service_tag = "\n\n" + "="*50 + "\n🤖 Generated by: Fallback Analysis (Basic)"
            
            self.results_text.delete('1.0', tk.END)
            formatted_result = f"🧠 AI Analysis Results\n{'='*50}\n\n{result}{service_tag}\n{'='*50}\n✅ Analysis Complete"
            self.results_text.insert('1.0', formatted_result)
            
            self.status_var.set("✅ Analysis complete - Scroll to view full results")
            
        except Exception as e:
            try:
                result = self.analyze_image_fallback(self.current_image_path)
                service_tag = "\n\n" + "="*50 + "\n🤖 Generated by: Fallback Analysis (Basic)"
                
                self.results_text.delete('1.0', tk.END)
                formatted_result = f"🧠 Basic Analysis Results\n{'='*50}\n\n{result}{service_tag}\n{'='*50}\n✅ Analysis Complete"
                self.results_text.insert('1.0', formatted_result)
                self.status_var.set("✅ Basic analysis complete")
            except:
                error_msg = f"Error: {str(e)}"
                self.results_text.delete('1.0', tk.END)
                self.results_text.insert('1.0', f"❌ Analysis Failed\n\n{error_msg}")
                self.status_var.set("❌ Analysis failed")
        
        finally:
            self.analyze_btn.configure(state="normal", bg='#00ff88', text="🤖 Analyze with AI")
    
    def analyze_with_chatgpt(self, image_path):
        """Analyze image using ChatGPT (OpenAI GPT-4 Vision API)"""
        if not self.api_key:
            return "Error: ChatGPT API key not found."
        
        try:
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": """Analyze this image in comprehensive detail following this exact structure:

Summary: Provide a one-sentence overview that captures the essence of the image.

Detailed Description:
Break down the image into relevant sections such as:

Person/People: (if applicable) Describe age range, appearance, clothing, pose, expression, and what they might be doing or feeling.

Setting: Describe the environment, location type, and physical surroundings.

Objects/Elements: Identify and describe key objects, structures, or elements in the scene.

Background: Describe what's visible in the background - buildings, landscapes, sky, etc.

Foreground: Describe elements in the immediate foreground.

Colors and Lighting: Analyze the color palette, lighting conditions, and visual tone.

Atmosphere and Mood: Describe the overall feeling, mood, and emotional tone of the image. What impression does it convey?

Be thorough, specific, and descriptive. Organize the information clearly under these headings."""
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 1500
            }
            
            response = requests.post("https://api.openai.com/v1/chat/completions", 
                                   headers=headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"API Error {response.status_code}: {response.text}"
                
        except Exception as e:
            return f"Error: {str(e)}"
    
    def analyze_with_imagedescriber(self, image_path):
        """Analyze image using ImageDescriber.online API"""
        if not self.api_key:
            return "Error: ImageDescriber API key not found."
        
        try:
            # Use multipart/form-data: keep file handle open during request
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }

            form_data = {
                "prompt": """Analyze this image in comprehensive detail following this exact structure:

Summary: Provide a one-sentence overview that captures the essence of the image.

Detailed Description:
Break down the image into relevant sections such as:

Person/People: (if applicable) Describe age range, appearance, clothing, pose, expression, and what they might be doing or feeling.

Setting: Describe the environment, location type, and physical surroundings.

Objects/Elements: Identify and describe key objects, structures, or elements in the scene.

Background: Describe what's visible in the background - buildings, landscapes, sky, etc.

Foreground: Describe elements in the immediate foreground.

Colors and Lighting: Analyze the color palette, lighting conditions, and visual tone.

Atmosphere and Mood: Describe the overall feeling, mood, and emotional tone of the image. What impression does it convey?

Be thorough, specific, and descriptive. Organize the information clearly under these headings."""
            }

            with open(image_path, "rb") as image_file:
                files = {
                    "image": (os.path.basename(image_path), image_file, "image/jpeg")
                }
                response = requests.post(
                    "https://imagedescriber.online/api/openapi-v2/describe-image",
                    headers=headers,
                    files=files,
                    data=form_data,
                    timeout=60
                )
            
            if response.status_code == 200:
                result = response.json()
                # Extract description from response
                extracted = None
                if 'description' in result:
                    extracted = result['description']
                elif 'data' in result:
                    data = result['data']
                    if isinstance(data, dict):
                        if 'content' in data and isinstance(data['content'], str):
                            extracted = data['content']
                        elif 'description' in data and isinstance(data['description'], str):
                            extracted = data['description']
                elif 'result' in result and isinstance(result['result'], str):
                    extracted = result['result']

                if isinstance(extracted, str) and extracted.strip():
                    return self._format_imagedescriber_text(extracted)

                # Fallback to stringifying, but ensure it's readable
                return json.dumps(result, ensure_ascii=False)
            else:
                return f"ImageDescriber API Error {response.status_code}: {response.text}"
                
        except Exception as e:
            return f"Error: {str(e)}"

    def _format_imagedescriber_text(self, text):
        """Normalize ImageDescriber text for consistent, readable display."""
        try:
            cleaned = text.strip()
            if cleaned.startswith('{') and cleaned.endswith('}'):
                # In case a JSON string slipped through
                return cleaned
            # Remove surrounding quotes
            if (cleaned.startswith('"') and cleaned.endswith('"')) or (cleaned.startswith("'") and cleaned.endswith("'")):
                cleaned = cleaned[1:-1].strip()
            # Normalize bullets like '*   ' to '• '
            lines = cleaned.splitlines()
            normalized_lines = []
            for line in lines:
                l = line.lstrip()
                if l.startswith('* '):
                    normalized_lines.append('• ' + l[2:])
                elif l.startswith('*\t'):
                    normalized_lines.append('• ' + l[2:])
                elif l.startswith('*') and '   ' in l[:4]:
                    normalized_lines.append('• ' + l[l.find(' ')+1:])
                else:
                    normalized_lines.append(line)
            cleaned = "\n".join(normalized_lines)
            return cleaned
        except Exception:
            return text

    def open_about_modal(self):
        """Show About modal with project information and usage instructions."""
        try:
            modal = tk.Toplevel(self.root)
            modal.title("About • AI Photo Analyzer Pro")
            modal.configure(bg='#1a1a1a')
            modal.transient(self.root)
            modal.grab_set()

            container = tk.Frame(modal, bg='#1a1a1a')
            container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

            title = tk.Label(container,
                             text="About This Project",
                             bg='#1a1a1a', fg='#00ff88',
                             font=('Segoe UI', 16, 'bold'))
            title.pack(anchor='w', pady=(0, 8))

            subtitle = tk.Label(container,
                                text="AI Photo Analyzer Pro • Purpose & How to Use",
                                bg='#1a1a1a', fg='#c0c0c0',
                                font=('Segoe UI', 11))
            subtitle.pack(anchor='w', pady=(0, 12))

            text_frame = tk.Frame(container, bg='#00d4ff', bd=0)
            text_frame.pack(fill=tk.BOTH, expand=True)

            text_area = scrolledtext.ScrolledText(text_frame,
                                                  bg='#0f0f0f', fg='#e0e0e0',
                                                  font=('Segoe UI', 10),
                                                  relief='flat', bd=0,
                                                  wrap=tk.WORD)
            text_area.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

            about_content = (
                "Purpose:\n"
                "- Provide AI-powered image analysis with clear, structured results.\n\n"
                "What this project is:\n"
                "- A desktop GUI built with Tkinter.\n"
                "- Integrates OpenAI (GPT-4o) and ImageDescriber.online for image understanding.\n\n"
                "How to use:\n"
                "1) Click '📁 Import Photo' to choose an image.\n"
                "2) Optionally set your API provider and key on the right panel.\n"
                "3) Click '🤖 Analyze with AI' to generate a structured description.\n"
                "4) Review results in the right pane; scroll for full details.\n\n"
                "Notes:\n"
                "- GPT-4o supports vision; ImageDescriber is an alternative provider.\n"
                "- If APIs are unavailable, a built-in fallback provides a basic technical analysis.\n"
            )
            text_area.insert('1.0', about_content)
            text_area.configure(state='disabled')

            btn_row = tk.Frame(container, bg='#1a1a1a')
            btn_row.pack(fill=tk.X, pady=(12, 0))
            close_btn = tk.Button(btn_row, text="Close",
                                  bg='#00ff88', fg='#000000',
                                  font=('Segoe UI', 10, 'bold'),
                                  relief='flat', bd=0,
                                  command=modal.destroy)
            close_btn.pack(side=tk.RIGHT)

            # Center modal
            modal.update_idletasks()
            w = modal.winfo_width()
            h = modal.winfo_height()
            x = (self.root.winfo_screenwidth() // 2) - (w // 2)
            y = (self.root.winfo_screenheight() // 2) - (h // 2)
            modal.geometry(f"{w}x{h}+{x}+{y}")
        except Exception as e:
            messagebox.showerror("About", f"Failed to open About: {str(e)}")
    
    def analyze_image_fallback(self, image_path):
        """Fallback analysis"""
        try:
            with Image.open(image_path) as img:
                width, height = img.size
                mode = img.mode
                format_name = img.format or "Unknown"
                file_size = os.path.getsize(image_path)
                
                # Analyze colors
                colors = img.getcolors(maxcolors=256*256*256)
                if colors:
                    color_info = "Rich color palette detected"
                else:
                    color_info = "Complex color composition"
                
                # Basic content analysis
                aspect_ratio = width / height
                if aspect_ratio > 1.5:
                    orientation = "landscape orientation"
                elif aspect_ratio < 0.7:
                    orientation = "portrait orientation"
                else:
                    orientation = "square orientation"
                
                # File size analysis
                if file_size > 5 * 1024 * 1024:
                    quality_note = "high resolution image"
                elif file_size > 1 * 1024 * 1024:
                    quality_note = "good quality image"
                else:
                    quality_note = "standard quality image"
            
            description = f"""📊 Technical Analysis:
• Dimensions: {width} × {height} pixels
• Format: {format_name} ({mode} mode)
• File Size: {file_size / 1024:.1f} KB
• {color_info}

🖼️ Visual Assessment:
• This is a {quality_note}
• Image has {orientation}
• Aspect ratio: {aspect_ratio:.2f}

📝 Basic Description:
This image contains visual content suitable for detailed AI analysis. The technical properties indicate it's ready for advanced computer vision processing.

💡 For full AI-powered analysis with object recognition, scene understanding, and detailed descriptions, ensure your OpenAI API key is properly configured."""
            
            return description
            
        except Exception as e:
            return f"Analysis error: {str(e)}"
    
    def clear_image(self):
        """Clear image and reset UI"""
        # Reset image display
        self.image_label.configure(image="", text="")
        self.image_label.image = None
        
        # Reset variables
        self.current_image_path = None
        
        # Reset buttons
        self.analyze_btn.configure(state="disabled", bg='#7f8c8d')
        
        # Clear image info
        self.info_text.delete('1.0', tk.END)
        self.info_text.insert('1.0', '📌 Sample Image Loaded\n\n☑️ Ready to import your own image!')
        
        # Clear results
        self.results_text.delete('1.0', tk.END)
        welcome_msg = """🚀 Welcome to AI Photo Analyzer Pro!

Import an image to get started with advanced AI analysis.

Features:
• Object and scene recognition
• Detailed descriptions
• Color and mood analysis
• Context understanding
• Professional insights

Your OpenAI API is ready! 🟢"""
        self.results_text.insert('1.0', welcome_msg)
        
        # Reset status
        self.status_var.set("🔮 Ready - Import a photo to begin AI analysis")
        
        # Reload sample image
        self.load_sample_image()
    
    def load_sample_image(self):
        """Load a beautiful sample image"""
        try:
            # Create enhanced gradient sample image
            width, height = 600, 550
            image = Image.new('RGB', (width, height), '#0a0a0a')
            draw = ImageDraw.Draw(image)
            
            # Create radial gradient background
            center_x, center_y = width // 2, height // 2
            max_radius = ((width/2)**2 + (height/2)**2)**0.5
            
            for y in range(height):
                for x in range(width):
                    # Calculate distance from center
                    distance = ((x - center_x)**2 + (y - center_y)**2)**0.5
                    # Create gradient
                    gradient_factor = distance / max_radius
                    base_color = int(15 + gradient_factor * 40)
                    color = (base_color, base_color + 5, base_color + 10)
                    draw.point((x, y), fill=color)
            
            # Add geometric shapes with glow effect
            # Circle with glow
            circle_center = (200, 200)
            circle_radius = 90
            
            # Outer glow
            for i in range(5, 0, -1):
                alpha_color = '#00ff88' if i == 1 else f'#{int(0x00 * (i/5)):02x}{int(0xff * (i/5)):02x}{int(0x88 * (i/5)):02x}'
                draw.ellipse([
                    circle_center[0] - circle_radius - i*2, 
                    circle_center[1] - circle_radius - i*2,
                    circle_center[0] + circle_radius + i*2, 
                    circle_center[1] + circle_radius + i*2
                ], outline='#00ff88', width=2)
            
            # Rectangle with glow
            rect_coords = [380, 150, 550, 280]
            for i in range(4, 0, -1):
                offset = i * 2
                draw.rectangle([
                    rect_coords[0] - offset, rect_coords[1] - offset,
                    rect_coords[2] + offset, rect_coords[3] + offset
                ], outline='#00d4ff', width=2)
            
            # Triangle with glow
            triangle_points = [(475, 330), (400, 450), (550, 450)]
            for i in range(3, 0, -1):
                for j in range(len(triangle_points)):
                    start = triangle_points[j]
                    end = triangle_points[(j + 1) % len(triangle_points)]
                    draw.line([start, end], fill='#ff4757', width=3)
            
            # Add glowing text
            try:
                font_large = ImageFont.truetype("arial.ttf", 42)
                font_medium = ImageFont.truetype("arial.ttf", 20)
                font_small = ImageFont.truetype("arial.ttf", 16)
            except:
                font_large = ImageFont.load_default()
                font_medium = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # Main title with shadow
            text = "AI Photo Analyzer"
            text_bbox = draw.textbbox((0, 0), text, font=font_large)
            text_width = text_bbox[2] - text_bbox[0]
            text_x = (width - text_width) // 2
            
            # Shadow effect
            draw.text((text_x + 3, 53), text, fill='#003322', font=font_large)
            draw.text((text_x, 50), text, fill='#00ff88', font=font_large)
            
            # Subtitle
            subtitle = "Drop your image here to analyze"
            subtitle_bbox = draw.textbbox((0, 0), subtitle, font=font_medium)
            subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
            subtitle_x = (width - subtitle_width) // 2
            draw.text((subtitle_x, 480), subtitle, fill='#888888', font=font_medium)
            
            # Add decorative elements
            # Corner accents
            accent_color = '#00d4ff'
            corner_size = 30
            
            # Top-left
            draw.line([(10, 10), (10 + corner_size, 10)], fill=accent_color, width=3)
            draw.line([(10, 10), (10, 10 + corner_size)], fill=accent_color, width=3)
            
            # Top-right
            draw.line([(width - 10, 10), (width - 10 - corner_size, 10)], fill=accent_color, width=3)
            draw.line([(width - 10, 10), (width - 10, 10 + corner_size)], fill=accent_color, width=3)
            
            # Bottom-left
            draw.line([(10, height - 10), (10 + corner_size, height - 10)], fill=accent_color, width=3)
            draw.line([(10, height - 10), (10, height - 10 - corner_size)], fill=accent_color, width=3)
            
            # Bottom-right
            draw.line([(width - 10, height - 10), (width - 10 - corner_size, height - 10)], fill=accent_color, width=3)
            draw.line([(width - 10, height - 10), (width - 10, height - 10 - corner_size)], fill=accent_color, width=3)
            
            # Convert to PhotoImage and display
            photo = ImageTk.PhotoImage(image)
            self.image_label.configure(image=photo, text="")
            self.image_label.image = photo
            
        except Exception as e:
            pass

def main():
    root = tk.Tk()
    app = SimplePhotoAnalyzer(root)
    root.mainloop()

if __name__ == "__main__":
    main()


