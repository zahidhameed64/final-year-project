"use client";

import React from "react";

export function BackgroundEffects() {
    return (
        <>
            <div className="absolute top-0 left-0 w-full h-[500px] bg-gradient-to-b from-primary/5 via-background to-background pointer-events-none" />
            <div className="absolute top-[-20%] right-[-10%] w-[600px] h-[600px] bg-primary/10 rounded-full blur-[120px] pointer-events-none" />
            <div className="absolute bottom-[-10%] left-[-10%] w-[500px] h-[500px] bg-accent/5 rounded-full blur-[100px] pointer-events-none" />
        </>
    );
}
