#!/usr/bin/env python3
"""
Project Mapper - Generates project-map.json for LLM-assisted code changes

This script analyzes a Next.js project and creates a comprehensive mapping
that helps LLMs understand where to make specific UI changes without 
reading the entire codebase.
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
import ast

class ProjectMapper:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.map_data = {
            "project_info": {},
            "ui_elements": {},
            "components": {},
            "styling": {},
            "file_purposes": {},
            "quick_references": {}
        }
        
    def analyze_project(self) -> Dict[str, Any]:
        """Main method to analyze the entire project"""
        print("🔍 Analyzing project structure...")
        
        # Analyze package.json for project info
        self._analyze_package_json()
        
        # Analyze components and UI elements
        self._analyze_components()
        
        # Analyze styling and themes
        self._analyze_styling()
        
        # Generate quick references for common queries
        self._generate_quick_references()
        
        # Add file purposes
        self._add_file_purposes()
        
        print("✅ Analysis complete!")
        return self.map_data
    
    def _analyze_package_json(self):
        """Extract project information from package.json"""
        package_file = self.project_root / "package.json"
        if package_file.exists():
            with open(package_file, 'r') as f:
                package_data = json.load(f)
                
            self.map_data["project_info"] = {
                "name": package_data.get("name", "unknown"),
                "version": package_data.get("version", "unknown"),
                "framework": "Next.js" if "next" in package_data.get("dependencies", {}) else "React",
                "styling": self._detect_styling_framework(package_data),
                "ui_library": self._detect_ui_library(package_data),
                "dependencies": list(package_data.get("dependencies", {}).keys())
            }
    
    def _detect_styling_framework(self, package_data: Dict) -> str:
        """Detect styling framework from dependencies"""
        deps = package_data.get("dependencies", {})
        if "tailwindcss" in deps or "@tailwindcss/postcss" in package_data.get("devDependencies", {}):
            return "Tailwind CSS"
        elif "styled-components" in deps:
            return "Styled Components"
        elif "@emotion/react" in deps:
            return "Emotion"
        return "CSS"
    
    def _detect_ui_library(self, package_data: Dict) -> str:
        """Detect UI library from dependencies"""
        deps = package_data.get("dependencies", {})
        if "@radix-ui" in str(deps):
            return "Radix UI / shadcn/ui"
        elif "@mui/material" in deps:
            return "Material-UI"
        elif "antd" in deps:
            return "Ant Design"
        return "Custom"
    
    def _analyze_components(self):
        """Analyze React components and extract UI elements"""
        src_dir = self.project_root / "src"
        if not src_dir.exists():
            return
            
        # Find all React/TypeScript files
        component_files = []
        for pattern in ["**/*.tsx", "**/*.jsx", "**/*.ts", "**/*.js"]:
            component_files.extend(src_dir.glob(pattern))
        
        for file_path in component_files:
            if file_path.name.startswith('.'):
                continue
                
            try:
                self._analyze_component_file(file_path)
            except Exception as e:
                print(f"⚠️  Error analyzing {file_path}: {e}")
    
    def _analyze_component_file(self, file_path: Path):
        """Analyze a single component file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        relative_path = str(file_path.relative_to(self.project_root))
        
        # Extract component info
        component_info = {
            "path": relative_path,
            "type": self._determine_file_type(file_path, content),
            "exports": self._extract_exports(content),
            "imports": self._extract_imports(content),
            "ui_elements": self._extract_ui_elements(content),
            "styling_classes": self._extract_styling_classes(content),
            "text_content": self._extract_text_content(content),
            "interactivity": self._extract_interactivity(content)
        }
        
        # Store in components
        component_name = file_path.stem
        self.map_data["components"][component_name] = component_info
        
        # Index UI elements for quick lookup
        for element in component_info["ui_elements"]:
            element_key = f"{element['type']}_{element['identifier']}"
            if element_key not in self.map_data["ui_elements"]:
                self.map_data["ui_elements"][element_key] = []
            
            self.map_data["ui_elements"][element_key].append({
                "file": relative_path,
                "component": component_name,
                "line_range": element["line_range"],
                "properties": element["properties"]
            })
    
    def _determine_file_type(self, file_path: Path, content: str) -> str:
        """Determine the type/purpose of a file"""
        name = file_path.name.lower()
        path_parts = file_path.parts
        
        if "layout" in name:
            return "layout"
        elif "page" in name and "app" in path_parts:
            return "page"
        elif "component" in path_parts or file_path.parent.name == "ui":
            return "ui_component"
        elif "lib" in path_parts or "utils" in name:
            return "utility"
        elif "hook" in name or "use" in name:
            return "hook"
        elif "provider" in name or "context" in name:
            return "context"
        elif "globals.css" in name:
            return "global_styles"
        elif name.endswith(".css"):
            return "styles"
        return "component"
    
    def _extract_exports(self, content: str) -> List[str]:
        """Extract exported functions/components"""
        exports = []
        
        # Default exports
        default_export = re.search(r'export\s+default\s+(?:function\s+)?(\w+)', content)
        if default_export:
            exports.append(default_export.group(1))
        
        # Named exports
        named_exports = re.findall(r'export\s+(?:function\s+|const\s+|let\s+|var\s+)?(\w+)', content)
        exports.extend(named_exports)
        
        # Export { } statements
        export_blocks = re.findall(r'export\s*{([^}]+)}', content)
        for block in export_blocks:
            names = re.findall(r'(\w+)', block)
            exports.extend(names)
        
        return list(set(exports))
    
    def _extract_imports(self, content: str) -> List[Dict[str, str]]:
        """Extract import statements"""
        imports = []
        
        # Standard imports
        import_patterns = [
            r'import\s+(\w+)\s+from\s+["\']([^"\']+)["\']',
            r'import\s*{\s*([^}]+)\s*}\s*from\s+["\']([^"\']+)["\']',
            r'import\s*\*\s*as\s+(\w+)\s*from\s+["\']([^"\']+)["\']'
        ]
        
        for pattern in import_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                imports.append({
                    "names": match[0].strip(),
                    "source": match[1]
                })
        
        return imports
    
    def _extract_ui_elements(self, content: str) -> List[Dict[str, Any]]:
        """Extract UI elements like buttons, inputs, etc."""
        elements = []
        lines = content.split('\n')
        
        # Patterns for different UI elements
        ui_patterns = {
            "button": [
                r'<Button\s+([^>]*?)>([^<]*?)</Button>',
                r'<button\s+([^>]*?)>([^<]*?)</button>'
            ],
            "input": [
                r'<Input\s+([^>]*?)/?>', 
                r'<input\s+([^>]*?)/?>'
            ],
            "link": [
                r'<Link\s+([^>]*?)>([^<]*?)</Link>',
                r'<a\s+([^>]*?)>([^<]*?)</a>'
            ],
            "heading": [
                r'<h([1-6])\s*([^>]*?)>([^<]*?)</h[1-6]>',
                r'<h([1-6])>([^<]*?)</h[1-6]>'
            ],
            "text": [
                r'<p\s*([^>]*?)>([^<]*?)</p>',
                r'<span\s*([^>]*?)>([^<]*?)</span>'
            ]
        }
        
        for element_type, patterns in ui_patterns.items():
            for pattern in patterns:
                for line_num, line in enumerate(lines, 1):
                    matches = re.finditer(pattern, line, re.IGNORECASE)
                    for match in matches:
                        element = {
                            "type": element_type,
                            "identifier": self._generate_element_id(match.group(0), element_type),
                            "line_range": [line_num, line_num],
                            "properties": self._parse_element_properties(match.group(0)),
                            "content": self._extract_element_content(match.group(0))
                        }
                        elements.append(element)
        
        return elements
    
    def _generate_element_id(self, element_html: str, element_type: str) -> str:
        """Generate a unique identifier for UI elements"""
        # Try to extract text content
        text_match = re.search(r'>([^<]+)<', element_html)
        if text_match:
            text = text_match.group(1).strip()
            if text and len(text) < 30:
                return re.sub(r'[^a-zA-Z0-9]', '_', text.lower())
        
        # Try to extract className or other attributes
        class_match = re.search(r'className=["\']([^"\']*)["\']', element_html)
        if class_match:
            classes = class_match.group(1).split()
            for cls in classes:
                if any(keyword in cls for keyword in ['btn', 'button', 'link', 'nav']):
                    return cls.replace('-', '_')
        
        return f"{element_type}_element"
    
    def _parse_element_properties(self, element_html: str) -> Dict[str, str]:
        """Parse properties/attributes from element HTML"""
        properties = {}
        
        # Extract common attributes
        attr_patterns = {
            "className": r'className=["\']([^"\']*)["\']',
            "href": r'href=["\']([^"\']*)["\']',
            "type": r'type=["\']([^"\']*)["\']',
            "placeholder": r'placeholder=["\']([^"\']*)["\']',
            "variant": r'variant=["\']([^"\']*)["\']',
            "size": r'size=["\']([^"\']*)["\']'
        }
        
        for prop, pattern in attr_patterns.items():
            match = re.search(pattern, element_html)
            if match:
                properties[prop] = match.group(1)
        
        return properties
    
    def _extract_element_content(self, element_html: str) -> str:
        """Extract text content from element"""
        content_match = re.search(r'>([^<]+)<', element_html)
        if content_match:
            return content_match.group(1).strip()
        return ""
    
    def _extract_styling_classes(self, content: str) -> List[str]:
        """Extract Tailwind/CSS classes used in the file"""
        classes = set()
        
        # Find className attributes
        class_matches = re.findall(r'className=["\']([^"\']*)["\']', content)
        for match in class_matches:
            classes.update(match.split())
        
        # Find class attributes (regular HTML)
        class_matches = re.findall(r'class=["\']([^"\']*)["\']', content)
        for match in class_matches:
            classes.update(match.split())
        
        return sorted(list(classes))
    
    def _extract_text_content(self, content: str) -> List[str]:
        """Extract text content that might need to be changed"""
        text_content = []
        
        # Extract JSX text content
        jsx_text = re.findall(r'>([^<>{]+)<', content)
        for text in jsx_text:
            text = text.strip()
            if text and len(text) > 1 and not text.startswith('{'):
                text_content.append(text)
        
        # Extract string literals
        string_literals = re.findall(r'["\']([^"\']+)["\']', content)
        for literal in string_literals:
            if len(literal) > 3 and ' ' in literal:
                text_content.append(literal)
        
        return list(set(text_content))
    
    def _extract_interactivity(self, content: str) -> List[str]:
        """Extract interactive elements and event handlers"""
        interactions = []
        
        # Event handlers
        event_patterns = [
            r'onClick={([^}]+)}',
            r'onSubmit={([^}]+)}',
            r'onChange={([^}]+)}',
            r'onHover={([^}]+)}'
        ]
        
        for pattern in event_patterns:
            matches = re.findall(pattern, content)
            interactions.extend(matches)
        
        return interactions
    
    def _analyze_styling(self):
        """Analyze CSS files and styling definitions"""
        css_files = list(self.project_root.glob("**/*.css"))
        
        for css_file in css_files:
            try:
                self._analyze_css_file(css_file)
            except Exception as e:
                print(f"⚠️  Error analyzing CSS {css_file}: {e}")
    
    def _analyze_css_file(self, css_file: Path):
        """Analyze a single CSS file"""
        with open(css_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        relative_path = str(css_file.relative_to(self.project_root))
        
        css_info = {
            "path": relative_path,
            "custom_properties": self._extract_css_variables(content),
            "color_definitions": self._extract_color_definitions(content),
            "theme_definitions": self._extract_theme_definitions(content),
            "component_classes": self._extract_component_classes(content)
        }
        
        self.map_data["styling"][css_file.stem] = css_info
    
    def _extract_css_variables(self, content: str) -> Dict[str, str]:
        """Extract CSS custom properties (variables)"""
        variables = {}
        
        # Find --variable: value patterns
        var_pattern = r'--([^:]+):\s*([^;]+);'
        matches = re.findall(var_pattern, content)
        
        for var_name, var_value in matches:
            variables[var_name.strip()] = var_value.strip()
        
        return variables
    
    def _extract_color_definitions(self, content: str) -> Dict[str, str]:
        """Extract color definitions"""
        colors = {}
        
        # Extract color variables
        color_patterns = [
            r'--color-([^:]+):\s*([^;]+);',
            r'--([^:]*(?:color|brand|accent)[^:]*?):\s*([^;]+);'
        ]
        
        for pattern in color_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for color_name, color_value in matches:
                colors[color_name.strip()] = color_value.strip()
        
        return colors
    
    def _extract_theme_definitions(self, content: str) -> Dict[str, Any]:
        """Extract theme-related definitions"""
        themes = {}
        
        # Find :root and .dark theme blocks
        theme_blocks = re.findall(r'(\.dark|:root)\s*{([^}]+)}', content, re.DOTALL)
        
        for theme_name, theme_content in theme_blocks:
            theme_vars = {}
            var_matches = re.findall(r'--([^:]+):\s*([^;]+);', theme_content)
            for var_name, var_value in var_matches:
                theme_vars[var_name.strip()] = var_value.strip()
            
            themes[theme_name.replace('.', '').replace(':', '')] = theme_vars
        
        return themes
    
    def _extract_component_classes(self, content: str) -> List[str]:
        """Extract custom component class definitions"""
        classes = []
        
        # Find class definitions
        class_pattern = r'\.([a-zA-Z][a-zA-Z0-9_-]*)\s*{'
        matches = re.findall(class_pattern, content)
        classes.extend(matches)
        
        return list(set(classes))
    
    def _generate_quick_references(self):
        """Generate quick reference guides for common queries"""
        quick_refs = {
            "buttons": self._find_buttons(),
            "colors": self._find_color_usage(),
            "navigation": self._find_navigation_elements(),
            "headings": self._find_headings(),
            "forms": self._find_form_elements(),
            "theme_elements": self._find_theme_elements()
        }
        
        self.map_data["quick_references"] = quick_refs
    
    def _find_buttons(self) -> List[Dict[str, Any]]:
        """Find all buttons in the project"""
        buttons = []
        
        for component_name, component_info in self.map_data["components"].items():
            for element in component_info["ui_elements"]:
                if element["type"] == "button":
                    buttons.append({
                        "text": element["content"],
                        "file": component_info["path"],
                        "component": component_name,
                        "line": element["line_range"][0],
                        "styling": element["properties"].get("className", ""),
                        "variant": element["properties"].get("variant", "default")
                    })
        
        return buttons
    
    def _find_color_usage(self) -> Dict[str, List[str]]:
        """Find where colors are used throughout the project"""
        color_usage = {}
        
        # Get color definitions from CSS
        for css_name, css_info in self.map_data["styling"].items():
            for color_name, color_value in css_info["color_definitions"].items():
                if color_name not in color_usage:
                    color_usage[color_name] = []
                color_usage[color_name].append(f"Defined in {css_info['path']}: {color_value}")
        
        # Find usage in components
        for component_name, component_info in self.map_data["components"].items():
            for class_name in component_info["styling_classes"]:
                for color_name in color_usage.keys():
                    if color_name.replace('-', '').replace('_', '') in class_name.replace('-', '').replace('_', ''):
                        color_usage[color_name].append(f"Used in {component_info['path']} (class: {class_name})")
        
        return color_usage
    
    def _find_navigation_elements(self) -> List[Dict[str, Any]]:
        """Find navigation-related elements"""
        nav_elements = []
        
        for component_name, component_info in self.map_data["components"].items():
            if "nav" in component_name.lower() or "header" in component_name.lower():
                nav_elements.append({
                    "type": "navigation_component",
                    "file": component_info["path"],
                    "component": component_name,
                    "links": [elem for elem in component_info["ui_elements"] if elem["type"] == "link"],
                    "buttons": [elem for elem in component_info["ui_elements"] if elem["type"] == "button"]
                })
        
        return nav_elements
    
    def _find_headings(self) -> List[Dict[str, Any]]:
        """Find all heading elements"""
        headings = []
        
        for component_name, component_info in self.map_data["components"].items():
            for element in component_info["ui_elements"]:
                if element["type"] == "heading":
                    headings.append({
                        "text": element["content"],
                        "level": element["properties"].get("level", "1"),
                        "file": component_info["path"],
                        "component": component_name,
                        "line": element["line_range"][0],
                        "styling": element["properties"].get("className", "")
                    })
        
        return headings
    
    def _find_form_elements(self) -> List[Dict[str, Any]]:
        """Find form-related elements"""
        form_elements = []
        
        for component_name, component_info in self.map_data["components"].items():
            for element in component_info["ui_elements"]:
                if element["type"] in ["input", "button"]:
                    if element["type"] == "input" or "submit" in element["properties"].get("type", ""):
                        form_elements.append({
                            "type": element["type"],
                            "file": component_info["path"],
                            "component": component_name,
                            "line": element["line_range"][0],
                            "properties": element["properties"]
                        })
        
        return form_elements
    
    def _find_theme_elements(self) -> Dict[str, Any]:
        """Find theme-related elements and controls"""
        theme_info = {
            "theme_toggle": [],
            "theme_variables": {},
            "dark_mode_classes": []
        }
        
        # Find theme toggle components
        for component_name, component_info in self.map_data["components"].items():
            if "theme" in component_name.lower():
                theme_info["theme_toggle"].append({
                    "file": component_info["path"],
                    "component": component_name
                })
        
        # Get theme variables from CSS
        for css_name, css_info in self.map_data["styling"].items():
            theme_info["theme_variables"].update(css_info["theme_definitions"])
        
        return theme_info
    
    def _add_file_purposes(self):
        """Add descriptions of what each file does"""
        purposes = {
            "src/app/page.tsx": "Main landing page with hero section, features, and CTA",
            "src/app/layout.tsx": "Root layout component with global providers",
            "src/app/globals.css": "Global styles, theme variables, and Tailwind configuration",
            "src/components/navbar.tsx": "Main navigation component with logo, menu, and theme toggle",
            "src/components/theme-provider.tsx": "Theme context provider for dark/light mode",
            "src/components/theme-toggle.tsx": "Theme switcher component (light/dark/system)",
            "src/components/ui/": "Reusable UI components (buttons, cards, inputs, etc.)",
            "src/lib/utils.ts": "Utility functions for styling and common operations"
        }
        
        # Add purposes for components
        for component_name, component_info in self.map_data["components"].items():
            file_path = component_info["path"]
            
            if file_path not in purposes:
                if component_info["type"] == "page":
                    purposes[file_path] = f"Page component: {component_name}"
                elif component_info["type"] == "layout":
                    purposes[file_path] = f"Layout component: {component_name}"
                elif component_info["type"] == "ui_component":
                    purposes[file_path] = f"UI component: {component_name}"
                elif "navbar" in component_name.lower() or "nav" in component_name.lower():
                    purposes[file_path] = f"Navigation component: {component_name}"
                elif "theme" in component_name.lower():
                    purposes[file_path] = f"Theme-related component: {component_name}"
                else:
                    purposes[file_path] = f"Component: {component_name}"
        
        self.map_data["file_purposes"] = purposes
    
    def save_map(self, output_path: str = "project-map.json"):
        """Save the generated map to a JSON file"""
        output_file = self.project_root / output_path
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.map_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Project map saved to: {output_file}")
        print(f"📊 Analysis summary:")
        print(f"   - Components analyzed: {len(self.map_data['components'])}")
        print(f"   - UI elements found: {len(self.map_data['ui_elements'])}")
        print(f"   - Styling files: {len(self.map_data['styling'])}")
        print(f"   - Buttons found: {len(self.map_data['quick_references']['buttons'])}")
        
        return output_file


def main():
    """Main function to run the project mapper"""
    import sys
    
    # Get project root from command line or use current directory
    project_root = sys.argv[1] if len(sys.argv) > 1 else "."
    
    print("🚀 Starting Project Mapper...")
    print(f"📁 Analyzing project at: {os.path.abspath(project_root)}")
    
    try:
        mapper = ProjectMapper(project_root)
        map_data = mapper.analyze_project()
        output_file = mapper.save_map()
        
        print("\n✨ Project mapping completed successfully!")
        print(f"🎯 Use this project-map.json to help LLMs understand your project structure")
        print(f"📍 File location: {output_file}")
        
        # Show some example queries
        print("\n🔍 Example LLM queries this project-map.json can help with:")
        print("   - 'Change the color of the Get Started button to green'")
        print("   - 'Update the navbar logo size'")
        print("   - 'Modify the hero section title text'")
        print("   - 'Change the dark mode primary color'")
        print("   - 'Add a new button to the CTA section'")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 