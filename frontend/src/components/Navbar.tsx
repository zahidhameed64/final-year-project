import Link from "next/link";
import { Youtube, BarChart3 } from "lucide-react";

export function Navbar() {
    return (
        <nav className="border-b border-border bg-background/50 backdrop-blur-xl sticky top-0 z-50">
            <div className="container mx-auto px-4 h-16 flex items-center justify-between">
                <Link href="/" className="flex items-center gap-2 font-heading font-bold text-xl tracking-tight hover:text-primary transition-colors">
                    <Youtube className="w-8 h-8 text-primary" />
                    <span>YouTube <span className="text-primary">Earnings</span> Intelligence</span>
                </Link>

                <div className="flex items-center gap-4">
                    <Link href="https://github.com" target="_blank" className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors">
                        Documentation
                    </Link>
                    <div className="h-4 w-px bg-border"></div>
                    <div className="flex items-center gap-1 text-sm font-medium text-accent">
                        <BarChart3 className="w-4 h-4" />
                        <span>v1.0.0</span>
                    </div>
                </div>
            </div>
        </nav>
    );
}
