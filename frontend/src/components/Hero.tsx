"use client";

import React from "react";

export function Hero() {
    return (
        <section className="mb-12 text-center max-w-3xl mx-auto space-y-4">
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-heading font-bold tracking-tight text-foreground">
                Unlock Your Channel's <br />
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-accent">
                    Earning Potential
                </span>
            </h1>
            <p className="text-lg text-muted-foreground md:text-xl">
                Leverage advanced machine learning to predict YouTube revenue with 98%
                accuracy based on channel metrics.
            </p>
        </section>
    );
}
