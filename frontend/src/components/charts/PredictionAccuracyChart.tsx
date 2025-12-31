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
import { useTheme } from "next-themes";

const mockScatterData = [
    { actual: 1000, predicted: 1000 }
];

export function PredictionAccuracyChart() {
    const [data, setData] = React.useState<any[]>([]);
    const { theme } = useTheme();

    const isDark = theme === 'dark';
    const gridColor = isDark ? "#27272a" : "#e4e4e7";
    const axisColor = isDark ? "#a1a1aa" : "#52525b";
    const dotColor = isDark ? "#22d3ee" : "#0ea5e9"; // Cyan 400 vs Sky 500
    const tooltipBg = isDark ? "#18181b" : "#ffffff";
    const tooltipBorder = isDark ? "#27272a" : "#e4e4e7";

    React.useEffect(() => {
        const fetchData = async () => {
            try {
                const res = await fetch("http://localhost:5000/api/model-accuracy");
                if (res.ok) {
                    const jsonData = await res.json();
                    if (jsonData.samples) {
                        setData(jsonData.samples);
                    }
                }
            } catch (err) {
                console.error("Failed to fetch accuracy data", err);
            }
        };
        fetchData();
    }, []);

    if (data.length === 0) return <div className="p-4 text-center text-muted-foreground">Loading accuracy data...</div>;

    return (
        <ResponsiveContainer width="100%" height={350}>
            <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke={gridColor} />
                <XAxis
                    type="number"
                    dataKey="actual"
                    name="Actual"
                    unit="$"
                    stroke={axisColor}
                    fontSize={12}
                    tickLine={false}
                    axisLine={false}
                />
                <YAxis
                    type="number"
                    dataKey="predicted"
                    name="Predicted"
                    unit="$"
                    stroke={axisColor}
                    fontSize={12}
                    tickLine={false}
                    axisLine={false}
                />
                <Tooltip
                    cursor={{ strokeDasharray: "3 3" }}
                    contentStyle={{
                        backgroundColor: tooltipBg,
                        borderColor: tooltipBorder,
                        borderRadius: "8px",
                        color: isDark ? "#fafafa" : "#09090b"
                    }}
                />
                <Scatter name="Earnings" data={data} fill={dotColor} />
            </ScatterChart>
        </ResponsiveContainer>
    );
}
