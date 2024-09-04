import { getData } from './actions';
import { ChartComponent } from './components';

export function Chart(props?: any) {
  return <ChartComponent {...props} data={getData()}></ChartComponent>;
}

export default function Index() {
  return (
    <div>
      <Chart />
    </div>
  );
}
