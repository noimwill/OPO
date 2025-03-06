// In your App.js file:

import React from 'react';
import { Web3ReactProvider } from '@web3-react/core';
import { Web3Provider } from '@ethersproject/providers';
import WalletConnect from './components/WalletConnect';
import './App.css';

// This is the function that returns the provider
function getLibrary(provider) {
  const library = new Web3Provider(provider);
  library.pollingInterval = 12000;
  return library;
}

function App() {
  return (
    <Web3ReactProvider getLibrary={getLibrary}>
      <div className="App">
        <header className="App-header">
          <h1>Portfolio Optimizer</h1>
          <WalletConnect />
        </header>
      </div>
    </Web3ReactProvider>
  );
}

export default App;