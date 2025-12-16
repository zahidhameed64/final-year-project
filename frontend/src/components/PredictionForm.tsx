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
        setResult(null);

        const formData = new FormData(e.target as HTMLFormElement);

        try {
            const response = await fetch('http://127.0.0.1:5000/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    subscribers: formData.get("subscribers"),
                    video_views: formData.get("views"),
                    uploads: formData.get("uploads"),
                    category: formData.get("category"),
                    created_year: formData.get("created_year"),
                    country: formData.get("country"),
                    title: formData.get("title"),
                    channel_type: "Entertainment" // Default since it was excluded from training
                }),
            });

            if (!response.ok) {
                throw new Error("Failed to fetch prediction");
            }

            const data = await response.json();
            if (data.success) {
                setResult(Math.round(data.predicted_earnings));
            } else {
                console.error("Prediction error:", data.error);
                alert("Error getting prediction: " + data.error);
            }
        } catch (error) {
            console.error("Error:", error);
            alert("Failed to connect to backend. Make sure train_model.py has been run and app.py is running on port 5000.");
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
                                    <Label htmlFor="title">Channel Name</Label>
                                    <Input id="title" name="title" type="text" placeholder="e.g. MrBeast" required />
                                </div>
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
                                    <Label htmlFor="created_year">Created Year</Label>
                                    <Input id="created_year" name="created_year" type="number" placeholder="e.g. 2012" required />
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="category">Category</Label>
                                    <Input id="category" name="category" type="text" placeholder="e.g. Entertainment" required />
                                </div>
                                <div className="md:col-span-2 space-y-2">
                                    <Label htmlFor="country">Country</Label>
                                    <Input id="country" name="country" type="text" placeholder="e.g. United States" required />
                                </div>
                            </div>
                        </CardContent>
                        <CardFooter>
                            <Button type="submit" className="w-full" disabled={loading} size="lg">
                                {loading ? (
                                    <>
                                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                        Connecting to AI Model...
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
        </div >
    );
}
