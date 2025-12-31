"use client";

import { useState } from "react";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/Card";
import { Input } from "@/components/ui/Input";
import { Label } from "@/components/ui/Label";
import { Button } from "@/components/ui/Button";
import { Loader2, DollarSign, TrendingUp } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

export function PredictionForm() {
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<number | null>(null);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setResult(null); // Reset previous result

        const formData = new FormData(e.target as HTMLFormElement);
        // Map frontend fields to backend expected feature names
        // Backend expects: 'subscribers', 'video views', 'uploads', 'category'
        const payload = {
            subscribers: Number(formData.get("subscribers")),
            "video views": Number(formData.get("views")),
            uploads: Number(formData.get("uploads")),
            category: formData.get("category") as string,
            Country: formData.get("country") as string,
            channel_type: formData.get("channel_type") as string,
            created_year: Number(formData.get("created_year")),
            video_views_for_the_last_30_days: Number(formData.get("views_30d")),
            subscribers_for_last_30_days: Number(formData.get("subs_30d"))
        };

        try {
            // In dev, Next.js rewrites can point /api to localhost:5000, 
            // or we use full URL if CORS is enabled (which we did).
            const response = await fetch("http://localhost:5000/api/predict", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                throw new Error("Failed to fetch prediction");
            }

            const data = await response.json();
            if (data.prediction !== undefined) {
                setResult(Math.round(data.prediction));
            } else {
                console.error("No prediction in response:", data);
            }
        } catch (error) {
            console.error("Prediction error:", error);
            // Optionally handle error state here
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="grid gap-8 lg:grid-cols-2">
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
            >
                <Card className="w-full h-full">
                    <CardHeader>
                        <CardTitle>Channel Statistics</CardTitle>
                        <CardDescription>Enter the YouTube channel's public metrics to predict earnings.</CardDescription>
                    </CardHeader>
                    <form onSubmit={handleSubmit}>
                        <CardContent className="space-y-4">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div className="space-y-2">
                                    <Label htmlFor="subscribers">Subscribers</Label>
                                    <Input id="subscribers" name="subscribers" type="number" placeholder="e.g. 1000000" required />
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="views">Total Video Views</Label>
                                    <Input id="views" name="views" type="number" placeholder="e.g. 500000000" required />
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="uploads">Uploads</Label>
                                    <Input id="uploads" name="uploads" type="number" placeholder="e.g. 500" required />
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="category">Category</Label>
                                    <Input id="category" name="category" type="text" placeholder="e.g. Entertainment" required />
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="country">Country</Label>
                                    <Input id="country" name="country" type="text" placeholder="e.g. United States" required />
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="channel_type">Channel Type</Label>
                                    <Input id="channel_type" name="channel_type" type="text" placeholder="e.g. Games" required />
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="created_year">Channel Creation Year</Label>
                                    <Input id="created_year" name="created_year" type="number" placeholder="e.g. 2018" required />
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="views_30d">Views (Last 30 Days)</Label>
                                    <Input id="views_30d" name="views_30d" type="number" placeholder="e.g. 1000000" required />
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="subs_30d">Subscribers (Last 30 Days)</Label>
                                    <Input id="subs_30d" name="subs_30d" type="number" placeholder="e.g. 5000" required />
                                </div>
                            </div>
                        </CardContent>
                        <CardFooter>
                            <Button type="submit" className="w-full" disabled={loading} size="lg">
                                {loading ? (
                                    <>
                                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                        Analyzing Channel...
                                    </>
                                ) : (
                                    "Predict Yearly Earnings"
                                )}
                            </Button>
                        </CardFooter>
                    </form>
                </Card>
            </motion.div>

            <AnimatePresence>
                {result !== null && (
                    <motion.div
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0 }}
                        transition={{ duration: 0.5, delay: 0.1 }}
                        className="h-full"
                    >
                        <Card className="w-full h-full border-primary/20 bg-primary/5 flex flex-col justify-center items-center text-center p-8">
                            <div className="mb-4 p-4 rounded-full bg-primary/20 text-primary">
                                <DollarSign className="w-12 h-12" />
                            </div>
                            <h3 className="text-lg font-medium text-muted-foreground mb-2">Estimated Yearly Earnings</h3>
                            <div className="text-5xl font-bold font-heading text-foreground mb-6">
                                ${result.toLocaleString()}
                            </div>

                            <div className="flex gap-2 items-center text-sm text-accent bg-accent/10 px-3 py-1 rounded-full">
                                <TrendingUp className="w-4 h-4" />
                                <span>Based on Random Forest Regression Model</span>
                            </div>
                        </Card>
                    </motion.div>
                )}

                {result === null && !loading && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="hidden lg:flex h-full items-center justify-center text-muted-foreground text-sm border-2 border-dashed border-border rounded-xl p-12"
                    >
                        Prediction results will appear here
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}
