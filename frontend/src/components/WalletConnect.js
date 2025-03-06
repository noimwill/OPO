// WalletConnect.js in your components folder:

import React, { useEffect, useState } from 'react';
import { useWeb3React } from '@web3-react/core';
import { injected } from '../wallet/connectors';
import { formatEther } from '@ethersproject/units';

function WalletConnect() {
  const { active, account, library, activate, deactivate } = useWeb3React();
  const [balance, setBalance] = useState("");
  
  async function connect() {
    try {
      await activate(injected);
    } catch (ex) {
      console.log("Connection error:", ex);
    }
  }

  async function disconnect() {
    try {
      deactivate();
      setBalance("");
    } catch (ex) {
      console.log("Disconnect error:", ex);
    }
  }
  
  useEffect(() => {
    if (library && account) {
      let stale = false;
      
      library.getBalance(account)
        .then((balance) => {
          if (!stale) {
            setBalance(formatEther(balance));
          }
        })
        .catch((error) => {
          if (!stale) {
            console.error("Error fetching balance:", error);
            setBalance("Error");
          }
        });
        
      return () => {
        stale = true;
        setBalance("");
      };
    }
  }, [library, account]);

  return (
    <div className="wallet-connect">
      <h2>Wallet Connection Test</h2>
      {active ? (
        <div>
          <p>Connected Account: {account}</p>
          <p>ETH Balance: {balance} ETH</p>
          <button onClick={disconnect}>Disconnect Wallet</button>
        </div>
      ) : (
        <button onClick={connect}>Connect Wallet</button>
      )}
    </div>
  );
}

export default WalletConnect;