"use client";

import React from "react";
import {
    CartesianGrid,
    ResponsiveContainer,
    Scatter,
    ScatterChart,
    Tooltip,
    XAxis,
    YAxis,
} from "recharts";

const mockScatterData = Array.from({ length: 20 }, (_, i) => ({
    actual: 1000 + i * 500 + Math.random() * 500,
    predicted: 1000 + i * 500 + Math.random() * 500 - 250,
}));

export function PredictionAccuracyChart() {
    return (
        <ResponsiveContainer width="100%" height={350}>
            <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" />
                <XAxis
                    type="number"
                    dataKey="actual"
                    name="Actual"
                    unit="$"
                    stroke="#a1a1aa"
                    fontSize={12}
                    tickLine={false}
                    axisLine={false}
                />
                <YAxis
                    type="number"
                    dataKey="predicted"
                    name="Predicted"
                    unit="$"
                    stroke="#a1a1aa"
                    fontSize={12}
                    tickLine={false}
                    axisLine={false}
                />
                <Tooltip
                    cursor={{ strokeDasharray: "3 3" }}
                    contentStyle={{
                        backgroundColor: "#18181b",
                        borderColor: "#27272a",
                        borderRadius: "8px",
                    }}
                />
                <Scatter name="Earnings" data={mockScatterData} fill="#22d3ee" />
            </ScatterChart>
        </ResponsiveContainer>
    );
}
