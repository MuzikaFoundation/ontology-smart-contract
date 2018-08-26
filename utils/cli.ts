
import { join } from 'path';
import { ConfigLoader } from './config-loader';

const commandLineArgs = require('command-line-args');

const OPTIONS = [
  { name: 'mode', alias: 'm', type: String },
  { name: 'deploy', type: Boolean }
];

async function main() {
  const options = commandLineArgs(OPTIONS);

  const config = new ConfigLoader(
    require(join(__dirname, '..', 'ontology.json')),
    options.mode,
    join(__dirname, '..')
  );

  if (options.deploy) {
  }
}

main()
  .catch(console.error);
