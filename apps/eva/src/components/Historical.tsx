'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { FC } from 'react';

import { Bar, useHistorical } from '@eva/hooks';

import { ChartComponent } from './chart';

const addTimestampDetails = (bar: Bar): any => {
  const date = new Date(bar.timestamp);
  return {
    ...bar,
    time: Math.floor(date.getTime() / 1000),
  };
};

export const HistoricalComponent: FC = () => {
  const { data, error, isError, isLoading } = useHistorical({
    symbol: 'AAPL',
    timeframe: '1D',
    limit: 10,
  });

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (isError) {
    return <div>Error: {error.message}</div>;
  }

  return data ? (
    <ChartComponent
      data={data.map((d) => addTimestampDetails(d)).sort((a, b) => a.time - b.time)}
    ></ChartComponent>
  ) : (
    <p>Somethind happen</p>
  );
};

const queryClient = new QueryClient();

export const Historical = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <HistoricalComponent />
    </QueryClientProvider>
  );
};
