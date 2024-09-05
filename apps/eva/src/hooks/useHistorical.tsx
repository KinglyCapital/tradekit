import { useQuery } from '@tanstack/react-query';

import { useFetch } from './useFetch';

export type Bar = {
  symbol: string;
  timestamp: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
  trade_count: number;
  vwap: number;
};

type HistoricalPricesParams = {
  symbol: string;
  timeframe: string;
  limit: number;
};

export const useHistorical = (params: HistoricalPricesParams) => {
  return useQuery<Bar[]>({
    queryKey: ['historical', params],
    queryFn: () => useFetch('historical', params),
  });
};
