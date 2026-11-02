// Usage: node cutout.mjs in.jpg out.png  (offline background removal, model bundled in the npm package)
import { removeBackground } from '@imgly/background-removal-node';
import fs from 'fs';
import path from 'path';
const [inp, out] = process.argv.slice(2);
const blob = await removeBackground('file://' + path.resolve(inp), { model: 'medium', output: { format: 'image/png' } });
fs.writeFileSync(out, Buffer.from(await blob.arrayBuffer()));
console.log('Saved', out);
