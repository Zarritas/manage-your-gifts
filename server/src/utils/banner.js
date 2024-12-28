import { readFileSync } from "fs";

const file = readFileSync(`${process.cwd()}/docs/banner.txt`, "utf8");

console.log(file);
