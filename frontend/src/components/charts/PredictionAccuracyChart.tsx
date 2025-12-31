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

const mockScatterData = [
    { actual: 1000, predicted: 1000 }
];

export function PredictionAccuracyChart() {
    const [data, setData] = React.useState<any[]>([]);

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
                <Scatter name="Earnings" data={data} fill="#22d3ee" />
            </ScatterChart>
        </ResponsiveContainer>
    );
}
