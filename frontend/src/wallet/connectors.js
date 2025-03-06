// In your frontend/src/wallet directory, create a file 'connectors.js':

import { InjectedConnector } from '@web3-react/injected-connector'

// Configure supported chains (e.g., Ethereum Mainnet, testnets)
export const injected = new InjectedConnector({
  supportedChainIds: [1, 5, 11155111] // Mainnet, Goerli, Sepolia
})