"use client";
import { useState, useEffect } from "react";
import { Bar, BarChart, CartesianGrid, XAxis } from "recharts";

import {
  ChartContainer,
  ChartLegend,
  ChartLegendContent,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart";
import type { ChartConfig } from "@/components/ui/chart";

export function App() {
  const [graphData, setGraphData] = useState<Record<string, any>>({});
  const [error, setError] = useState(null);
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/");
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setGraphData(data);
      } catch (err: any) {
        setError(err.message || "Unknown error");
      }
    };
    fetchData();
  }, []);

  if (error) {
    return (
      <div className="w-full h-screen flex items-center justify-center p-4 bg-stone-950">
        <div className="text-red-500">{error}</div>
      </div>
    );
  }

  const chartData =
    Array.isArray(graphData) && graphData.length > 0
      ? graphData.map((item: any) => ({
          month: item.date,
          exercise: item.exercise,
          weight: item.weight,
        }))
      : [];

  const chartConfig = {
    exercise: {
      label: "exercise",
      color: "#60a5fa",
    },
    weight: {
      label: "weight",
      color: "#2563eb",
    },
  } satisfies ChartConfig;

  return (
    <div className="w-full h-screen flex items-center justify-center p-4 bg-stone-950">
      <ChartContainer
        config={chartConfig}
        className="max-h-96 w-2xl p-4 border-2 bg-stone-900 border-stone-600 rounded-2xl"
      >
        <BarChart accessibilityLayer data={chartData}>
          <CartesianGrid vertical={false} />
          <XAxis dataKey="month" tickLine={false} tickMargin={10} />
          <ChartTooltip content={<ChartTooltipContent />} />
          <ChartLegend content={<ChartLegendContent />} />
          <Bar dataKey="exercise" fill="var(--color-exercise)" radius={4} />
          <Bar dataKey="weight" fill="var(--color-weight)" radius={4} />
        </BarChart>
      </ChartContainer>
    </div>
  );
}
