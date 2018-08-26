
export interface OntologyConfig {
  avm: string;
  network: {
    [networkType: string]: {
      method: 'rpc' | 'rest' | 'websocket';
      host: string;
      wallet: any;
    }
  };
}