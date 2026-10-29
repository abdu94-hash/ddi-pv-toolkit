// Check every test vector in ../spec/vectors.json against calculators.js.
// Run with:  node docs/test_vectors.mjs   (Node 14 or later; no dependencies)
// Exits with status 1 if any vector fails.
//
// The vectors are the worked numbers from "Drug-Drug Interactions in Drug Safety
// and Pharmacovigilance". Educational use only; not for clinical decisions.

import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);
const DDI = require(join(here, "calculators.js"));
const doc = JSON.parse(readFileSync(join(here, "..", "spec", "vectors.json"), "utf8"));

let passed = 0;
const failures = [];

for (const v of doc.vectors) {
  const label = `${v.calculator} [${v.source}]`;
  const fn = DDI.calculators[v.calculator];
  if (!fn) {
    failures.push(`${label}: no such calculator in calculators.js`);
    continue;
  }
  let result;
  try {
    result = fn(v.inputs);
  } catch (err) {
    failures.push(`${label}: threw ${err.message}`);
    continue;
  }
  const problems = [];
  for (const [key, expected] of Object.entries(v.expected)) {
    const actual = result[key];
    const tol = v.tolerance[key];
    if (typeof tol !== "number") problems.push(`${key}: no tolerance`);
    else if (typeof actual !== "number" || !Number.isFinite(actual)) problems.push(`${key}: got ${actual}`);
    else if (Math.abs(actual - expected) > tol * (1 + 1e-9) + 1e-12) {
      problems.push(`${key}: got ${actual}, book ${expected} ± ${tol}`);
    }
  }
  if (problems.length) failures.push(`${label}: ${problems.join("; ")}`);
  else passed += 1;
}

// Every calculator needs at least one vector.
const covered = new Set(doc.vectors.map((v) => v.calculator));
for (const name of Object.keys(DDI.calculators)) {
  if (!covered.has(name)) failures.push(`${name}: no vector in spec/vectors.json`);
}

// A few validation checks: invalid input must throw with a clear message.
const invalid = [
  ["fm_ceiling", { fm: 1.5 }, "fm must be in the range [0, 1), got 1.5"],
  ["auc_ratio_inhibition", { fm: 0.5 }, "give exactly one of fraction_inhibited or i_over_ki"],
  ["inhibition_from_auc_ratio", { fm: 0.75, auc_ratio: 4.2 }, "exceeds the ceiling"],
  ["qt_correction", { qt: 480, heart_rate: 0 }, "heart_rate must be greater than 0, got 0"],
  ["reporting_rate", { cases: 4.5, exposure: 1000 }, "cases must be a whole number, got 4.5"],
  ["prr_ror", { a: 0, b: 1, c: 1, d: 1 }, "a must be at least 1, got 0"],
];
let validationPassed = 0;
for (const [name, inputs, message] of invalid) {
  try {
    DDI.calculators[name](inputs);
    failures.push(`${name} ${JSON.stringify(inputs)}: expected an error`);
  } catch (err) {
    if (err.name === "ValidationError" && err.message.includes(message)) validationPassed += 1;
    else failures.push(`${name}: wrong error "${err.message}"`);
  }
}

console.log(`vectors: ${passed} of ${doc.vectors.length} passed`);
console.log(`calculators covered: ${covered.size} of ${Object.keys(DDI.calculators).length}`);
console.log(`validation checks: ${validationPassed} of ${invalid.length} passed`);
if (failures.length) {
  console.log(`\n${failures.length} failure(s):`);
  for (const f of failures) console.log("  " + f);
  process.exit(1);
}
console.log("all checks passed");
