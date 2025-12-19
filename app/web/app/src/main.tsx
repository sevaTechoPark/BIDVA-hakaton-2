import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import 'primereact/resources/themes/saga-green/theme.css';
import 'primeicons/primeicons.css';
import 'primeflex/primeflex.css';
import './index.css';
import App from './App.tsx';
import { PrimeReactProvider } from 'primereact/api';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
      <PrimeReactProvider>
          <App />
      </PrimeReactProvider>
  </StrictMode>,
)
