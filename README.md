# Django-Core Full-Stack Terminal
### Django Backend Authentication & RBAC System

This project was developed as the **Capstone Final Project for Harvard University's CS50W: Web Programming with Python and JavaScript**. 

The following documentation outlines the architecture, logic, and testing protocols required to satisfy the course's "Distinctiveness and Complexity" standards. It serves as a comprehensive demonstration of full-stack engineering, featuring a custom-built terminal interface, multi-tier Role-Based Access Control (RBAC), and asynchronous integration with local LLM and Vision models.

---

## 📺 Video Demonstrations

To see the **Django-Core Full-Stack Terminal** in action, including the integrated AI workflows and automated testing suite, please view the demonstrations below:

### 🤖 Core System & AI Integration
**[Watch the System Overview](https://www.youtube.com/watch?v=aV-RZuVNV5U)** *This video demonstrates the terminal interface, the 5-tier security clearance system, and real-time asynchronous communication with Llama 3.1 and Flux .1.*

### 🧪 Automated Testing & QA Validation
**[Watch the Test Execution](https://www.youtube.com/watch?v=INaGrY5kSoY)** *A live demonstration of the automated testing suite. This video showcases **32+ Selenium and Django TestCase** suites running in real-time to validate frontend interactivity, backend logic, and system-wide security protocols.*

---

# OCP Management Portal
### CS50W Final Project - Capstone

The OCP (Omni Consumer Products) Management Portal is a **full-stack web application** designed as a sophisticated, corporate-themed terminal inspired by the *RoboCop* universe. 

This project demonstrates a complex integration of a **Python/Django** backend with a dynamic **JavaScript, HTML5, and CSS3** frontend. It serves as a comprehensive internal operations system, blending a retro-cyberpunk aesthetic with modern "Local-First" AI integrations. The application features a custom five-tier security system and handles asynchronous API communication with local generative engines: **Ollama (Llama 3.1:8b)** for personality-driven dialogue and **ComfyUI (Flux .1)** for high-fidelity vision synthesis. 

The project includes a robust automated testing suite—comprising 32 Django unit tests and Selenium browser automation—to ensure system integrity across all security clearances.

---

## 🛡️ Security Clearance System
The core of the portal is its dynamic five-tier access control system. The user experience, available tools, and AI interactions shift based on the rank assigned to the account:

1.  **Level 1: Guest** (Default access for new registrations)
2.  **Level 2: Employee**
3.  **Level 3: Mid-Management**
4.  **Level 4: Senior Executive**
5.  **Level 5: OCP Board Member**

---

## 🖥️ Platform Features

### Non-Member Interface (Public)
General users can explore the public-facing corporate site to learn about OCP operations:
* **Services:** View the "Current Product Lineup" and "Future Initiatives."
* **Employment:** Learn how to join the OCP workforce.
* **About:** Corporate history and the official OCP Mission Statement.
* **Access:** Secure portals for account registration and authentication.

### Member Terminal (Restricted)
Once logged in, the interface transforms into a functional terminal. All members have access to basic directives, while high-level features are restricted to executives:

* **Dashboard:** The landing hub for all employees, displaying quick-access links to authorized tools and corporate status.
* **Asset Feed:** A visual database of AI-generated assets. This module features pagination, the ability to download images, and a community feedback system for leaving comments on specific assets.
* **ED-209 Chat Interface:** A real-time AI chat module connecting to **Ollama (Llama 3.1:8b)**. 
    * **Live Status:** Features a visual notification system indicating if the LLM connection is online or offline.
    * **Behavioral Protocols:** The AI’s personality is rank-dependent. It treats lower-level staff with hostility and aggression, while becoming obedient only for Board Members. However, a "malfunction" factor remains, adding a layer of unpredictability.
* **ED-209 Vision Generator:** A deep-integration image suite connecting to **ComfyUI (Flux .1)**.
    * **AI Influence:** The AI utilizes Llama 3.1:8b to interpret and "improve" prompts based on rank. Lower-clearance users will find the AI adding OCP branding and logos into the background of their images, while Level 5 users receive exact generations.
    * **Workspace UI:** Completed images populate a history gallery where users can zoom, download, or drag/move images across the screen for closer inspection.
* **User Profile:** Displays personal corporate data, including Employee ID, Clearance Status, and Access Level.
* **Security Settings (Level 4 & 5 Only):** An executive management tool used to search the personnel database and promote users. To maintain corporate hierarchy, executives can only promote users to one level below their own rank.

---

## Distinctiveness and Complexity

### Distinctiveness
This project is distinct from other CS50W assignments as it is not a standard social network or e-commerce site, but a specialized Corporate Management Portal with heavy emphasis on external AI integration and role-based interface dynamics. Unlike "Network," where users interact in a uniform way, this project implements a strict Five-Tier Security Clearance system that fundamentally alters the website’s functionality, UI layout, and AI behavior based on the user's rank. Furthermore, the integration of local Generative AI (Ollama and ComfyUI) through custom API handlers sets this project apart from the standard CRUD applications seen in the course.

### Complexity
The complexity of the OCP Management Portal is demonstrated through several technical implementations:

1. AI Connectivity & Asynchronous Requests: The project utilizes httpx and Requests to maintain communication with local AI models. It features a real-time "Online/Offline" status detection system for external services, ensuring the UI remains informative even if a backend AI service is disconnected.

2. Dynamic Persona Engine: Using Llama 3.1:8b, I developed a system where the AI’s personality shifts according to the user's clearance level. This required complex prompt engineering and backend logic to translate user rank into specific AI "moods" (Hostile vs. Obedient).

3. Vision Generation Logic: The ED-209 Vision Generator manages a complex workflow where user prompts are intercepted, modified by an LLM to add "corporate influence" (branding/logos) for lower-level users, and then passed to ComfyUI/Flux .1 for image generation. The resulting files are stored locally with their paths mapped in a Django database for the Asset Feed.

4. Interactive Frontend: The Generated History UI goes beyond basic HTML/CSS. It allows users to zoom, download, and move image elements dynamically across the screen, providing a "terminal" feel that is more interactive than standard static pages.

5. Comprehensive Testing Suite: To ensure the stability of the security clearance tiers, I implemented a suite of 32 automated tests. This includes Django unit tests for backend logic and extensive Selenium tests for end-to-end browser automation. These tests verify that UI elements (like Security Settings) are strictly hidden or revealed based on the authenticated user's rank.

6. Scalable Security Management: Level 4 and 5 users have access to a custom administration interface within the app to manage other users. This involves complex filtering logic to ensure executives can only promote users to a rank lower than their own, maintaining the hierarchy through the application's business logic.

---

## 🛠️ Installation & Setup Guide

To fully experience the OCP Management Portal, you must configure the following environment. This project utilizes a "Local-First" AI architecture, requiring both the Django web server and local AI inference engines to be active simultaneously.

### 1. Python Environment & Core Setup
Ensure you have Python 3.12+ installed on your system.

* Install Dependencies: 
  pip install -r requirements.txt

    ```text
    asgiref==3.9.2
    Django==6.0.3
    httpx==0.28.1
    psutil==7.1.0
    Requests==2.33.0
    selenium==4.41.0
    ```
* Initialize OCP Database: 
  python manage.py migrate
* Launch Terminal: 
  python manage.py runserver
  Access the portal at: http://127.0.0.1:8000/

### 2. External AI Dependencies
The portal requires two local services to be running to handle AI Directives:

* Ollama (LLM Engine):
    * Install Ollama (https://ollama.com/).
    * Download the required model: ollama pull llama3.1:8b.
    * The service must be active on its default port (11434).
* ComfyUI (Vision Synthesis):
    * Install ComfyUI (https://github.com/comfyanonymous/ComfyUI).
    * Ensure the flux1-schnell-fp8.safetensors model is in the models/checkpoints/ directory.
    * Launch ComfyUI on its default port (8188).

---

## 🧪 Automated Testing Suite
The project includes 32 automated tests to ensure system integrity across the backend and the UI.

### Configuration
You can toggle the Selenium browser mode by editing test_selenium.py:
* HEADLESS = True: Runs tests in the background (Ideal for server environments).
* HEADLESS = False: Opens a visible Firefox window to observe automated navigation.
* Note: Requires Firefox Geckodriver installed in your system PATH.

### Execution Commands
* Run All Tests: python manage.py test
* Django Backend Tests: python manage.py test ocp.tests
* Selenium UI Tests: python manage.py test ocp.test_selenium

### Test Results Can Be Seen In : 
* test_results.txt

---

## 📝 Additional Information for the Staff

The OCP Management Portal was designed as a "Local-First" AI application. Here are the technical details regarding the infrastructure:

* Hardware Requirements: Due to the integration of Flux .1 and Llama 3.1, a machine with a dedicated GPU (8GB+ VRAM) is recommended for real-time vision synthesis.
* Service Fail-safes: I have implemented "Heartbeat" monitoring via image_creation.js. If AI services are not detected, the UI will display a "SERVICE OFFLINE" status in the terminal header.
* Media Management: AI-generated assets are stored in the media/visions/ directory. The project includes a cleanup routine in flux_image_creation.py to manage temporary session files.
* Browser Compatibility: The terminal aesthetic utilizes advanced CSS features like backdrop-filter and -webkit-text-stroke. It is optimized for modern Chromium-based browsers and Firefox.

---

# OCP Project Directory Structure

## Python Logic and Backend (ocp/)
* **admin.py**:
    Configures the Django administrative interface. It registers the User, Asset, Comment, and Directive models, allowing administrators to manage personnel records, moderate AI-generated assets, and audit ED-209 chat logs directly from the backend.

* **flux_image_creation.py**:
            The primary engine for AI visual generation. This script bridges Django with ComfyUI, handling:
    - Directory Management: Dynamically resolves Django media paths for "Vision" storage.
    - Workflow Execution: Loads JSON-based Flux .1 blueprints to generate high-resolution images (1280x720).
    - VRAM Optimization: Includes a specialized 'freemem' routine that sends a signal to ComfyUI to flush its memory cache after every generation, preventing local hardware crashes.
    - Session Handling: Uses UUID-based session IDs to prevent filename collisions during concurrent generations.

* **models.py**:
    The database blueprint for the OCP ecosystem, featuring:
    - Custom User Model: Extends AbstractUser to include a 5-tier "Clearance Level" system.
    - Automated ID Generation: A custom save() method that automatically assigns unique employee IDs (e.g., OCP-100001) in sequence, including a "Personnel Capacity" error once ID limits are reached.
    - Asset Tracking: Stores Flux .1 generations with associated prompts, technical seeds, and an "Executive Approval" (like) system.
    - Comment System: Allows for threaded feedback on generated assets in the Asset Feed.
    - Directive Logs: Captures full LLM chat interactions between users and ED-209, including the user's specific clearance level at the time of the conversation for audit purposes.

* **ollama_model.py**:
    The intelligence engine for the ED-209 Chat and Vision systems. This module manages local LLM communication using Ollama (Llama 3.1:8b) and features:
    - Multi-Model Support: Pre-configured for various models including Llama 3.1, Gemma 3, and DeepSeek, allowing for rapid model swapping.
    - Short-Term Memory Logic: Implements a sophisticated context windowing system. It preserves global "System Instructions" while maintaining a rolling "Short-Term Memory" of the last 6 messages. This ensures ED-209 maintains conversation context without exceeding token limits or losing its "personality" instructions.
    - VRAM Keep-Alive Management: Specifically handles GPU memory efficiency by utilizing 'keep_alive' parameters. This allows the model to remain in memory for fast responses during active chat sessions or be flushed immediately to free resources for the Vision Generator.
    - Persona Integration: Supports dynamic system instructions, enabling the "Hostility vs. Obedience" behavior logic defined by the user's security clearance.

* **test_selenium.py**: 
    A comprehensive browser automation suite that performs end-to-end testing of the portal’s security and navigation. This file is a primary driver of the project's technical complexity, featuring:
    - Automated Personnel Lifecycle: Includes helper functions to programmatically create, log in, and verify users across all 5 clearance tiers during a single test run.
    - Tiered Access Verification: 32+ automated tests ensure that restricted UI elements (like Executive Security Settings) are physically inaccessible and hidden from lower-level accounts.
    - Interactive Search Testing: Validates the JavaScript-driven personnel search engine, testing both full-name and partial-string queries within the OCP database.
    - Dynamic UI Interaction: Uses Selenium to handle complex browser behaviors, including navigating multi-level dropdown menus, submitting rank-escalation forms, and accepting JavaScript confirmation alerts.
    - Environment Flexibility: Supports both 'Headless' mode for efficient background execution and standard browser mode for visual debugging, with built-in logic to auto-detect GitHub Actions environments.
    - Security Escalation Logic: Specifically tests the "Promote" feature, ensuring that Level 4/5 users can successfully upgrade subordinates while verifying the business rule that prevents users from promoting others to a rank equal to or higher than their own.

* **tests.py**: 
    Focuses on backend performance and data integrity through automated Django Unit Tests. Key features include:
    - Cache Validation (ETags): Implements tests to verify that the server correctly issues ETags. It uses `unittest.mock` to "fake" file modification times, confirming the server returns a `304 Not Modified` status when files are unchanged and a `200 OK` (with a new ETag) immediately after a template update.
    - Template Integrity: Systematically iterates through all non-member routes (About, Mission, Careers, etc.) to ensure the correct HTML templates are being served and that specific "OCP" corporate headers are present in the response body.
    - Route Hardening: Includes tests for 404 error handling to ensure the application gracefully manages invalid URL requests.

* **urls.py**: 
    The routing architecture of the OCP Portal, defining the access points for all guest and internal services:
    - Corporate Public Routes: Maps the primary "Guest" landing pages (Index, About, Mission, etc.) to their respective caching-optimized views.
    - Authentication Engine: Handles the endpoints for the custom OCP registration, login, and logout flows.
    - AI & Vision Directives: Configures the specialized endpoints for real-time asynchronous communication, including:
        - Chat: Endpoints for interacting with the ED-209 LLM and retrieving historical conversation logs.
        - Vision: Dedicated paths for triggering ComfyUI image generation and performing system health checks.
    - Personnel & Asset Management: Routes for the dynamic Asset Feed (including AJAX-based commenting), unique User Profiles, and the high-clearance Security Settings dashboard for rank-escalation logic.

* **views.py**: 
    The core logic engine of the OCP Portal, managing complex interactions between the Django framework and external AI services:
    - Dynamic ETag Caching: Implements a custom `render_with_etag_for_guests` wrapper. This optimizes performance for non-authenticated users by using file modification timestamps (`os.path.getmtime`) to trigger `304 Not Modified` responses, reducing server bandwidth.
    - Hierarchical Security Logic: Enforces an access-level system (1-5). Higher-level executives (Level 4+) gain administrative powers to modify personnel clearance, while lower levels experience more restrictive AI interactions.
    - ED-209 Chat Interface: Orchestrates real-time communication with the Ollama model. It includes a "Hard Guard" protocol to prevent prompt injections and a "Malfunction" randomizer that alters the AI's persona into a hostile state.
    - Vision Synthesis (Asynchronous): Features a sophisticated `generate_vision` pipeline using `httpx` and `asgiref.sync_to_async`. It processes raw user prompts through an AI "theme filter" before sending them to a ComfyUI/Flux .1 backend for image generation.
    - Asset & Community Management: Handles the paginated "Asset Feed," AJAX-based commenting systems, and dynamic user profile rendering.

* **wan22_handler_async.py**: 
    The integration layer for OCP’s "Vision Synthesis" system. This class-based handler automates the interaction with the ComfyUI API:
    - Asynchronous Workflow Management: Utilizes `httpx.AsyncClient` to dispatch JSON-based neural network workflows to the Flux .1 engine. This ensures the web server remains responsive during high-latency AI generation tasks.
    - Dynamic Node Injection: Programmatically traverses and modifies the ComfyUI graph (CLIPTextEncode, KSampler, etc.) to inject randomized seeds, custom OCP visual spec prompts, and image dimensions on-the-fly.
    - Active File Polling: Implements a non-blocking monitoring loop that tracks the ComfyUI output directory. It uses `os.path.exists` and `os.path.getsize` to verify that images are fully rendered and written to disk before passing them back to the database.
    - Contextual Image Processing: Supports "Flux Kontext" workflows, allowing for multi-image reference handling (Image-to-Image) by dynamically mapping input file paths to specific LoadImage nodes.
    - System Self-Healing: Includes a `restart_comfyui` utility that monitors and manages the backend Python process, ensuring the AI services can recover automatically from VRAM or model-loading failures.

## HTML Templates (templates/ocp/)

### Base Layouts
* **base/layout.html**: The master template containing the persistent top navigation and terminal interface.
* **base/index.html**: The primary corporate landing page for the site.
* **base/login.html**: Secure authentication interface for existing personnel.
* **base/register.html**: New member registration portal for Level 1: Guest access.

### Non-Member Corporate Pages
* **non-members/about.html**: Detailed background on Omni Consumer Products.
* **non-members/comingsoon.html**: Teasers for future OCP product initiatives.
* **non-members/currentproducts.html**: Overview of the existing OCP product catalog.
* **non-members/employment.html**: Career opportunities and recruitment information.
* **non-members/mission.html**: The official mission statement from the Chairman of the Board.

### Member Directives
* **members/directives/chat.html**: Interactive terminal for communication with ED-209.
* **members/directives/image_creation.html**: Interface for the ED-209 Vision Generator.

### Member Terminal
* **members/terminal/assetfeed.html**: Paginated gallery showing all user-created images with commenting features.
* **members/terminal/dashboard.html**: The primary member hub displaying clearance levels and authorized tools.

### User Settings
* **members/user_settings/security_settings.html**: Executive tool for Level 4 and 5 users to manage clearance upgrades.
* **members/user_settings/user_profile.html**: Displays detailed personnel files and clearance status.

## JavaScript Logic (static/ocp/js/)
* **assetfeed.js**: 
    The frontend controller for the OCP Asset Gallery, providing a high-fidelity interface for inspecting and discussing generated "Visions":
    - Unified Modal Architecture: Implements a singleton `AssetManager` that handles full-screen image inspection. It uses a "Flex-First" rendering strategy to ensure images are correctly centered before applying coordinate-based transforms.
    - Advanced Inspection Logic: Features a refined zoom and pan system utilizing 2D CSS transforms. It calculates precise mouse-to-image offsets during `onwheel` events to allow users to zoom into specific technical details of OCP assets.
    - Asynchronous Interaction: Manages the "Comment Drawer" via vanilla JavaScript and the Fetch API. It handles CSRF-protected POST requests to update the backend database without a page reload and uses `insertAdjacentHTML` for real-time DOM injection of new comments.
    - State Parity: Refactored to maintain logic parity with `image_creation.js`, ensuring that the UI behavior (zoom scales, panning speed, and cursor states) is consistent across the entire members-only terminal.

* **image_creation.js**: 
    The primary interface controller for the OCP "Vision" Synthesis terminal. This script manages high-stakes asynchronous operations and tactile UI feedback:
    - Persistent Server Heartbeat: Implements an automated `monitorServerStatus` loop using the Fetch API and `AbortController`. It performs 5000ms polling of the Django health-check endpoint to verify the ComfyUI/Flux link, dynamically disabling user inputs if the connection is severed.
    - Asynchronous Generation Pipeline: Orchestrates the CSRF-protected POST requests to the synthesis engine. It manages a robust state machine (`isProcessing`) to prevent multiple simultaneous uplink attempts and provides real-time terminal status updates.
    - Tactical Vision Inspection: Features a sophisticated modal system with coordinate-aware zooming and panning. It calculates scale factors and translation points in real-time to allow users to inspect industrial details within the 10x zoom range.
    - Session-Based History: Dynamically populates a local gallery (`updateVisionGallery`) of visions generated during the current session, allowing users to hot-swap between archived and active data without page reloads.
    - Binary Export Protocol: Handles high-resolution image downloads by converting remote URLs into local Blobs, ensuring that corporate assets are saved with standardized OCP timestamps and naming conventions.

* **script.js**: 
    The primary communications controller for the ED-209 Terminal interface, managing global state and real-time server synchronization:
    - Archive Synchronization: Implements `loadHistory`, an asynchronous routine that retrieves historical directives from the Django backend. It provides visual feedback ("ACCESSING OCP ARCHIVES...") while parsing JSON payloads into the local state.
    - ED-209 Uplink: Manages the `sendToEd209` function, which handles the secure POSTing of user queries. It includes "Input Locking" logic that disables terminal interaction during AI inference to prevent race conditions and redundant server calls.
    - Connection Monitoring: Features a robust `updateChatConnectionStatus` system providing real-time visual cues (Online/Offline) based on the success of backend handshakes, ensuring the user knows the status of the local LLM link.
    - Tactical DOM Management: Automates interface behaviors such as `scrollToBottom` for terminal readability and dynamic class injection for differentiating between User, AI, and System timestamp messages.
    - Security Integration: Includes a specialized `getCookie` utility to extract `csrftoken` values from the document's cookie store, ensuring all JavaScript-initiated fetch requests comply with Django’s security middleware.

* **security_settings.js**: 
    The administrative oversight controller for managing OCP personnel and security clearances:
    - Real-Time Personnel Filtering: Implements a high-performance `keyup` listener that allows administrators to search the personnel database without page refreshes.
    - Multi-Key Indexing: Supports dual-identifier searching, allowing rows to be filtered by both Username (Human Identifier) and Employee Tech ID (System Identifier) for rapid record retrieval.
    - Dynamic DOM Manipulation: Utilizes a non-destructive display-toggle logic to hide or show personnel rows, ensuring that the OCP database remains interactive even during heavy administrative tasks.
    - Security Hierarchy Logic: Serves as the frontend gatekeeper for processing rank upgrades and modifying user access levels within the corporate infrastructure.

## CSS Styling (static/ocp/css/)
* **baseline.css**: 
    The master stylesheet and design framework for the OCP Portal:
    - Centralized Asset Pipeline: Utilizes `@import` rules to orchestrate a modular CSS architecture, loading specific styles for the ED-209 Chat, Vision Synthesis, and Personnel Files.
    - Corporate Visual Identity: Establishes a "Deep Black" (#050505) canvas with high-contrast OCP Blue (#00a2ff) accents to simulate a high-end CRT command interface.
    - Responsive Terminal UI: Features specialized media queries and a flex-based grid system to ensure the terminal remains functional across various display aspect ratios.
    - Brutalist Design Patterns: Implements standardized "Image Holder" containers with contrast-enhanced filtering and sharp-edged borders to reinforce the industrial aesthetic.

* **base/index.css**: 
    The primary layout engine for the OCP landing page, establishing the corporate "Hero" aesthetic:
    - Hero Branding: Implements a high-impact `index-hero` section featuring heavy letter-spacing and a `-webkit-text-stroke` effect to create the signature 1980s corporate logo style.
    - Structural Geometry: Uses a centralized `index-wrapper` and a flex-based `ops-grid` to organize OCP's vertical operations into a professional, scannable terminal layout.
    - Thematic Typography: Sets high-contrast headers with a `border-left` accent to simulate a digital dossier or mission briefing.
    - Legal Compliance Layer: Includes a dedicated `legal-banner` utilizing monospace fonts and dimmed colors to mimic the "fine print" of a dystopian corporate contract.
    
* **base/standard-page-outline.css**: 
    The core structural utility for maintaining OCP's corporate visual uniformity:
    - Unified Container System: Defines the `page-wrapper` and `page-content` parameters to ensure a centered, high-readability dossier layout across all sub-pages.
    - Tactical Imagery Standards: Implements a "Tight Border" protocol for images, featuring OCP-Blue glow effects (`box-shadow`) and high-contrast filtering to simulate digital surveillance feeds.
    - Hierarchical Typography: Standardizes `page-title` and `section-label` styles with heavy uppercase lettering and geometric borders to reinforce a sense of departmental authority.
    - Directive Layout Tools: Provides standardized "Quote Boxes" and "List Styles" (using square bullets) to present mission statements and corporate requirements in a clean, industrial format.

* **members/dashboard.css**: 
    The layout configuration for the OCP Member Command Hub:
    - Tactical Status Bar: Implements a `user-stats-bar` with a low-fi monospace aesthetic, providing a centralized data readout for active session parameters.
    - Adaptive Grid Architecture: Utilizes a CSS Grid (`dashboard-grid`) with `auto-fit` logic to ensure the command cards remain accessible across various terminal resolutions.
    - Clearance-Based Accents: Features a hierarchical color-coding system (Blue, Gold, and Pulsing Red) to visually distinguish between standard directives and high-priority restricted access sectors.
    - Interactive Card Feedback: Employs CSS transitions and box-shadow glows on `dash-card` elements to simulate a high-performance, touch-responsive workstation environment.
    
* **members/directive/chat.css**: 
    The styling framework for the ED-209 "Directive" chat interface:
    - Dynamic Status Indicators: Implements high-visibility `online` and `offline` classes with neon text-shadows to provide immediate feedback on the local LLM connection status.
    - Tactical Container Design: Features a centered, high-contrast `ed-chat-container` with custom scrollbar styling to maintain a unified "workstation" feel.
    - Message Hierarchy: Defines distinct bubble styles for user and AI responses, utilizing `flex-end` and `flex-start` alignment for intuitive conversation flow within the OCP terminal.
    - Interactive Input UI: Styles the command-line input and transmission buttons with focus-state transitions and hover effects to ensure a responsive, high-fidelity user experience.
    
* **members/directive/image_creation.css**: 
    The tactical layout for the OCP AI Vision generator workspace:
    - Synchronized Terminal Aesthetic: Color-matched to the chat interface with a deep-contrast container and OCP-Blue accents to maintain visual continuity across the "Directives" suite.
    - Tri-State Status Logic: Features a dynamic server status bar with CSS-driven states for Online (Green), Offline (Red), and Busy (Amber), including a "Tactical Blink" animation for active uplinks.
    - Precision Inspection Modal: Styles the high-resolution inspection environment with a "Deep OCP black-out" background and coordinate-aware transition effects for image zooming and panning.
    - Integrated History Gallery: Implements a horizontal-scroll "Archive" container with grayscale-to-color hover effects and active-selection glows for hot-swapping between generated assets.
    - Interactive Logic Feedback: Defines distinct button states (Disabled/Active) and auto-expanding text areas to facilitate professional-grade prompt engineering within the corporate terminal.

* **members/grid/assetfeed.css**: 
    Grid-based styling for the paginated OCP image gallery and asset auditing system:
    - CRT Visual Processing: Employs a complex `::after` pseudo-element with dual linear gradients to simulate horizontal scanlines and RGB "ghosting" effects on all archived images.
    - Interactive Asset Cards: Implements the `asset-display` container featuring OCP-Cobalt Blue accents, hover-triggered zoom hints, and a grayscale-to-contrast transition for "enhanced" image inspection.
    - Tactical Metadata Layer: Organizes file technical IDs and approval counts into a high-readability monospace grid, utilizing `backdrop-filter: blur` for authenticated data overlays.
    - Integrated Comment Architecture: Features a "Hidden Drawer" system for personnel feedback, utilizing a column-based flex layout to ensure large-scale input fields remain contained within the 400px card constraints.
    - Lightbox Inspection Environment: Defines a high-z-index `modal` with background blurring to allow for full-screen high-fidelity review of corporate assets.
    
* **members/user_settings/security_settings.css**: 
    The styling framework for the high-clearance Administrative Security Console:
    - Terminal Box Architecture: Employs a centered `terminal-box` layout with a 1px OCP-Blue border and subtle glow to simulate a secure command workstation.
    - Personnel Data Grid: Standardizes administrative tables with sticky headers (`position: sticky`) and high-contrast row styling, including a `high-value` red-tinted background for restricted targets.
    - Dynamic Clearance Badges: Implements a hierarchical color system for user ranks, ranging from standard Level-1 (Gray) to high-threat Level-5 (Red Alert with matching borders).
    - Integrated Search UI: Styles the `terminal-search-bar` with a monospace input and custom-themed scrollbars to maintain the OCP aesthetic during large-scale database queries.
    - Status-Locked Logic: Features "Ghosted" styling for non-interactive elements, reinforcing the sense of strict corporate hierarchy and access control.
    
* **members/user_settings/user_profile.css**: 
    The layout configuration for OCP personnel profile cards and dossiers:
    - Command-Grade Data Grid: Utilizes a flexible `data-grid` system that organizes user metadata into a high-readability two-column layout, with a mobile-responsive fallback to single-column stacking.
    - Personnel Status Monitoring: Implements a live `pulse` animation and green-lit `status-indicator` to simulate real-time heart-rate or connectivity tracking for active employees.
    - Security Clearance Highlighting: Features specialized CSS hooks for Level-4 and Level-5 clearances, applying red text-glow effects to signify high-threat or executive-level data access.
    - Dystopian Branding: Integrates a `security-notice` block with `border-left` accents and dimmed typography to mimic corporate disclaimer text found in restricted OCP files.
    - Tactical Typography: Pairs bold headers with `Courier New` values to reinforce the contrast between the OCP design language and raw system data.

* **non-members/about.css**: 
    The corporate identity stylesheet for the OCP "About Us" briefing:
    - Executive Header Design: Implements a high-impact `header-about` section using `-webkit-text-stroke` and heavy letter-spacing to project institutional authority.
    - Strategic Asset Scaling: Features a localized override for `standard-image` dimensions, expanding the visual footprint of corporate banners to 50% for a more cinematic presentation.
    - High-Contrast Palette: Utilizes a "True Black" background with OCP-Blue borders to maintain the brand’s signature 1980s corporate-minimalist aesthetic for the general public.
    
* **non-members/comingsoon.css**: 
    The aesthetic framework for OCP’s future development and "Delta City" preview pages:
    - Unified Executive Header: Shares the `header-about` styling to ensure brand continuity across all high-level corporate briefings, utilizing Blue-OCP outlines for heavy typography.
    - Standardized Portraiture: Implements an explicit 40% width constraint on the `standard-image` class to maintain a strictly professional aspect ratio for executive profile assets.
    - Minimalist Preview Layout: Uses a centralized, "True Black" structure to emphasize upcoming corporate milestones without over-saturating the public interface with raw system data.

* **non-members/currentproducts.css**: 
    The public catalog framework for OCP’s active product line:
    - Unified Brand Header: Maintains the signature high-contrast Blue-OCP outlined typography to ensure a consistent corporate look.
    - Tactical Scaling: Implements a 60% width override for the `standard-image` class, specifically designed to give large-scale hardware like the ED-209 a dominant and intimidating visual presence.
    - Industrial Presentation: Utilizes a minimalist "True Black" layout to showcase product assets with professional-grade clarity and departmental authority.
    
* **non-members/employment.css**: 
    The aesthetic framework for OCP’s public recruitment and "Employee of the Month" portal:
    - Corporate Header Standardization: Maintains the signature OCP-Blue outlined `h1` and 48px heavy-weight typography for a professional, high-impact first impression.
    - Regimented Image Parameters: Enforces a strict 40% width on the `standard-image` class, specifically calibrated for the "Employee of the Month" banner to ensure a uniform, institutional appearance.
    - High-Efficiency Layout: Utilizes a "True Black" background and centralized content flow to present OCP career directives with corporate clarity and departmental precision.
    
* **non-members/mission.css**: 
    The aesthetic framework for OCP’s public Mission Statement and Executive Directives:
    - Chairman Hero Section: Implements a high-intensity `chairman-hero` container with a 2px signature blue border and contrast filtering to give the "Old Man" portrait a sharp, CRT-inspired visual presence.
    - Monumental Typography: Features a 42px `mission-title` and an italicized `mission-quote` block, utilizing geometric borders to emphasize the uncompromising nature of the OCP vision.
    - Directive Indexing: Styles the `mission-list` with square bullets and blue highlights (`strong` tags) to organize corporate goals into a strictly regimented, high-readability list.
    - Professional Formatting: Defines the `mission-wrapper` with a 1000px constraint and specific line-heights to ensure the corporate briefing remains legible across all high-resolution displays.

## Static Images (static/ocp/images/)
* This directory contains all static corporate branding, UI icons, and background assets used throughout the site.

## Configuration & AI Workflow Files (files/)
* **Flux_No_Image_APP_1_API_1.json**: 
    The primary JSON workflow blueprint for the OCP AI Vision Synthesis engine:
    - Model Architecture: Configured for the `flux1-schnell-fp8` checkpoint, optimized for high-speed, 4-step latent diffusion.
    - Tactical Resolution: Forces a standardized 1280x720 (720p) widescreen aspect ratio, maintaining consistency with the "Asset Feed" grid.
    - Hyper-Specific Prompting: Encapsulates a detailed "Industrial Abandonment" positive prompt, establishing the default cinematic look (fluorescent blues, emergency reds, and high-contrast textures).
    - VRAM Management: Integrates `easy cleanGpuUsed` and `easy clearCacheAll` nodes to ensure the server remains stable during high-frequency generation requests from multiple OCP personnel.
    - API Integration: Designed in "API Format" to allow the Django backend to inject dynamic user prompts directly into the `CLIPTextEncode` node.
    
* **free_mem_API_1.json**: 
    A specialized administrative workflow for VRAM optimization and memory management:
    - Automated Garbage Collection: Triggers the `easy clearCacheAll` and `easy cleanGpuUsed` nodes to force-release occupied VRAM back to the system.
    - Leak Prevention: Designed to be called between heavy generation batches to prevent cumulative memory overhead during multi-user "Vision Directive" sessions.
    - Minimalist Footprint: Utilizes a lightweight `LoadImage` node as a sequential anchor to execute the memory-clearing logic without the overhead of a full diffusion pass.
    - API-Only Utility: Functions as a non-visual background task, allowing the OCP backend to maintain server health without interrupting the user terminal's frontend experience.
