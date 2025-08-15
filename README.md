# HackStarter 🚀

The ultimate Next.js 15 starter template designed for hackathons. Get your project up and running in minutes with a modern, production-ready foundation.

## ✨ Features

- **⚡ Next.js 15** - Latest App Router with server components
- **🎨 Tailwind CSS** - Extended color palette with brand and accent colors
- **🧩 shadcn/ui** - Beautiful, accessible component library
- **🌙 Dark Mode** - Built-in theme switching with next-themes
- **📱 Responsive** - Mobile-first design that works everywhere
- **🔧 TypeScript** - Full type safety and developer experience
- **🎯 ESLint** - Code quality and consistency
- **⚡ Fast Refresh** - Instant feedback during development

## 🎨 Design System

### Brand Colors
```css
brand: {
  50: "#eef2ff",
  100: "#e0e7ff",
  200: "#c7d2fe",
  300: "#a5b4fc",
  400: "#818cf8",
  500: "#6366f1", /* Default */
  600: "#4f46e5",
  700: "#4338ca",
  800: "#3730a3",
  900: "#312e81"
}
```

### Accent Colors
```css
accent: {
  50: "#fdf2f8",
  100: "#fce7f3",
  200: "#fbcfe8",
  300: "#f9a8d4",
  400: "#f472b6", /* Default */
  500: "#ec4899",
  600: "#db2777",
  700: "#be185d",
  800: "#9d174d",
  900: "#831843"
}
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- npm, yarn, or pnpm

### Installation

1. Clone the repository
```bash
git clone <your-repo-url>
cd hackathon-project
```

2. Install dependencies
```bash
npm install
# or
yarn install
# or
pnpm install
```

3. Start the development server
```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

## 📦 What's Included

### Components
- **Navbar** - Responsive navigation with theme toggle
- **Theme Toggle** - Dark/light mode switcher
- **Landing Page** - Hero section with feature cards
- **UI Components** - Button, Card, Input, Dialog, Tabs, Dropdown Menu, Toast

### Utilities
- **cn()** - clsx + tailwind-merge for className handling
- **Theme Provider** - next-themes integration

### Layout
- **Root Layout** - Configured with fonts, theme provider, and global styles
- **Responsive Design** - Mobile-first approach with breakpoints

## 🛠️ Built With

- [Next.js 15](https://nextjs.org/) - React framework
- [TypeScript](https://www.typescriptlang.org/) - Type safety
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS
- [shadcn/ui](https://ui.shadcn.com/) - Component library
- [next-themes](https://github.com/pacocoursey/next-themes) - Theme management
- [Lucide React](https://lucide.dev/) - Icon library
- [clsx](https://github.com/lukeed/clsx) - Conditional classes
- [tailwind-merge](https://github.com/dcastil/tailwind-merge) - Tailwind class merging

## 📝 Customization

### Colors
Modify the color palette in `src/app/globals.css`:

```css
@theme inline {
  /* Add your custom colors here */
  --color-your-brand-500: #your-color;
}
```

### Components
All shadcn/ui components are located in `src/components/ui/` and can be customized.

### Theme
Update the theme provider configuration in `src/app/layout.tsx`.

## 📁 Project Structure

```
src/
├── app/
│   ├── globals.css      # Global styles and theme configuration
│   ├── layout.tsx       # Root layout with providers
│   └── page.tsx         # Landing page
├── components/
│   ├── ui/              # shadcn/ui components
│   ├── navbar.tsx       # Navigation component
│   ├── theme-provider.tsx
│   └── theme-toggle.tsx
└── lib/
    └── utils.ts         # Utility functions
```

## 🎯 For Hackathons

This template is optimized for rapid development:

1. **Start Coding Immediately** - No setup required
2. **Modern Stack** - Latest tools and best practices
3. **Responsive Design** - Works on all devices
4. **Dark Mode** - Professional appearance
5. **Type Safety** - Catch errors early
6. **Extensible** - Easy to add new features

## 🤝 Contributing

Feel free to contribute to this template! Whether it's bug fixes, new features, or improvements.

## 📄 License

MIT License - feel free to use this for your hackathon projects!

---

**Happy Hacking! 🎉**