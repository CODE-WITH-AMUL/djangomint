#--------------------------[IMPORT MODELS]--------------------------#
import os, re, sys, time, shutil
import threading
from dataclasses import dataclass
from typing import Optional, Generator, List, Tuple
from contextlib import contextmanager
from colorama import init, Fore, Style, Back

# Initialize colorama for cross-platform colored output
init(autoreset=True)


#--------------------------[CONFIGURATION]--------------------------#

@dataclass(frozen=True)
class Config:
    """Immutable configuration container"""
    VERSION: str = "2.0.0"
    DEVELOPER: str = "Amul Sharma"
    GITHUB_URL: str = "https://github.com/CODE-WITH-AMUL"
    DOCS_URL: str = "https://djangomint.readthedocs.io"
    ISSUES_URL: str = "https://github.com/CODE-WITH-AMUL/djangomint/issues"
    REPO_URL: str = "https://github.com/CODE-WITH-AMUL/djangomint"
    PROJECT_NAME: str = "DjangoMint"

CONFIG = Config()

#--------------------------[THEME & STYLING]--------------------------#

class Theme:
    """Professional color theme with gradient and accent colors"""
    # Primary palette
    PRIMARY = Fore.CYAN
    PRIMARY_BRIGHT = Fore.LIGHTCYAN_EX
    SECONDARY = Fore.MAGENTA
    SECONDARY_BRIGHT = Fore.LIGHTMAGENTA_EX
    
    # Accent colors
    ACCENT = Fore.BLUE
    ACCENT_BRIGHT = Fore.LIGHTBLUE_EX
    GOLD = Fore.YELLOW
    GOLD_BRIGHT = Fore.LIGHTYELLOW_EX
    
    # Status colors
    SUCCESS = Fore.GREEN
    SUCCESS_BRIGHT = Fore.LIGHTGREEN_EX
    ERROR = Fore.RED
    ERROR_BRIGHT = Fore.LIGHTRED_EX
    WARNING = Fore.YELLOW
    INFO = Fore.WHITE
    INFO_BRIGHT = Fore.LIGHTWHITE_EX
    
    # Style modifiers
    DIM = Style.DIM
    BRIGHT = Style.BRIGHT
    NORMAL = Style.NORMAL
    RESET = Style.RESET_ALL
    
    # Background colors
    BG_DARK = Back.BLACK
    BG_ACCENT = Back.BLUE
    BG_SUCCESS = Back.GREEN
    BG_ERROR = Back.RED
    
    @classmethod
    def gradient_text(cls, text: str, start_color: str = PRIMARY, end_color: str = SECONDARY) -> str:
        """Create a gradient effect across text"""
        colors = [start_color, Fore.CYAN, Fore.BLUE, Fore.MAGENTA, end_color]
        result = ""
        for i, char in enumerate(text):
            color_idx = int((i / len(text)) * (len(colors) - 1))
            result += f"{colors[color_idx]}{char}"
        return result + cls.RESET
    
    @classmethod
    def highlight(cls, text: str, color: str = PRIMARY) -> str:
        """Highlight important text"""
        return f"{color}{cls.BRIGHT}{text}{cls.RESET}"

#--------------------------[TERMINAL UTILITIES]--------------------------#

