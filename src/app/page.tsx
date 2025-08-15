import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ArrowRight, Code, Zap, Shield, Palette, Moon, Sparkles } from "lucide-react";

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen">
      {/* Hero Section */}
      <section className="flex-1 flex items-center justify-center px-4 py-12 md:py-24 lg:py-32">
        <div className="container">
          <div className="flex flex-col items-center space-y-4 text-center">
            <div className="space-y-2">
              <Badge variant="secondary" className="mb-4">
                <Sparkles className="h-3 w-3 mr-1" />
                Ready for Hackathons
              </Badge>
              <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl lg:text-6xl/none">
                Build Amazing Projects with{" "}
                <span className="text-brand-500 dark:text-brand-400">HackStarter</span>
              </h1>
              <p className="mx-auto max-w-[700px] text-muted-foreground md:text-xl">
                The ultimate Next.js 15 starter template designed for hackathons. 
                Pre-configured with Tailwind CSS, shadcn/ui, dark mode, and everything you need to ship fast.
              </p>
            </div>
            <div className="space-x-4">
              <Button size="lg" className="bg-brand-500 hover:bg-brand-600 text-white">
                Get Started
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
              <Button variant="outline" size="lg">
                View on GitHub
              </Button>
            </div>
            <div className="flex items-center space-x-4 text-sm text-muted-foreground pt-4">
              <div className="flex items-center">
                <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                TypeScript
              </div>
              <div className="flex items-center">
                <div className="w-2 h-2 bg-blue-500 rounded-full mr-2"></div>
                Next.js 15
              </div>
              <div className="flex items-center">
                <div className="w-2 h-2 bg-purple-500 rounded-full mr-2"></div>
                Tailwind CSS
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-12 md:py-24 lg:py-32 bg-muted/50">
        <div className="container">
          <div className="flex flex-col items-center justify-center space-y-4 text-center">
            <div className="space-y-2">
              <h2 className="text-3xl font-bold tracking-tighter sm:text-5xl">
                Everything You Need to Win
              </h2>
              <p className="max-w-[900px] text-muted-foreground md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
                Pre-built components, modern design system, and developer experience optimized for rapid prototyping.
              </p>
            </div>
          </div>
          <div className="mx-auto grid max-w-5xl items-start gap-6 py-12 lg:grid-cols-3 lg:gap-12">
            <Card className="group hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="flex items-center space-x-2">
                  <div className="p-2 bg-brand-100 dark:bg-brand-900 rounded-lg">
                    <Code className="h-6 w-6 text-brand-600 dark:text-brand-400" />
                  </div>
                  <CardTitle>Modern Stack</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <CardDescription>
                  Built with Next.js 15, TypeScript, and Tailwind CSS. App Router, server components, 
                  and modern React patterns out of the box.
                </CardDescription>
              </CardContent>
            </Card>
            <Card className="group hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="flex items-center space-x-2">
                  <div className="p-2 bg-accent-custom-100 dark:bg-accent-custom-900 rounded-lg">
                    <Zap className="h-6 w-6 text-accent-custom-600 dark:text-accent-custom-400" />
                  </div>
                  <CardTitle>Ship Fast</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <CardDescription>
                  Pre-configured with shadcn/ui components, responsive layouts, and optimized build setup. 
                  Focus on your idea, not the boilerplate.
                </CardDescription>
              </CardContent>
            </Card>
            <Card className="group hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="flex items-center space-x-2">
                  <div className="p-2 bg-green-100 dark:bg-green-900 rounded-lg">
                    <Shield className="h-6 w-6 text-green-600 dark:text-green-400" />
                  </div>
                  <CardTitle>Production Ready</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <CardDescription>
                  ESLint configuration, TypeScript strict mode, and performance optimizations. 
                  Ready for deployment from day one.
                </CardDescription>
              </CardContent>
            </Card>
            <Card className="group hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="flex items-center space-x-2">
                  <div className="p-2 bg-purple-100 dark:bg-purple-900 rounded-lg">
                    <Palette className="h-6 w-6 text-purple-600 dark:text-purple-400" />
                  </div>
                  <CardTitle>Beautiful Design</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <CardDescription>
                  Extended color palette, responsive design system, and carefully crafted components 
                  that look great out of the box.
                </CardDescription>
              </CardContent>
            </Card>
            <Card className="group hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="flex items-center space-x-2">
                  <div className="p-2 bg-yellow-100 dark:bg-yellow-900 rounded-lg">
                    <Moon className="h-6 w-6 text-yellow-600 dark:text-yellow-400" />
                  </div>
                  <CardTitle>Dark Mode</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <CardDescription>
                  Built-in dark mode support with next-themes. Seamless theme switching with 
                  system preference detection.
                </CardDescription>
              </CardContent>
            </Card>
            <Card className="group hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="flex items-center space-x-2">
                  <div className="p-2 bg-orange-100 dark:bg-orange-900 rounded-lg">
                    <Sparkles className="h-6 w-6 text-orange-600 dark:text-orange-400" />
                  </div>
                  <CardTitle>Developer Experience</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <CardDescription>
                  Hot reload, TypeScript intellisense, auto-formatting, and optimized bundling. 
                  Spend time building, not configuring.
                </CardDescription>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-12 md:py-24 lg:py-32">
        <div className="container">
          <div className="flex flex-col items-center justify-center space-y-4 text-center">
            <div className="space-y-2">
              <h2 className="text-3xl font-bold tracking-tighter sm:text-5xl">
                Ready to Start Building?
              </h2>
              <p className="max-w-[600px] text-muted-foreground md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
                Get started with HackStarter today and turn your ideas into reality faster than ever.
              </p>
            </div>
            <div className="space-x-4">
              <Button size="lg" className="bg-brand-500 hover:bg-brand-600 text-white">
                Clone Repository
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
              <Button variant="outline" size="lg">
                Documentation
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t">
        <div className="container flex flex-col items-center justify-between gap-4 py-10 md:h-24 md:flex-row md:py-0">
          <div className="flex flex-col items-center gap-4 md:flex-row md:gap-2">
            <Link className="flex items-center space-x-2" href="/">
              <div className="h-6 w-6 rounded-full bg-brand-500"></div>
              <span className="font-bold text-brand-600 dark:text-brand-400">HackStarter</span>
            </Link>
            <p className="text-center text-sm leading-loose text-muted-foreground md:text-left">
              Built for hackathons. Made with ❤️ for developers.
            </p>
          </div>
          <div className="flex items-center space-x-4">
            <Link
              href="#"
              className="text-sm font-medium text-muted-foreground hover:text-foreground"
            >
              GitHub
            </Link>
            <Link
              href="#"
              className="text-sm font-medium text-muted-foreground hover:text-foreground"
            >
              Documentation
            </Link>
            <Link
              href="#"
              className="text-sm font-medium text-muted-foreground hover:text-foreground"
            >
              Support
            </Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
