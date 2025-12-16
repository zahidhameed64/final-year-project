"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/Card";
import { FeatureImportanceChart } from "@/components/charts/FeatureImportanceChart";
import { PredictionAccuracyChart } from "@/components/charts/PredictionAccuracyChart";

export function Dashboard() {
    return (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7 mt-8">
            <Card className="col-span-4 glass-card">
                <CardHeader>
                    <CardTitle>Model Feature Importance</CardTitle>
                    <CardDescription>
                        Relative impact of each channel metric on earnings prediction (Random Forest)
                    </CardDescription>
                </CardHeader>
                <CardContent className="pl-2">
                    <FeatureImportanceChart />
                </CardContent>
            </Card>

            <Card className="col-span-3 glass-card">
                <CardHeader>
                    <CardTitle>Prediction Accuracy</CardTitle>
                    <CardDescription>
                        Actual vs Predicted Earnings (Test Set Sample)
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <PredictionAccuracyChart />
                </CardContent>
            </Card>
        </div>
    );
}
