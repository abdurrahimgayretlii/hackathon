"use client";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ThemeToggle } from "@/components/theme-toggle";
import { Menu, X } from "lucide-react";
import { useState } from "react";
export function Navbar() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const navigation = [
    { name: "Home", href: "/" },
    { name: "Features", href: "#features" },
    { name: "About", href: "#about" },
    { name: "Contact", href: "#contact" },
  ];
  return (
    <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 items-center">
        <div className="mr-4 hidden md:flex">
          <Link className="mr-6 flex items-center space-x-2" href="/">
            <div className="h-6 w-6 rounded-full bg-brand-500"></div>
            <span className="hidden font-bold sm:inline-block text-brand-600 dark:text-brand-400">
              HackStarter
            </span>
          </Link>
          <nav className="flex items-center gap-4 text-sm lg:gap-6">
            {navigation.map((item) => (
              <Link
                key={item.name}
                className="transition-colors hover:text-foreground/80 text-foreground/60"
                href={item.href}
              >
                {item.name}
              </Link>
            ))}
          </nav>
        </div>
        {/* Mobile menu button */}
        <Button
          variant="ghost"
          className="mr-2 px-0 text-base hover:bg-transparent focus-visible:bg-transparent focus-visible:ring-0 focus-visible:ring-offset-0 md:hidden"
          onClick={() => setIsMenuOpen(!isMenuOpen)}
        >
          <Menu className="h-5 w-5" />
          <span className="sr-only">Toggle Menu</span>
        </Button>
        {/* Mobile brand */}
        <div className="flex flex-1 items-center justify-between space-x-2 md:justify-end">
          <div className="w-full flex-1 md:w-auto md:flex-none">
            <Link
              className="mr-6 flex items-center space-x-2 md:hidden"
              href="/"
            >
              <div className="h-6 w-6 rounded-full bg-brand-500"></div>
              <span className="font-bold text-brand-600 dark:text-brand-400">
                HackStarter
              </span>
            </Link>
          </div>
          <nav className="flex items-center gap-2">
            <Button variant="ghost" className="hidden md:inline-flex">
              Sign In
            </Button>
            <Button className="hidden md:inline-flex" style={{ backgroundColor: '#0F0F0F' }}>
              Get Started
            </Button>
            <ThemeToggle />
          </nav>
        </div>
      </div>
      {/* Mobile menu */}
    </header>
  );
}