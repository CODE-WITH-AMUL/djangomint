import os
import re
from cli.service.display import print_success, print_warning


def project_name_from_path(current_dir):
    """Extract project name from current directory path"""
    return os.path.basename(current_dir.rstrip(os.sep))


def update_settings_file(settings_file):
    """Update settings.py to add 'accounts' to INSTALLED_APPS"""
    try:
        with open(settings_file, 'r') as f:
            lines = f.readlines()
        
        # Check if 'accounts' is already in INSTALLED_APPS
        content = ''.join(lines)
        if "'accounts'" in content or '"accounts"' in content:
            print_warning("'accounts' already in INSTALLED_APPS")
            return
        
        # Find the INSTALLED_APPS section
        in_installed_apps = False
        installed_apps_start = -1
        installed_apps_end = -1
        bracket_count = 0
        
        for i, line in enumerate(lines):
            if 'INSTALLED_APPS' in line and '=' in line:
                installed_apps_start = i
                in_installed_apps = True
                bracket_count += line.count('[') - line.count(']')
                
                # Check if list starts and ends on same line
                if bracket_count == 0 and ']' in line:
                    installed_apps_end = i
                    break
                continue
            
            if in_installed_apps:
                bracket_count += line.count('[') - line.count(']')
                if bracket_count == 0:
                    installed_apps_end = i
                    break
        
        if installed_apps_start >= 0 and installed_apps_end >= 0:
            # Get indentation from existing apps
            indent = "    "  # Default indentation
            
            # Find indentation from the first app in the list
            for i in range(installed_apps_start + 1, installed_apps_end + 1):
                stripped = lines[i].strip()
                if stripped and not stripped.startswith('#') and not stripped.startswith(']'):
                    indent = lines[i][:len(lines[i]) - len(lines[i].lstrip())]
                    break
            
            # Check if this is a single-line list
            if installed_apps_start == installed_apps_end:
                # Single line INSTALLED_APPS, convert to multi-line
                line = lines[installed_apps_start]
                # Find the position of '['
                bracket_pos = line.index('[')
                before_bracket = line[:bracket_pos + 1]
                after_bracket = line[bracket_pos + 1:]
                
                # Extract existing apps
                existing_apps = after_bracket.replace(']', '').strip()
                
                # Create multi-line format
                if existing_apps:
                    apps_list = [app.strip() for app in existing_apps.split(',') if app.strip()]
                    new_lines = [before_bracket + '\n']
                    for app in apps_list:
                        new_lines.append(f"{indent}{app},\n")
                    new_lines.append(f"{indent}'accounts',\n")
                    new_lines.append(']\n')
                else:
                    new_lines = [
                        before_bracket + '\n',
                        f"{indent}'accounts',\n"
                        ']\n'
                    ]
                
                # Replace the single line with multi-line format
                lines[installed_apps_start:installed_apps_end + 1] = new_lines
            
            else:
                # Multi-line list - add accounts before the closing bracket
                
                # Find the last app line before the closing bracket
                last_app_line_idx = installed_apps_end - 1
                while last_app_line_idx > installed_apps_start:
                    stripped = lines[last_app_line_idx].strip()
                    if stripped and not stripped.startswith('#'):
                        break
                    last_app_line_idx -= 1
                
                # Add comma to the last app if needed
                if last_app_line_idx > installed_apps_start:
                    last_line = lines[last_app_line_idx].rstrip()
                    if last_line and not last_line.endswith(','):
                        lines[last_app_line_idx] = last_line + ',\n'
                
                # Insert the accounts app before the closing bracket
                lines.insert(installed_apps_end, f"{indent}'accounts',\n")
            
            # Write the updated content
            with open(settings_file, 'w') as f:
                f.writelines(lines)
            
            print_success("Added 'accounts' to INSTALLED_APPS")
        else:
            print_warning("Could not find INSTALLED_APPS in settings.py")
            
    except Exception as e:
        print_warning(f"Error updating settings.py: {e}")


def update_urls_file(urls_file):
    """Update main urls.py to include accounts.urls"""
    try:
        with open(urls_file, 'r') as f:
            content = f.read()
        
        # Check if accounts.urls is already included
        if 'accounts.urls' in content or "accounts.urls" in content:
            print_warning("accounts.urls already in urlpatterns")
            return
        
        # Add import for include if not present
        if 'from django.urls import' in content:
            # Check if include is already imported
            if 'include' not in content:
                content = re.sub(
                    r'from django.urls import ([^\n]+)',
                    r'from django.urls import \1, include',
                    content
                )
        elif 'from django.conf.urls import' in content:
            # Add the import statement
            content = re.sub(
                r'(from django\.conf\.urls import [^\n]+)',
                r'from django.urls import path, include\n\1',
                content
            )
        else:
            # Add import if not present at all
            # Find the last import statement
            import_pattern = r'(import [^\n]+\n)(?!import )'
            last_import = re.search(r'(?:import|from)\s+[^\n]+\n(?!.*(?:import|from)\s+)', content, re.DOTALL)
            if last_import:
                insert_pos = last_import.end()
                content = content[:insert_pos] + 'from django.urls import path, include\n' + content[insert_pos:]
        
        # Find urlpatterns and add accounts path
        pattern = r"(urlpatterns\s*=\s*\[)([\s\S]*?)(\])"
        match = re.search(pattern, content)
        
        if match:
            start = match.group(1)
            middle = match.group(2)
            end = match.group(3)
            
            # Add accounts path with proper formatting
            if middle.strip():
                # Check if the last line ends with a comma
                last_line = middle.rstrip().split('\n')[-1] if middle.rstrip() else ''
                
                if last_line.strip() and not last_line.rstrip().endswith(','):
                    # Add comma to the last line
                    middle_lines = middle.split('\n')
                    for i in range(len(middle_lines) - 1, -1, -1):
                        if middle_lines[i].strip():
                            middle_lines[i] = middle_lines[i].rstrip() + ','
                            break
                    middle = '\n'.join(middle_lines)
                
                accounts_path = "\n    path('accounts/', include('accounts.urls')),"
                new_middle = middle.rstrip() + accounts_path + "\n"
            else:
                # Empty list
                new_middle = "\n    path('accounts/', include('accounts.urls')),\n"
            
            new_content = content.replace(match.group(0), start + new_middle + end)
            
            with open(urls_file, 'w') as f:
                f.write(new_content)
            
            print_success("Updated main urls.py with accounts URL patterns")
        else:
            print_warning("Could not find urlpatterns in urls.py")
            
    except Exception as e:
        print_warning(f"Error updating urls.py: {e}")