import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const sourceDir = dirname(fileURLToPath(import.meta.url));
const sourceFile = resolve(sourceDir, "entry.png");
const targetDir =
  process.env.MAKEFUN_OUTPUT_DIR ?? resolve(sourceDir, "out");

if (!existsSync(sourceFile)) {
  throw new Error(`entry.png not found in ${sourceDir}`);
}

mkdirSync(targetDir, { recursive: true });
copyFileSync(sourceFile, resolve(targetDir, "entry.png"));
console.log(`entry.png written to ${targetDir}`);