class Terminal:
    """Terminal interaction utilities with ANSI tracking awareness"""
    
    _width: Optional[int] = None
    _height: Optional[int] = None
    ANSI_ESCAPE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    
    @classmethod
    def visible_len(cls, text: str) -> int:
        """Calculate the string length excluding ANSI color escape sequences"""
        return len(cls.ANSI_ESCAPE.sub('', text))
    
    @classmethod
    def width(cls) -> int:
        """Get terminal width with fallback"""
        if cls._width is None:
            try:
                cls._width = shutil.get_terminal_size().columns
            except Exception:
                cls._width = 100
        return cls._width
    
    @classmethod
    def height(cls) -> int:
        """Get terminal height with fallback"""
        if cls._height is None:
            try:
                cls._height = shutil.get_terminal_size().lines
            except Exception:
                cls._height = 30
        return cls._height
    
    @classmethod
    def clear(cls) -> None:
        """Clear screen cross-platform"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @classmethod
    def truncate(cls, text: str, max_len: int = 56) -> str:
        """Truncate text safely with ellipsis accounting for visible characters"""
        v_len = cls.visible_len(text)
        if v_len <= max_len:
            return text
        plain_text = cls.ANSI_ESCAPE.sub('', text)
        return plain_text[:max_len-3] + "..."
    
    @classmethod
    def center_text(cls, text: str, width: int = None) -> str:
        """Center text accounting for ANSI codes"""
        if width is None:
            width = cls.width()
        v_len = cls.visible_len(text)
        padding = max(0, (width - v_len) // 2)
        return ' ' * padding + text


#--------------------------[PROFESSIONAL UI COMPONENTS]--------------------------#

class BoxStyles:
    """Premium box drawing styles"""
    SINGLE = {
        'tl': '┌', 'tr': '┐', 'bl': '└', 'br': '┘',
        'h': '─', 'v': '│', 'lc': '├', 'rc': '┤',
        'tc': '┬', 'bc': '┴', 'c': '┼'
    }
    DOUBLE = {
        'tl': '╔', 'tr': '╗', 'bl': '╚', 'br': '╝',
        'h': '═', 'v': '║', 'lc': '╠', 'rc': '╣',
        'tc': '╦', 'bc': '╩', 'c': '╬'
    }
    ROUNDED = {
        'tl': '╭', 'tr': '╮', 'bl': '╰', 'br': '╯',
        'h': '─', 'v': '│', 'lc': '├', 'rc': '┤',
        'tc': '┬', 'bc': '┴', 'c': '┼'
    }
    HEAVY = {
        'tl': '┏', 'tr': '┓', 'bl': '┗', 'br': '┛',
        'h': '━', 'v': '┃', 'lc': '┣', 'rc': '┫',
        'tc': '┳', 'bc': '┻', 'c': '╋'
    }

class Box:
    """Professional box drawing with multiple styles"""
    
    @classmethod
    def create_box(cls, content: List[str], title: str = "", 
                   style: dict = BoxStyles.ROUNDED, 
                   border_color: str = Theme.SECONDARY,
                   title_color: str = Theme.PRIMARY_BRIGHT,
                   content_color: str = Theme.INFO,
                   padding: int = 2,
                   max_width: int = None) -> str:
        """Create a professional looking box with content"""
        
        if max_width is None:
            max_width = min(Terminal.width() - 4, 90)
        
        inner_width = max_width - 4  # Account for borders and padding
        
        # Process content lines to fit width
        processed_lines = []
        for line in content:
            if Terminal.visible_len(line) > inner_width:
                # Word wrap logic
                words = line.split()
                current_line = ""
                for word in words:
                    test_line = f"{current_line} {word}".strip()
                    if Terminal.visible_len(test_line) <= inner_width:
                        current_line = test_line
                    else:
                        if current_line:
                            processed_lines.append(current_line)
                        current_line = word
                if current_line:
                    processed_lines.append(current_line)
            else:
                processed_lines.append(line)
        
        # Build the box
        border = f"{border_color}{Theme.DIM}"
        reset = Theme.RESET
        
        lines = []
        
        # Top border with title
        if title:
            title_text = f" {title} "
            top_line = f"{border}{style['tl']}{style['h']*3}{title_color}{Theme.BRIGHT}{title_text}{border}{style['h']*max(0, max_width - len(title_text) - 8)}{style['tr']}{reset}"
        else:
            top_line = f"{border}{style['tl']}{style['h']*(max_width-2)}{style['tr']}{reset}"
        lines.append(top_line)
        
        # Empty line for padding
        for _ in range(padding - 1):
            lines.append(f"{border}{style['v']}{' '*(max_width-2)}{style['v']}{reset}")
        
        # Content lines
        for line in processed_lines:
            v_len = Terminal.visible_len(line)
            padding_right = max_width - v_len - 4
            lines.append(f"{border}{style['v']}{reset}  {content_color}{line}{' '*padding_right}{border}{style['v']}{reset}")
        
        # Empty line for padding
        for _ in range(padding - 1):
            lines.append(f"{border}{style['v']}{' '*(max_width-2)}{style['v']}{reset}")
        
        # Bottom border
        bottom_line = f"{border}{style['bl']}{style['h']*(max_width-2)}{style['br']}{reset}"
        lines.append(bottom_line)
        
        return '\n'.join(lines)
    
    @classmethod
    def section_header(cls, title: str, width: int = None) -> str:
        """Create a professional section header"""
        if width is None:
            width = min(Terminal.width() - 4, 80)
        
        icon_map = {
            'rocket': '🚀', 'gear': '⚙️', 'star': '⭐',
            'check': '✅', 'error': '❌', 'warning': '⚠️',
            'info': 'ℹ️', 'folder': '📁', 'file': '📄',
            'key': '🔑', 'lock': '🔒', 'world': '🌍',
            'tools': '🛠️', 'package': '📦', 'terminal': '💻'
        }
        
        return f"\n{Theme.SECONDARY}{Theme.DIM}{'─'*3} {Theme.PRIMARY_BRIGHT}{Theme.BRIGHT}{title} {Theme.SECONDARY}{Theme.DIM}{'─'*(width - len(title) - 6)}{Theme.RESET}\n"


#--------------------------[ENHANCED BANNER]--------------------------#

class Banner:
    """Professional animated banner with modern design"""
    
    LOGO_ART = f"""
{Theme.GOLD}     ██████╗      ██╗ █████╗ ███╗   ██╗ ██████╗  ██████╗ 
     ██╔══██╗     ██║██╔══██╗████╗  ██║██╔════╝ ██╔═══██╗
{Theme.PRIMARY}     ██║  ██║     ██║███████║██╔██╗ ██║██║  ███╗██║   ██║
     ██║  ██║██   ██║██╔══██║██║╚██╗██║██║   ██║██║   ██║
{Theme.SECONDARY}     ██████╔╝╚█████╔╝██║  ██║██║ ╚████║╚██████╔╝╚██████╔╝
     ╚═════╝  ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝  ╚═════╝ 
{Theme.RESET}"""
    
    SUBTITLE = f"{Theme.PRIMARY}▸ {Theme.GOLD}Premium Django Boilerplate Generator {Theme.PRIMARY}◂{Theme.RESET}"
    TAGLINE = f"{Theme.DIM}Professional CLI Toolkit for Rapid Development{Theme.RESET}"
    
    @classmethod
    def show(cls) -> None:
        """Display the premium animated banner"""
        Terminal.clear()
        
        # Print decorative top border
        width = min(Terminal.width() - 4, 80)
        print(f"{Theme.SECONDARY}{Theme.DIM}╔{'═'*(width-2)}╗{Theme.RESET}")
        
        # Logo with gradual reveal effect
        for line in cls.LOGO_ART.strip().split('\n'):
            if line.strip():
                print(f"{Theme.SECONDARY}{Theme.DIM}║{Theme.RESET}{Terminal.center_text(line, width-2)}{Theme.SECONDARY}{Theme.DIM}║{Theme.RESET}")
        
        # Separator
        print(f"{Theme.SECONDARY}{Theme.DIM}╠{'═'*(width-2)}╣{Theme.RESET}")
        
        # Subtitle
        print(f"{Theme.SECONDARY}{Theme.DIM}║{Theme.RESET}{Terminal.center_text(cls.SUBTITLE, width-2)}{Theme.SECONDARY}{Theme.DIM}║{Theme.RESET}")
        print(f"{Theme.SECONDARY}{Theme.DIM}║{Theme.RESET}{Terminal.center_text(cls.TAGLINE, width-2)}{Theme.SECONDARY}{Theme.DIM}║{Theme.RESET}")
        
        # Information section
        print(f"{Theme.SECONDARY}{Theme.DIM}╠{'═'*(width-2)}╣{Theme.RESET}")
        
        info_data = [
            (f"⚡ Version", CONFIG.VERSION),
            (f"👨‍💻 Developer", CONFIG.DEVELOPER),
            (f"📦 Repository", CONFIG.REPO_URL),
        ]
        
        for label, value in info_data:
            line = f"  {Theme.GOLD}{label}{Theme.RESET}: {Theme.INFO}{value}{Theme.RESET}"
            print(f"{Theme.SECONDARY}{Theme.DIM}║{Theme.RESET}{line}{' '*(width - Terminal.visible_len(line) - 2)}{Theme.SECONDARY}{Theme.DIM}║{Theme.RESET}")
        
        # Bottom border
        print(f"{Theme.SECONDARY}{Theme.DIM}╚{'═'*(width-2)}╝{Theme.RESET}")
        print()


#--------------------------[ENHANCED ANIMATIONS]--------------------------#

class Animator:
    """Premium animation engine with smooth transitions"""
    
    SPINNER_FRAMES = {
        'dots': ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷'],
        'pulse': ['█', '▓', '▒', '░', '▒', '▓'],
        'bounce': ['[=    ]', '[ =   ]', '[  =  ]', '[   = ]', '[    =]', '[   = ]', '[  =  ]', '[ =   ]'],
        'snake': ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'],
        'moon': ['🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘'],
        'clock': ['🕐', '🕑', '🕒', '🕓', '🕔', '🕕', '🕖', '🕗', '🕘', '🕙', '🕚', '🕛'],
    }
    
    @classmethod
    def typewriter(cls, text: str, delay: float = 0.03, 
                   color: str = Theme.PRIMARY_BRIGHT, 
                   end: str = '\n') -> None:
        """Professional typewriter effect with smooth rendering"""
        sys.stdout.write(f"{color}{Theme.BRIGHT}")
        try:
            for char in text:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(delay)
        finally:
            sys.stdout.write(f"{Theme.RESET}{end}")
            sys.stdout.flush()
    
    @classmethod
    def countdown(cls, seconds: int, message: str = "Starting in") -> None:
        """Animated countdown display"""
        for i in range(seconds, 0, -1):
            sys.stdout.write(f"\r{Theme.GOLD}{message} {Theme.PRIMARY_BRIGHT}{i}{Theme.RESET}... ")
            sys.stdout.flush()
            time.sleep(1)
        sys.stdout.write(f"\r{' '*50}\r")
    
    @classmethod
    @contextmanager
    def spinner(cls, message: str = "Processing", 
                style: str = 'dots',
                success_message: str = None,
                error_message: str = None) -> Generator[None, None, None]:
        """
        Professional spinner with customizable styles
        
        Usage:
            with Animator.spinner("Installing dependencies", style='moon'):
                # Your code here
                time.sleep(2)
        """
        frames = cls.SPINNER_FRAMES.get(style, cls.SPINNER_FRAMES['dots'])
        stop_event = threading.Event()
        error_occurred = False
        
        def animate():
            i = 0
            while not stop_event.is_set():
                frame = frames[i % len(frames)]
                status = f"\r  {Theme.SECONDARY}{frame}{Theme.RESET} {Theme.PRIMARY}{message}..."
                sys.stdout.write(status)
                sys.stdout.flush()
                time.sleep(0.08)
                i += 1
        
        spinner_thread = threading.Thread(target=animate, daemon=True)
        spinner_thread.start()
        
        try:
            yield
        except Exception:
            error_occurred = True
            raise
        finally:
            stop_event.set()
            spinner_thread.join()
            
            # Clear the spinner line
            clear_line = '\r' + ' ' * (Terminal.visible_len(message) + 20) + '\r'
            sys.stdout.write(clear_line)
            
            # Show final status
            if error_occurred and error_message:
                Status.error(error_message)
            elif not error_occurred and success_message:
                Status.success(success_message)
            
            sys.stdout.flush()
    
    @classmethod
    def progress_bar(cls, current: int, total: int, 
                     width: int = 40, 
                     prefix: str = "", 
                     suffix: str = "") -> str:
        """Premium progress bar with gradient effect"""
        ratio = max(0.0, min(1.0, current / total))
        filled = int(width * ratio)
        
        # Create gradient effect in the progress bar
        bar = ""
        for i in range(filled):
            if i < width * 0.3:
                bar += f"{Theme.SUCCESS}█"
            elif i < width * 0.7:
                bar += f"{Theme.GOLD}█"
            else:
                bar += f"{Theme.PRIMARY}█"
        
        bar += f"{Theme.DIM}{'░' * (width - filled)}{Theme.RESET}"
        percent = int(ratio * 100)
        
        return f"{prefix}[{bar}] {Theme.BRIGHT}{percent}%{Theme.RESET} ({current}/{total}) {suffix}"

    @classmethod
    def loading_sequence(cls, steps: List[Tuple[str, float]], 
                        style: str = 'dots') -> None:
        """Run a sequence of loading steps with animations"""
        for step_name, duration in steps:
            with cls.spinner(step_name, style=style):
                time.sleep(duration)


#--------------------------[STATUS REPORTING]--------------------------#

class Status:
    """Premium status reporting with icons and formatting"""
    
    ICONS = {
        'success': ('✓', Theme.SUCCESS_BRIGHT),
        'error': ('✗', Theme.ERROR_BRIGHT),
        'warning': ('⚠', Theme.WARNING),
        'info': ('ℹ', Theme.SECONDARY_BRIGHT),
        'working': ('⚙', Theme.PRIMARY_BRIGHT),
        'done': ('✅', Theme.SUCCESS_BRIGHT),
        'failed': ('❌', Theme.ERROR_BRIGHT),
        'star': ('⭐', Theme.GOLD_BRIGHT),
        'rocket': ('🚀', Theme.PRIMARY_BRIGHT),
        'lock': ('🔒', Theme.SECONDARY_BRIGHT),
        'key': ('🔑', Theme.GOLD),
        'bulb': ('💡', Theme.GOLD_BRIGHT),
        'target': ('🎯', Theme.PRIMARY_BRIGHT),
    }
    
    @classmethod
    def show(cls, status_type: str, message: str, 
             inline: bool = False, timestamp: bool = False) -> None:
        """Professional status display with optional timestamp"""
        icon, color = cls.ICONS.get(status_type, ('›', Theme.PRIMARY))
        
        if timestamp:
            current_time = time.strftime("%H:%M:%S")
            prefix = f"{Theme.DIM}[{current_time}]{Theme.RESET}"
        else:
            prefix = ""
        
        end = " " if inline else "\n"
        output = f"\r{prefix} {color}{icon}{Theme.RESET} {message}"
        print(output, end=end, flush=True)
    
    @classmethod
    def success(cls, message: str) -> None: 
        cls.show('success', f"{Theme.SUCCESS}{message}{Theme.RESET}")
    
    @classmethod
    def error(cls, message: str) -> None: 
        cls.show('error', f"{Theme.ERROR}{message}{Theme.RESET}")
    
    @classmethod
    def info(cls, message: str) -> None: 
        cls.show('info', f"{Theme.INFO}{message}{Theme.RESET}")
    
    @classmethod
    def warning(cls, message: str) -> None: 
        cls.show('warning', f"{Theme.WARNING}{message}{Theme.RESET}")
    
    @classmethod
    def step(cls, step_num: int, message: str) -> None:
        """Show a numbered step"""
        cls.show('target', f"{Theme.PRIMARY}Step {step_num}:{Theme.RESET} {message}")
    
    @classmethod
    def checklist(cls, items: List[Tuple[bool, str]]) -> None:
        """Display a professional checklist"""
        for completed, item in items:
            if completed:
                cls.show('done', f"{Theme.SUCCESS}{item}{Theme.RESET}")
            else:
                cls.show('failed', f"{Theme.ERROR}{item}{Theme.RESET}")


#--------------------------[DIVIDER AND SECTION]--------------------------#

class Divider:
    """Professional dividers and separators"""
    
    @classmethod
    def simple(cls, width: int = None) -> str:
        """Simple thin divider"""
        if width is None:
            width = min(Terminal.width() - 4, 80)
        return f"{Theme.DIM}{'─' * width}{Theme.RESET}"
    
    @classmethod
    def double(cls, width: int = None) -> str:
        """Double line divider"""
        if width is None:
            width = min(Terminal.width() - 4, 80)
        return f"{Theme.DIM}{'═' * width}{Theme.RESET}"
    
    @classmethod
    def dotted(cls, width: int = None) -> str:
        """Dotted divider"""
        if width is None:
            width = min(Terminal.width() - 4, 80)
        return f"{Theme.DIM}{'·' * width}{Theme.RESET}"
    
    @classmethod
    def gradient(cls, width: int = None) -> str:
        """Gradient divider effect"""
        if width is None:
            width = min(Terminal.width() - 4, 60)
        chars = "█▓▒░"
        result = ""
        for i in range(width):
            idx = int((i / width) * len(chars))
            result += f"{Theme.DIM}{chars[idx]}{Theme.RESET}"
        return result
    
    @classmethod
    def section(cls, title: str, width: int = None) -> str:
        """Section divider with title"""
        if width is None:
            width = min(Terminal.width() - 4, 80)
        
        title_text = f" {title} "
        remaining = width - len(title_text) - 4
        left = remaining // 2
        right = remaining - left
        
        return (f"\n{Theme.SECONDARY}{Theme.DIM}{'━'*left}"
                f"{Theme.PRIMARY_BRIGHT}{Theme.BRIGHT}{title_text}"
                f"{Theme.SECONDARY}{Theme.DIM}{'━'*right}{Theme.RESET}\n")


#--------------------------[APP VERIFICATION ENGINE]--------------------------#

def check_environment() -> bool:
    """Validates structural pre-flight conditions"""
    print(Divider.section("Environment Verification"))
    
    checks = [
        ("Python 3.8+", sys.version_info >= (3, 8)),
        ("Color Support", True),
        ("Terminal Size", Terminal.width() >= 60),
    ]
    
    all_passed = True
    results = []
    
    for name, passed in checks:
        results.append((passed, f"{name:<30} {'✅' if passed else '❌'}"))
        if not passed:
            all_passed = False
    
    Status.checklist(results)
    return all_passed


#--------------------------[WELCOME SCREEN]--------------------------#

def show_welcome_screen():
    """Professional welcome screen with feature highlights"""
    Banner.show()
    
    # Welcome message
    Animator.typewriter(
        "Welcome to the Premium Django Development Toolkit",
        delay=0.02,
        color=Theme.GOLD_BRIGHT
    )
    
    time.sleep(0.5)
    
    # Feature highlights
    features_box = Box.create_box(
        [
            f"{Theme.GOLD}🚀{Theme.RESET} Rapid Django project scaffolding",
            f"{Theme.GOLD}⚡{Theme.RESET} Built-in authentication system",
            f"{Theme.GOLD}🎨{Theme.RESET} Beautiful UI components & templates",
            f"{Theme.GOLD}🔒{Theme.RESET} Security best practices included",
            f"{Theme.GOLD}📦{Theme.RESET} Production-ready configurations",
            f"{Theme.GOLD}🛠️{Theme.RESET} Developer-friendly CLI tools",
        ],
        title="🌟 Features",
        style=BoxStyles.DOUBLE,
        border_color=Theme.SECONDARY,
        title_color=Theme.GOLD_BRIGHT
    )
    print(features_box)
    print()
    
    # Quick start guide
    quick_start = Box.create_box(
        [
            f"1. {Theme.PRIMARY}Create project{Theme.RESET}   → Select from menu",
            f"2. {Theme.PRIMARY}Add apps{Theme.RESET}        → Automatic setup",
            f"3. {Theme.PRIMARY}Configure{Theme.RESET}       → Auto-configuration",
            f"4. {Theme.PRIMARY}Run server{Theme.RESET}      → Start developing",
        ],
        title="📋 Quick Start",
        style=BoxStyles.ROUNDED,
        border_color=Theme.ACCENT,
        title_color=Theme.PRIMARY_BRIGHT
    )
    print(quick_start)
    print()


#--------------------------[MAIN ENTRYPOINT]--------------------------#

def main() -> None:
    """Core runtime orchestration routine with premium UI"""
    
    # Show welcome screen
    show_welcome_screen()
    
    # Environment check
    Status.info("Running system diagnostics...")
    
    with Animator.spinner("Verifying environment", style='dots',
                         success_message="Environment checks passed"):
        time.sleep(1.5)  # Simulate checks
        
        if not check_environment():
            print()
            Status.error("Environment verification failed")
            error_box = Box.create_box(
                ["Please ensure all requirements are met before proceeding."],
                title="❌ Error",
                style=BoxStyles.DOUBLE,
                border_color=Theme.ERROR
            )
            print(error_box)
            sys.exit(1)
    
    print()
    Status.success("All systems operational!")
    
    print()
    print(Divider.section("Launching Application"))
    print()
    
    # Countdown for dramatic effect
    Animator.countdown(3, "Initializing in")
    
    try:
        # Import and run main application
        from cli.service.cmd import main_app
        main_app()
        
    except ImportError as e:
        print()
        Status.error(f"Module import failed: {e}")
        
        help_box = Box.create_box(
            [
                f"{Theme.WARNING}⚠{Theme.RESET} Make sure you're in the project root directory",
                f"{Theme.INFO}💡{Theme.RESET} Try: cd djangomint",
                f"{Theme.INFO}📚{Theme.RESET} Docs: {CONFIG.DOCS_URL}",
            ],
            title="🔧 Troubleshooting",
            style=BoxStyles.ROUNDED,
            border_color=Theme.WARNING
        )
        print(help_box)
        sys.exit(1)
        
    except KeyboardInterrupt:
        print(f"\n\n{Theme.WARNING}⚠ Operation cancelled by user{Theme.RESET}")
        
        goodbye_box = Box.create_box(
            [f"{Theme.GOLD}Thank you for using {CONFIG.PROJECT_NAME}!{Theme.RESET}"],
            title="👋 Goodbye",
            style=BoxStyles.ROUNDED,
            border_color=Theme.PRIMARY
        )
        print(goodbye_box)
        sys.exit(0)
        
    except Exception as e:
        print(f"\n{Theme.ERROR}✗ Unexpected error: {e}{Theme.RESET}")
        
        error_box = Box.create_box(
            [
                f"{Theme.ERROR}Error: {str(e)[:50]}...{Theme.RESET}",
                f"{Theme.INFO}Report issues: {CONFIG.ISSUES_URL}{Theme.RESET}",
            ],
            title="❌ Critical Error",
            style=BoxStyles.DOUBLE,
            border_color=Theme.ERROR
        )
        print(error_box)
        sys.exit(1)


#--------------------------[ENTRYPOINT]--------------------------#

if __name__ == "__main__":
    try:
        main()
    except Exception as critical_error:
        print(f"\n{Theme.ERROR}Critical failure: {critical_error}{Theme.RESET}")
        sys.exit(1)