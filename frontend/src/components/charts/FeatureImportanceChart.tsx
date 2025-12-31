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
import { useTheme } from "next-themes";

const featureImportanceData = [
    { name: "Video Views", importance: 0.65, fill: "#8b5cf6" },
];

export function FeatureImportanceChart() {
    const [data, setData] = React.useState<any[]>([]);
    const { theme } = useTheme();

    // Theme-aware colors
    const isDark = theme === 'dark';
    const axisColor = isDark ? "#a1a1aa" : "#52525b"; // Zinc 400 vs Zinc 600
    const tooltipBg = isDark ? "#18181b" : "#ffffff";
    const tooltipBorder = isDark ? "#27272a" : "#e4e4e7";
    const tooltipText = isDark ? "#fafafa" : "#09090b";

    React.useEffect(() => {
        const fetchData = async () => {
            try {
                const res = await fetch("http://localhost:5000/api/feature-importance");
                if (res.ok) {
                    const jsonData = await res.json();
                    // Assuming jsonData is [{name: string, importance: number}, ...]
                    // Map to include random colors or standard colors
                    const colors = ["#8b5cf6", "#22d3ee", "#a1a1aa", "#f472b6", "#34d399"];
                    const formattedData = jsonData.map((item: any, index: number) => ({
                        ...item,
                        fill: colors[index % colors.length]
                    }));
                    setData(formattedData);
                }
            } catch (err) {
                console.error("Failed to fetch importance data", err);
            }
        };
        fetchData();
    }, []);

    if (data.length === 0) return <div className="p-4 text-center text-muted-foreground">Loading importance data...</div>;

    return (
        <ResponsiveContainer width="100%" height={350}>
            <BarChart
                data={data}
                layout="vertical"
                margin={{ left: 20 }}
            >
                <XAxis type="number" hide />
                <YAxis
                    dataKey="name"
                    type="category"
                    width={100}
                    tick={{ fill: axisColor, fontSize: 12 }}
                    axisLine={false}
                    tickLine={false}
                />
                <Tooltip
                    contentStyle={{
                        backgroundColor: tooltipBg,
                        borderColor: tooltipBorder,
                        borderRadius: "8px",
                    }}
                    itemStyle={{ color: tooltipText }}
                    cursor={{ fill: "transparent" }}
                />
                <Bar dataKey="importance" radius={[0, 4, 4, 0]} barSize={32} />
            </BarChart>
        </ResponsiveContainer>
    );
}
