"use client";

import React from "react";
import {
    Bar,
    BarChart,
    ResponsiveContainer,
    Tooltip,
    XAxis,
    YAxis,
} from "recharts";

const featureImportanceData = [
    { name: "Video Views", importance: 0.65, fill: "#8b5cf6" },
    { name: "Subscribers", importance: 0.25, fill: "#22d3ee" },
    { name: "Uploads", importance: 0.05, fill: "#a1a1aa" },
    { name: "Channel Age", importance: 0.03, fill: "#a1a1aa" },
    { name: "Category", importance: 0.02, fill: "#a1a1aa" },
];

export function FeatureImportanceChart() {
    return (
        <ResponsiveContainer width="100%" height={350}>
            <BarChart
                data={featureImportanceData}
                layout="vertical"
                margin={{ left: 20 }}
            >
                <XAxis type="number" hide />
                <YAxis
                    dataKey="name"
                    type="category"
                    width={100}
                    tick={{ fill: "#a1a1aa", fontSize: 12 }}
                    axisLine={false}
                    tickLine={false}
                />
                <Tooltip
                    contentStyle={{
                        backgroundColor: "#18181b",
                        borderColor: "#27272a",
                        borderRadius: "8px",
                    }}
                    itemStyle={{ color: "#fafafa" }}
                    cursor={{ fill: "transparent" }}
                />
                <Bar dataKey="importance" radius={[0, 4, 4, 0]} barSize={32} />
            </BarChart>
        </ResponsiveContainer>
    );
}
