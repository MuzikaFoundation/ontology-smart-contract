import { Crypto, Wallet, Account, RpcClient } from 'ontology-ts-sdk';

export class NRpcClient extends RpcClient {
  constructor() {
    super();
  }
}

const wallet = Wallet.create('hello');
const account = Account.create(Crypto.PrivateKey.random(), 'test', 'test');
account.isDefault = true;
wallet.addAccount(account);

console.dir(wallet.toJsonObj(), { depth: null, colors: true });

console.dir(new NRpcClient());